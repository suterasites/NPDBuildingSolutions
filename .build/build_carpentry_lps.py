#!/usr/bin/env python3
"""
build_carpentry_lps.py - generate the Carpentry x suburb landing pages for NPD Building Solutions.

One page per target suburb: carpentry-<slug>.html (clean URL /carpentry-<slug> on Cloudflare Pages).
Chrome (head assets, nav, footer, scripts) is transcribed VERBATIM from the live, 100-clean pages
(lakes-entrance.html / general-carpentry.html) so every Tailwind class is already in the compiled
styles.css - the site purges any utility class that is not already used, so we never invent classes.

Filenames are carpentry-<slug> so the WP HQ coverage detector attributes each to
(Carpentry x <suburb>): the service term "carpentry" is a substring and the suburb slug is a
contiguous token-run. Copy is genuinely localised (East Gippsland geography, housing character,
distance from the Bairnsdale base) so pages are not thin doorway duplicates, and NO specific
project is claimed in a suburb - only the documented, site-wide facts (10+ years in East Gippsland;
16 bathrooms in 14 months alongside Cutting Edge Constructions; the Paynesville deck already on the
site). No em dashes anywhere (site + repo hard rule).

Run:  python3 .build/build_carpentry_lps.py    (writes into the site root, one dir up)
Re-runnable: overwrites the generated carpentry-*.html files in place; hand pages are untouched.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOMAIN = "https://npdbuildingsolutions.com.au"
BUSINESS_ID = f"{DOMAIN}/#business"

# ---------------------------------------------------------------------------
# Per-suburb data. `intro` is a list of paragraphs (carpentry + real local
# character). `why_local` is the localised bullet. `faq_local` are two
# localised Q&A (the two shared Q&A are appended by faq_items()). `nearby`
# cross-links the carpentry cluster. `meta_tail` is unused; meta is templated.
# ---------------------------------------------------------------------------
SUBURBS = [
    {
        "name": "Bairnsdale", "slug": "bairnsdale",
        "lead": "Structural and finishing carpentry for Bairnsdale homes, from framing and repairs through to fit-outs, doors and windows. This is our home base, so we are on the tools here most days.",
        "intro": [
            "Bairnsdale is where we are based, and where we have built our name over 10+ years on the tools. The town runs from character weatherboards and period homes around the centre through to newer brick estates on the edges, and each generation of home brings its own carpentry. Older places need weatherboard repairs, door and window adjustments as they settle, and verandah and floor work; newer builds need fit-outs, storage and the finishing carpentry that turns a house into a home.",
            "Because we live here, there is no travel loaded into a Bairnsdale quote and we can usually get to site quickly to look at a job. Over the last few years we completed 16 bathrooms in 14 months alongside Cutting Edge Constructions, and a lot of that work is carpentry: framing, sheeting, fit-out and the finishing that ties a renovation together.",
            "Whether it is a small repair, a full fit-out or the carpentry stage of a larger renovation, you deal with one local carpenter from the first look through to the final clean-up, with a fixed price agreed upfront.",
        ],
        "why_local": ("Bairnsdale-based.", "This is our home town, so there is no travel cost in a local quote and we can get to site fast."),
        "faq_local": [
            ("Are you actually based in Bairnsdale?",
             "Yes. Bairnsdale is our home base and has been for 10+ years. Most of our work is right here and across East Gippsland, so a Bairnsdale job means no travel loaded into the quote and a quick site visit."),
            ("Do you repair older weatherboard homes around Bairnsdale?",
             "Yes. A lot of Bairnsdale's older homes are weatherboard and timber-framed, and they need sympathetic repairs as they age: board replacement, door and window adjustments, and verandah and floor work. We handle that kind of carpentry regularly."),
        ],
        "nearby": [("Lucknow", "lucknow"), ("Nicholson", "nicholson"), ("Eagle Point", "eagle-point")],
    },
    {
        "name": "Lakes Entrance", "slug": "lakes-entrance",
        "lead": "Carpentry for Lakes Entrance homes, rentals and holiday properties, from framing and repairs to fit-outs and doors. Coastal-aware builds from a local East Gippsland team.",
        "intro": [
            "Lakes Entrance splits into permanent homes, long-term rentals and short-stay holiday properties, and each one keeps carpenters busy in a different way. A lot of the housing stock dates from the 80s and 90s, so there is steady demand for repairs, door and window replacement, and the internal carpentry that comes with updating a tired home. The salt air and sun down this coast are hard on external timber, so choosing the right materials and fixings matters more here than inland.",
            "We have spent 10+ years working across East Gippsland, and Lakes Entrance is a regular route for us, about 35 kilometres east along the Princes Highway. That means site visits and quotes are easy to fit in, and for rental owners we can sequence work around booking windows so as few nights as possible are lost.",
            "From a single repair through to the carpentry stage of a full renovation, you get one local carpenter across the job and a fixed price agreed upfront.",
        ],
        "why_local": ("Coastal-aware carpentry.", "Correct timber, corrosion-resistant fixings and finishes that stand up to Lakes Entrance salt air and sun."),
        "faq_local": [
            ("How far is Lakes Entrance from your Bairnsdale base?",
             "About 35 kilometres east, roughly a 30 to 35 minute drive along the Princes Highway. We service Lakes Entrance regularly, so travel is not a barrier and it is factored into the quote upfront."),
            ("Can you work around holiday rental bookings?",
             "Yes. We schedule carpentry work on short-stay rentals around your booking calendar so you lose as few nights as possible, and we keep the site tidy between stages."),
        ],
        "nearby": [("Metung", "metung"), ("Nicholson", "nicholson"), ("Paynesville", "paynesville")],
    },
    {
        "name": "Paynesville", "slug": "paynesville",
        "lead": "Carpentry for Paynesville's waterfront and canal-estate homes, from framing and repairs to fit-outs, doors and outdoor timber. Local builder, 10+ years in East Gippsland.",
        "intro": [
            "Paynesville is built around the water, with canal-front homes, jetties and a strong boating culture, and that shapes the carpentry. Waterfront and canal-estate homes want light-filled living spaces, big glazed doors opening to the water, and outdoor timber that copes with a damp, exposed setting. Older cottages in the town centre need the usual repairs and fit-outs that come with age.",
            "We are based about 20 minutes north in Bairnsdale and have worked in Paynesville for years. In fact one of our projects here, a second-floor deck and carport alongside Cutting Edge Constructions, is on our own site. Carpentry near the water needs the right timber and fixings so it does not rust out or swell, and 10+ years locally means we know what holds up.",
            "Whether it is repairs, a fit-out or the carpentry behind a bigger renovation, you deal with one local carpenter and a price agreed before we start.",
        ],
        "why_local": ("Built for the water.", "Timber and fixings chosen for Paynesville's canal-front, damp and exposed conditions, so the work lasts."),
        "faq_local": [
            ("Do you work on waterfront and canal homes in Paynesville?",
             "Yes, regularly. Carpentry near the water needs corrosion-resistant fixings and timber chosen for damp, exposed conditions. We have worked in Paynesville for years, including a second-floor deck and carport alongside Cutting Edge Constructions."),
            ("How far is Paynesville from Bairnsdale?",
             "About 18 kilometres, roughly a 20 minute drive south-east. We are in Paynesville often, so site visits and quotes are easy to arrange."),
        ],
        "nearby": [("Eagle Point", "eagle-point"), ("Bairnsdale", "bairnsdale"), ("Metung", "metung")],
    },
    {
        "name": "Sale", "slug": "sale",
        "lead": "Carpentry for Sale and the Wellington Shire, from framing and repairs to interior fit-outs and doors. A Bairnsdale-based team that services Sale regularly.",
        "intro": [
            "Sale is the largest town in the Wellington Shire and a mix of established period homes, post-war brick and newer estates spreading out from the centre. That range means everything from sympathetic repairs on older timber homes through to fit-outs and finishing carpentry in newer builds. As a bigger regional centre there is steady renovation activity, and carpentry sits at the heart of most of it.",
            "We are based in Bairnsdale, about 50 minutes east along the Princes Highway, and Sale is a town we service regularly rather than as a one-off. Over 10+ years across Gippsland we have built a reputation for turning up, doing the job properly and finishing it, including 16 bathrooms in 14 months alongside Cutting Edge Constructions.",
            "From a small repair to the carpentry stage of a full renovation, you get one carpenter across the job and a fixed price agreed upfront, travel included.",
        ],
        "why_local": ("We service Sale regularly.", "Sale is a standing part of our run, so travel is factored into the quote and a site visit is easy to book."),
        "faq_local": [
            ("Do you travel to Sale from Bairnsdale?",
             "Yes. Sale is about 65 kilometres west, roughly a 50 minute drive along the Princes Highway, and we service it regularly. Travel is factored into the quote upfront so there are no surprises."),
            ("Do you work across the Wellington Shire, not just Sale itself?",
             "Yes. We cover Sale and the surrounding Wellington Shire towns. If you are near Sale and not sure whether we reach you, give us a call and we will let you know."),
        ],
        "nearby": [("Stratford", "stratford"), ("Bairnsdale", "bairnsdale"), ("Paynesville", "paynesville")],
    },
    {
        "name": "Stratford", "slug": "stratford",
        "lead": "Carpentry for Stratford's heritage and riverside homes, from sympathetic repairs to fit-outs, doors and finishing work. Local East Gippsland builder, 10+ years on the tools.",
        "intro": [
            "Stratford is a historic town on the Avon River, known for its period streetscape and character homes. That heritage stock is largely timber-framed and weatherboard, which means carpentry here is often about sympathetic repair and restoration: matching existing profiles, fixing verandahs and floors, and adjusting doors and windows in homes that have moved over a century. Newer homes on the edges need the usual fit-outs and finishing.",
            "We work across East Gippsland and into the Wellington Shire, and Stratford sits on our Sale run, about 45 minutes west of our Bairnsdale base. Over 10+ years we have learned to work with older homes rather than against them, keeping the character intact while bringing the carpentry up to standard.",
            "Whether it is a heritage repair, a fit-out or the carpentry behind a larger renovation, you deal with one carpenter and a price agreed before the work starts.",
        ],
        "why_local": ("Sympathetic to older homes.", "Stratford's heritage timber homes need matched profiles and careful repair, and that is work we do regularly."),
        "faq_local": [
            ("Do you work on heritage and period homes in Stratford?",
             "Yes. A lot of Stratford's housing is period timber and weatherboard, and we handle sympathetic repairs, matching existing profiles and keeping the character intact while bringing the carpentry up to standard."),
            ("How far is Stratford from Bairnsdale?",
             "About 55 kilometres west, roughly a 40 to 45 minute drive, and it sits on our Sale run. We service it regularly, with travel factored into the quote."),
        ],
        "nearby": [("Sale", "sale"), ("Bairnsdale", "bairnsdale"), ("Lindenow", "lindenow")],
    },
    {
        "name": "Metung", "slug": "metung",
        "lead": "Carpentry for Metung's waterfront and holiday homes, from framing and repairs to fit-outs, doors and outdoor timber. Coastal-aware builds from a local East Gippsland team.",
        "intro": [
            "Metung is a small waterfront village on the Gippsland Lakes with a strong boating and holiday-home character. A lot of the housing is second homes and higher-end waterfront properties, where carpentry leans towards quality fit-outs, big glazed doors framing the water, and outdoor timber built to handle an exposed lakeside setting. There is also steady repair and maintenance work on older holiday cottages.",
            "We are based in Bairnsdale, about 30 minutes west, and Metung is a regular part of our East Gippsland patch. Waterfront carpentry needs the right timber and corrosion-resistant fixings so it holds up to salt air and damp, and 10+ years locally means we know what works down this coast.",
            "From repairs and fit-outs to the carpentry stage of a bigger renovation, you get one local carpenter across the job and a price agreed upfront.",
        ],
        "why_local": ("Lakeside-ready.", "Timber and fixings chosen for Metung's exposed, waterfront conditions, so the carpentry lasts."),
        "faq_local": [
            ("Do you work on waterfront homes in Metung?",
             "Yes. Metung's waterfront and holiday homes need carpentry built for an exposed lakeside setting, with corrosion-resistant fixings and timber that copes with salt air and damp. We work in Metung regularly."),
            ("How far is Metung from Bairnsdale?",
             "About 30 kilometres east, roughly a 30 minute drive. Metung is a regular part of our patch, so site visits and quotes are easy to arrange."),
        ],
        "nearby": [("Lakes Entrance", "lakes-entrance"), ("Paynesville", "paynesville"), ("Nicholson", "nicholson")],
    },
    {
        "name": "Nicholson", "slug": "nicholson",
        "lead": "Carpentry for Nicholson's homes and rural properties, from framing and repairs to fit-outs, doors and shed work. Based just up the road in Bairnsdale.",
        "intro": [
            "Nicholson is a small township on the Nicholson River just east of Bairnsdale, a semi-rural pocket of homes on larger blocks and hobby properties. That setting brings a slightly different carpentry mix: as well as the usual home repairs and fit-outs, there is shed and outbuilding work, verandahs, and the kind of practical timber jobs that come with living on a bit of land.",
            "Being only about 10 minutes from our Bairnsdale base, Nicholson is genuinely local for us. There is effectively no travel to load into a quote and we can get to site quickly to look at a job. Over 10+ years across East Gippsland we have built a name for turning up and finishing the work.",
            "Whether it is a home repair, a fit-out, a shed or the carpentry behind a renovation, you deal with one local carpenter and a fixed price agreed upfront.",
        ],
        "why_local": ("Right next door.", "Nicholson is about 10 minutes from our Bairnsdale base, so there is next to no travel in the quote and a fast site visit."),
        "faq_local": [
            ("Do you do rural and shed carpentry around Nicholson?",
             "Yes. Nicholson's semi-rural blocks often need shed and outbuilding work, verandahs and practical timber repairs alongside the usual home carpentry, and we take on all of it."),
            ("How far is Nicholson from Bairnsdale?",
             "Only about 10 kilometres, a 10 to 12 minute drive east. It is genuinely local for us, so there is next to no travel loaded into a quote."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Eagle Point", "eagle-point"), ("Lucknow", "lucknow")],
    },
    {
        "name": "Eagle Point", "slug": "eagle-point",
        "lead": "Carpentry for Eagle Point's waterfront and rural-residential homes, from framing and repairs to fit-outs, doors and outdoor timber. Local Bairnsdale builder.",
        "intro": [
            "Eagle Point sits above Lake King and the Mitchell River silt jetties, a quiet spot of waterfront and rural-residential homes on generous blocks. The outlook is a big part of living here, so carpentry often centres on making the most of it: decks and outdoor timber, glazed doors, and light-filled living spaces, alongside the repairs and fit-outs any home needs over time.",
            "We are based about 15 minutes north in Bairnsdale, so Eagle Point is genuinely local and a regular part of our run. Being close to the water, timber and fixings need to be chosen for damp and exposed conditions, and 10+ years locally means we know what holds up here.",
            "From repairs and fit-outs to the carpentry stage of a bigger project, you get one local carpenter and a price agreed before we start.",
        ],
        "why_local": ("Local and close.", "Eagle Point is about 15 minutes from our Bairnsdale base, so travel is minimal and site visits are easy."),
        "faq_local": [
            ("Do you build decks and outdoor timber for Eagle Point's views?",
             "Yes. A lot of Eagle Point homes are about the outlook over Lake King, so decks, outdoor timber and glazed doors are common jobs. We build them with timber and fixings chosen for the waterfront setting."),
            ("How far is Eagle Point from Bairnsdale?",
             "About 15 kilometres south-east, roughly a 15 to 18 minute drive. It is genuinely local for us, so site visits and quotes are easy to arrange."),
        ],
        "nearby": [("Paynesville", "paynesville"), ("Nicholson", "nicholson"), ("Bairnsdale", "bairnsdale")],
    },
    {
        "name": "Lucknow", "slug": "lucknow",
        "lead": "Carpentry for Lucknow homes, from framing and repairs to interior fit-outs and doors. Effectively on our doorstep, just east of our Bairnsdale base.",
        "intro": [
            "Lucknow sits on the eastern edge of Bairnsdale, close enough to be part of the town but with its own established residential character. The housing is a mix of older homes and newer builds, which means the full carpentry range: repairs and door and window work on the older places, and fit-outs, storage and finishing carpentry in the newer ones.",
            "For us Lucknow is about as local as it gets, only a few minutes from our Bairnsdale base. That means no travel to speak of in a quote and a quick turnaround on a site visit. Over 10+ years in the area we have built a reputation for doing the job properly and finishing it.",
            "Whether it is a small repair, a full fit-out or the carpentry stage of a renovation, you deal with one local carpenter and a fixed price agreed upfront.",
        ],
        "why_local": ("On our doorstep.", "Lucknow is only minutes from our Bairnsdale base, so there is no real travel in the quote and a fast site visit."),
        "faq_local": [
            ("Are you local to Lucknow?",
             "Very. Lucknow is on the eastern edge of Bairnsdale, just a few minutes from our base, so it is effectively home turf. There is no real travel to load into a quote."),
            ("Do you handle both older homes and newer builds in Lucknow?",
             "Yes. Lucknow has a mix of both. We do sympathetic repairs and door and window work on older homes, and fit-outs, storage and finishing carpentry in newer builds."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Nicholson", "nicholson"), ("Eagle Point", "eagle-point")],
    },
    {
        "name": "Lindenow", "slug": "lindenow",
        "lead": "Carpentry for Lindenow's rural homes and properties, from framing and repairs to fit-outs, verandahs and shed work. Practical timber work from a local Bairnsdale team.",
        "intro": [
            "Lindenow is a small farming township on the rich Mitchell River flats, market-garden country west of Bairnsdale. Homes here tend to sit on land, often older farmhouses and rural-residential properties, so the carpentry is practical: verandah and floor repairs, weatherboard work, sheds and outbuildings, and the fit-outs and finishing that come with updating an older rural home.",
            "We are based about 20 minutes east in Bairnsdale and cover the rural areas around it, not just the bigger towns. Over 10+ years locally we have done plenty of the honest, practical carpentry that rural properties need, and we turn up and finish what we start.",
            "From a verandah repair or a shed through to the carpentry behind a full renovation, you deal with one local carpenter and a fixed price agreed upfront.",
        ],
        "why_local": ("We cover the rural areas too.", "Lindenow and the Mitchell River flats are part of our patch, not too far out, and travel is factored into the quote."),
        "faq_local": [
            ("Do you do farmhouse and shed carpentry around Lindenow?",
             "Yes. Lindenow is rural, so a lot of the work is practical: verandah and floor repairs, weatherboard work, sheds and outbuildings, alongside home fit-outs and finishing. We take on all of it."),
            ("How far is Lindenow from Bairnsdale?",
             "About 20 kilometres, roughly a 20 minute drive. We cover the rural areas around Bairnsdale, so Lindenow is a regular part of our patch."),
        ],
        "nearby": [("Bairnsdale", "bairnsdale"), ("Lucknow", "lucknow"), ("Stratford", "stratford")],
    },
]

# Two shared FAQ, appended after the two localised ones.
SHARED_FAQ = [
    ("What carpentry jobs do you take on?",
     "Everything from structural framing, roof timbers and load-bearing work through to repairs, interior fit-outs, skirting and architraves, door and window installation, and finishing carpentry. If it is timber and it needs a carpenter, it is worth a call."),
    ("Do you take on small repairs, or only large jobs?",
     "Both. We are happy to take on small carpentry repairs as well as full fit-outs and the carpentry stage of larger renovations. You get the same care either way, and a fixed price agreed upfront."),
]

# Shared "what we cover" cards. (title, body, href-or-None)
COVER_CARDS = [
    ("Structural & Framing", "Wall framing, roof timbers, subfloors and load-bearing work, built right from the ground up.", None),
    ("Repairs & Restoration", "Rotted, damaged or weathered timber put right, from weatherboards and verandahs to floors and structural fixes.", None),
    ("Interior Fit-Outs", "Skirting, architraves, door hanging, shelving and built-in storage, finished with clean lines.", None),
    ("Doors & Windows", "Supply and installation of doors and windows, including architraves and adjustments as a home settles.", "/windows-doors"),
    ("Decking & Outdoor Timber", "Verandahs, decks, pergolas and outdoor structures built for the East Gippsland climate.", "/decks-pergolas"),
    ("Custom Carpentry", "One-off builds, feature timber work and bespoke joinery tailored to your home.", "/custom-work"),
]

# Shared why-choose bullets (appended after the localised one). (strong, text)
SHARED_WHY = [
    ("10+ years in East Gippsland.", "We are local, we know the homes and the climate, and we have the track record to back it."),
    ("16 bathrooms in 14 months", "with Cutting Edge Constructions, proof of consistent volume and consistent quality."),
    ("One point of contact.", "You deal with one carpenter from the first look to the final clean-up, with a fixed price agreed upfront."),
]

CHECK_SVG = '<svg class="w-5 h-5 text-brand flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>'
PLUS_SVG = '<svg class="w-5 h-5 text-brand transition-transform duration-200 group-open:rotate-45" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>'
PIN_SVG = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>'
PHONE_SVG = '<svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>'
DOC_SVG = '<svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'

HERO_IMG_URL = "Assets/optimized/Major%20Project/Interior%20Renovation%20-%20Kitchen%20and%20Dining"
WHY_IMG_URL = "Assets/optimized/Major%20Project/Interior%20Renovation%20-%20Open%20Plan%20Living"


def esc(t):
    return t.replace("&", "&amp;")


def fit_title(name):
    for t in (
        f"Carpenter {name} VIC | NPD Building Solutions",
        f"Carpenter in {name} VIC | NPD Building Solutions",
        f"Carpenter & Renovations {name} | NPD Building Solutions",
    ):
        if 50 <= len(t) <= 60:
            return t
    # fallback: never seen for the 10 target suburbs
    return f"Carpenter {name} VIC | NPD Building Solutions"


def meta_desc(name):
    return (f"General carpentry in {name}, VIC: framing, repairs, interior fit-outs, "
            f"doors and windows. Your local Bairnsdale-based carpenter with 10+ years on the tools.")


def faq_items(s):
    return list(s["faq_local"]) + list(SHARED_FAQ)


# ---- Verbatim chrome (transcribed from lakes-entrance.html, 100-clean) -----

HEAD_ASSETS = '''  <link rel="preload" as="image" imagesrcset="Assets/optimized/Major%20Project/Interior%20Renovation%20-%20Kitchen%20and%20Dining-400.webp 400w, Assets/optimized/Major%20Project/Interior%20Renovation%20-%20Kitchen%20and%20Dining-800.webp 800w, Assets/optimized/Major%20Project/Interior%20Renovation%20-%20Kitchen%20and%20Dining-1600.webp 1600w" imagesizes="(max-width: 640px) 100vw, (max-width: 1024px) 100vw, 1600px" type="image/webp" fetchpriority="high">
  <link rel="stylesheet" href="/styles.css">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap">
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>

  <style>
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', system-ui, sans-serif; }
    h1, h2, h3, .font-display { font-family: 'Barlow Condensed', 'Arial Narrow', sans-serif; font-weight: 700; text-transform: uppercase; }

    .grain::before {
      content: '';
      position: absolute;
      inset: 0;
      opacity: 0.04;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
      pointer-events: none;
      z-index: 1;
    }

    .shadow-elevated {
      box-shadow:
        0 1px 2px rgba(232, 113, 10, 0.04),
        0 4px 8px rgba(232, 113, 10, 0.06),
        0 12px 24px rgba(0, 0, 0, 0.06);
    }
    .shadow-floating {
      box-shadow:
        0 2px 4px rgba(232, 113, 10, 0.06),
        0 8px 16px rgba(232, 113, 10, 0.08),
        0 24px 48px rgba(0, 0, 0, 0.1);
    }

    .transition-spring {
      transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .btn-primary:focus-visible,
    .btn-secondary:focus-visible {
      outline: 3px solid #E8710A;
      outline-offset: 3px;
    }
    /* Skip to content link */
    .skip-to-content {
      position: absolute;
      top: -100px;
      left: 0;
      background: #E8710A;
      color: #fff;
      padding: 12px 20px;
      z-index: 100;
      font-weight: 600;
      text-decoration: none;
    }
    .skip-to-content:focus {
      top: 0;
      outline: 3px solid #fff;
      outline-offset: 2px;
    }

  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FM0EVYVJBP"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-FM0EVYVJBP');
  </script>
  <!-- Sutera lead events (GA4) -->
  <script>/* SUTERA_LEAD_EVENTS */
  (function(){
    function ev(n, p){ if (typeof window.gtag === 'function') { window.gtag('event', n, Object.assign({transport_type:'beacon'}, p||{})); } }
    document.addEventListener('click', function(e){
      var a = e.target.closest ? e.target.closest('a[href^="tel:"]') : null;
      if (a) ev('click_to_call', { link_url: a.getAttribute('href') });
    }, true);
    document.addEventListener('submit', function(e){
      var f = e.target;
      if (!f || f.tagName !== 'FORM' || f.hasAttribute('data-no-lead')) return;
      var action = f.getAttribute('action') || '';
      var isLead = /formspree/i.test(action) || f.querySelector('input[type="email"], input[type="tel"], textarea');
      if (isLead) ev('generate_lead', { form_id: f.id || f.getAttribute('name') || 'contact' });
    }, true);
  })();
  </script>'''

NAV_HTML = '''<body class="bg-white text-gray-900 antialiased">

  <a href="#main" class="skip-to-content">Skip to content</a>

  <!-- Navigation -->
  <header>
  <nav id="main-nav" class="fixed top-0 w-full z-50 bg-black border-b border-gray-800 transition-transform duration-300" role="navigation" aria-label="Main navigation">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        <a href="/" class="flex items-center gap-2" aria-label="NPD Building Solutions home">
          <picture><source type="image/webp" srcset="Assets/optimized/Logo-200.webp 200w, Assets/optimized/Logo-400.webp 400w" sizes="(max-width: 640px) 100vw, 800px"><img src="Assets/Logo.jpg" alt="NPD Building Solutions" width="797" height="386" loading="lazy" decoding="async" class="h-10 sm:h-12 w-auto"></picture>
        </a>
        <div class="hidden md:flex items-center gap-8">
          <div class="relative group">
            <a href="/services" class="text-sm font-medium text-gray-300 hover:text-brand transition-colors duration-200 inline-flex items-center gap-1">
              Services
              <svg class="w-3.5 h-3.5 transition-transform duration-200 group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </a>
            <div class="absolute left-1/2 -translate-x-1/2 top-full pt-4 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-200 z-50">
              <div class="bg-white border border-gray-200 shadow-floating p-6 w-[520px]">
                <div class="grid grid-cols-2 gap-3">
                  <a href="/general-carpentry" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">General Carpentry</p>
                      <p class="text-xs text-gray-500 mt-0.5">Structural and finishing carpentry</p>
                    </div>
                  </a>
                  <a href="/bathroom-renovations" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">Bathroom Renovations</p>
                      <p class="text-xs text-gray-500 mt-0.5">Full renovations from start to finish</p>
                    </div>
                  </a>
                  <a href="/windows-doors" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">Windows & Door Replacements</p>
                      <p class="text-xs text-gray-500 mt-0.5">All-inclusive: architraves + painting</p>
                    </div>
                  </a>
                  <a href="/decks-pergolas" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">Decks & Pergolas</p>
                      <p class="text-xs text-gray-500 mt-0.5">Custom outdoor living spaces</p>
                    </div>
                  </a>
                  <a href="/tiling" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">High-Quality Tiling</p>
                      <p class="text-xs text-gray-500 mt-0.5">Precision tiling for any space</p>
                    </div>
                  </a>
                  <a href="/fencing-gates" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">Fencing, Gates & Pool Fencing</p>
                      <p class="text-xs text-gray-500 mt-0.5">Secure your property</p>
                    </div>
                  </a>
                  <a href="/custom-work" class="flex items-start gap-3 p-3 hover:bg-brand-50 transition-colors duration-200">
                    <div>
                      <p class="text-sm font-semibold text-gray-900">Custom Work</p>
                      <p class="text-xs text-gray-500 mt-0.5">Bespoke builds for any vision</p>
                    </div>
                  </a>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100">
                  <a href="/services" class="flex items-center gap-2 text-sm font-semibold text-brand hover:text-brand-dark transition-colors duration-200">
                    View All Services
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <a href="/about" class="text-sm font-medium text-gray-300 hover:text-brand transition-colors duration-200">About</a>
          <a href="/our-work" class="text-sm font-medium text-gray-300 hover:text-brand transition-colors duration-200">Our Work</a>
          <a href="/contact" class="text-sm font-medium text-gray-300 hover:text-brand transition-colors duration-200">Contact</a>
        </div>
        <div class="flex items-center gap-3">
          <a href="tel:0427278285" class="btn-primary inline-flex items-center gap-2 bg-brand hover:bg-brand-dark active:bg-brand-dark text-white font-semibold text-sm px-5 py-2.5 transition-spring transition-transform duration-300 hover:scale-[1.03] active:scale-[0.98]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            <span class="hidden sm:inline">0427 278 285</span>
            <span class="sm:hidden">Call Now</span>
          </a>
          <button id="mobile-menu-btn" class="md:hidden flex items-center justify-center w-10 h-10 text-gray-300 hover:text-brand focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand active:scale-95 transition-transform duration-200" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
            <svg id="hamburger-icon" class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
            <svg id="close-icon" class="w-6 h-6 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>
    </div>

    <div id="mobile-menu" class="md:hidden overflow-hidden transition-[max-height] duration-300 ease-out max-h-0 bg-black border-t border-gray-800">
      <div class="px-4 py-4 flex flex-col gap-1">
        <a href="/services" class="mobile-nav-link block px-4 py-3 text-sm font-semibold text-gray-300 hover:text-brand hover:bg-gray-800 active:bg-gray-700 rounded-lg transition-colors duration-200">Services</a>
        <a href="/about" class="mobile-nav-link block px-4 py-3 text-sm font-semibold text-gray-300 hover:text-brand hover:bg-gray-800 active:bg-gray-700 rounded-lg transition-colors duration-200">About</a>
        <a href="/our-work" class="mobile-nav-link block px-4 py-3 text-sm font-semibold text-gray-300 hover:text-brand hover:bg-gray-800 active:bg-gray-700 rounded-lg transition-colors duration-200">Our Work</a>
        <a href="/contact" class="mobile-nav-link block px-4 py-3 text-sm font-semibold text-gray-300 hover:text-brand hover:bg-gray-800 active:bg-gray-700 rounded-lg transition-colors duration-200">Contact</a>
      </div>
    </div>
  </nav>
  </header>
  <script>
    (function() {
      const btn = document.getElementById('mobile-menu-btn');
      const menu = document.getElementById('mobile-menu');
      const hamburger = document.getElementById('hamburger-icon');
      const closeIcon = document.getElementById('close-icon');
      const servicesBtn = document.getElementById('mobile-services-toggle');
      const servicesPanel = document.getElementById('mobile-services-panel');
      const servicesChevron = document.getElementById('mobile-services-chevron');
      if (!btn || !menu) return;

      function closeMenu() {
        // Lock to current height so we can animate to 0
        menu.style.maxHeight = menu.scrollHeight + 'px';
        requestAnimationFrame(function() {
          menu.style.maxHeight = '0px';
        });
        hamburger.classList.remove('hidden');
        closeIcon.classList.add('hidden');
        btn.setAttribute('aria-expanded', 'false');
        if (servicesPanel) {
          servicesPanel.style.maxHeight = '0px';
          servicesChevron && servicesChevron.classList.remove('rotate-180');
          servicesBtn && servicesBtn.setAttribute('aria-expanded', 'false');
        }
      }

      function openMenu() {
        menu.style.maxHeight = menu.scrollHeight + 'px';
        // After the open transition finishes, release the height so nested panels can grow.
        const onEnd = function(e) {
          if (e.target !== menu || e.propertyName !== 'max-height') return;
          menu.style.maxHeight = 'none';
          menu.removeEventListener('transitionend', onEnd);
        };
        menu.addEventListener('transitionend', onEnd);
        hamburger.classList.add('hidden');
        closeIcon.classList.remove('hidden');
        btn.setAttribute('aria-expanded', 'true');
      }

      function toggleMenu() {
        const isOpen = btn.getAttribute('aria-expanded') === 'true';
        if (isOpen) closeMenu(); else openMenu();
      }

      btn.addEventListener('click', toggleMenu);

      if (servicesBtn && servicesPanel) {
        servicesBtn.addEventListener('click', function() {
          const open = servicesBtn.getAttribute('aria-expanded') === 'true';
          if (open) {
            servicesPanel.style.maxHeight = servicesPanel.scrollHeight + 'px';
            requestAnimationFrame(function() { servicesPanel.style.maxHeight = '0px'; });
            servicesChevron && servicesChevron.classList.remove('rotate-180');
            servicesBtn.setAttribute('aria-expanded', 'false');
          } else {
            servicesPanel.style.maxHeight = servicesPanel.scrollHeight + 'px';
            servicesChevron && servicesChevron.classList.add('rotate-180');
            servicesBtn.setAttribute('aria-expanded', 'true');
          }
        });
      }

      menu.querySelectorAll('a.mobile-nav-link').forEach(function(link) {
        link.addEventListener('click', closeMenu);
      });
    })();
  </script>

  <script>
    (function() {
      var nav = document.getElementById('main-nav');
      var lastScroll = 0;
      window.addEventListener('scroll', function() {
        var current = window.scrollY;
        if (current > lastScroll && current > 80) {
          nav.style.transform = 'translateY(-100%)';
        } else {
          nav.style.transform = 'translateY(0)';
        }
        lastScroll = current;
      });
    })();
  </script>'''

FOOTER_HTML = '''  <!-- Footer -->
  </main>

  <footer class="bg-black py-12" role="contentinfo">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
        <div>
          <div class="mb-4">
            <a href="/"><picture><source type="image/webp" srcset="Assets/optimized/Logo-200.webp 200w, Assets/optimized/Logo-400.webp 400w" sizes="(max-width: 640px) 100vw, 800px"><img src="Assets/Logo.jpg" alt="NPD Building Solutions" width="797" height="386" loading="lazy" decoding="async" class="h-12 w-auto"></picture></a>
          </div>
          <p class="text-sm text-gray-400" style="line-height: 1.7;">Bairnsdale-based carpentry and renovations with 10+ years experience. Decks, pergolas, tiling, bathroom renovations, fencing, gates, custom work and more.</p>
        </div>
        <div>
          <h3 class="text-sm font-semibold text-white uppercase tracking-wide mb-4">Quick Links</h3>
          <nav class="space-y-2" aria-label="Footer navigation">
            <a href="/services" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Services</a>
            <a href="/about" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">About</a>
            <a href="/our-work" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Our Work</a>
            <a href="/contact" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Contact</a>
            <a href="privacy.html" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Privacy Policy</a>
          </nav>
        </div>
        <div>
          <h3 class="text-sm font-semibold text-white uppercase tracking-wide mb-4">Service Areas</h3>
          <nav class="space-y-2" aria-label="Service areas">
            <a href="/" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Bairnsdale</a>
            <a href="/sale" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Sale</a>
            <a href="/paynesville" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Paynesville</a>
            <a href="/lakes-entrance" class="block text-sm text-gray-300 hover:text-brand transition-colors duration-200">Lakes Entrance</a>
          </nav>
        </div>
        <div>
          <h3 class="text-sm font-semibold text-white uppercase tracking-wide mb-4">Contact</h3>
          <div class="space-y-2">
            <a href="tel:0427278285" class="flex items-center gap-2 text-sm text-gray-300 hover:text-brand transition-colors duration-200">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
              0427 278 285
            </a>
            <a href="#" onclick="window.location='mailto:'+atob('bnBkYnVpbGRpbmdzb2x1dGlvbnNAb3V0bG9vay5jb20=');return false;" class="flex items-center gap-2 text-sm text-gray-300 hover:text-brand transition-colors duration-200">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              <span class="email-protect">npdbuildingsolutions<span class="at-sign">[at]</span>outlook.com</span>
            </a>
            <p class="flex items-center gap-2 text-sm text-gray-300">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              Bairnsdale & Surrounding Areas, VIC
            </p>
          </div>
          <div class="flex items-center gap-3 mt-4">
            <a href="https://www.facebook.com/profile.php?id=61588392252999" target="_blank" rel="noopener noreferrer" class="w-9 h-9 bg-white/10 flex items-center justify-center hover:bg-brand transition-colors duration-200" aria-label="Follow NPD Building Solutions on Facebook">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
          </div>
        </div>
      </div>
      <div class="border-t border-white/10 pt-8 text-center">
        <p class="text-xs text-gray-500">&copy; 2026 NPD Building Solutions. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script>
  document.querySelectorAll('.email-protect').forEach(function(el){el.innerHTML='npdbuildingsolutions@outlook.com';});
  </script>

</body>
</html>'''


# ---- Dynamic sections ------------------------------------------------------

def business_node():
    return {
        "@type": "LocalBusiness",
        "@id": BUSINESS_ID,
        "name": "NPD Building Solutions",
        "url": f"{DOMAIN}/",
        "description": "Carpentry and renovations business based in Bairnsdale, VIC, with over 10 years of experience. General carpentry, tiling, decks, pergolas, bathroom renovations, fencing, gates and custom work.",
        "telephone": "+61427278285",
        "email": "npdbuildingsolutions@outlook.com",
        "image": f"{DOMAIN}/Assets/optimized/Paynesville%202nd%20floor%20deck%20-%20carport%20in%20conjunction%20with%20cutting-edge%20constructions-800.webp",
        "logo": f"{DOMAIN}/Assets/Logo.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": "Bairnsdale", "addressRegion": "VIC", "addressCountry": "AU"},
        "areaServed": [
            {"@type": "Place", "name": "Bairnsdale"},
            {"@type": "Place", "name": "East Gippsland"},
            {"@type": "Place", "name": "Paynesville"},
            {"@type": "Place", "name": "Lakes Entrance"},
            {"@type": "Place", "name": "Sale"},
        ],
        "serviceType": ["General Carpentry", "High-Quality Tiling", "Decks", "Pergolas", "Custom Work", "Pool Fencing", "Fencing", "Gates", "Bathroom Renovations"],
        "priceRange": "$$",
        "sameAs": ["https://www.facebook.com/profile.php?id=61588392252999"],
    }


def head_jsonld(s):
    url = f"{DOMAIN}/carpentry-{s['slug']}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            business_node(),
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "General Carpentry", "item": f"{DOMAIN}/general-carpentry"},
                    {"@type": "ListItem", "position": 3, "name": f"{s['name']} VIC", "item": url},
                ],
            },
            {
                "@type": "Service",
                "name": f"General Carpentry in {s['name']}",
                "description": f"Structural framing, repairs, interior fit-outs, door and window installation and finishing carpentry in {s['name']}, East Gippsland.",
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


def render_cover_cards(name):
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
    bullets = [s["why_local"]] + SHARED_WHY
    out = []
    for strong, text in bullets:
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
        out.append(f'''        <a href="/carpentry-{slug}" class="inline-block px-5 py-2.5 border border-gray-200 text-sm font-semibold text-gray-700 hover:border-brand hover:text-brand transition-colors duration-200">{esc(name)}</a>''')
    return "\n".join(out)


def render_intro(paras):
    return "\n".join(f'        <p>{esc(p)}</p>' for p in paras)


def page_html(s):
    name = s["name"]
    ename = esc(name)
    slug = s["slug"]
    url = f"{DOMAIN}/carpentry-{slug}"
    title = fit_title(name)
    desc = meta_desc(name)
    keywords = (f"carpenter {name}, carpentry {name} VIC, general carpentry {name}, builder {name}, "
                f"timber repairs {name}, interior fit-outs {name}, East Gippsland carpenter")

    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="apple-touch-icon" href="Assets/Logo.jpg">
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">

  <meta property="og:title" content="Carpenter in {ename} VIC | NPD Building Solutions">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_AU">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="NPD Building Solutions">
  <meta property="og:image" content="{DOMAIN}/{HERO_IMG_URL}-800.webp">
  <meta property="og:image:width" content="800">
  <meta property="og:image:height" content="600">
  <meta property="og:image:alt" content="Carpentry work by NPD Building Solutions in {ename}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Carpenter in {ename} VIC | NPD Building Solutions">
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
        <li><a href="/general-carpentry" class="hover:text-brand transition-colors">General Carpentry</a></li>
        <li class="text-gray-500" aria-hidden="true">/</li>
        <li class="text-brand" aria-current="page">{ename} VIC</li>
      </ol>
    </div>
  </nav>

  <section class="relative pt-32 sm:pt-40 pb-16 sm:pb-20 bg-gray-900 overflow-hidden grain">
    <div class="absolute inset-0">
      <picture><source type="image/webp" srcset="{HERO_IMG_URL}-400.webp 400w, {HERO_IMG_URL}-800.webp 800w, {HERO_IMG_URL}-1600.webp 1600w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 100vw, 1600px"><img src="Assets/Major Project/Interior Renovation - Kitchen and Dining.jpg" alt="Carpentry services in {ename} VIC by NPD Building Solutions" width="4032" height="3024" loading="eager" fetchpriority="high" decoding="sync" class="w-full h-full object-cover opacity-30"></picture>
      <div class="absolute inset-0 bg-gradient-to-b from-gray-900/80 via-gray-900/60 to-gray-900/90"></div>
      <div class="absolute inset-0 bg-brand/5 mix-blend-multiply"></div>
    </div>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="max-w-2xl">
        <p class="inline-flex items-center gap-2 text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">
          {PIN_SVG}
          Carpenter in {ename}, VIC
        </p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-display text-white leading-[0.95] mb-6" style="letter-spacing: -0.03em;">Carpenter in {ename}</h1>
        <p class="text-gray-300 text-base max-w-lg" style="line-height: 1.7;">{esc(s['lead'])}</p>
      </div>
    </div>
  </section>

  <!-- Local Intro -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Local Carpenter</p>
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Your Carpenter in {ename}</h2>
      <div class="space-y-5 text-gray-600" style="line-height: 1.8;">
{render_intro(s['intro'])}
      </div>
    </div>
  </section>

  <!-- What We Cover -->
  <section class="py-20 sm:py-28 bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">What We Cover in {ename}</p>
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">Carpentry for Every Job</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{render_cover_cards(name)}
      </div>
    </div>
  </section>

  <!-- Why Choose Us -->
  <section class="py-20 sm:py-28 bg-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        <div>
          <p class="text-brand font-semibold text-xs tracking-[0.2em] uppercase mb-3">Why {ename} Chooses NPD</p>
          <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-6" style="letter-spacing: -0.03em;">Local Carpentry, Done Properly</h2>
          <ul class="space-y-4">
{render_why(s)}
          </ul>
        </div>
        <div class="relative">
          <div class="overflow-hidden shadow-floating">
            <div class="relative">
              <picture><source type="image/webp" srcset="{WHY_IMG_URL}-400.webp 400w, {WHY_IMG_URL}-800.webp 800w, {WHY_IMG_URL}-1600.webp 1600w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 100vw, 1600px"><img src="Assets/Major Project/Interior Renovation - Open Plan Living.jpg" alt="Finishing carpentry by NPD Building Solutions near {ename}" width="4032" height="3024" loading="lazy" decoding="async" class="w-full h-[350px] sm:h-[420px] object-cover"></picture>
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
        <h2 class="text-3xl sm:text-4xl font-display text-gray-900" style="letter-spacing: -0.03em;">{ename} Carpentry FAQ</h2>
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
      <h2 class="text-3xl sm:text-4xl font-display text-gray-900 mb-8" style="letter-spacing: -0.03em;">Carpentry Nearby</h2>
      <div class="flex flex-wrap justify-center gap-3">
{render_nearby(s['nearby'])}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 sm:py-28 relative overflow-hidden" style="background-color: #E8710A;" aria-label="Call to action">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      <h2 class="text-3xl sm:text-4xl lg:text-5xl font-display text-white mb-6" style="letter-spacing: -0.03em;">Carpentry Project in {ename}?</h2>
      <p class="text-lg text-white/90 mb-10 max-w-xl mx-auto" style="line-height: 1.7;">
        Call for a free quote. We will come out, look at the job, and give you a fair price upfront.
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
    written = []
    warns = []
    for s in SUBURBS:
        html = page_html(s)
        path = os.path.join(ROOT, f"carpentry-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(os.path.basename(path))
        t = fit_title(s["name"])
        d = meta_desc(s["name"])
        if not (50 <= len(t) <= 60):
            warns.append(f"  TITLE {s['slug']}: {len(t)} chars -> {t}")
        if not (150 <= len(d) <= 165):
            warns.append(f"  META  {s['slug']}: {len(d)} chars")
    print(f"Wrote {len(written)} carpentry suburb LPs:")
    for w in written:
        print("  " + w)
    if warns:
        print("\nLength warnings (want title 50-60, meta 150-165):")
        print("\n".join(warns))
    else:
        print("\nAll titles 50-60 and metas 150-165 chars.")


if __name__ == "__main__":
    main()
