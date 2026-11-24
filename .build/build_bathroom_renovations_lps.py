#!/usr/bin/env python3
"""
build_bathroom_renovations_lps.py - generate the Bathroom Renovations x suburb landing
pages for NPD Building Solutions.

One page per suburb in SUBURBS: bathroom-renovations-<slug>.html (clean URL
/bathroom-renovations-<slug> on Cloudflare Pages). The filename carries BOTH the
coverage term "bathroom renovation" (a substring of "bathroom-renovations") and the
suburb slug as a contiguous token-run, which is what the WP HQ coverage detector
attributes on - same mechanism as build_carpentry_lps.py and build_decks_pergolas_lps.py.

Started 2026-11-24 (WP HQ suburb move) with the three towns that already send
bathroom searches to the site: Bairnsdale (the home base, "bathroom renovators in
bairnsdale" landing on the hub at ~#26), Sale ("bathroom renovations sale" at #1.5-4.5
through the Sale location page, with clicks) and Paynesville (bathroom-carpentry
searches landing on the Paynesville page). WP HQ staggers changes at three new pages
per move, so the other seven target towns are a later window: add them to SUBURBS.

Chrome (head assets, nav, footer, scripts, SVGs, JSON-LD business node) is IMPORTED from
build_carpentry_lps.py rather than re-transcribed, so there is exactly one copy of the
site chrome to maintain and every Tailwind class is already in the compiled styles.css
(the site purges any utility class it cannot see, so we never invent classes). The only
change to the imported head is the hero preload, swapped to this page's own hero.

Duplication gate (scripts/wphq-validate-site.py): a prose sentence (14+ words) found on
4+ pages counts as a component; one on 2-3 pages counts as copy. With three pages, any
NEW sentence shared between them is copy, so the shared parts are either carried
verbatim from sentences already on the site (the why bullets, the CTA line, the trade
coordination FAQ from bathroom-renovations-quote.html) or kept under 14 words (the
cards). Everything local is written fresh per town.

Facts only from the client's own site and CRM: 16 bathrooms in 14 months with Cutting
Edge Constructions, full strip-out / waterproofing / tiling / fit-out, trades
coordinated, 10+ years, Bairnsdale base, the published distances. No project is claimed
in any town, and the photos are captioned as NPD bathrooms, never as a named suburb
(the "Major Project" bathroom photos are the Queensland job and are not used here).
No prices and no turnaround promises (house design system). No em dashes anywhere.

Run:  python3 .build/build_bathroom_renovations_lps.py    (writes into the site root)
Re-runnable: overwrites the generated bathroom-renovations-<suburb>.html files in place;
hand pages (bathroom-renovations.html, bathroom-renovations-quote.html) are untouched.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# Shared chrome, verbatim from the 100-clean pages. Imported, not re-transcribed.
from build_carpentry_lps import (  # noqa: E402
    BUSINESS_ID, CHECK_SVG, DOC_SVG, DOMAIN, FOOTER_HTML, HEAD_ASSETS, NAV_HTML,
    PHONE_SVG, PIN_SVG, PLUS_SVG, business_node, esc,
)

# Real bathroom photography from the client's own gallery (already on bathroom-renovations.html).
HERO_IMG_URL = "Assets/optimized/Bathroom%20Renovation%20-%20Spa%20Bath%20and%20Tiling"
HERO_IMG_SRC = "Assets/Bathroom Renovation - Spa Bath and Tiling.jpg"
HERO_IMG_W, HERO_IMG_H = 1200, 1600
WHY_IMG_URL = "Assets/optimized/Bathroom%20Renovation%20-%20Modern%20Shower%20and%20Vanity"
WHY_IMG_SRC = "Assets/Bathroom Renovation - Modern Shower and Vanity.jpg"
WHY_IMG_W, WHY_IMG_H = 1200, 1600

# The carpentry head preloads the carpentry hero. Swap it for this page's hero, using the
# exact tag bathroom-renovations.html already ships, and refuse to run if the carpentry
# preload ever changes shape (a silent miss would preload the wrong image on every page).
_CARPENTRY_PRELOAD = HEAD_ASSETS.split("\n", 1)[0]
assert _CARPENTRY_PRELOAD.lstrip().startswith('<link rel="preload" as="image"'), _CARPENTRY_PRELOAD
BATH_PRELOAD = (
    f'  <link rel="preload" as="image" imagesrcset="{HERO_IMG_URL}-400.webp 400w, '
    f'{HERO_IMG_URL}-800.webp 800w" imagesizes="(max-width: 640px) 100vw, 800px" '
    f'type="image/webp" fetchpriority="high">'
)
BATH_HEAD_ASSETS = BATH_PRELOAD + "\n" + HEAD_ASSETS.split("\n", 1)[1]

# ---------------------------------------------------------------------------
# Per-suburb data. `intro` is a list of paragraphs (bathrooms + real local
# character). `why_local` is the localised bullet. `faq_local` are three localised
# Q&A (the shared one is appended by faq_items()). `nearby` cross-links the
# bathroom cluster; `also` links the same town's other NPD pages.
# ---------------------------------------------------------------------------
SUBURBS = [
    {
        "name": "Bairnsdale", "slug": "bairnsdale",
        "lead": "Full bathroom renovations for Bairnsdale homes, from strip-out to the last tile. We are based here, so a Bairnsdale quote carries nothing for travel.",
        "intro": [
            "Bairnsdale is home, and bathrooms are a big part of the work we do here. The older weatherboard and brick homes around the centre often still have their original bathroom, or a refresh from decades ago: a shower over the bath, small tiles, a vanity that has swollen around the basin. On the newer estates the job is usually narrower, a tired ensuite or a main bathroom the family has outgrown.",
            "A bathroom is the most trade-heavy room in a house. A full renovation strips the room back to the frame, then runs through plumbing, waterproofing, sheeting, tiling and fit-out in the right order, and a delay in one trade holds up everything behind it. We run that sequence ourselves and coordinate the plumber and electrician, so you are not ringing around town trying to line people up.",
            "That process is how we got through 16 bathrooms in 14 months alongside Cutting Edge Constructions, and it is the same process on one bathroom in a Bairnsdale family home. Older houses can hide water damage under the old tiles, and because we are carpenters first we repair the floor and wall framing properly before the new room goes on top of it. You get one fixed price after a site visit, and one person to call from the first look to the final clean.",
        ],
        "why_local": ("Bairnsdale-based.", "Our home town, so a Bairnsdale bathroom quote carries nothing for getting here and back."),
        "faq_local": [
            ("Do you renovate bathrooms in Bairnsdale itself?",
             "Yes. Bairnsdale has been our home base for 10+ years, and bathroom renovations are a standout part of our work. A job in town has no travel loaded into the price, and coming out to measure up is a short drive across Bairnsdale."),
            ("What if you find rot or water damage under the old bathroom?",
             "It is common in older Bairnsdale homes, usually under a leaking shower base or around the toilet. Because we are carpenters as well as renovators, we repair or replace the damaged floor and wall framing ourselves before any waterproofing goes down. If we find it, we show you and talk through the fix before the job goes any further."),
            ("Can you replace an old bath and shower with a walk-in shower?",
             "Yes. Taking out an old bath frees up floor space, and a properly waterproofed, fully tiled shower is easier to step into and easier to keep clean. Whether the step can be low or flush depends on the floor and the drainage, which we check on site before we quote."),
        ],
        "nearby": [("Paynesville", "paynesville"), ("Sale", "sale")],
        "also": [("Carpentry in Bairnsdale", "/carpentry-bairnsdale"), ("Decks & Pergolas in Bairnsdale", "/decks-pergolas-bairnsdale")],
    },
    {
        "name": "Sale", "slug": "sale",
        "lead": "Bathroom renovations for Sale and the Wellington Shire, from full strip-outs to the last tile. A Bairnsdale builder who works in Sale regularly, with the travel already in the quote.",
        "intro": [
            "Plenty of Sale homes still have the bathroom they were built with. The period houses near the centre and the brick homes from the 60s, 70s and 80s that make up much of the town each came with a bathroom of their decade, and a lot of those rooms are still in use: a bath under the shower, grout that will not come clean, a window that fogs and drips every winter morning. Those are full renovations, and they are the jobs we are most often asked to quote in Sale.",
            "Our yard is about an hour east in Bairnsdale, and that changes how a Sale bathroom has to be run. A full renovation is several trades in a fixed order, and nobody wants a crew driving an hour only to find the waterproofing has not cured or the tiles have not arrived. So the job is sequenced before it starts, with materials on site and the plumber and electrician booked to the plan, which keeps every day on site productive.",
            "The price you are quoted for a Sale bathroom already includes getting here and back. It is worked out after a site visit, once we have seen the room, the floor under it and what the plumbing allows, and it covers the whole job from strip-out to the final clean.",
        ],
        "why_local": ("A regular run west.", "We work in Sale often, and the cost of getting there is in the quote rather than added afterwards."),
        "faq_local": [
            ("Do you do bathroom renovations in Sale?",
             "Yes. We are based in Bairnsdale, about an hour east along the Princes Highway, and we work in Sale and the Wellington Shire regularly. The travel is built into the quoted price, so it never turns up as an extra on the invoice."),
            ("My bathroom has not been touched since the house was built. Is a full renovation worth it?",
             "Usually, yes. In a room that old the waterproofing, if there is any, is well past its life, and new tiles laid over it tend to fail the same way the old ones did. A full strip-out lets us see the frame and the floor, fix what needs fixing and waterproof the room properly before anything new goes down. If a smaller job would genuinely do, we will tell you after the site visit."),
            ("Do you work in Maffra and Longford as well?",
             "Yes. Maffra, Longford, Stratford and the towns around Sale are all part of the same run for us. If you are not sure whether we cover your area, give us a call and ask."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Paynesville", "paynesville")],
        "also": [("Carpentry in Sale", "/carpentry-sale"), ("Decks & Pergolas in Sale", "/decks-pergolas-sale"), ("Everything We Do in Sale", "/sale")],
    },
    {
        "name": "Paynesville", "slug": "paynesville",
        "lead": "Bathroom renovations for Paynesville homes and holiday weekenders, from full strip-outs to the last tile. About 25 minutes from our Bairnsdale base, with every trade coordinated for you.",
        "intro": [
            "Paynesville bathrooms tend to be one of two jobs. Permanent homes, many of them owned by people who have retired to the Lakes, want a bathroom that will suit them for the next twenty years: a shower that is easy to step into, good light, and surfaces that wipe clean. Holiday homes and rentals want finishes that stand up to a steady turnover of guests and still look fresh in the listing.",
            "Living by the water is hard on a bathroom. A house near the canals sits in damp air for much of the year, and a room that is not waterproofed and ventilated properly shows it: mould in the grout, swollen cabinetry, paint lifting off the ceiling. We waterproof every wet area before a tile goes down, choose a vanity and fittings that cope with the humidity, and make sure the room can actually get rid of its steam.",
            "For owners who are not in town while the work happens, a holiday-home bathroom runs on regular updates rather than site meetings. Our base is about 25 minutes up the road in Bairnsdale, so checking on the job between trades is easy, and the room is handed back finished and clean, ready for the next guests rather than the next tradesman.",
        ],
        "why_local": ("Holiday homes are normal work.", "We plan around your bookings and keep you updated while the job runs, whether you are in Paynesville or not."),
        "faq_local": [
            ("Can you fit a bathroom renovation between holiday bookings?",
             "Usually, if we know the dates early. A full bathroom renovation needs an uninterrupted run on site, so we work out the sequence with you before we start and book the trades to that window. If the gap between bookings is too short for the job, we will tell you when we quote rather than leave the room half finished."),
            ("How do you stop mould coming back in a bathroom near the water?",
             "It comes down to three things: proper waterproofing under the tiles, an exhaust fan sized for the room that takes the steam out of the house, and finishes that do not hold moisture. A bathroom missing any one of those will grow mould again however often it is cleaned, so all three are covered in the quote."),
            ("How far is Paynesville from your base?",
             "About 20 kilometres from our yard in Bairnsdale, roughly a 25 minute drive. Paynesville is one of the towns we work in most often, so there is very little travel in a Paynesville bathroom quote."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Sale", "sale")],
        "also": [("Carpentry in Paynesville", "/carpentry-paynesville"), ("Decks & Pergolas in Paynesville", "/decks-pergolas-paynesville"), ("Everything We Do in Paynesville", "/paynesville")],
    },
]

# One shared FAQ, appended after the localised ones. Carried VERBATIM from
# bathroom-renovations-quote.html so it reads as a component, not copy, to the gate.
SHARED_FAQ = [
    ("Do you coordinate the plumber and electrician?",
     "Yes. We manage every trade involved so you don't have to chase anyone yourself. Plumbing, electrical, waterproofing, tiling and fit-out are all coordinated by one builder."),
]

# Shared "what's included" cards. Bodies stay under 14 words (the gate's prose floor),
# so three pages sharing them is a component. (title, body, href-or-None)
COVER_CARDS = [
    ("Full Strip-Out", "Old tiles, fittings and linings removed, right back to the frame.", None),
    ("Frame & Floor Repairs", "Rotted or water-damaged framing fixed properly before anything new goes in.", "/general-carpentry"),
    ("Waterproofing", "Every wet area waterproofed before a single tile goes down.", None),
    ("Tiling", "Floors and walls tiled with clean lines and even grout joints.", "/tiling"),
    ("Plumbing & Electrical", "Plumber and electrician booked and coordinated by us, not chased by you.", None),
    ("Vanity, Fixtures & Fit-Out", "Vanity, shower screen, tapware and accessories fitted and checked before hand-over.", None),
]

# Shared why-choose bullets (appended after the localised one). (strong, text)
# Carried verbatim from the published carpentry and decks pages.
SHARED_WHY = [
    ("16 bathrooms in 14 months", "with Cutting Edge Constructions, proof of consistent volume and consistent quality."),
    ("10+ years in East Gippsland.", "We are local, we know the homes and the climate, and we have the track record to back it."),
    ("One point of contact.", "You deal with one builder from the first look to the final clean-up, with a fixed price agreed upfront."),
]


def fit_title(name):
    for t in (
        f"Bathroom Renovations {name} VIC | NPD Building Solutions",
        f"Bathroom Renovations {name} | NPD Building Solutions",
        f"Bathroom Renovations in {name} | NPD Building",
    ):
        if 50 <= len(t) <= 60:
            return t
    return f"Bathroom Renovations {name} | NPD Building Solutions"


def meta_desc(name):
    for d in (
        f"Bathroom renovations in {name}, VIC. Full strip-outs, waterproofing, tiling and "
        f"fit-out, with the plumber and electrician coordinated by your local Bairnsdale builder.",
        f"Bathroom renovations in {name}, VIC. Strip-outs, waterproofing, tiling and fit-out, "
        f"with every trade coordinated by your local Bairnsdale builder. Free quotes.",
        f"Bathroom renovations in {name}, VIC. Full strip-outs, waterproofing, tiling and "
        f"fit-out, with every trade coordinated by your local Bairnsdale builder.",
    ):
        if 150 <= len(d) <= 165:
            return d
    return (f"Bathroom renovations in {name}, VIC. Full strip-outs, waterproofing, tiling and "
            f"fit-out, with every trade coordinated by your local Bairnsdale builder.")


def faq_items(s):
    return list(s["faq_local"]) + list(SHARED_FAQ)


def head_jsonld(s):
    url = f"{DOMAIN}/bathroom-renovations-{s['slug']}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            business_node(),
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "Bathroom Renovations", "item": f"{DOMAIN}/bathroom-renovations"},
                    {"@type": "ListItem", "position": 3, "name": f"{s['name']} VIC", "item": url},
                ],
            },
            {
                "@type": "Service",
                "name": f"Bathroom Renovations in {s['name']}",
                "description": f"Full bathroom renovations in {s['name']}, East Gippsland: strip-out, frame and floor repairs, waterproofing, tiling, plumbing and electrical coordination, and fit-out.",
                "provider": {"@id": BUSINESS_ID},
                "areaServed": [{"@type": "Place", "name": s["name"]}, {"@type": "Place", "name": "East Gippsland"}],
                "url": url,
            },
        ],
    }
    return json.dumps(graph, indent=2, ensure_ascii=False)


def faq_jsonld(s):
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_items(s)
        ],
    }
    return json.dumps(faq, indent=2, ensure_ascii=False)


def render_cover_cards():
    out = []
    for title, body, href in COVER_CARDS:
        if href:
            out.append(f'''        <a href="{href}" class="group block bg-white p-8 shadow-elevated hover:shadow-floating transition-shadow duration-300">
          <h3 class="text-xl font-display text-gray-900 mb-3 group-hover:text-brand transition-colors duration-200" style="letter-spacing: -0.02em;">{esc(title)}</h3>
          <p class="text-sm text-gray-600" style="line-height: 1.7;">{esc(body)}</p>
        </a>''')
        else:
            out.append(f'''        <div class="bg-white p-8 shadow-elevated hover:shadow-floating transition-shadow duration-300">
          <h3 class="text-xl font-display text-gray-900 mb-3" style="letter-spacing: -0.02em;">{esc(title)}</h3>
          <p class="text-sm text-gray-600" style="line-height: 1.7;">{esc(body)}</p>
        </div>''')
    return "\n".join(out)


def render_why(s):
    out = []
    for strong, text in [s["why_local"]] + SHARED_WHY:
        out.append(f'''            <li class="flex items-start gap-3 text-base text-gray-700" style="line-height: 1.7;">
              {CHECK_SVG}
              <span><strong class="text-gray-900">{esc(strong)}</strong> {esc(text)}</span>
            </li>''')
    return "\n".join(out)


def render_faq_html(s):
    out = []
    for q, a in faq_items(s):
        out.append(f'''        <details class="group bg-white p-6 shadow-elevated cursor-pointer">
          <summary class="flex items-center justify-between list-none">
            <h3 class="text-lg font-display text-gray-900" style="letter-spacing: -0.02em;">{esc(q)}</h3>
            {PLUS_SVG}
          </summary>
          <p class="text-sm text-gray-600 mt-4" style="line-height: 1.7;">{esc(a)}</p>
        </details>''')
    return "\n".join(out)


PILL = "inline-block px-5 py-2.5 border border-gray-200 text-sm font-semibold text-gray-700 hover:border-brand hover:text-brand transition-colors duration-200"


def render_nearby(nearby):
    out = [f'''        <a href="/bathroom-renovations-{slug}" class="{PILL}">{esc(name)}</a>'''
           for name, slug in nearby]
    out.append(f'''        <a href="/bathroom-renovations" class="{PILL}">All of East Gippsland</a>''')
    return "\n".join(out)


def render_also(also):
    return "\n".join(f'''          <a href="{href}" class="{PILL}">{esc(label)}</a>''' for label, href in also)


def render_intro(paras):
    return "\n".join(f'        <p>{esc(p)}</p>' for p in paras)


def page_html(s):
    name = s["name"]
    ename = esc(name)
    slug = s["slug"]
    url = f"{DOMAIN}/bathroom-renovations-{slug}"
    title = fit_title(name)
    desc = meta_desc(name)
    keywords = (f"bathroom renovations {name}, bathroom renovation {name} VIC, bathroom renovator {name}, "
                f"ensuite renovation {name}, shower renovation {name}, bathroom tiling {name}, East Gippsland bathroom renovations")

    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="apple-touch-icon" href="Assets/Logo.jpg">
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">

  <meta property="og:title" content="Bathroom Renovations in {ename} VIC | NPD Building Solutions">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_AU">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="NPD Building Solutions">
  <meta property="og:image" content="{DOMAIN}/{HERO_IMG_URL}-800.webp">
  <meta property="og:image:width" content="800">
  <meta property="og:image:height" content="1067">
  <meta property="og:image:alt" content="Bathroom renovation with spa bath and tiling by NPD Building Solutions">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Bathroom Renovations in {ename} VIC | NPD Building Solutions">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/{HERO_IMG_URL}-800.webp">

  <!-- Geo -->
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="Bairnsdale">

  <script type="application/ld+json">
{head_jsonld(s)}
  </script>

  <script type="application/ld+json">
{faq_jsonld(s)}
  </script>

{BATH_HEAD_ASSETS}
</head>
{NAV_HTML}

  <!-- Page Hero -->
  <main id="main">

  <!-- Breadcrumb -->
  <nav aria-label="Breadcrumb" class="bg-black border-b border-gray-800 pt-20 sm:pt-24">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <ol class="flex flex-wrap items-center gap-2 text-xs sm:text-sm text-gray-400">
        <li><a href="/" class="hover:text-brand transition-colors">Home</a></li>
        <li class="text-gray-500" aria-hidden="true">/</li>
        <li><a href="/bathroom-renovations" class="hover:text-brand transition-colors">Bathroom Renovations</a></li>
        <li class="text-gray-500" aria-hidden="true">/</li>
        <li class="text-brand" aria-current="page">{ename} VIC</li>
      </ol>
    </div>
  </nav>

  <section class="relative pt-32 sm:pt-40 pb-16 sm:pb-20 bg-gray-900 overflow-hidden grain">
    <div class="absolute inset-0">
      <picture><source type="image/webp" srcset="{HERO_IMG_URL}-400.webp 400w, {HERO_IMG_URL}-800.webp 800w" sizes="(max-width: 640px) 100vw, 800px"><img src="{HERO_IMG_SRC}" alt="Bathroom renovation with spa bath and tiling by NPD Building Solutions" width="{HERO_IMG_W}" height="{HERO_IMG_H}" loading="eager" fetchpriority="high" decoding="sync" class="w-full h-full object-cover opacity-30"></picture>
      <div class="absolute inset-0 bg-gradient-to-b from-gray-900/80 via-gray-900/60 to-gray-900/90"></div>
      <div class="absolute inset-0 bg-brand/5 mix-blend-multiply"></div>
    </div>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="max-w-2xl">
        <p class="inline-flex items-center gap-2 text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">
          {PIN_SVG}
          Bathroom Renovations in {ename}, VIC
        </p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-display text-white leading-[0.95] mb-6" style="letter-spacing: -0.03em;">Bathroom Renovations in {ename}</h1>
        <p class="text-gray-300 text-base max-w-lg" style="line-height: 1.7;">{esc(s['lead'])}</p>
      </div>
    </div>
  </section>

  <!-- Local Intro -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Local Bathroom Renovator</p>
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Renovating a Bathroom in {ename}</h2>
      <div class="space-y-5 text-gray-600" style="line-height: 1.8;">
{render_intro(s['intro'])}
      </div>
    </div>
  </section>

  <!-- What's Included -->
  <section class="py-20 sm:py-28 bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">What a {ename} Renovation Includes</p>
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">A Full Bathroom, Start to Finish</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{render_cover_cards()}
      </div>
    </div>
  </section>

  <!-- Why Choose Us -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        <div>
          <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Why {ename} Chooses NPD</p>
          <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Bathrooms, Done Properly</h2>
          <ul class="space-y-4">
{render_why(s)}
          </ul>
        </div>
        <div class="relative">
          <div class="overflow-hidden shadow-floating">
            <div class="relative">
              <picture><source type="image/webp" srcset="{WHY_IMG_URL}-400.webp 400w, {WHY_IMG_URL}-800.webp 800w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 600px"><img src="{WHY_IMG_SRC}" alt="Bathroom renovation with modern shower and vanity by NPD Building Solutions" width="{WHY_IMG_W}" height="{WHY_IMG_H}" loading="lazy" decoding="async" class="w-full h-[350px] sm:h-[420px] object-cover"></picture>
              <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>
              <div class="absolute inset-0 bg-brand/10 mix-blend-multiply"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="py-20 sm:py-28 bg-gray-50">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Common Questions</p>
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">{ename} Bathroom Renovation FAQ</h2>
      </div>
      <div class="space-y-4">
{render_faq_html(s)}
      </div>
    </div>
  </section>

  <!-- Nearby Areas -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Other Areas We Service</p>
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-8" style="letter-spacing: -0.03em;">Bathroom Renovations Nearby</h2>
      <div class="flex flex-wrap justify-center gap-3">
{render_nearby(s['nearby'])}
      </div>
      <div class="mt-12 text-center">
        <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-6">More From NPD in {ename}</p>
        <div class="flex flex-wrap justify-center gap-3">
{render_also(s['also'])}
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 sm:py-28 relative overflow-hidden" style="background-color: #E8710A;" aria-label="Call to action">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      <h2 class="text-3xl sm:text-4xl lg:text-5xl font-display text-white mb-6" style="letter-spacing: -0.03em;">Planning a Bathroom Renovation in {ename}?</h2>
      <p class="text-lg text-white/90 mb-10 max-w-xl mx-auto" style="line-height: 1.7;">
        Call for a free quote. We will come out, look at the space, and give you a fair price upfront.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="tel:0427278285" class="btn-primary inline-flex items-center justify-center gap-2 sm:gap-3 bg-gray-900 hover:bg-gray-800 active:bg-gray-950 text-white font-bold text-base px-7 py-3.5 sm:text-lg sm:px-10 sm:py-5 transition-spring transition-transform duration-300 hover:scale-[1.03] active:scale-[0.98] shadow-floating">
          {PHONE_SVG}
          Call 0427 278 285
        </a>
        <a href="/contact" class="btn-secondary inline-flex items-center justify-center gap-2 sm:gap-3 bg-white hover:bg-gray-100 active:bg-gray-200 text-gray-900 font-semibold text-base px-7 py-3.5 sm:text-lg sm:px-10 sm:py-5 border border-white transition-spring transition-transform duration-300 hover:scale-[1.03] active:scale-[0.98]">
          {DOC_SVG}
          Request a Quote
        </a>
      </div>
    </div>
  </section>

{FOOTER_HTML}
'''


def main():
    written, warns = [], []
    for s in SUBURBS:
        path = os.path.join(ROOT, f"bathroom-renovations-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page_html(s))
        written.append(os.path.basename(path))
        t, d = fit_title(s["name"]), meta_desc(s["name"])
        if not (50 <= len(t) <= 60):
            warns.append(f"  TITLE {s['slug']}: {len(t)} chars -> {t}")
        if not (150 <= len(d) <= 165):
            warns.append(f"  META  {s['slug']}: {len(d)} chars")
    print(f"Wrote {len(written)} bathroom renovation suburb LPs:")
    for w in written:
        print("  " + w)
    if warns:
        print("\nLength warnings (want title 50-60, meta 150-165):")
        print("\n".join(warns))
    else:
        print("\nAll titles 50-60 and metas 150-165 chars.")


if __name__ == "__main__":
    main()
