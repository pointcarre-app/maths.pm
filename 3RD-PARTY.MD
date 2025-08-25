# 3RD-PARTY.md

This file documents **all third-party dependencies** used in the **maths.pm repository** and its related Pointcarre projects (Nagini, Papyrus, Teachers) that we build, their licenses, runtime usage, and AGPLv3 compatibility.

**Primary Repository:** maths.pm (this repository)  
**Related Projects:** Nagini, Papyrus, PCA Teachers (built from this repository)

***

## AGPLv3 Compatibility Matrix (All Dependencies)

| Dependency | License | Usage / Import Context | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| ipykernel | BSD 3-Clause | Jupyter/IPython kernel (dev, core) | ✅ Compatible |
| matplotlib | PSF/BSD-like | Plotting/data viz (dev, core) | ✅ Compatible |
| djlint | MIT | Jinja/Django linter (dev) | ✅ Compatible |
| black | MIT | Code formatter (dev) | ✅ Compatible |
| ruff | MIT | Python linter (dev) | ✅ Compatible |
| httpx | BSD 3-Clause | HTTP client (runtime, app) | ✅ Compatible |
| fastapi | MIT | Web framework (runtime, app) | ✅ Compatible |
| jinja2 | BSD 3-Clause | Templates (runtime, app/Teachers) | ✅ Compatible |
| markdown | BSD 3-Clause | Markdown parsing | ✅ Compatible |
| orjson | Apache 2.0 | Fast JSON handling | ✅ Compatible |
| pydantic | MIT | Data validation | ✅ Compatible |
| pydantic-settings | MIT | Settings/configuration | ✅ Compatible |
| python-dotenv | BSD 3-Clause | Env management | ✅ Compatible |
| uvicorn | BSD 3-Clause | ASGI server (runtime) | ✅ Compatible |
| gunicorn | MIT | WSGI server (runtime, prod) | ✅ Compatible |
| jupyterlite-core | BSD 3-Clause | Browser Jupyter environment | ✅ Compatible |
| jupyterlite-pyodide-kernel | BSD 3-Clause | Pyodide kernel for JupyterLite | ✅ Compatible |
| jupyterlite-p5-kernel | BSD 3-Clause | p5.js kernel for JupyterLite | ✅ Compatible |
| bs4 (BeautifulSoup) | MIT | HTML/XML parsing | ✅ Compatible |
| strictyaml | MIT | YAML validation | ✅ Compatible |
| minify-html | MIT | HTML minification (future) | ✅ Compatible |
| sympy | BSD 3-Clause | Symbolic mathematics (future) | ✅ Compatible |
| passlib | BSD/Apache 2.0 | Authentication utils (future) | ✅ Compatible |
| pyjwt | MIT | JWT authentication (future) | ✅ Compatible |
| python-multipart | Apache 2.0 | Multipart form data (future) | ✅ Compatible |
| PyYAML | MIT | YAML parsing | ✅ Compatible |
| Pyodide | MPL 2.0 | Python runtime in browser | ✅ Compatible |
| Brython | BSD 3-Clause | Python-to-JS transpiler | ✅ Compatible |
| ANTLR4-Python3-runtime | BSD/MIT | Parsing runtime | ✅ Compatible |
| KaTeX | MIT | Math typography in frontend | ✅ Compatible |
| Tailwind CSS | MIT | CSS utility framework | ✅ Compatible |
| DaisyUI | MIT | CSS component library | ✅ Compatible |
| Google Fonts (multiple) | SIL Open Font License 1.1 | Web font typography | ✅ Compatible |
| MathLive | MIT | Interactive math input editor | ✅ Compatible |
| Lit | BSD 3-Clause | Web components library | ✅ Compatible |
| lit-html | BSD 3-Clause | HTML templating library | ✅ Compatible |

All dependencies above are **fully AGPLv3 compatible**.

***

## Usage Model

- **maths.pm Backend:** All Python dependencies in app and library code are under permissive licenses.
- **maths.pm Frontend:** Browser/CDN dependencies (KaTeX, Tailwind, DaisyUI, Google Fonts, MathLive, Lit) are loaded at runtime, not redistributed.
- **Nagini/JupyterLite:** Runtime dependencies loaded at runtime by users via browser.
- **Papyrus:** Frontend framework using CDN-loaded dependencies.
- **Teachers:** Distributed exclusively via PyPI requirements under AGPLv3, no modification or redistribution of third-party code.
- **Development tools:** Only relevant for development, not runtime obligations.

***

## License Requirements

- **MIT/BSD/Apache2/OFL:** Require attribution only, do not impose copyleft on your own code.
- **MPL 2.0 (Pyodide):** Only triggers copyleft if code is modified—runtime use is not affected.

***

## AGPLv3 Compliance Checklist

- [x] Attribution: All notices preserved (runtime/CDN/PyPI).
- [x] No source code modification of third-party projects.
- [x] No redistribution outside standard packaging.
- [x] License compatibility: All licenses are AGPLv3 compatible.
- [x] Documentation: This file serves as compliance documentation.
- [x] Source availability: All custom code is AGPLv3.
- [x] Network use: AGPLv3 provisions honored.

***

## Full License Reference Set

- MIT: https://opensource.org/licenses/MIT
- BSD 3-Clause: https://opensource.org/licenses/BSD-3-Clause
- Apache 2.0: https://www.apache.org/licenses/LICENSE-2.0
- MPL 2.0: https://mozilla.org/MPL/2.0/
- SIL OFL 1.1: https://scripts.sil.org/OFL
- AGPL v3: https://www.gnu.org/licenses/agpl-3.0

***

## Nagini Dependency Table (Related Project)

| Dependency | License | Usage | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| Pyodide | MPL 2.0 | Python runtime for browser | ✅ Compatible |
| Brython | BSD 3-Clause | Python-to-JS transpiler | ✅ Compatible |
| JupyterLite-pyodide-kernel | BSD 3-Clause | Browser Python kernel | ✅ Compatible |
| JupyterLite-p5-kernel | BSD 3-Clause | Processing JS kernel | ✅ Compatible |
| Sympy | BSD 3-Clause | Symbolic mathematics | ✅ Compatible |
| StrictYAML | MIT | YAML validation | ✅ Compatible |
| Pydantic | MIT | Data modeling/validation | ✅ Compatible |
| ANTLR4-Python3-runtime | BSD/MIT | Parsing runtime | ✅ Compatible |

***

## Papyrus Dependency Table (Related Project)

| Dependency | License | Usage | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| KaTeX | MIT | Math typesetting | ✅ Compatible |
| Tailwind CSS | MIT | CSS framework | ✅ Compatible |
| DaisyUI | MIT | Component library for Tailwind | ✅ Compatible |
| Google Fonts | SIL Open Font License | Comfortaa, Spectral, Inter, JetBrains Mono, Lexend, Playfair Display, EB Garamond, Source Serif 4, Dancing Script, Cormorant Garamond, Lora (CDN) | ✅ Compatible |

***

## maths.pm Dependency Table (This Repository)

| Dependency | License | Usage | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| httpx | BSD 3-Clause | HTTP client for static site generation | ✅ Compatible |
| fastapi | MIT | Web API framework | ✅ Compatible |
| jinja2 | BSD 3-Clause | Template engine for FastAPI | ✅ Compatible |
| markdown | BSD 3-Clause | Markdown parsing for README/docs | ✅ Compatible |
| orjson | Apache 2.0 | Fast JSON serialization | ✅ Compatible |
| pydantic | MIT | Data schema validation | ✅ Compatible |
| pydantic-settings | MIT | Configuration and settings management | ✅ Compatible |
| python-dotenv | BSD 3-Clause | Environment variable management | ✅ Compatible |
| uvicorn | BSD 3-Clause | ASGI web server | ✅ Compatible |
| jupyterlite-core | BSD 3-Clause | Browser-based Jupyter core | ✅ Compatible |
| jupyterlite-pyodide-kernel | BSD 3-Clause | Pyodide kernel for JupyterLite | ✅ Compatible |
| jupyterlite-p5-kernel | BSD 3-Clause | p5.js kernel for JupyterLite | ✅ Compatible |
| bs4 (BeautifulSoup4) | MIT | HTML/XML parsing | ✅ Compatible |
| PyYAML | MIT | YAML parsing | ✅ Compatible |
| strictyaml | MIT | YAML validation | ✅ Compatible |
| MathLive | MIT | Interactive math input editor (frontend) | ✅ Compatible |
| Lit | BSD 3-Clause | Web components library (frontend) | ✅ Compatible |
| lit-html | BSD 3-Clause | HTML templating library (frontend) | ✅ Compatible |

### Development Dependencies (requirements-dev.txt)
| Dependency | License | Usage | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| ipykernel | BSD 3-Clause | Jupyter/IPython kernel (dev) | ✅ Compatible |
| matplotlib | PSF/BSD-like | Plotting/data visualization (dev) | ✅ Compatible |
| djlint | MIT | Jinja/Django template linter | ✅ Compatible |
| black | MIT | Python code formatter | ✅ Compatible |
| ruff | MIT | Python linter | ✅ Compatible |

### Planned/Commented Dependencies (in requirements.txt)
| Dependency | License | Planned Usage | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| gunicorn | MIT | Production WSGI server | ✅ Compatible |
| minify-html | MIT | HTML minification for optimization | ✅ Compatible |
| sympy | BSD 3-Clause | Symbolic mathematics | ✅ Compatible |
| passlib[bcrypt] | BSD/Apache 2.0 | Password hashing | ✅ Compatible |
| pyjwt | MIT | JWT authentication | ✅ Compatible |
| python-multipart | Apache 2.0 | Multipart form data handling | ✅ Compatible |

***

## PCA Teachers Dependency Table (Related Project)

| Dependency | License | Usage Type | AGPLv3 Compatibility |
| :-- | :-- | :-- | :-- |
| antlr4-python3-runtime | BSD 3-Clause | Runtime (LaTeX parsing via SymPy) | ✅ Compatible |
| pydantic | MIT | Runtime (data validation/settings) | ✅ Compatible |
| sympy | BSD 3-Clause | Runtime (symbolic mathematics engine) | ✅ Compatible |

***

## PCA Teachers Usage Model

**Important:** PCA Teachers distributes dependencies through standard PyPI mechanisms under AGPL v3.0 licensing; no modification, forking, or bundling third-party source code.  
- **No source modification:** Dependencies used as-is from PyPI.  
- **No redistribution:** Dependencies installed independently by end users.  
- **AGPL obligations:** Full source provided for all AGPL network use scenarios.  

***

## Compliance Checklist (Teachers)

- [x] License compatibility: Permissive, AGPLv3-safe.
- [x] No redistribution: All from PyPI only.
- [x] No modification: Official distributions only.
- [x] Attribution: Handled via PyPI metadata.
- [x] AGPLv3 distribution: Full source included.
- [x] Network use: AGPLv3 covered.
- [x] Versioning: antlr4 locked for SymPy compatibility.

***

## Legal Disclaimer

This analysis is based on publicly available licensing information and standard usage patterns.  
For critical deployments, always consult qualified legal counsel to confirm compliance with all license terms and regulations.[1][3]

***

**All dependencies and usage are documented for AGPLv3 compliance. All required legal and practical details—in tables, usage notes, and references—are now provided.*

[1] https://packaging.python.org/en/latest/guides/licensing-examples-and-user-scenarios/
[2] https://software.rcc.uchicago.edu/git/help/user/compliance/license_compliance/index.md
[3] https://www.python4data.science/en/24.3.0/productive/licensing.html
[4] https://github.com/franneck94/Python-Project-Template/blob/master/LICENSE
[5] https://gitlab.com/gitlab-org/gitlab-foss/-/tree/b558264c9d10841f46a8ffeb15f18d0cee60fa7a/doc/user/application_security/license_compliance
[6] https://src.koda.cnrs.fr/hermes/cst-python-api/-/blob/main/docs/source/license.rst
[7] https://py-generic-project.readthedocs.io/_/downloads/en/latest/pdf/
[8] https://gitlab.eopf.copernicus.eu/sde/project-template/-/blob/ci-windows-unit-tests/LICENSE
[9] https://docs.infoblox.com/space/MAG8/912294077/PSF+License+Agreement+for+Python+3.5.0
[10] https://pypi.org/project/compliance-trestle/