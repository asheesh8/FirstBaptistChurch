# Sanctuary

A concept identity and site redesign for **First Congregational Church of St. Albans, Vermont** — a 133-year-old Richardsonian Romanesque church on Church Street, facing Taylor Park.

> **Unofficial.** This is a self-directed design concept. It is not commissioned, endorsed by, or affiliated with the church. All photographs and quoted text belong to First Congregational Church and were taken from their public website.

Note: the repository is named `FirstBaptistChurch`, but the subject is First **Congregational** Church (United Church of Christ) — a different denomination. The name is a holdover.

---

**Live:** https://first-baptist-church-virid.vercel.app — Vercel serves the two built HTML files as-is; there is no server code and no environment variables.

## Output

| File | What it is |
|---|---|
| `index.html` | The site — seven pages, hash-routed, single self-contained file |
| `brand.html` | The identity board — mark, palette, type, components, motion plan |

Both are single files with fonts and photographs inlined as base64. They open directly in a browser with no server, no build step, and no network access.

## Build

```
python3 build.py
```

Regenerates `index.html` and `brand.html` from `src/` plus `assets/`. No dependencies beyond the standard library.

The build enforces two invariants that are easy to break by hand:

- **No unreplaced placeholders.** Fails loudly rather than shipping a literal `__ORGAN__` into the page.
- **Output must be pure ASCII.** These pages are published as Artifacts, where the host generates `<head>` and the page cannot declare its own charset. Non-ASCII must be an HTML entity or a `\u` escape, or em dashes render as `â€"`.

It also rewrites `fill="var(--x)"` on SVG elements to `style="fill:var(--x)"`, because CSS custom properties are not reliable inside SVG *presentation* attributes.

---

## The direction

The brief started at "make it like Duolingo." Two things argued against copying that directly:

**Megachurch design is downstream of a media machine.** Elevation and Life.Church lead with dark mode, video, and sermons-first navigation because they have production teams and a band. This church has a choir that runs September to mid-June and an 1893 tracker organ. Copying that layout produces permanently empty content slots.

**A cartoon mascot on a 133-year-old church reads as trying too hard**, and alienates the congregation that funds the building.

What Duolingo *did* solve is worth stealing: making an intimidating first step feel safe. First-time visitors are genuinely anxious — what to wear, where to park, whether they'll be singled out. So the psychology carries over; the costume does not.

### Three things the research turned up

1. **Their best line is on Facebook, not their website.** The site opens with UCC boilerplate used by thousands of congregations. Their Facebook bio says *"a welcoming community of seekers, believers, and doubters."* "Doubters" is the word no church puts on its front door — and it became the headline.

2. **They play 90s pop songs on the 1893 organ.** An instrument an organ company called the finest of its kind in New England, treated with affection rather than reverence. That is the brand's sense of humour, and it already exists.

3. **The building is the logo.** A clock tower that has chimed over Taylor Park since 1893, which changes with the seasons — a living visual system at zero production cost. No mascot required.

### Colour

Sampled from the church's own photographs rather than invented, so the site and the room agree.

| | | |
|---|---|---|
| `#6F1322` Sanctuary Crimson — the chancel carpet | `#8B5A36` Pew Oak | `#D8D0BD` Plaster |
| `#3E6FA8` Winter Sky — the February exterior | `#C89B5A` Lamplight | `#2A1712` Timber |

Most heritage institutions default to a warm cream ground with a terracotta accent. Pairing this crimson against a cool **Winter Sky** blue — taken from their best photograph — is what keeps it from looking like every other church site.

### Type

**Fraunces** for the voice of the church: an old-style serif with a slight wobble, warm and a little imperfect, like a building that has settled for 133 years. **Figtree** for anything a person has to *use* — navigation, service times, buttons. Both open-licence and embedded, so nothing depends on an external font service.

### The arch

The building is Richardsonian Romanesque, and its defining feature is the round arch. So containers are capped with a true semicircle rather than the usual rounded rectangle — one rule, `border-radius: 9999px 9999px 0 0`, used throughout. It gives the warmth that made the Duolingo reference appealing, drawn from this church's own masonry.

---

## Notable pieces

**Seasonal hero.** Picks spring/summer/autumn/winter from the current date, with a manual override in the top bar (clock icon = automatic). Changing season also swaps the hero copy — winter reads "Christmas Eve · Everyone welcome."

**Vermont map.** Hand-drawn SVG: the state outline draws itself on arrival, Lake Champlain along the western edge, a ridge line for the Greens, and four towns with drive times. Hovering a town highlights it on the map *and* in the list, in both directions, and it is fully keyboard-navigable.

Deliberately **not** generated video — a clip can't be hovered, tabbed through, or restyled to match the palette, and would cost several MB where a vector costs kilobytes and stays sharp at any zoom.

**Choose your pew.** Free, no account. Solves the most common first-visit anxiety — *where do I sit, and will I be in someone's seat?* — and incidentally tells the office how much coffee to make.

**Giving is mocked.** Clearly labelled, no form fields, no inputs. Nothing on the page could be mistaken for collecting money.

The site commits to a single warm palette rather than following the viewer's system theme — the plaster, crimson and oak of the actual room, painted explicitly so the page holds on any host background. All motion respects `prefers-reduced-motion`.

---

## Found on the current site

Worth fixing regardless of whether any of this design ships:

- **The `<title>` tag is empty** — every browser tab and search result is blank. Highest-value fix on the list.
- **Weekly bulletins are `.docx` → PDF embeds** — their most frequent content, effectively unreadable on a phone.
- **Two different music directors** — the staff page says Bailey Brown, the music page says to contact Erin Grainger.
- **The sanctuary seats 350, or 380** — both numbers appear across three pages.
- **"This slideshow requires JavaScript"** printed on the Building Use page, where the wedding photographs should be.
- **The history page is four PDF links** — the clock, the windows and the organ are the most interesting things they own.

## Known gaps

- **No autumn photograph exists.** Their library has winter, spring and summer only. The autumn slot currently uses an overcast spring exterior as a stand-in, and it matters because autumn is when their concert series runs.
- Content is a snapshot taken 18 August 2026.
- The giving flow is presentational only.

---

## Layout

```
build.py              reproducible build
index.html            built site
brand.html            built identity board
src/                  templates with __PLACEHOLDER__ tokens
assets/fonts/         Fraunces + Figtree (SIL Open Font License)
assets/site/          images used by the site build
assets/brand/         images used by the brand board
research/photos/      58 photographs recovered from the current site
research/content.json text of all 10 pages and 100 bulletin posts
research/images.json  source URLs for every image
```
