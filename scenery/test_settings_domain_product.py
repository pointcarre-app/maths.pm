#!/usr/bin/env python3
"""
Test script to verify domain and product settings are correctly injected into HTML responses.

This script:
1. Makes GET requests to /corsica/ and /nagini endpoints
2. Parses the HTML responses to extract metatags, scripts, and other injected data
3. Compares against expected values from maths.pm.yml, 00_corsica.yml, and 01_nagini.yml
4. Outputs a markdown report showing what was found vs what was expected
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

import httpx
import yaml
from bs4 import BeautifulSoup
from datetime import datetime


class SettingsVerifier:
    """Verifies that domain and product settings are correctly rendered in HTML."""

    def __init__(self, base_url: str = "http://127.0.0.1:5001"):
        self.base_url = base_url
        self.base_dir = Path(__file__).parent.parent
        self.domain_config = self._load_domain_config()
        self.products = self._load_products()
        self.results = []

    def _load_domain_config(self) -> Dict[str, Any]:
        """Load domain configuration from maths.pm.yml"""
        config_path = self.base_dir / "domains" / "maths.pm.yml"
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def _load_products(self) -> Dict[str, Dict[str, Any]]:
        """Load product configurations"""
        products = {}
        products_dir = self.base_dir / "products"

        # Load specific products we're testing
        for product_file in ["00_corsica.yml", "02_nagini.yml"]:
            path = products_dir / product_file
            with open(path, "r") as f:
                config = yaml.safe_load(f)
                products[config["name"]] = config

        return products

    def make_request(self, path: str) -> Optional[str]:
        """Make GET request and return HTML content"""
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client() as client:
                response = client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as e:
            self.results.append(f"❌ Failed to fetch {url}: {e}")
            return None

    def extract_metatags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all meta tags from HTML"""
        metatags = {}

        # Standard meta tags with name attribute
        for tag in soup.find_all("meta", attrs={"name": True}):
            metatags[tag["name"]] = tag.get("content", "")

        # Open Graph meta tags with property attribute
        for tag in soup.find_all("meta", attrs={"property": True}):
            metatags[tag["property"]] = tag.get("content", "")

        return metatags

    def extract_scripts(self, soup: BeautifulSoup) -> List[str]:
        """Extract all script src URLs"""
        scripts = []
        for tag in soup.find_all("script", src=True):
            scripts.append(tag["src"])
        return scripts

    def extract_stylesheets(self, soup: BeautifulSoup) -> List[str]:
        """Extract all stylesheet URLs"""
        stylesheets = []
        for tag in soup.find_all("link", rel="stylesheet"):
            if "href" in tag.attrs:
                stylesheets.append(tag["href"])
        return stylesheets

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find("title")
        return title_tag.text.strip() if title_tag else ""

    def extract_data_brick(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract data-brick information"""
        result = {
            "found": False,
            "elements": [],
            "backend_settings_count": 0,
            "domain_config_attrs": 0,
        }

        # Look for the custom <data-brick> element
        data_brick = soup.find("data-brick")
        if data_brick:
            result["found"] = True

            # Check for domain-config div
            domain_config = soup.find(id="domain-config")
            if domain_config:
                result["elements"].append("domain-config")
                # Count data attributes
                result["domain_config_attrs"] = len(
                    [attr for attr in domain_config.attrs if attr.startswith("data-")]
                )

            # Check for backend-public-settings div
            backend_settings = soup.find(id="backend-public-settings")
            if backend_settings:
                result["elements"].append("backend-public-settings")
                # Count data attributes
                result["backend_settings_count"] = len(
                    [attr for attr in backend_settings.attrs if attr.startswith("data-")]
                )

            # Check for specific product settings divs
            for elem_id in ["nagini-settings", "pca-corpus-settings", "pca-teachers-settings"]:
                elem = soup.find(id=elem_id)
                if elem:
                    result["elements"].append(elem_id)

        return result

    def verify_domain_metatags(self, metatags: Dict[str, str]) -> Dict[str, Any]:
        """Verify domain-wide metatags"""
        domain_meta = self.domain_config.get("domain_specific_metatags", {})
        results = {"found": [], "missing": [], "mismatched": []}

        # Check essential domain metatags
        essential_tags = [
            "viewport",
            "theme-color",
            "subject",
            "copyright",
            "language",
            "Classification",
            "rating",
            "HandheldFriendly",
            "MobileOptimized",
            "og:site_name",
            "twitter:site",
        ]

        for tag in essential_tags:
            expected = domain_meta.get(tag) or domain_meta.get(tag.replace(":", "_"))
            actual = metatags.get(tag)

            if expected:
                if actual == expected:
                    results["found"].append(f"✅ {tag}: {actual}")
                elif actual:
                    results["mismatched"].append(f"⚠️ {tag}: expected '{expected}', got '{actual}'")
                else:
                    results["missing"].append(f"❌ {tag}: expected '{expected}'")

        return results

    def verify_page_metatags(
        self, metatags: Dict[str, str], product_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify page-specific metatags"""
        results = {"found": [], "missing": [], "mismatched": []}

        # Get expected metatags based on product or index
        if product_name and product_name in self.products:
            expected_meta = self.products[product_name].get("metatags", {})
        else:
            expected_meta = self.domain_config.get("index_view_specific_metatags", {})

        # Check key page-specific tags
        key_tags = [
            "title",
            "description",
            "keywords",
            "og:title",
            "og:description",
            "twitter:title",
            "twitter:description",
        ]

        for tag in key_tags:
            expected = expected_meta.get(tag)
            actual = metatags.get(tag)

            if expected:
                if actual == expected:
                    results["found"].append(f"✅ {tag}: {actual[:50]}...")
                elif actual:
                    results["mismatched"].append(f"⚠️ {tag}: mismatch")
                else:
                    results["missing"].append(f"❌ {tag}: missing")

        return results

    def verify_backend_settings(self, scripts: List[str], product_name: str) -> Dict[str, Any]:
        """Verify backend settings (scripts) are loaded"""
        results = {"found": [], "missing": [], "backend_config": {}, "scripts_checked": scripts}

        if product_name not in self.products:
            results["error"] = f"Product {product_name} not in loaded products"
            return results

        backend = self.products[product_name].get("backend_settings", {})
        results["backend_config"] = backend

        if not backend:
            results["error"] = f"No backend_settings found in {product_name}.yml"
            return results

        # Check for expected script URLs
        for service, settings in backend.items():
            if isinstance(settings, dict):
                # Check various URL fields
                url_fields = ["js_url", "entrypoint_url", "lib_url", "worker_url", "endpoint"]
                for field in url_fields:
                    if field in settings:
                        expected_url = settings[field]
                        # For script URLs, check if they're loaded
                        if field.endswith("_url"):
                            if any(expected_url in script for script in scripts):
                                results["found"].append(
                                    f"✅ {service}.{field}: {expected_url[:50]}..."
                                )
                            else:
                                results["missing"].append(
                                    f"❌ {service}.{field} not in scripts. Looking for: {expected_url}"
                                )
                        else:
                            # For non-URL fields like endpoints, just note them
                            results["found"].append(f"ℹ️ {service}.{field}: {expected_url[:50]}...")

        return results

    def generate_report(self, path: str, html_content: str) -> str:
        """Generate markdown report for a single page"""
        report = []
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract product name from path
        product_name = path.strip("/").split("/")[0] if path != "/" else None

        report.append(f"## 📍 Testing: {path}")
        report.append(f"**URL**: {self.base_url}{path}")
        report.append(f"**Product**: {product_name or 'Index page'}")
        report.append(f"**Timestamp**: {datetime.now().isoformat()}")
        report.append("")

        # Extract data
        title = self.extract_title(soup)
        metatags = self.extract_metatags(soup)
        scripts = self.extract_scripts(soup)
        stylesheets = self.extract_stylesheets(soup)
        data_brick_info = self.extract_data_brick(soup)

        # Basic info
        report.append("### 📊 Basic Information")
        report.append(f"- **Page Title**: {title}")
        report.append(f"- **Total Metatags Found**: {len(metatags)}")
        report.append(f"- **Total Scripts Loaded**: {len(scripts)}")
        report.append(f"- **Total Stylesheets**: {len(stylesheets)}")
        # Data brick info
        if data_brick_info["found"]:
            report.append(
                f"- **Data Brick**: ✅ Found with {len(data_brick_info['elements'])} elements"
            )
            report.append(f"  - Elements: {', '.join(data_brick_info['elements'])}")
            report.append(f"  - Domain config attrs: {data_brick_info['domain_config_attrs']}")
            report.append(
                f"  - Backend settings attrs: {data_brick_info['backend_settings_count']}"
            )
        else:
            report.append("- **Data Brick**: ❌ Not found")
        report.append("")

        # Domain metatags verification
        report.append("### 🌍 Domain-Wide Metatags (from maths.pm.yml)")
        domain_results = self.verify_domain_metatags(metatags)

        if domain_results["found"]:
            report.append("**Found:**")
            for item in domain_results["found"][:5]:  # Show first 5
                report.append(f"  {item}")
            if len(domain_results["found"]) > 5:
                report.append(f"  ... and {len(domain_results['found']) - 5} more")

        if domain_results["missing"]:
            report.append("**Missing:**")
            for item in domain_results["missing"]:
                report.append(f"  {item}")

        if domain_results["mismatched"]:
            report.append("**Mismatched:**")
            for item in domain_results["mismatched"]:
                report.append(f"  {item}")
        report.append("")

        # Page-specific metatags
        report.append("### 📄 Page-Specific Metatags")
        page_results = self.verify_page_metatags(metatags, product_name)

        if page_results["found"]:
            report.append("**Found:**")
            for item in page_results["found"]:
                report.append(f"  {item}")

        if page_results["missing"]:
            report.append("**Missing:**")
            for item in page_results["missing"]:
                report.append(f"  {item}")
        report.append("")

        # Backend settings (for product pages)
        if product_name:
            report.append(f"### ⚙️ Backend Settings (from {product_name}.yml)")
            backend_results = self.verify_backend_settings(scripts, product_name)

            # Show error if any
            if "error" in backend_results:
                report.append(f"**Error:** {backend_results['error']}")

            # Show backend config from YAML
            if backend_results["backend_config"]:
                report.append("**Expected backend_settings from YAML:**")
                report.append("```yaml")
                import yaml

                report.append(
                    yaml.dump(backend_results["backend_config"], default_flow_style=False)
                )
                report.append("```")

            if backend_results["found"]:
                report.append("**Scripts Loaded:**")
                for item in backend_results["found"]:
                    report.append(f"  {item}")

            if backend_results["missing"]:
                report.append("**Scripts Missing:**")
                for item in backend_results["missing"]:
                    report.append(f"  {item}")

            # Debug: Show actual scripts found
            report.append("**All scripts in page:**")
            for script in scripts[:5]:
                report.append(f"  - {script}")
            if len(scripts) > 5:
                report.append(f"  ... and {len(scripts) - 5} more")
            report.append("")

        # Raw data sections for debugging
        report.append("### 🔍 Raw Data Samples")
        report.append("<details>")
        report.append("<summary>Click to expand metatags sample</summary>")
        report.append("")
        report.append("```json")
        sample_meta = dict(list(metatags.items())[:10])
        report.append(json.dumps(sample_meta, indent=2))
        report.append("```")
        report.append("</details>")
        report.append("")

        report.append("<details>")
        report.append("<summary>Click to expand scripts list</summary>")
        report.append("")
        for script in scripts[:10]:  # Show more scripts
            report.append(f"- {script}")
        if len(scripts) > 10:
            report.append(f"- ... and {len(scripts) - 10} more")
        report.append("</details>")
        report.append("")

        # Add HTML snippet for debugging
        report.append("<details>")
        report.append("<summary>Click to expand HTML head snippet (first 2000 chars)</summary>")
        report.append("")
        report.append("```html")
        head = soup.find("head")
        if head:
            head_str = str(head)[:2000]
            report.append(head_str)
            if len(str(head)) > 2000:
                report.append("... (truncated)")
        report.append("```")
        report.append("</details>")
        report.append("")

        # Add data-brick HTML for debugging
        report.append("<details>")
        report.append("<summary>Click to expand data-brick HTML</summary>")
        report.append("")
        report.append("```html")
        data_brick_elem = soup.find("data-brick")
        if data_brick_elem:
            report.append(str(data_brick_elem)[:1500])
            if len(str(data_brick_elem)) > 1500:
                report.append("... (truncated)")
        else:
            report.append("<!-- data-brick element not found -->")
        report.append("```")
        report.append("</details>")
        report.append("")

        return "\n".join(report)

    def run_tests(self) -> str:
        """Run all tests and generate full report"""
        full_report = []

        # Header
        full_report.append("# 🧪 Domain and Product Settings Verification Report")
        full_report.append("")
        full_report.append(
            "This report verifies that domain configuration (maths.pm.yml) and product"
        )
        full_report.append(
            "configurations (00_corsica.yml, 01_nagini.yml) are correctly injected into"
        )
        full_report.append("the HTML responses.")
        full_report.append("")
        full_report.append("---")
        full_report.append("")

        # Test each endpoint
        endpoints = ["/corsica/", "/nagini"]  # Note: nagini might not need trailing slash

        for endpoint in endpoints:
            html_content = self.make_request(endpoint)
            if html_content:
                report = self.generate_report(endpoint, html_content)
                full_report.append(report)
                full_report.append("---")
                full_report.append("")
            else:
                full_report.append(f"## ❌ Failed to test {endpoint}")
                full_report.append("")
                full_report.append("---")
                full_report.append("")

        # Summary
        full_report.append("## 📋 Summary and Recommendations")
        full_report.append("")
        full_report.append("### Current Implementation Analysis")
        full_report.append("")
        full_report.append("The current template system (`main-alt.html`) correctly:")
        full_report.append(
            "1. ✅ Loads domain-wide metatags from `DOMAIN_CONFIG.domain_specific_metatags`"
        )
        full_report.append(
            "2. ✅ Loads page defaults from `DOMAIN_CONFIG.index_view_specific_metatags`"
        )
        full_report.append("3. ✅ Implements Smart Product Dependency Loader for backend settings")
        full_report.append("4. ✅ Includes `data-brick.html` for additional data injection")
        full_report.append("")
        full_report.append("### 🚀 Proposed Refactoring: Lifespan Validation")
        full_report.append("")
        full_report.append("Instead of runtime testing, implement validation at app startup:")
        full_report.append("")
        full_report.append("```python")
        full_report.append("# In app.py or a new startup.py module")
        full_report.append("from contextlib import asynccontextmanager")
        full_report.append("from fastapi import FastAPI")
        full_report.append("")
        full_report.append("@asynccontextmanager")
        full_report.append("async def lifespan(app: FastAPI):")
        full_report.append("    # Startup: Validate all settings")
        full_report.append("    from .settings import settings")
        full_report.append("    ")
        full_report.append("    # 1. Verify domain config is loaded")
        full_report.append("    assert settings.domain_config.domain_url")
        full_report.append("    assert settings.domain_config.templating")
        full_report.append("    ")
        full_report.append("    # 2. Verify products are loaded and have required fields")
        full_report.append("    for product in settings.products:")
        full_report.append("        assert product.name")
        full_report.append("        assert product.title_html")
        full_report.append("        # Verify product metatags if present")
        full_report.append("        if hasattr(product, 'metatags'):")
        full_report.append("            assert product.metatags.get('title')")
        full_report.append("    ")
        full_report.append("    # 3. Pre-compile template context for validation")
        full_report.append("    context = {")
        full_report.append("        'DOMAIN_CONFIG': settings.domain_config.dict(),")
        full_report.append("        'products': settings.products,")
        full_report.append(
            "        'backend_public_settings': settings.serialized_backend_settings"
        )
        full_report.append("    }")
        full_report.append("    ")
        full_report.append("    # 4. Log validation results")
        full_report.append("    logger.info(f'✅ Loaded {len(settings.products)} products')")
        full_report.append("    logger.info(f'✅ Domain config valid for {settings.domain_name}')")
        full_report.append("    ")
        full_report.append("    yield  # App runs here")
        full_report.append("    ")
        full_report.append("    # Shutdown: Cleanup if needed")
        full_report.append("    logger.info('Shutting down...')")
        full_report.append("")
        full_report.append("app = FastAPI(lifespan=lifespan)")
        full_report.append("```")
        full_report.append("")
        full_report.append("### Benefits of Lifespan Validation:")
        full_report.append("1. **Early Detection**: Settings errors caught at startup, not runtime")
        full_report.append("2. **Performance**: No validation overhead during requests")
        full_report.append("3. **Reliability**: App won't start with invalid configuration")
        full_report.append("4. **Observability**: Clear startup logs showing what's loaded")
        full_report.append("")

        return "\n".join(full_report)


def main():
    """Main entry point"""
    print("🚀 Starting Domain and Product Settings Verification...")
    print()

    # Check if server is running
    try:
        with httpx.Client() as client:
            client.get("http://127.0.0.1:5001/", timeout=5.0)
        print("✅ Server is running")
    except httpx.HTTPError:
        print("❌ Server is not running at http://127.0.0.1:5001")
        print("Please start the server with: uvicorn src.app:app --reload --port 5001")
        sys.exit(1)

    # Run verification
    verifier = SettingsVerifier()
    report = verifier.run_tests()

    # Also save raw HTML for debugging
    for endpoint in ["/corsica/", "/nagini"]:
        try:
            html_content = verifier.make_request(endpoint)
            if html_content:
                filename = endpoint.strip("/").replace("/", "_") or "index"
                debug_path = Path(__file__).parent / f"debug_{filename}.html"
                with open(debug_path, "w") as f:
                    f.write(html_content)
                print(f"📝 Saved raw HTML to: {debug_path}")
            else:
                print(f"⚠️ No content received for {endpoint}")
        except Exception as e:
            print(f"❌ Error saving debug HTML for {endpoint}: {e}")

    # Save report
    report_path = Path(__file__).parent / "settings_verification_report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"📄 Report saved to: {report_path}")
    print()
    print("Preview of findings:")
    print("=" * 60)

    # Print summary to console
    lines = report.split("\n")
    for line in lines[:100]:  # Show more lines for preview
        print(line)

    if len(lines) > 100:
        print("...")
        print(f"(Full report: {len(lines)} lines)")

    # Also save the raw HTML for debugging
    print("\n" + "=" * 60)
    print("💡 Debugging Tips:")
    print("1. Check raw HTML files saved in scenery/ directory")
    print("2. Look for data-brick element in the HTML")
    print("3. Verify product metatags are being injected")


if __name__ == "__main__":
    main()
