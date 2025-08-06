# Data Models

This document outlines the main data models used in the application for configuration and content management.

## `ProductModel`

Represents a single service or "product" displayed on the homepage. This model is populated from the `.yml` files in the `/products` directory.

### Attributes

| Attribute           | Type               | Description                                                                 |
| ------------------- | ------------------ | --------------------------------------------------------------------------- |
| `name`              | `str`              | A unique identifier for the product (e.g., "jupyterlite").                  |
| `title_html`        | `str`              | The main title of the product card, HTML is allowed.                        |
| `subtitle_html`     | `Optional[str]`    | An optional subtitle, HTML is allowed.                                      |
| `description`       | `str`              | A short description of the product displayed on the card.                   |
| `local_path`        | `Optional[str]`    | The internal link to the service (e.g., `/jupyterlite/lab/index.html`).     |
| `source_link`       | `Optional[str]`    | An external link to the source code repository.                             |
| `figure_svg`        | `Optional[str]`    | The filename of an SVG figure to display in the card header.                |
| `figure_png`        | `Optional[str]`    | The path to a PNG image to display in the card header.                      |
| `color`             | `str`              | The theme color for the product card (e.g., "primary", "warning").          |
| `classes_formatted` | `Optional[List[str]]` | A list of badges or tags to display (e.g., grade levels).                 |
| `tags`              | `Optional[List[str]]` | A list of keywords for filtering or metadata.                               |
| `domains`           | `List[str]`        | A list of domains where this product should be displayed.                   |

---

## `DomainModel`

A robust Pydantic model for the entire domain configuration, loaded from `domains/maths.pm.yml`. It provides default values for optional sections to prevent template errors.

### Nested Models

#### `TemplatingModel`

Defines the structure for templating settings.

| Attribute             | Type    | Description                                       |
| --------------------- | ------- | ------------------------------------------------- |
| `base_template`       | `str`   | Path to the main base template file.              |
| `footer_template`     | `str`   | Path to the domain-specific footer template.      |
| `navbar_title`        | `str`   | The title displayed in the navigation bar.        |
| `button_primary_text` | `str`   | Text for the primary call-to-action button.       |
| `button_primary_href` | `str`   | Link for the primary call-to-action button.       |
| `button_ghost_text`   | `str`   | Text for the secondary (ghost) button.            |
| `button_ghost_href`   | `str`   | Link for the secondary (ghost) button.            |

#### `ExtraHeadModel`

Defines the structure for extra JavaScript or CSS dependencies.

| Attribute | Type         | Default     | Description                               |
| --------- | ------------ | ----------- | ----------------------------------------- |
| `js`      | `List[str]`  | `[]`        | A list of URLs for JavaScript files to include. |
| `css`     | `List[str]`  | `[]`        | A list of URLs for CSS files to include.      |

### Main `DomainModel` Attributes

| Attribute                      | Type                    | Default           | Description                                                        |
| ------------------------------ | ----------------------- | ----------------- | ------------------------------------------------------------------ |
| `domain_url`                   | `str`                   |                   | The root URL of the domain.                                        |
| `domain_specific_metatags`     | `Dict[str, Any]`        | `{}`              | A dictionary of meta tags for all pages in the domain.             |
| `index_view_specific_metatags` | `Dict[str, Any]`        | `{}`              | A dictionary of meta tags specific to the homepage.                |
| `templating`                   | `TemplatingModel`       |                   | An object containing templating settings.                          |
| `extra_head`                   | `ExtraHeadModel`        | `ExtraHeadModel()` | An object containing lists of extra JS and CSS files.              |
| `backend_settings`             | `Dict[str, Any]`        | `{}`              | A dictionary of settings to be passed to the frontend.             | 