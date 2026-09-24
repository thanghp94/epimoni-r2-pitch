# Epimoni MicroQuest — R2 Pitch Deck Handoff (v7)

## Typography (v7)
One scale for everything under 17px, applied to CSS **and** inline styles:
`13px` micro labels (section tag, counter, captions) · `14px` card kickers / table heads ·
`15px` chips / small captions · `16px` list text / chat bubbles · `17px` body text.
All slide headlines are 56px (the stylesheet default). Minimum on-screen size is now 13px.

An automated fit check measures every slide's `scrollHeight` at 1280×720 — it must be ≤ 720.
Re-run it after any content or type change:
```js
// inject before </body>, then read <title> from --dump-dom
const sl=[...document.querySelectorAll('.slide')];
sl.forEach((x,i)=>{const c=x.className;x.classList.add('active');
  out.push((i+1)+':'+x.scrollHeight);x.className=c;});
```
Current: all 16 slides report 720 (no overflow).

## Live
- **Deck (v7, current):** https://epimoni-r2-pitch.vercel.app
- **All versions:** https://epimoni-r2-pitch.vercel.app/versions.html
- **Rehearsal script:** https://epimoni-r2-pitch.vercel.app/pitch-script.md
- Named files: `/epimoni-round2-pitch-v2.html` … `-v6.html` · Repo: github.com/thanghp94/epimoni-r2-pitch (push = auto-deploy ~20s)

## What the deck is (v6 structure, v7 type)
Restructured to the **official 13-section VICEE / Israel-Embassy structure**, in natural Grade 7-8 English.

**16 main slides:** S1 Title · S2 Problem 1/2 (Minh + Mom at one table) · S3 Problem 2/2 (paradox 2×2 + research) ·
S4 Solution 1/2 (5-min quests) · S5 Solution 2/2 (two-window demo, SCIENCE/MATH tabs) ·
S6 Market Opportunity (app sizes, "paid for ≠ learned") · S7 Target Market (funnel + 1% capture) ·
S8 Marketing Strategy (student KOLs / parent ambassadors / quest community, $0 ads) ·
S9 Sales Strategy (competition seats, 5-yr founding plan, bundles) · S10 Revenue Streams (199k family plan) ·
S11 Competition (positioning table, plain words) · S12 Client Retention (come-back loop, grade ladder, LTV ≈7M VND) ·
S13 Management Team (4 named roles + mentor + shipped proof + real screenshot) ·
S14 5-Year Forecast (2.4B → 45B VND bar chart) · S15 Capital Needs (<$300 proved → $25k ask, use-of-funds) ·
S16 Exit Strategy + callback close (3 doors + "Mom's phone — 1 app" + QR).

**No appendix** — the deck is exactly 16 slides. (The earlier 16+7 version with the Q&A / evidence / 6R / subjects / pilot / engine / template-map appendix slides is in git history.)

**Script:** 1,080 spoken words ≈ **9:00–9:50** at 110–120 wpm. S16 is the designated compress slide.

## Build
Decks are generated — never hand-edit the HTML.
```
build-v2.py … build-v5.py   # earlier versions
build-v6.py                 # current: v5 → v6 (restructure, new slides, JS re-index, new NOTES)
python3 build-v6.py         # → epimoni-round2-pitch-v6.html
```
`build-v6.py` extracts v5 sections by index, reassembles in the new order, authors 6 new slides, re-indexes `enter[]/leave[]`, rewrites `BEATS`, disables the overview appendix branch, sets the quest-chip range, then swaps in the new `NOTES` + `TRIM` script tables. Dead JS for the removed ring/subject slides is left in place (never called); unused CSS is harmless.

**Q&A prep moved out of the deck** when the appendix was removed — the hostile-question answers live in git history (`build-v6.py` before the "remove appendix" commit) if the team wants them as a separate one-pager.

## Deploy
```
cp epimoni-round2-pitch-v6.html deploy/epimoni-r2-pitch/index.html
cp epimoni-round2-pitch-v6.html deploy/epimoni-r2-pitch/epimoni-round2-pitch-v6.html
cd deploy/epimoni-r2-pitch && git add -A && git commit -m "..." && git push
```

## Verify
- `node --check` on the extracted `<script>`; 23 sections; div balance 443/443; no font < 12px.
- Nav lives in an IIFE — for screenshots dispatch synthetic `ArrowRight` keydowns (not `go()`).
- Headless: `--screenshot --window-size=1280,720 --virtual-time-budget=9000`.

## Controls
Arrows/Space nav · `N`/`S` script dock · `T` timer · `O` overview · `F` fullscreen · `H` hints · Esc closes.

## Open items / honest flags
1. **Numbers are estimates.** Kahoot/Quizizz/IXL/Raz-Kids figures are public claims; Acellus tuition is published; VN edtech ≈$1.1B; forecast and LTV are modelled. All labeled `est.` on-slide.
2. **Sales strategy names Fermat / Geniusstar Vietnam** as example competition partners — say "we sponsor seats, they run the competitions." Not yet agreed with them.
3. **Y1 = 1,000 families with ~$0 marketing** is the weakest number; the honest mix (paying + sponsored seats) should be stated if challenged.
4. **LTV:CAC ~35:1 is too good** — always add "excluding our time".
5. Live product demo link on S16 sits behind Vercel SSO on a different project — the in-deck sim is the fallback.
6. Drive folder for student co-editing still unresolved (service account has no Drive quota).
7. `pitch-script.md` is regenerated from v6 NOTES — keep in sync if scripts change.
