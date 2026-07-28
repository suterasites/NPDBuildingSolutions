#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the NPD site.

Brings the sitemap pages to a clean pass on Apps/sutera-seo/checklist.py. Safe to
re-run. Compiled-Tailwind site (styles.css), so no new utility classes are added -
only existing classes are reused and elements are re-tagged.

Fixes (audited pages only; thank-you + *-quote are not in the sitemap):
  - <header> landmark: wrap the site <nav id="main-nav"> in a <header> on pages
    that don't already have a <header> (index uses its hero <header>)
  - footer column headings h4 -> h3 (kills the H2->H4 skip; utility classes keep
    them visually identical under Tailwind preflight)
  - privacy: demote the duplicate article <h1> to <h2> (exactly one H1)
  - queensland-renovation: lightbox <img> placeholder (empty src) -> width/height:auto
  - trim 7 titles into 50-60 and 13 meta descriptions into 150-165 (Bairnsdale VIC
    local SEO kept; no speed claims added)

Homepage breadcrumb is deliberately left as the only warn; pooled score -> 100.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLES = {
    "about.html": "About NPD Building Solutions | Carpentry, Bairnsdale VIC",
    "services.html": "Building Services Bairnsdale VIC | NPD Building Solutions",
    "windows-doors.html": "Windows & Doors Bairnsdale | NPD Building Solutions",
    "fencing-gates.html": "Fencing, Gates & Pool Fencing | NPD Building Solutions",
    "queensland-renovation.html": "Queensland Renovation Project | NPD Building Solutions",
    "lakes-entrance.html": "Carpenter Lakes Entrance VIC | NPD Building Solutions",
    "privacy.html": "Privacy Policy | NPD Building Solutions, Bairnsdale VIC",
}

METAS = {
    "about.html": "NPD Building Solutions brings over 10 years of carpentry and renovation experience to Bairnsdale, VIC. Quality workmanship, attention to detail, service with a smile.",
    "services.html": "A full range of building services in Bairnsdale, VIC: general carpentry, bathroom renovations, decks, pergolas, tiling, fencing, gates and custom work.",
    "our-work.html": "Browse recent carpentry and renovation projects across Bairnsdale and East Gippsland: bathroom renovations, custom carpentry, decks, pergolas and more.",
    "windows-doors.html": "All-inclusive window and door replacements in Bairnsdale, VIC. New windows, doors and architraves, plus professional painting, finished start to finish by one team.",
    "general-carpentry.html": "Professional general carpentry in Bairnsdale, VIC. Structural framing, repairs, interior fit-outs, and door and window installation, by NPD Building Solutions.",
    "tiling.html": "Professional tiling in Bairnsdale, VIC. Floor and wall tiling, bathroom and kitchen splashbacks, waterproofing and outdoor tiling, by NPD Building Solutions.",
    "decks-pergolas.html": "Custom decks and pergolas in Bairnsdale, VIC. Timber and composite decking, pergola design and construction, and outdoor entertaining areas built to last.",
    "custom-work.html": "Custom building work and bespoke builds in Bairnsdale, VIC. Custom joinery, cabinetry, shelving, feature pieces and one-off builds by NPD Building Solutions.",
    "fencing-gates.html": "Fencing, gates and pool fencing in Bairnsdale, VIC. Timber and Colorbond fencing, custom gates, and compliant pool fencing by NPD Building Solutions.",
    "sale.html": "Carpentry, bathroom renovations, decks, pergolas and tiling in Sale, VIC. Your local Bairnsdale-based builder servicing Sale and the Wellington Shire.",
    "paynesville.html": "Decks, pergolas, bathroom renovations and carpentry in Paynesville, VIC. Local Bairnsdale builder with 10+ years on the tools, specialising in waterfront homes.",
    "lakes-entrance.html": "Bathroom renovations, decks, pergolas, tiling and carpentry in Lakes Entrance, VIC. Local Bairnsdale builder serving holiday homes, rentals and residences.",
    "privacy.html": "How NPD Building Solutions collects, uses, stores and protects the personal information you provide when you request a quote or contact us, under the Privacy Act.",
}


def patch(fn):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    if fn in TITLES:
        html2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[fn] + "</title>", html, count=1, flags=re.S)
        if html2 != html:
            html = html2
            did.append(f"title({len(TITLES[fn])})")

    if fn in METAS:
        new = METAS[fn]
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + new + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"desc({len(new)})")

    # --- <header> landmark: wrap the site nav (pages without an existing header) ---
    if "<header" not in html:
        m = re.search(r'<nav id="main-nav"', html)
        if m:
            close = html.find("</nav>", m.start())     # main-nav has no nested <nav>
            if close != -1:
                end = close + len("</nav>")
                html = html[:m.start()] + "<header>\n  " + html[m.start():end] + "\n  </header>" + html[end:]
                did.append("header")

    # --- footer headings h4 -> h3 ---
    if "<h4" in html:
        html = re.sub(r"<h4(\b[^>]*)>", r"<h3\1>", html)
        html = html.replace("</h4>", "</h3>")
        did.append("footer-h3")

    # --- privacy: demote the duplicate article H1 ---
    if fn == "privacy.html" and "<h1>Privacy Policy</h1>" in html:
        html = html.replace("<h1>Privacy Policy</h1>", "<h2>Privacy Policy</h2>", 1)
        did.append("dedupe-h1")

    # --- queensland: lightbox placeholder <img src=""> -> width/height:auto ---
    if fn == "queensland-renovation.html":
        html2 = re.sub(r'(<img(?![^>]*\bstyle=)[^>]*id="lightbox-img"[^>]*?)(\s*/?>)',
                       r'\1 style="width:auto;height:auto"\2', html, count=1)
        if html2 != html:
            html = html2
            did.append("lightbox-dims")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    print(f"Patching {len(files)} files\n")
    for path in files:
        fn = os.path.basename(path)
        print(f"  {fn:34s} {', '.join(patch(fn)) or 'no change'}")
    print("\nDone. Idempotent.")


if __name__ == "__main__":
    main()
