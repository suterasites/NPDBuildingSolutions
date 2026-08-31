#!/usr/bin/env python3
"""
build_decks_pergolas_lps.py - generate the Decks & Pergolas x suburb landing pages
for NPD Building Solutions.

One page per target suburb: decks-pergolas-<slug>.html (clean URL /decks-pergolas-<slug>
on Cloudflare Pages). The filename carries BOTH the coverage term "pergola" (a substring
of "pergolas") and the suburb slug as a contiguous token-run, which is what the WP HQ
coverage detector attributes on - same mechanism as build_carpentry_lps.py.

Chrome (head assets, nav, footer, scripts, SVGs, JSON-LD business node) is IMPORTED from
build_carpentry_lps.py rather than re-transcribed, so there is exactly one copy of the
site chrome to maintain and every Tailwind class is already in the compiled styles.css
(the site purges any utility class it cannot see, so we never invent classes).

Copy is genuinely localised: how people actually use outdoor space in each town, the
decking and pergola decisions that setting forces (salt air, lake frontage, exposed
rural blocks, heritage streetscapes), and the real distance from the Bairnsdale base.
Distances and local character are kept CONSISTENT with the already-published carpentry
pages. No specific project is claimed in a suburb except the two that are documented on
the client's own site: the Paynesville second-floor deck and carport built alongside
Cutting Edge Constructions, and a covered composite deck in the Bairnsdale region.
No em dashes anywhere (site + repo hard rule).

Run:  python3 .build/build_decks_pergolas_lps.py    (writes into the site root, one dir up)
Re-runnable: overwrites the generated decks-pergolas-*.html files in place; hand pages
(including the decks-pergolas.html service hub) are untouched.
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

# Real deck photography from the client's own gallery (already on decks-pergolas.html).
HERO_IMG_URL = "Assets/optimized/Composite%20Deck%20and%20Verandah"
HERO_IMG_SRC = "Assets/Composite Deck and Verandah.jpg"
HERO_IMG_W, HERO_IMG_H = 1600, 1200
WHY_IMG_URL = "Assets/optimized/Waterfront%20Composite%20Deck%20with%20Glass%20Balustrade%20-%20Paynesville"
WHY_IMG_SRC = "Assets/Waterfront Composite Deck with Glass Balustrade - Paynesville.jpg"
WHY_IMG_W, WHY_IMG_H = 2142, 2856

# ---------------------------------------------------------------------------
# Per-suburb data. `intro` is a list of paragraphs (decks/pergolas + real local
# character). `why_local` is the localised bullet. `faq_local` are two localised
# Q&A (the two shared Q&A are appended by faq_items()). `nearby` cross-links the
# decks cluster.
# ---------------------------------------------------------------------------
SUBURBS = [
    {
        "name": "Bairnsdale", "slug": "bairnsdale",
        "lead": "Custom decks and pergolas for Bairnsdale homes, in timber or composite. This is our home base, so there is no travel in the quote and we can look at the job quickly.",
        "intro": [
            "Bairnsdale is where we are based and where most of our decking work happens. The town runs from character weatherboards near the centre out to newer brick estates on the edges, and the outdoor space each one wants is different. Older homes usually need a verandah rebuilt or a deck replaced where the original timber has finally gone, matched to the height and proportions of the existing house. Newer builds tend to want an alfresco area off the living room, often with a pergola over it so the space is usable through summer.",
            "Because we live here there is no travel loaded into a Bairnsdale quote, and we can usually get out to look at the job within a few days. One of the covered composite decks in our gallery was built right here in the Bairnsdale region: low-maintenance two-tone boards, clean steel posts and a roof that makes it a year-round room rather than a fair-weather one.",
            "We build in both timber and composite, and we will tell you honestly which one suits your budget, your aspect and how much maintenance you actually want to do. Either way you deal with one local builder from the first look to the final clean-up, with a fixed price agreed upfront.",
        ],
        "why_local": ("Bairnsdale-based.", "This is our home town, so there is no travel cost in a local quote and we can get to site fast."),
        "faq_local": [
            ("Have you built decks in Bairnsdale itself?",
             "Yes, regularly. Bairnsdale is our home base and has been for 10+ years. The covered composite deck in our gallery, with the two-tone boards and steel posts, was built in the Bairnsdale region."),
            ("Should I go timber or composite for a Bairnsdale deck?",
             "It depends on aspect and how much upkeep you want. Timber costs less upfront and can be stained to suit the house, but it needs re-oiling every year or two. Composite costs more to start and then essentially looks after itself. We will walk you through both against your actual budget rather than push one."),
        ],
        "nearby": [("Lucknow", "lucknow"), ("Nicholson", "nicholson"), ("Eagle Point", "eagle-point")],
    },
    {
        "name": "Lakes Entrance", "slug": "lakes-entrance",
        "lead": "Decks and pergolas for Lakes Entrance homes, rentals and holiday properties, built for salt air and sun. Coastal-aware decking from a local East Gippsland team.",
        "intro": [
            "Lakes Entrance splits into permanent homes, long-term rentals and short-stay holiday properties, and the deck is doing a different job in each. On a holiday property it is often the main selling point of the listing, the photo people book from, so it has to look sharp and stay that way through a full season of guests. On a permanent home it is where summer is spent. A lot of the housing stock dates from the 80s and 90s, which means plenty of original decks are now well past their service life and due for replacement rather than another coat of stain.",
            "The salt air and sun down this coast are hard on external timber, harder than anywhere inland, and it shows up first in the fixings and the substructure rather than the boards you can see. That is the argument for composite here more than most places: it does not split, cup or need re-oiling every summer. Where we do build in timber we use corrosion-resistant fixings and detail the frame so water drains rather than sits.",
            "We have spent 10+ years across East Gippsland and Lakes Entrance is a regular route for us, about 35 kilometres east along the Princes Highway. For rental owners we can sequence a deck build around booking windows so you lose as few nights as possible, and we keep the site tidy between stages.",
        ],
        "why_local": ("Coastal-aware decking.", "Correct boards, corrosion-resistant fixings and frame detailing that stand up to Lakes Entrance salt air and sun."),
        "faq_local": [
            ("Will a timber deck survive the salt air at Lakes Entrance?",
             "It will if it is built for it. The failures we get called to are almost always fixings and frame detailing rather than the boards themselves. We use corrosion-resistant fixings and detail the substructure so water drains away. If you want to stop thinking about it altogether, composite is the better answer on this coast."),
            ("Can you build around holiday rental bookings?",
             "Yes. We schedule deck and pergola work on short-stay properties around your booking calendar so you lose as few nights as possible, and we leave the site safe and tidy between stages."),
        ],
        "nearby": [("Metung", "metung"), ("Nicholson", "nicholson"), ("Paynesville", "paynesville")],
    },
    {
        "name": "Paynesville", "slug": "paynesville",
        "lead": "Decks and pergolas for Paynesville's waterfront and canal-estate homes, built for a damp, exposed setting. We have built here, including a second-floor deck and carport.",
        "intro": [
            "Paynesville is built around the water, with canal-front homes, jetties and a strong boating culture, and the deck is usually the whole point of the house. Canal-estate homes want the living space pushed out towards the water with a balustrade that does not block the view, which is why glass balustrade comes up so often here. Older cottages in the town centre are a different job: a modest deck or a pergola over the back door, done well and in proportion.",
            "We have worked in Paynesville for years and two of the builds in our gallery are from here. One is a second-floor deck and carport built alongside Cutting Edge Constructions. The other is a waterfront composite deck with a glass balustrade, which is about as direct an example as you can get of what this setting asks for.",
            "Building near the water is unforgiving about materials. Damp, salt-laden air gets into fixings and end-grain, so board choice, fixing choice and how the frame sheds water matter more here than they do a few kilometres inland. We are based about 20 minutes north in Bairnsdale, so site visits are easy and 10+ years locally means we know what actually holds up.",
        ],
        "why_local": ("Built for the water.", "Boards and fixings chosen for Paynesville's canal-front, damp and exposed conditions, so the deck lasts."),
        "faq_local": [
            ("Have you built decks on Paynesville waterfront homes?",
             "Yes. Two builds in our gallery are from Paynesville: a second-floor deck and carport completed alongside Cutting Edge Constructions, and a waterfront composite deck with a glass balustrade. Both were detailed for a damp, exposed canal-front setting."),
            ("Can you fit a glass balustrade so it does not block the water view?",
             "Yes, and on a canal or waterfront block it is usually worth it. Glass keeps the outlook you paid for while still meeting the height and load requirements. We can price it alongside a standard balustrade so you can see the difference before deciding."),
        ],
        "nearby": [("Eagle Point", "eagle-point"), ("Bairnsdale", "bairnsdale"), ("Metung", "metung")],
    },
    {
        "name": "Sale", "slug": "sale",
        "lead": "Decks, pergolas and alfresco areas for Sale and the Wellington Shire, in timber or composite. A Bairnsdale-based builder that services Sale regularly.",
        "intro": [
            "Sale is the largest town in the Wellington Shire, a mix of established period homes, post-war brick and newer estates spreading out from the centre. That range shows up in the decking work. Period homes usually want a verandah restored or rebuilt in keeping with the front of the house. Post-war brick homes tend to want a proper entertaining deck off the back where there was only ever a concrete slab. Newer estate homes want the alfresco finished properly, often with a pergola or a roofed section so the barbecue area is usable in more than three months of the year.",
            "Sale sits inland, away from the salt, so timber is a genuinely competitive option here in a way it is not on the coast. It comes down to how much maintenance you want to take on. We will quote both and be straight with you about the difference over ten years rather than just the difference today.",
            "We are based in Bairnsdale, about 50 minutes east along the Princes Highway, and Sale is a town we service regularly rather than as a one-off. Travel is factored into the quote upfront, so there are no surprises on the invoice.",
        ],
        "why_local": ("We service Sale regularly.", "Sale is a standing part of our run, so travel is factored into the quote and a site visit is easy to book."),
        "faq_local": [
            ("Do you travel to Sale for deck and pergola work?",
             "Yes. Sale is about 65 kilometres west, roughly a 50 minute drive along the Princes Highway, and we service it regularly. Travel is factored into the quote upfront so there are no surprises."),
            ("Can you roof a pergola so the area is usable in winter?",
             "Yes. A flat-roof pergola with proper fall, or a pitched roof tied into the house, turns an alfresco area from a summer-only space into one you use most of the year. We will talk through the options against your budget and how the space actually gets used."),
        ],
        "nearby": [("Stratford", "stratford"), ("Bairnsdale", "bairnsdale"), ("Paynesville", "paynesville")],
    },
    {
        "name": "Stratford", "slug": "stratford",
        "lead": "Decks, verandahs and pergolas for Stratford's heritage and riverside homes, built in proportion with the house. Local East Gippsland builder, 10+ years on the tools.",
        "intro": [
            "Stratford is a historic town on the Avon River, known for its period streetscape and character homes. Outdoor timber here is often about restoration rather than a brand new entertaining deck: a front verandah that has dropped, posts and bearers that have rotted at the base, decking boards that need replacing in a profile that matches what is already there. Get the proportions or the detailing wrong on a period home and it reads as wrong from the street even if the carpentry is sound.",
            "There is newer housing on the edges of town too, and that work is more conventional: an alfresco deck off the living area, a pergola over it, built for the way the family uses the yard. Stratford sits inland on the river rather than the coast, so timber holds up well here provided the frame is detailed to drain and the boards get looked after.",
            "Stratford is on our Sale run, about 45 minutes west of our Bairnsdale base, and we service it regularly. Over 10+ years we have learned to work with older homes rather than against them, keeping the character intact while bringing the structure up to standard.",
        ],
        "why_local": ("Sympathetic to older homes.", "Stratford's heritage homes need matched profiles and correct proportions, and that is work we do regularly."),
        "faq_local": [
            ("Can you rebuild a verandah on a Stratford period home?",
             "Yes. That is a regular job here. We match the existing profiles, keep the proportions right for the front of the house and replace what has actually failed, usually posts and bearers at the base, rather than tearing off more than the job needs."),
            ("How far is Stratford from Bairnsdale?",
             "About 55 kilometres west, roughly a 40 to 45 minute drive, and it sits on our Sale run. We service it regularly, with travel factored into the quote."),
        ],
        "nearby": [("Sale", "sale"), ("Bairnsdale", "bairnsdale"), ("Lindenow", "lindenow")],
    },
    {
        "name": "Metung", "slug": "metung",
        "lead": "Decks and pergolas for Metung's waterfront and holiday homes, built for an exposed lakeside setting. Coastal-aware decking from a local East Gippsland team.",
        "intro": [
            "Metung is a small waterfront village on the Gippsland Lakes with a strong boating and holiday-home character. A lot of the housing is second homes and higher-end waterfront properties, and the brief here is usually a deck that frames the water: a clean balustrade that does not interrupt the outlook, boards that stay presentable without anyone being on site to maintain them, and a pergola or roofed section that makes the space usable when the wind comes off the lake.",
            "That last part matters more in Metung than people expect. An exposed lakeside deck with no shelter gets used far less than one with a roof over part of it, so we will often suggest covering a section rather than the whole thing. It keeps the open feel while giving you somewhere to sit when the weather turns.",
            "We are based in Bairnsdale, about 30 minutes west, and Metung is a regular part of our East Gippsland patch. Waterfront decking needs the right boards and corrosion-resistant fixings so it holds up to salt air and damp, and 10+ years locally means we know what works down this coast.",
        ],
        "why_local": ("Lakeside-ready.", "Boards and fixings chosen for Metung's exposed, waterfront conditions, so the deck lasts."),
        "faq_local": [
            ("What holds up best on an exposed Metung waterfront deck?",
             "Composite, in most cases. It does not split or cup, it does not need re-oiling, and on a second home that nobody is maintaining week to week that matters. If you prefer the look of timber we will build it in timber with corrosion-resistant fixings and a frame detailed to drain."),
            ("Should I roof the whole deck or part of it?",
             "Usually part of it. Covering a section gives you somewhere usable when the wind comes off the lake while keeping the open outlook over the rest. We will work out the split with you on site rather than guess it off a plan."),
        ],
        "nearby": [("Lakes Entrance", "lakes-entrance"), ("Paynesville", "paynesville"), ("Nicholson", "nicholson")],
    },
    {
        "name": "Nicholson", "slug": "nicholson",
        "lead": "Decks, pergolas and verandahs for Nicholson's semi-rural properties, including shed and outbuilding work. Only about 10 minutes east of our Bairnsdale base.",
        "intro": [
            "Nicholson is a small settlement on the river just east of Bairnsdale, mostly semi-rural blocks with room around the house. Outdoor timber on a block like that is usually practical as much as decorative: a wide verandah that shades the western wall, a deck that connects the house to the yard, a pergola or a lean-to roof over an outdoor working area rather than a formal entertaining space.",
            "Bigger blocks also mean sheds and outbuildings, and those often need the same trade: a verandah off a shed, a covered area between buildings, timber structures that have to stand up to sun and stock rather than look pretty in a photo. We take that work on as readily as a residential deck.",
            "Nicholson is only about 10 kilometres east of us, a 10 to 12 minute drive, so it is genuinely local and there is next to no travel loaded into a quote. Being close also means we can get out and look at a job quickly rather than booking you in for a fortnight away.",
        ],
        "why_local": ("Practically next door.", "Nicholson is about 10 minutes from our Bairnsdale base, so there is next to no travel in a quote."),
        "faq_local": [
            ("Do you build verandahs and covered areas on rural blocks around Nicholson?",
             "Yes. Semi-rural blocks often want a wide verandah for shade, a covered area between the house and a shed, or practical timber structures around outbuildings. We take on that work alongside conventional decks."),
            ("How far is Nicholson from Bairnsdale?",
             "Only about 10 kilometres, a 10 to 12 minute drive east. It is genuinely local for us, so there is next to no travel loaded into a quote."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Eagle Point", "eagle-point"), ("Lucknow", "lucknow")],
    },
    {
        "name": "Eagle Point", "slug": "eagle-point",
        "lead": "Decks and pergolas for Eagle Point homes overlooking Lake King, built to make the most of the outlook. Local Bairnsdale builder, about 15 minutes away.",
        "intro": [
            "Eagle Point sits above Lake King and the Mitchell River silt jetties, a quiet spot of waterfront and rural-residential homes on generous blocks. The outlook is the reason people live here, so the deck is rarely an afterthought. Most of the work is about getting the living space out towards the view, keeping the balustrade as unobtrusive as the rules allow, and building at a height that suits a block that often falls away towards the water.",
            "Sloping blocks are the technical part of the job here. A deck that steps down the fall, sits on properly footed posts and stays rigid at height is a different build from a slab-level deck, and it is worth getting the substructure right the first time. Being close to the water, boards and fixings also need choosing for damp and exposed conditions.",
            "We are based about 15 minutes north in Bairnsdale, so Eagle Point is genuinely local and a regular part of our run. You get one local builder across the job and a price agreed before we start.",
        ],
        "why_local": ("Local and close.", "Eagle Point is about 15 minutes from our Bairnsdale base, so travel is minimal and site visits are easy."),
        "faq_local": [
            ("Can you build a deck on a sloping Eagle Point block?",
             "Yes, and it is common here with the fall towards Lake King. An elevated deck needs properly footed posts and a substructure that stays rigid at height, so it is worth doing correctly from the start. We will work the levels out on site."),
            ("How far is Eagle Point from Bairnsdale?",
             "About 15 kilometres south-east, roughly a 15 to 18 minute drive. It is genuinely local for us, so site visits and quotes are easy to arrange."),
        ],
        "nearby": [("Paynesville", "paynesville"), ("Nicholson", "nicholson"), ("Bairnsdale", "bairnsdale")],
    },
    {
        "name": "Lucknow", "slug": "lucknow",
        "lead": "Decks, pergolas and alfresco areas for Lucknow homes, in timber or composite. Effectively on our doorstep, just east of our Bairnsdale base.",
        "intro": [
            "Lucknow sits on the eastern edge of Bairnsdale, close enough to be part of the town but with its own established residential character. The housing is a mix of older homes and newer builds, and the outdoor work splits along the same line. Older places often have a deck or verandah at the end of its life, where the boards are still passable but the frame underneath is not, and that is a rebuild rather than a resurface. Newer homes usually want the alfresco area finished properly, with a pergola over it so the space works beyond summer.",
            "For us Lucknow is about as local as it gets, only a few minutes from our Bairnsdale base. That means no travel to speak of in a quote and a quick turnaround on a site visit, which matters when you are trying to get a deck finished before Christmas rather than after it.",
            "We build in both timber and composite and will give you a straight comparison of the two for your particular spot, including what each will cost you in upkeep rather than just on the day.",
        ],
        "why_local": ("On our doorstep.", "Lucknow is only minutes from our Bairnsdale base, so there is no real travel in the quote and a fast site visit."),
        "faq_local": [
            ("Can you resurface my old deck instead of rebuilding it?",
             "Sometimes, and we will tell you honestly which one you are looking at. If the substructure is sound, new boards and a refinish is the cheaper job. If the frame has gone, new boards on a failing frame is money wasted. We check the frame before quoting either way."),
            ("Are you local to Lucknow?",
             "Very. Lucknow is on the eastern edge of Bairnsdale, just a few minutes from our base, so it is effectively home turf. There is no real travel to load into a quote."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Nicholson", "nicholson"), ("Eagle Point", "eagle-point")],
    },
    {
        "name": "Lindenow", "slug": "lindenow",
        "lead": "Verandahs, decks and pergolas for Lindenow's rural homes and properties, built practically and built to last. Local Bairnsdale team, about 20 minutes away.",
        "intro": [
            "Lindenow is a small farming township on the rich Mitchell River flats, market-garden country west of Bairnsdale. Homes here tend to sit on land, often older farmhouses and rural-residential properties, and the outdoor timber follows suit. A wide verandah that shades the house through summer does more work on a farm than a compact entertaining deck ever would, and it is usually the first thing we are asked about.",
            "Rural properties are also exposed. There is less shelter from wind and sun than a suburban block gets, so posts, footings and roof fixings have to be specified for it, and a pergola that would be fine behind a fence in town needs more holding it down out here. Sheds and outbuildings often need covered areas too, and that is the same trade.",
            "We are based about 20 minutes east in Bairnsdale and we cover the rural areas around it, not just the bigger towns. Over 10+ years locally we have done plenty of the honest, practical timber work that rural properties need, and we turn up and finish what we start.",
        ],
        "why_local": ("We cover the rural areas too.", "Lindenow and the Mitchell River flats are part of our patch, and travel is factored into the quote."),
        "faq_local": [
            ("Do you build wide verandahs on farmhouses around Lindenow?",
             "Yes, and on a rural block it is often the most useful thing you can build. A wide verandah shades the walls through summer and gives you covered space year-round. We size the posts and footings for an exposed site rather than a sheltered suburban one."),
            ("How far is Lindenow from Bairnsdale?",
             "About 20 kilometres, roughly a 20 minute drive. We cover the rural areas around Bairnsdale, so Lindenow is a regular part of our patch."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Lucknow", "lucknow"), ("Stratford", "stratford")],
    },
]

# Two shared FAQ, appended after the two localised ones.
SHARED_FAQ = [
    ("How long does a deck or pergola take to build?",
     "Most domestic decks are a week to two weeks on site once we start, depending on size, height and whether there is demolition first. A pergola on its own is usually quicker. We give you a realistic window with the quote rather than an optimistic one, and we tell you if a permit is going to add time."),
    ("Do you handle repairs, or only new builds?",
     "Both. Plenty of our decking work is bringing an existing deck back: replacing failed boards, repairing or rebuilding the frame, then sanding, staining and refinishing. If a repair is the sensible option we will say so rather than quote you a rebuild."),
]

# Shared "what we cover" cards. (title, body, href-or-None)
COVER_CARDS = [
    ("Timber Decking", "Hardwood and treated pine decks built level, solid and finished properly, then stained to suit the house.", None),
    ("Composite Decking", "Low-maintenance boards that do not split, cup or need re-oiling, ideal near the water and on holiday properties.", None),
    ("Pergolas", "Flat-roof and traditional pitched pergolas, freestanding or tied into the house, for shade and shelter.", None),
    ("Alfresco & Outdoor Living", "Entertaining areas and covered outdoor rooms that connect the house to the yard and get used year-round.", None),
    ("Repairs & Refinishing", "Failed boards and frames put right, then sanded, stained and refinished so weathered timber looks new again.", None),
    ("Verandahs & Custom Builds", "Verandahs, carports and one-off outdoor structures built to suit the home and the block.", "/custom-work"),
]

# Shared why-choose bullets (appended after the localised one). (strong, text)
SHARED_WHY = [
    ("10+ years in East Gippsland.", "We are local, we know the homes and the climate, and we have the track record to back it."),
    ("Timber or composite, honestly compared.", "We quote both and tell you what each costs to own, not just what it costs on the day."),
    ("One point of contact.", "You deal with one builder from the first look to the final clean-up, with a fixed price agreed upfront."),
]


def fit_title(name):
    for t in (
        f"Decks & Pergolas {name} VIC | NPD Building",
        f"Decks & Pergolas {name} | NPD Building Solutions",
        f"Decks & Pergolas in {name} | NPD Building Solutions",
        f"Deck Builder {name} VIC | NPD Building Solutions",
        f"Deck & Pergola Builder {name} | NPD Building Solutions",
    ):
        if 50 <= len(t) <= 60:
            return t
    return f"Decks & Pergolas {name} | NPD Building Solutions"


def meta_desc(name):
    for d in (
        f"Custom decks and pergolas in {name}, VIC, in timber or composite. Alfresco "
        f"areas, verandahs, repairs and refinishing from your local Bairnsdale builder.",
        f"Decks and pergolas in {name}, VIC, built in timber or composite. Alfresco "
        f"areas, verandahs, repairs and refinishing from your local Bairnsdale builder.",
        f"Custom decks and pergolas in {name}, VIC, in timber or composite. Alfresco "
        f"areas, verandahs and deck repairs from your local Bairnsdale builder.",
    ):
        if 150 <= len(d) <= 165:
            return d
    return (f"Custom decks and pergolas in {name}, VIC, in timber or composite. Alfresco "
            f"areas, verandahs and deck repairs from your local Bairnsdale builder.")


def faq_items(s):
    return list(s["faq_local"]) + list(SHARED_FAQ)


def head_jsonld(s):
    url = f"{DOMAIN}/decks-pergolas-{s['slug']}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            business_node(),
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "Decks & Pergolas", "item": f"{DOMAIN}/decks-pergolas"},
                    {"@type": "ListItem", "position": 3, "name": f"{s['name']} VIC", "item": url},
                ],
            },
            {
                "@type": "Service",
                "name": f"Decks & Pergolas in {s['name']}",
                "description": f"Custom timber and composite decks, pergolas, alfresco areas, verandahs and deck repairs in {s['name']}, East Gippsland.",
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


def render_nearby(nearby):
    out = []
    for name, slug in nearby:
        out.append(f'''        <a href="/decks-pergolas-{slug}" class="inline-block px-5 py-2.5 border border-gray-200 text-sm font-semibold text-gray-700 hover:border-brand hover:text-brand transition-colors duration-200">{esc(name)}</a>''')
    return "\n".join(out)


def render_intro(paras):
    return "\n".join(f'        <p>{esc(p)}</p>' for p in paras)


def page_html(s):
    name = s["name"]
    ename = esc(name)
    slug = s["slug"]
    url = f"{DOMAIN}/decks-pergolas-{slug}"
    title = fit_title(name)
    desc = meta_desc(name)
    keywords = (f"decks {name}, pergolas {name}, deck builder {name} VIC, composite decking {name}, "
                f"timber decking {name}, alfresco {name}, verandah {name}, East Gippsland deck builder")

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

  <meta property="og:title" content="Decks &amp; Pergolas in {ename} VIC | NPD Building Solutions">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_AU">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="NPD Building Solutions">
  <meta property="og:image" content="{DOMAIN}/{HERO_IMG_URL}-800.webp">
  <meta property="og:image:width" content="800">
  <meta property="og:image:height" content="600">
  <meta property="og:image:alt" content="Composite deck and verandah built by NPD Building Solutions near {ename}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Decks &amp; Pergolas in {ename} VIC | NPD Building Solutions">
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

{HEAD_ASSETS}
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
        <li><a href="/decks-pergolas" class="hover:text-brand transition-colors">Decks &amp; Pergolas</a></li>
        <li class="text-gray-500" aria-hidden="true">/</li>
        <li class="text-brand" aria-current="page">{ename} VIC</li>
      </ol>
    </div>
  </nav>

  <section class="relative pt-32 sm:pt-40 pb-16 sm:pb-20 bg-gray-900 overflow-hidden grain">
    <div class="absolute inset-0">
      <picture><source type="image/webp" srcset="{HERO_IMG_URL}-400.webp 400w, {HERO_IMG_URL}-800.webp 800w, {HERO_IMG_URL}-1600.webp 1600w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 100vw, 1600px"><img src="{HERO_IMG_SRC}" alt="Composite deck and verandah built by NPD Building Solutions, serving {ename} VIC" width="{HERO_IMG_W}" height="{HERO_IMG_H}" loading="eager" fetchpriority="high" decoding="sync" class="w-full h-full object-cover opacity-30"></picture>
      <div class="absolute inset-0 bg-gradient-to-b from-gray-900/80 via-gray-900/60 to-gray-900/90"></div>
      <div class="absolute inset-0 bg-brand/5 mix-blend-multiply"></div>
    </div>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="max-w-2xl">
        <p class="inline-flex items-center gap-2 text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">
          {PIN_SVG}
          Decks &amp; Pergolas in {ename}, VIC
        </p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-display text-white leading-[0.95] mb-6" style="letter-spacing: -0.03em;">Decks &amp; Pergolas in {ename}</h1>
        <p class="text-gray-300 text-base max-w-lg" style="line-height: 1.7;">{esc(s['lead'])}</p>
      </div>
    </div>
  </section>

  <!-- Local Intro -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Local Deck Builder</p>
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Outdoor Living in {ename}</h2>
      <div class="space-y-5 text-gray-600" style="line-height: 1.8;">
{render_intro(s['intro'])}
      </div>
    </div>
  </section>

  <!-- What We Cover -->
  <section class="py-20 sm:py-28 bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">What We Build in {ename}</p>
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">Decks, Pergolas and Everything Around Them</h2>
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
          <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Outdoor Timber, Done Properly</h2>
          <ul class="space-y-4">
{render_why(s)}
          </ul>
        </div>
        <div class="relative">
          <div class="overflow-hidden shadow-floating">
            <div class="relative">
              <picture><source type="image/webp" srcset="{WHY_IMG_URL}-400.webp 400w, {WHY_IMG_URL}-800.webp 800w, {WHY_IMG_URL}-1600.webp 1600w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 600px"><img src="{WHY_IMG_SRC}" alt="Waterfront composite deck with glass balustrade built by NPD Building Solutions in Paynesville" width="{WHY_IMG_W}" height="{WHY_IMG_H}" loading="lazy" decoding="async" class="w-full h-[350px] sm:h-[420px] object-cover"></picture>
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
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">{ename} Decking FAQ</h2>
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
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-8" style="letter-spacing: -0.03em;">Decks &amp; Pergolas Nearby</h2>
      <div class="flex flex-wrap justify-center gap-3">
{render_nearby(s['nearby'])}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 sm:py-28 relative overflow-hidden" style="background-color: #E8710A;" aria-label="Call to action">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      <h2 class="text-3xl sm:text-4xl lg:text-5xl font-display text-white mb-6" style="letter-spacing: -0.03em;">Planning a Deck in {ename}?</h2>
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
        path = os.path.join(ROOT, f"decks-pergolas-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page_html(s))
        written.append(os.path.basename(path))
        t, d = fit_title(s["name"]), meta_desc(s["name"])
        if not (50 <= len(t) <= 60):
            warns.append(f"  TITLE {s['slug']}: {len(t)} chars -> {t}")
        if not (150 <= len(d) <= 165):
            warns.append(f"  META  {s['slug']}: {len(d)} chars")
    print(f"Wrote {len(written)} decks & pergolas suburb LPs:")
    for w in written:
        print("  " + w)
    if warns:
        print("\nLength warnings (want title 50-60, meta 150-165):")
        print("\n".join(warns))
    else:
        print("\nAll titles 50-60 and metas 150-165 chars.")


if __name__ == "__main__":
    main()
