# IPPL Manual

This repository contains the Quarto source for the IPPL manual. The rendered HTML book is written to `docs/` and published with GitHub Pages at:

```text
https://IPPL-framework.github.io/Manual/
```

## Render locally

```bash
quarto render
```

Open the rendered manual at:

```text
docs/index.html
```

## API reference

The manual is intended to be paired with Doxygen output generated from the IPPL source tree:

```bash
cd /Users/adelmann/git/ippl
doxygen doc/Doxyfile
```

The manual repository also contains `Doxyfile.api`, which writes API HTML directly under `docs/api/`:

```bash
IPPL_SOURCE_DIR=/Users/adelmann/git/ippl doxygen Doxyfile.api
```

For GitHub Pages, render the Quarto book to `docs/` and place generated Doxygen HTML under `docs/api/`, or link to the hosted Doxygen site from the API reference chapter.

## GitHub Pages

The workflow in `.github/workflows/publish.yml` builds the complete site on every push to `main`:

1. Check out this manual repository.
2. Check out `IPPL-framework/ippl` as the Doxygen source tree.
3. Render the Quarto book to `docs/`.
4. Render Doxygen API HTML to `docs/api/`.
5. Upload `docs/` as a GitHub Pages artifact and deploy it.

In the repository settings, Pages must be configured to use **GitHub Actions** as the build and deployment source.

The public URL `https://IPPL-framework.github.io/Manual/` assumes this repository is hosted as `IPPL-framework/Manual` and that Pages is configured to use the GitHub Actions workflow.

## Structure

- `_quarto.yml`: Quarto book configuration.
- `index.qmd`: manual landing page.
- `sections/*/index.qmd`: chapter sources.
- `references.bib`: IPPL literature and software records.
- `figures/`: manual image assets.
- `docs/`: rendered HTML output.

## Documentation approach

The manual explains workflows, concepts, examples, and design contracts for IPPL users and developers. Exact C++ signatures should remain in Doxygen comments in the IPPL source tree and be linked from the API reference chapter.
