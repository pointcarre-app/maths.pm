---
title: Layout directives for responsive columns
---

# Layout directives for responsive columns

This guide shows how to place two or three fragments side-by-side using a simple markdown directive, without writing any HTML.

## Syntax

Use a horizontal rule with an attribute list to declare the layout container. The directive is recognized at runtime and wraps the next N fragments into a responsive grid.

```
--- {: .pm-cols-[bp]-[n] [optional Tailwind classes] }
```

- `[bp]`: `sm`, `md`, or `lg` breakpoint. If omitted, defaults to `md`.
- `[n]`: column count `2` or `3`.
- Optional utilities after the directive class (e.g., `gap-4`) are applied to the container.

The directive consumes itself and wraps the next `n` fragments (whatever their types are), keeping mobile as a single column and switching to columns at your chosen breakpoint.

## Example: two columns on small screens and up

Below example uses your paragraph and SVG side-by-side starting at the `sm` breakpoint. On smaller screens it stacks.

```md
--- {: .pm-cols-sm-2 }

On a représenté la Corse sur la carte ci-dessous. Cette carte est en $2$ dimensions, elle est représentée sur une surface plane ($=$ "à plat").  On superpose un quadrillage assez particulier sur la carte, il s'agit de ce type de quadrillage qui sont (entre autres) sur les globes terrestres.

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .max-w-[340px] .mx-auto}
```

### Variants

- `--- {: .pm-cols-md-2 }` two columns on `md` and up
- `--- {: .pm-cols-lg-2 }` two columns on `lg` and up
- `--- {: .pm-cols-md-3 }` three columns on `md` and up
- Add spacing: `--- {: .pm-cols-md-2 gap-4 }`

## Custom column percentages

You can set explicit percentages for each column with a `.cols-…` token:

```md
--- {: .pm-cols-md-2 gap-4 .cols-30-70 }

Texte (30%).

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_with_labels.svg)
{: .max-w-[600px] .mx-auto}
```

Works with three columns too, e.g. `.cols-25-50-25`.

## Vertically centering a single fragment

Use helper classes on the fragment to align within its grid cell:

- `.pm-self-center`: vertical centering (`align-self: center`)
- `.pm-place-center`: both vertical and horizontal centering (`place-self: center`)

Example:

```md
--- {: .pm-cols-sm-2 gap-5 .cols-60-40 }

Paragraphe centré verticalement dans sa colonne.
{: .pm-self-center }

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_simple_no_title.svg)
{: .max-w-[420px] .mx-auto}
```

## Notes

- No HTML is required. Keep writing normal markdown.
- Any fragment types can be grouped (paragraphs, images, SVGs, lists, radios, etc.).
- Attribute-list classes on your fragments (like the image’s `.max-w-[340px] .mx-auto` or `.pm-self-center`) are preserved.


