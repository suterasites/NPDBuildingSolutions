# CLAUDE.md - NPD Building Solutions

## Business Context

**Business Name:** NPD Building Solutions
**Phone:** 0427 278 285
**Email:** npdbuildingsolutions@outlook.com
**Location:** Based in Bairnsdale, VIC - servicing Bairnsdale and surrounding areas
**Experience:** 10+ years

### About
- Carpentry and renovations business based in Bairnsdale, VIC, with over 10 years of experience
- Bairnsdale is the primary service area and home base - use this for local SEO targeting (e.g. "carpenter Bairnsdale", "renovations Bairnsdale VIC")
- Positions themselves as an all-round building solution with a focus on high-quality renovations and attention to detail
- Wide service range covering carpentry, tiling, decks, pergolas, custom work, fencing, gates, and bathroom renovations
- Bathroom renovation work is a standout - completed 16 quality bathrooms in 14 months working alongside Cutting Edge Constructions, showing solid volume and an established builder relationship
- Strong word-of-mouth reputation built over 10+ years in the area, now building out digital presence
- Tone is friendly and approachable ("service with a smile") - fits well for a regional trades business where personal connection matters
- Branding is clean and professional with a black and orange logo
- Contactable via phone, email, or Facebook Messenger

### Services
- General Carpentry
- High-Quality Tiling
- Decks
- Pergolas
- Custom Work
- Pool Fencing
- Fencing
- Gates
- Bathroom Renovations

### Social Media
- **Facebook:** NPD Building Solutions (https://www.facebook.com/profile.php?id=61588392252999) - ~38 followers, no reviews yet. Currently categorised as "Carpenter" - could be broadened to "General contractor" or "Building services" for better discoverability. Most recent post (13 March 2026) showcases bathroom renovation work with photos - real finished work builds trust

### Forms
- **Formspree:** https://formspree.io/f/maqpkepq - used for contact forms on index.html and contact.html

---

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Reference Images
- If a reference image is provided: match layout, spacing, typography, and color exactly. Swap in placeholder content (images via `https://placehold.co/`, generic copy). Do not improve or add to the design.
- If no reference image: design from scratch with high craft (see guardrails below).
- Screenshot your output, compare against reference, fix mismatches, re-screenshot. Do at least 2 comparison rounds. Stop only when no visible differences remain or user says so.

## Local Server
- **Always serve on localhost** - never screenshot a `file:///` URL.
- Start the dev server: `node serve.mjs` (serves the project root at `http://localhost:3000`)
- `serve.mjs` lives in the project root. Start it in the background before taking any screenshots.
- If the server is already running, do not start a second instance.

## Screenshot Workflow
- Puppeteer is installed at `C:/Users/nateh/AppData/Local/Temp/puppeteer-test/`. Chrome cache is at `C:/Users/nateh/.cache/puppeteer/`.
- **Always screenshot from localhost:** `node screenshot.mjs http://localhost:3000`
- Screenshots are saved automatically to `./temporary screenshots/screenshot-N.png` (auto-incremented, never overwritten).
- Optional label suffix: `node screenshot.mjs http://localhost:3000 label` → saves as `screenshot-N-label.png`
- `screenshot.mjs` lives in the project root. Use it as-is.
- After screenshotting, read the PNG from `temporary screenshots/` with the Read tool - Claude can see and analyze the image directly.
- When comparing, be specific: "heading is 32px but reference shows ~24px", "card gap is 16px but should be 24px"
- Check: spacing/padding, font size/weight/line-height, colors (exact hex), alignment, border-radius, shadows, image sizing

## Output Defaults
- Single `index.html` file, all styles inline, unless user says otherwise
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Placeholder images: `https://placehold.co/WIDTHxHEIGHT`
- Mobile-first responsive

## Brand Assets
- Always check the `brand_assets/` folder before designing. It may contain logos, color guides, style guides, or images.
- If assets exist there, use them. Do not use placeholders where real assets are available.
- If a logo is present, use it. If a color palette is defined, use those exact values - do not invent brand colors.

## Anti-Generic Guardrails
- **Colors:** Never use default Tailwind palette (indigo-500, blue-600, etc.). Pick a custom brand color and derive from it.
- **Shadows:** Never use flat `shadow-md`. Use layered, color-tinted shadows with low opacity.
- **Typography:** Never use the same font for headings and body. Pair a display/serif with a clean sans. Apply tight tracking (`-0.03em`) on large headings, generous line-height (`1.7`) on body.
- **Gradients:** Layer multiple radial gradients. Add grain/texture via SVG noise filter for depth.
- **Animations:** Only animate `transform` and `opacity`. Never `transition-all`. Use spring-style easing.
- **Interactive states:** Every clickable element needs hover, focus-visible, and active states. No exceptions.
- **Images:** Add a gradient overlay (`bg-gradient-to-t from-black/60`) and a color treatment layer with `mix-blend-multiply`.
- **Spacing:** Use intentional, consistent spacing tokens - not random Tailwind steps.
- **Depth:** Surfaces should have a layering system (base → elevated → floating), not all sit at the same z-plane.

## Deployment
- **Always deploy changes to GitHub and Vercel** after making code changes.
- Git remote: `origin` (check with `git remote -v` for current URL)
- Push to `main` branch, then deploy to Vercel with `vercel --prod --yes`.

## Multi-Page Consistency
- **Navbar:** The navbar must be identical across all pages. If the navbar is modified on any page, apply the same change to every other page immediately.
- **Footer:** The footer must be identical across all pages. If the footer is modified on any page, apply the same change to every other page immediately.
- **Internal links:** All text links that reference a page on the site must link to the correct page URL. When a new page is created, scan all existing pages and update any mentions of that topic to link to the new page.

## Hard Rules
- Do not add sections, features, or content not in the reference
- Do not "improve" a reference design - match it
- Do not stop after one screenshot pass
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo as primary color
- Do not use em dashes (—) anywhere in content, code, or comments. Use hyphens (-), commas, or periods instead
