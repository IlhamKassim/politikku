# Asset provenance

- `sans.woff2`: existing repository IBM Plex Sans variable font.
- `serif.woff2`: existing repository Newsreader variable font.
- `grotesk.woff2`: existing repository Space Grotesk font.
- `seat-index.js`: built from `data/postcode_seat_index.json`, preserving all candidate Seat codes and names. Source retrieval date 26 August 2026. The source file documents SPR delimitation data and the MIT-licensed malaysia-postcodes dataset.
- Malaysia map paths: `frontend/public/data/seats-parlimen.json`. Counts derived from these records: Peninsular Malaysia 165, Sarawak 31, Sabah 25, Labuan 1.
- Skyline and street image: original assets generated with the built-in image generation tool for these editions. The original files remain under the user's generated_images directory, with copied project assets under each edition's `assets` folder.
- Scrollcraft runtime: unchanged copies from `tools/scroll-craft/plugins/nateherk-design/skills/scroll-craft/engine`.

## Skyline prompt

Create one photorealistic architectural skyline asset for an original Malaysian civic website. Wide landscape 3:2 composition. Kuala Lumpur skyline with unmistakable Petronas Twin Towers on the right half and KL Tower left, photographed at late blue hour, dark desaturated teal buildings with a few warm window lights, rich realistic architectural detail, atmospheric far buildings. Entire skyline occupies lower 65% of image, towers fully visible with ample margin. Skyline isolated on a genuinely transparent background, with no sky, no text, no logos, no frame. Bottom edge full width layered city buildings fade into near-black teal. Sophisticated tilt-shift architectural photography, restrained natural lighting, no neon glow, no illustration, no cartoon, no toy-like buildings. This is a decorative skyline cutout to be composited over a CSS sky, headline behind parts of the skyline.

## Street prompt

Original editorial documentary photograph for a Malaysian civic field guide website. Wide 3:2 landscape photo of a quiet historic Kuala Lumpur street with warm weathered terracotta and peach shophouses and a traditional kopitiam, green plants and one parked bicycle, with the Petronas Twin Towers rising softly in the far background. Early morning direct tropical sunlight from upper left creates long geometric shadows. A few small candid pedestrians in the middle distance, nobody posing. Beautiful architectural details, textured plaster, ceramic pavement, slightly faded coral, muted teal and cream palette. Shot on 35mm analog film, refined travel magazine editorial, honest lived-in city, no fake stock smiles, no over-saturation. Main street vanishing point slightly right of center, foreground negative space at lower left. No legible signage, text, logos, watermark. This is a standalone decorative photograph, no browser frame, no interface.
