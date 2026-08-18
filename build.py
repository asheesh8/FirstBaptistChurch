#!/usr/bin/env python3
"""
Build the two deliverables from source templates plus assets.

Both outputs are single self-contained HTML files: fonts and photographs are
inlined as base64 data URIs, because the pages are published as Artifacts and a
strict CSP there blocks every external host (font CDNs and image hosts alike).

    python3 build.py

Writes index.html (the seven-page site) and brand.html (the identity board).
"""

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
FONTS = ROOT / "assets" / "fonts"

# placeholder in the template -> file supplying its bytes
SITE = {
    "__FIGTREE__":   FONTS / "figtree.woff2",
    "__FRAUNCES__":  FONTS / "fraunces.woff2",
    "__S_SPRING__":  ROOT / "assets/site/s-spring.jpg",
    "__S_SUMMER__":  ROOT / "assets/site/s-summer.jpg",
    "__S_AUTUMN__":  ROOT / "assets/site/s-autumn.jpg",
    "__S_WINTER__":  ROOT / "assets/site/s-winter.jpg",
    "__SANCTUARY__": ROOT / "assets/site/sanctuary.jpg",
    "__ORGAN__":     ROOT / "assets/site/organ.jpg",
    "__POTLUCK__":   ROOT / "assets/site/potluck.jpg",
    "__CHOIR__":     ROOT / "assets/site/choir.jpg",
    "__CHRISTMAS__": ROOT / "assets/site/christmas.jpg",
    "__PICNIC__":    ROOT / "assets/site/picnic.jpg",
    "__PASTOR__":    ROOT / "assets/site/pastor.jpg",
}

BRAND = {
    "__FIGTREE__":       FONTS / "figtree.woff2",
    "__FRAUNCES__":      FONTS / "fraunces.woff2",
    "__IMG_WINTER__":    ROOT / "assets/brand/winter.jpg",
    "__IMG_SANCTUARY__": ROOT / "assets/brand/sanctuary.jpg",
    "__IMG_ORGAN__":     ROOT / "assets/brand/organ.jpg",
    "__IMG_POTLUCK__":   ROOT / "assets/brand/potluck.jpg",
    "__IMG_CHRISTMAS__": ROOT / "assets/brand/christmas.jpg",
    "__IMG_SUMMER__":    ROOT / "assets/brand/summer.jpg",
}

# CSS custom properties are not reliable inside SVG *presentation* attributes,
# so fill="var(--x)" is rewritten to style="fill:var(--x)", which is.
SVG_VAR = re.compile(r'(fill|stroke)="var\((--[a-z0-9-]+)\)"')


def b64(path):
    if not path.exists():
        sys.exit("missing asset: %s" % path)
    return base64.b64encode(path.read_bytes()).decode()


def build(template, mapping, out):
    html = template.read_text(encoding="utf-8")
    html = SVG_VAR.sub(r'style="\1:var(\2)"', html)
    for token, path in mapping.items():
        html = html.replace(token, b64(path))

    left = re.findall(r"__[A-Z_]+__", html)
    if left:
        sys.exit("unreplaced placeholders in %s: %s" % (template.name, sorted(set(left))))

    # The Artifact host generates <head>, so the page cannot declare a charset.
    # Anything non-ASCII must already be an entity or a \u escape.
    non_ascii = sorted({c for c in html if ord(c) > 127})
    if non_ascii:
        sys.exit("non-ASCII in %s: %r" % (template.name, non_ascii))

    out.write_text(html, encoding="utf-8")
    print("%-12s %6.2f MB" % (out.name, out.stat().st_size / 1048576))


if __name__ == "__main__":
    build(ROOT / "src" / "site.html", SITE, ROOT / "index.html")
    build(ROOT / "src" / "brand.html", BRAND, ROOT / "brand.html")
