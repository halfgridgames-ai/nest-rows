# Nest Rows

An owl-placement logic puzzle by Half Grid Games. Every nest hollow wants exactly one owl on a branch beside it, owls never touch (not even diagonally), and the numbers on the edges say how many owls sit in each row and column.

65 levels in 4 woods (Saplings: 3x3 to 5x5 with tips, Hollow Grove: 6x6, Moonfall Pines: 7x7, Old Oak: 8x8), plus the Daily Roost, a new 7x7 board every day with a streak to keep. Every level has one solution that pure deduction reaches, and a hint makes the next deduction and says why. The art is a risograph print at night: misregistered inks, coral owls, bare trees and fireflies. The game ships no image or audio files.

- `index.html`: the whole game, one file. Open it in a browser to play.
- `build-web.py`: builds the installable web version into `web/` (GitHub Pages publishes it on every push to `main`).
- `android-app/`: the Android app (Capacitor 8), built by GitHub Actions. See `android-app/README.md` for signing and release steps.
- `privacy.html`: the privacy policy, published at `/privacy.html` on the Pages site.
- `store/`: Play Store listing text, the feature graphic and phone screenshots.
- `tools/make-icon.py`: redraws the icon and feature graphic (then run `android-app/tools/make-icons.py` for the launcher icons).

Hints are not free: each one costs a short rewarded ad, or comes from a bought hint pack. Ads use Google's test ids and purchases are free test purchases until the real ids are swapped in (see `android-app/README.md`, "Before launch"). In-app products: `remove_ads`, `hints_10`, `hints_40`, `feather_pack`.
