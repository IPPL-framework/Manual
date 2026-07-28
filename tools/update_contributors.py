#!/usr/bin/env python3
"""Generate the manual contributor appendix from IPPL's CONTRIBUTORS.md."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "sections" / "appendix" / "contributors" / "index.qmd"


def default_source() -> Path:
    explicit = os.environ.get("IPPL_CONTRIBUTORS_FILE")
    if explicit:
        return Path(explicit).expanduser()

    ippl_source_dir = os.environ.get("IPPL_SOURCE_DIR")
    if ippl_source_dir:
        return Path(ippl_source_dir).expanduser() / "CONTRIBUTORS.md"

    local_checkout = Path("/Users/adelmann/git/ippl/CONTRIBUTORS.md")
    if local_checkout.exists():
        return local_checkout

    ci_checkout = REPO_ROOT / "ippl-src" / "CONTRIBUTORS.md"
    if ci_checkout.exists():
        return ci_checkout

    return REPO_ROOT.parent / "ippl" / "CONTRIBUTORS.md"


def demote_headings(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        if line.startswith("#"):
            lines.append("#" + line)
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def build_page(source_path: Path) -> str:
    contributors = demote_headings(source_path.read_text(encoding="utf-8"))
    return f"""---
subtitle: "Contributor registry generated from IPPL."
---

# Contributors {{#sec-contributors}}

::: {{.callout-note}}
This page is generated from IPPL's `CONTRIBUTORS.md`.
Edit the source file in the IPPL repository, then regenerate this page with
`python3 tools/update_contributors.py`.
:::

{contributors}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source(),
        help="Path to IPPL CONTRIBUTORS.md.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Generated Quarto contributor page.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(f"Contributor source not found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_page(source), encoding="utf-8")
    print(f"Generated {output} from {source}")


if __name__ == "__main__":
    main()
