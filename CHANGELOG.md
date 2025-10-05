# CHANGELOG.md




## [v0.0.10] size of repo < 50Mb


+ redeployed


```bash
git clone --depth 1 https://github.com/pointcarre-app/maths.pm temp-check

# Cloning into 'temp-check'...
# remote: Enumerating objects: 771, done.
# remote: Counting objects: 100% (771/771), done.
# remote: Compressing objects: 100% (668/668), done.
# remote: Total 771 (delta 124), reused 490 (delta 72), pack-reused 0 (from 0)
# Receiving objects: 100% (771/771), 15.82 MiB | 31.70 MiB/s, done.
# Resolving deltas: 100% (124/124), done.
```

```bash
du -sh temp-check
# 45M	temp-check
```



## Git manip

- Removed "cubrick" folder at root (anims + videos movs for roll one, twice, thrice) etc..


## Git manip

- Deleted branches `origin/mad-2025-09-16`
- Deleted all local branches (cause all merged):
    - `sel-dataviz2-stable-isolation-and-backend`
    - `bac-main`


## [v0.0.9]

- Isolation dependencies for products logic done + dataviz2


## [v0.0.5]

- Sujets0:
    - Generation of pdf with 1 to 12 questions for 1 to 50 students WITH FORM
    - Working remotely using static website (except Fiches Réponses Enseignants)
    - 🟡 Tentative Gandi domain name for github.io



## [v0.0.4]

- Generation using `/pm` ok for sujet 1 Spé Maths + priting with chrome


## [v0.0.3]

### Infrastructure
- **Safari CSS Download Management**:
  - Automatic download of external CSS files for Safari CORS compatibility  
  - Smart CI/GitHub Actions detection ensures assets are always present in deployment
  - Local development optimization: checks existing files, only downloads if missing
  - Environment variable `DOWNLOAD_SAFARI_CSS` for manual control
  - Improved error handling: critical failures stop CI deployment, warnings in local dev
  - Force download with `force_download=True` parameter in CI environments
  - Downloads Google Fonts, DaisyUI, KaTeX, and Papyrus styles locally
  - Documentation: `notes/SAFARI_CSS_DOWNLOAD.md`
  - Fixed: CI now skips CSS downloads entirely (files are committed to git)
  - Added: Better server startup retry logic in GitHub Actions build script
  - Safari CSS files are now committed to repository in `src/static/css/safari-local/`
  - 🔴 empty page at the end when printing... safari...

## [v0.0.2]

- Sujets0:
    - Safari:
        - svg working
        - text-2xs injection (TODO sel: generalize) 
        - button print multiple use if multiple generation / 🔴 empty page at the end when printing


[v0.0.1]

- Sujets0: 
    - Generation of pdf with 1 to 12 questions for 1 to 50 students
    - Working remotely using static website (except Fiches Réponses Enseignants)