# Verification record

## Completed

- Built and inspected both sites in the Codex in-app browser.
- Desktop layouts inspected at 1280 × 800 and 1440 × 1000.
- Mobile compositions inspected at 390 × 844.
- DOM bounds checked at widths 375, 390, 768, 1024 and 1440. Document width matched viewport width. No out-of-bounds headings, paragraphs, inputs, buttons or headers were found.
- Six intermediate desktop captures for the chamber and six for the folding atlas. Coordinate and transform records accompany the PNGs in `lab`.
- Hero, middle sections, interactive elements, and endings were inspected. Original image and local font loads succeeded. Browser error and warning logs were empty in the checked sessions.
- Both mobile navigation menus opened and their links reached the intended sections.
- Suara question disclosures opened correctly, including the Majority explanation.
- The Observatory renders exactly 222 points. The Majority control produces 112 highlighted points and 110 remaining points, confirmed by computed fill counts after the transition.
- Both forms returned correct single and ambiguous results. `06050` returns Kubang Pasu, P.006. `06650` returns Kuala Kedah, P.010, and Baling, P.016. A malformed postcode and `99999` produced the intended explanatory messages.
- Result URLs were checked against the production app's encoder in `frontend/public/lib.js`. The P.006 destination loaded the production map shell. The external app was still loading its data during that observation, so the final external detail panel is not claimed as verified.
- Pause motion was tested on both sites. Text remained readable, the chamber resolved, and the extra pinned scroll height collapsed. System `prefers-reduced-motion` handling is implemented; the OS preference itself was not changed for this test.
- Core color pairs were checked numerically. Cobalt body text on Suara's coral closing area is 4.55:1; the atlas text is 4.85:1. Observatory muted body text is 8.69:1 on its dark ground. The secondary chamber heading is 3.85:1 and is large display text.
- `.venv/bin/pytest -q`: 657 passed, 9 deselected. The first sandboxed run failed its local-server bind test; the rerun with local-server permission passed.
- `.venv/bin/ruff check`: passed.
- `.venv/bin/mypy`: passed, 37 source files.
- `node --check` passed for all three custom JavaScript files.

## Corrections made during review

- Reduced atlas fold angle and bounded panel height after an early fold extended into the heading area.
- Changed the phone skyline crop so both Petronas towers remain visible.
- Corrected Seat result links to match the production hash route.
- Shortened the collage note after its first version produced an awkward isolated word.

## Feel check

Observatory: recognition → curiosity → clarity → confidence → agency. The chamber is the main visual change. Its final short hold leaves time to read and use the Majority control.

Suara: belonging → curiosity → discovery → understanding → agency. The folding atlas is the main spatial change. It opens fully before leaving the viewport. The final coral search area resolves the story with a useful action.

The initial atlas fold felt cramped. Reducing the fold and fixing the panel height restored the intended calm discovery. The mobile map stack keeps the same reading order without a long pin.

## Limits

These are browser-verified static editions. They have not been tested on a physical iPhone or Android phone. No claim is made about winning or qualifying for a particular award. The supplied generated images are decorative concept artwork, not documentary evidence. The local postcode snapshot is deliberately incomplete and reports missing matches.

## Public deployment — 9 September 2026

- Published both editions at https://politikku-design-editions.ilhamkassim2003.workers.dev/ using Cloudflare static assets, separate from the production site.
- Deployment version: `ad8a9c5f-e1a0-4f21-9e4c-c8496eeb6c99`.
- Public comparison page, Observatory, and Suara loaded in the browser. Public screenshot review returned HTTP 200.
- Final repository checks: 666 tests passed, 9 deselected; Ruff passed; mypy passed for 37 source files.
