#!/usr/bin/env python3
"""
Build script for Astralia RPG's browser HTML bundles.

The canonical source (../margonem-mini-rpg.jsx) is a real ES module (it has
`import ... from '...'` at the top and `export default function AstraliaRPG()`)
meant for a real bundler. The browser build instead runs everything through
Babel-in-browser via a plain <script type="text/babel"> tag, which CANNOT
execute `import`/`export` statements — leaving them in silently breaks the
live page (it hangs forever on the loading screen with no console error
until you manually run the script text through Babel.transform + eval).

So this script always strips those lines before concatenating the source
into the two HTML bundles:
  - index.html         — full standalone page, for GitHub Pages
                          (full-page-header.html + source + postamble.jsx + full-page-footer.html)
  - astralia-rpg.html  — fragment (no doctype/html/head/body), for the
                          claude.ai Artifact tool, which wraps it itself
                          (preamble.html + source + postamble.jsx + closing.html)

Run this from the artifact/ directory: `python3 build.py`
"""
import re
import pathlib

ARTIFACT_DIR = pathlib.Path(__file__).parent
# The source lives next to this script when checked out from the GitHub
# repo's source/ folder, or one directory up in the original dev sandbox
# layout (artifact/ subfolder next to the .jsx). Support both so this
# script works unmodified in either layout.
_candidates = [ARTIFACT_DIR / "margonem-mini-rpg.jsx", ARTIFACT_DIR.parent / "margonem-mini-rpg.jsx"]
SOURCE = next((p for p in _candidates if p.exists()), _candidates[0])


def strip_es_module_syntax(src: str) -> str:
    # Remove single-line `import ...;` statements from the top of the file.
    src = re.sub(r"^import [^\n]*?;\n", "", src, flags=re.MULTILINE)
    # Remove the multi-line `import { ... } from '...';` block (lucide-react icons).
    src = re.sub(r"^import \{[^}]*\} from '[^']*';\n", "", src, flags=re.DOTALL | re.MULTILINE)
    # Strip the ES module export keyword (browser build calls AstraliaRPG directly).
    src = src.replace("export default function AstraliaRPG()", "function AstraliaRPG()")
    assert "import " not in src.split("\n\n")[0], "import lines may remain at top"
    assert "export default" not in src, "export default still present"
    return src


def read(name: str) -> str:
    return (ARTIFACT_DIR / name).read_text(encoding="utf-8")


def main():
    game_src = strip_es_module_syntax(SOURCE.read_text(encoding="utf-8"))
    postamble = read("postamble.jsx")

    index_html = read("full-page-header.html") + game_src + postamble + read("full-page-footer.html")
    (ARTIFACT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    artifact_html = read("preamble.html") + game_src + postamble + read("closing.html")
    (ARTIFACT_DIR / "astralia-rpg.html").write_text(artifact_html, encoding="utf-8")

    print(f"Wrote index.html ({len(index_html)} bytes) and astralia-rpg.html ({len(artifact_html)} bytes)")


if __name__ == "__main__":
    main()
