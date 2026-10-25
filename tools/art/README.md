# Owl art pipeline

1. Cut out the Midjourney owls (coral, snowy, moonlit) with rembg (`isnet-general-use` model).
2. `recolor.py` (run next to coral.png) makes tawny, ember and starry-new from the Coral Owl.
3. `poses.py <name> <dx> <dy>` adds the party hat, sunglasses and nightcap for the win poses
   (dx/dy shift the eye positions: ember 100 100, moonlit 0 62, others 0 0) and writes <name>-box.json.
4. The images are resized, saved as WebP data URIs and pasted into OWL_ART in index.html.

Originals live in the project files under games/nest-rows/art/.
