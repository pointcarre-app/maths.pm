#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Lifespan manager for Maths.pm
Encapsulates startup and shutdown logic used by FastAPI lifespan.
"""

import os
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from shutil import copy2, rmtree
import logging
import httpx

from fastapi import FastAPI

from ..settings import settings

logger = logging.getLogger("maths_pm")


def build_jupyterlite():
    try:
        source_dir = settings.jupyterlite_content_dir
        jupyterlite_dir = settings.jupyterlite_dir

        if not source_dir.exists():
            logger.warning(f"⚠️  JupyterLite source not found: {source_dir}")
            return

        jupyterlite_dir.mkdir(parents=True, exist_ok=True)

        import subprocess

        original_cwd = os.getcwd()
        os.chdir(str(jupyterlite_dir))

        try:
            relative_source = os.path.relpath(source_dir, jupyterlite_dir)
            build_cmd = [
                "jupyter",
                "lite",
                "build",
                "--contents",
                relative_source,
            ]
            subprocess.run(build_cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            logger.error("❌ JupyterLite build failed")
        finally:
            os.chdir(original_cwd)

        output_dir = jupyterlite_dir / "_output"
        index_exists = (output_dir / "index.html").exists()
        lab_exists = (output_dir / "lab" / "index.html").exists()

        if index_exists and lab_exists:
            files_dir = output_dir / "files"
            if files_dir.exists():
                data_files_dir = files_dir / "data"
                if data_files_dir.exists():
                    file_count = sum(1 for _, _, files in os.walk(data_files_dir) for _ in files)
                    logger.info(f"✅ JupyterLite ready ({file_count} data files)")
                else:
                    logger.info("✅ JupyterLite ready")
            else:
                logger.info("✅ JupyterLite ready")
        else:
            logger.error("❌ JupyterLite build failed")
    except Exception as e:
        logger.error(f"❌ JupyterLite build failed: {e}")


async def async_build_jupyterlite(force_rebuild: bool = True):
    import subprocess

    if force_rebuild:
        output_dir = settings.jupyterlite_dir / "_output"
        cache_db = settings.jupyterlite_dir / ".jupyterlite.doit.db"
        try:
            if output_dir.exists():
                subprocess.run(["rm", "-rf", str(output_dir)], check=True)
            if cache_db.exists():
                subprocess.run(["rm", "-f", str(cache_db)], check=True)
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Cache cleanup failed: {e}")

    build_jupyterlite()
    await cleanup_service_worker_issues()


async def cleanup_service_worker_issues():
    try:
        service_worker_path = settings.jupyterlite_dir / "_output" / "service-worker.js"
        if service_worker_path.exists():
            with open(service_worker_path, "r", encoding="utf-8") as f:
                sw_content = f.read()
            import time

            timestamp = int(time.time())
            cache_buster = f"\n// Cache buster: {timestamp}\n// Service worker updated at startup\n"
            with open(service_worker_path, "w", encoding="utf-8") as f:
                f.write(cache_buster + sw_content)
    except Exception as e:
        logger.warning(f"⚠️  Failed to cleanup service worker: {e}")


async def download_safari_css_files(force_download: bool = False):
    try:
        safari_css_dir = settings.static_dir / "css" / "safari-local"
        safari_css_dir.mkdir(parents=True, exist_ok=True)

        css_urls = {
            "fonts-comfortaa.css": "https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Dancing+Script:wght@400..700&family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Lora:ital,wght@0,400..700;1,400..700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap",
            "fonts-lexend.css": "https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap",
            "daisyui.css": "https://cdn.jsdelivr.net/npm/daisyui@5",
            "daisyui-themes.css": "https://cdn.jsdelivr.net/npm/daisyui@5/themes.css",
            "katex.min.css": "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css",
            "papyrus-index.css": "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/index.css",
            "papyrus-print.css": "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/print.css",
        }

        if not force_download:
            all_exist = all((safari_css_dir / filename).exists() for filename in css_urls.keys())
            if all_exist:
                logger.info("🦁 Safari CSS files already exist, skipping download")
                return
            else:
                logger.info("🦁 Some Safari CSS files missing, downloading...")

        fonts_dir = safari_css_dir / "fonts"
        fonts_dir.mkdir(parents=True, exist_ok=True)

        async with httpx.AsyncClient(timeout=10.0) as client:
            download_tasks = []
            for filename, url in css_urls.items():
                download_tasks.append(
                    download_css_file(client, url, safari_css_dir / filename, fonts_dir)
                )
            results = await asyncio.gather(*download_tasks, return_exceptions=True)
            successful = sum(1 for r in results if not isinstance(r, Exception))
            if successful > 0:
                logger.info(f"🦁 Safari CSS files downloaded ({successful}/{len(css_urls)} files)")
            else:
                logger.warning("⚠️  No Safari CSS files downloaded")
    except Exception as e:
        logger.warning(f"⚠️  Failed to download Safari CSS files: {e}")


async def download_css_file(client, url, dest_path, fonts_dir):
    try:
        response = await client.get(url)
        if response.status_code == 200:
            content = response.text
            if "fonts.googleapis" in url or "fonts.gstatic" in url:
                import re

                font_urls = re.findall(r"url\((https://[^)]+)\)", content)
                for font_url in font_urls:
                    font_filename = font_url.split("/")[-1].split("?")[0]
                    font_dest = fonts_dir / font_filename
                    font_response = await client.get(font_url)
                    if font_response.status_code == 200:
                        font_content = font_response.content
                        with open(font_dest, "wb") as f:
                            f.write(font_content)
                    relative_font_path = f"./fonts/{font_filename}"
                    content = content.replace(font_url, relative_font_path)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        else:
            logger.warning(f"⚠️  Failed to download {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"⚠️  Error downloading {url}: {e}")
        return False


def _resolve_paths_relative_to_base(paths: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for p in paths:
        try:
            candidate = (settings.base_dir / p).resolve()
            if candidate.exists():
                resolved.append(candidate)
            else:
                logger.warning(f"⚠️ Notebook path not found: {candidate}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to resolve path {p}: {e}")
    return resolved


def _gather_notebooks_from_dirs(source_dirs: list[Path]) -> list[Path]:
    notebooks: list[Path] = []
    for d in source_dirs:
        if d.exists() and d.is_dir():
            notebooks.extend(d.rglob("*.ipynb"))
        else:
            logger.debug(f"Notebook dir missing or not a dir: {d}")
    # De-duplicate while preserving order
    seen = set()
    unique: list[Path] = []
    for nb in notebooks:
        if nb not in seen:
            unique.append(nb)
            seen.add(nb)
    return unique


def _get_configured_notebook_sources() -> tuple[list[Path], list[Path]]:
    """
    Return (explicit_files, source_dirs) from domain backend settings and sane defaults.
    Domain config example:
      backend_settings:
        jupyterlite:
          notebooks: ["files-for-lite/example.ipynb", "notebooks/demo.ipynb"]
          notebooks_dirs: ["notebooks", "files/notebooks"]
    """
    configured = settings.domain_backend_settings or {}
    jl_cfg = configured.get("jupyterlite", {}) if isinstance(configured, dict) else {}

    files_cfg = jl_cfg.get("notebooks", []) or []
    dirs_cfg = jl_cfg.get("notebooks_dirs", []) or []

    explicit_files = _resolve_paths_relative_to_base([str(p) for p in files_cfg])
    source_dirs = _resolve_paths_relative_to_base([str(p) for p in dirs_cfg])

    # Provide sensible defaults if nothing configured
    if not explicit_files and not source_dirs:
        default_dirs = [
            settings.base_dir / "notebooks",
            settings.base_dir / "files" / "notebooks",
        ]
        source_dirs.extend([d for d in default_dirs if d.exists()])

    # Also allow EXTRA_NOTEBOOKS_DIRS env (colon-separated)
    extra_env = os.environ.get("EXTRA_NOTEBOOKS_DIRS", "")
    if extra_env:
        extra_dirs = [Path(p.strip()) for p in extra_env.split(":") if p.strip()]
        source_dirs.extend([d if d.is_absolute() else (settings.base_dir / d) for d in extra_dirs])

    return explicit_files, source_dirs


def _copy_file_preserve_name(src: Path, dest_dir: Path) -> bool:
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / src.name
        copy2(src, dest_path)
        return True
    except Exception as e:
        logger.warning(f"⚠️ Failed to copy notebook {src} -> {dest_dir}: {e}")
        return False


def preload_notebooks_into_jupyterlite_output() -> int:
    """
    Ensure configured .ipynb notebooks are present in the built JupyterLite output.
    Works for both runtime hosting and static build (since 'src/static' is copied).
    Returns number of notebooks copied.
    """
    output_files_dir = settings.jupyterlite_dir / "_output" / "files"
    target_dir = output_files_dir / "notebooks"

    if not (settings.jupyterlite_dir / "_output").exists():
        logger.debug("JupyterLite output missing; skipping notebook preload")
        return 0

    explicit_files, source_dirs = _get_configured_notebook_sources()

    # Start with explicitly listed files
    notebooks: list[Path] = []
    notebooks.extend([p for p in explicit_files if p.exists() and p.suffix == ".ipynb"])

    # Add notebooks discovered in source directories
    notebooks.extend(_gather_notebooks_from_dirs(source_dirs))

    # De-duplicate by name to avoid collisions; last one wins
    seen_names: set[str] = set()
    copied = 0
    for nb in notebooks:
        if nb.suffix != ".ipynb":
            continue
        # If duplicate names occur, later entries overwrite earlier ones
        if nb.name in seen_names:
            # Still copy to overwrite to ensure precedence
            if _copy_file_preserve_name(nb, target_dir):
                copied += 1
        else:
            if _copy_file_preserve_name(nb, target_dir):
                copied += 1
                seen_names.add(nb.name)

    if copied > 0:
        logger.info(f"📓 JupyterLite notebooks preloaded into output ({copied} files)")
    else:
        logger.info("📓 No extra notebooks to preload")

    return copied


def mirror_files_for_lite_into_output() -> int:
    """
    Mirror the entire files-for-lite/ directory tree into JupyterLite _output/files/.
    Preserves subdirectories like data/, and copies all file types (.ipynb, .svg, etc.).

    Returns number of files copied/updated.
    """
    source_dir = settings.jupyterlite_content_dir
    dest_root = settings.jupyterlite_dir / "_output" / "files"

    if not (settings.jupyterlite_dir / "_output").exists():
        logger.debug("JupyterLite output missing; skipping files-for-lite mirroring")
        return 0

    if not source_dir.exists():
        logger.warning(f"⚠️ files-for-lite/ not found: {source_dir}")
        return 0

    copied = 0
    for root, dirs, files in os.walk(source_dir):
        rel_root = os.path.relpath(root, source_dir)
        dest_dir = dest_root / rel_root if rel_root != "." else dest_root
        dest_dir.mkdir(parents=True, exist_ok=True)

        for filename in files:
            src_file = Path(root) / filename
            dest_file = dest_dir / filename
            try:
                # Copy if missing or source is newer
                if not dest_file.exists() or src_file.stat().st_mtime > dest_file.stat().st_mtime:
                    copy2(src_file, dest_file)
                    copied += 1
            except Exception as e:
                logger.warning(f"⚠️ Failed to copy {src_file} -> {dest_file}: {e}")

    if copied > 0:
        logger.info(f"📦 files-for-lite mirrored into JupyterLite files/ ({copied} files)")
    else:
        logger.info("📦 files-for-lite already up-to-date in JupyterLite files/")

    return copied


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    logger.info(f"🚀 Starting Maths.pm ({settings.domain_config.domain_url or 'localhost'})")
    if settings.jupyterlite_enabled:
        await async_build_jupyterlite()
        # After JupyterLite is built, mirror files-for-lite fully and then ensure notebooks
        try:
            mirror_files_for_lite_into_output()
        except Exception as e:
            logger.warning(f"⚠️ Failed to mirror files-for-lite into JupyterLite: {e}")
        try:
            preload_notebooks_into_jupyterlite_output()
        except Exception as e:
            logger.warning(f"⚠️ Failed to preload notebooks into JupyterLite: {e}")

    is_ci = os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true"
    should_download = os.environ.get("DOWNLOAD_SAFARI_CSS", "").lower() in ["true", "1", "yes"]

    if is_ci:
        logger.info("🚀 GitHub Actions detected: Using Safari CSS files from repository")
    elif should_download:
        logger.info(
            "📦 Local environment: Force downloading Safari CSS files (DOWNLOAD_SAFARI_CSS=true)"
        )
        try:
            await download_safari_css_files(force_download=True)
        except Exception as e:
            logger.warning(f"⚠️  Safari CSS download failed (non-critical): {e}")
    else:
        logger.info("💻 Local environment: Checking Safari CSS files...")
        try:
            await download_safari_css_files(force_download=False)
        except Exception as e:
            logger.warning(f"⚠️  Safari CSS check/download failed (non-critical): {e}")

    try:
        pms_dir = settings.base_dir / "pms"
        static_pm_dir = settings.static_dir / "pm"
        if pms_dir.exists():
            if static_pm_dir.exists():
                rmtree(static_pm_dir)
            static_pm_dir.mkdir(parents=True, exist_ok=True)
            for root, dirs, files in os.walk(pms_dir):
                rel_root = os.path.relpath(root, pms_dir)
                dest_root = static_pm_dir / rel_root if rel_root != "." else static_pm_dir
                dest_root.mkdir(parents=True, exist_ok=True)
                for file_name in files:
                    src_file = Path(root) / file_name
                    dest_file = dest_root / file_name
                    try:
                        copy2(src_file, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {src_file} -> {dest_file}: {e}")
            file_count = sum(1 for _, _, files in os.walk(static_pm_dir) for _ in files)
            logger.info(f"🌍 PM files copied in static/pm/ ({file_count})")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying PM files: {e}")

    try:
        generators_dir = settings.base_dir / "src" / "sujets0" / "generators"
        static_generators_dir = settings.static_dir / "sujets0" / "generators"
        if generators_dir.exists():
            if static_generators_dir.exists():
                rmtree(static_generators_dir)
            static_generators_dir.mkdir(parents=True, exist_ok=True)
            for file_path in generators_dir.glob("*.py"):
                if file_path.name != "__pycache__":
                    try:
                        dest_file = static_generators_dir / file_path.name
                        copy2(file_path, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {file_path} -> {dest_file}: {e}")
            file_count = len(list(static_generators_dir.glob("*.py")))
            logger.info(f"📝  {file_count}  Sujets0 generators ready")
        else:
            logger.warning(f"⚠️ Generators directory not found: {generators_dir}")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying sujets0 generators: {e}")

    try:
        official_curriculums_dir = settings.base_dir / "official_curriculums"
        static_official_curriculums_dir = settings.static_dir / "official_curriculums"
        os.makedirs(static_official_curriculums_dir, exist_ok=True)
        for root, dirs, files in os.walk(official_curriculums_dir):
            rel_root = os.path.relpath(root, official_curriculums_dir)
            dest_root = (
                static_official_curriculums_dir / rel_root
                if rel_root != "."
                else static_official_curriculums_dir
            )
            os.makedirs(dest_root, exist_ok=True)
            for file_path in official_curriculums_dir.glob("**/*"):
                if file_path.is_file():
                    try:
                        dest_file = static_official_curriculums_dir / file_path.relative_to(
                            official_curriculums_dir
                        )
                        copy2(file_path, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {file_path} -> {dest_file}: {e}")
        file_count = len(list(static_official_curriculums_dir.glob("**/*")))
        logger.info(f"📝 Official curriculums ready ({file_count} files)")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying official_curriculums: {e}")

    logger.info(
        "✅ All static files copied: JupyterLite (optional), PM, Sujets0, Official curriculums"
    )

    try:
        yield
    finally:
        logger.info("👋 Shutting down...")
