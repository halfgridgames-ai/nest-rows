#!/usr/bin/env python3
"""Draws the Nest Rows icon (a coral owl on a leafy branch of a bare brown tree, with an owlet
peeking from the hollow, on a night-blue sky) as web/icon-512.png, icon-192.png and
apple-touch-icon.png, plus a 1024x500 Play feature graphic in store/.
Run from the repo root: python3 tools/make-icon.py  (needs Pillow).
Then run python3 android-app/tools/make-icons.py to refresh the Android launcher icons."""
import os, random
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 4  # supersample

NIGHT = (21, 24, 56)
NIGHT_2 = (31, 35, 82)
INK = (12, 12, 36)
BARK = (122, 78, 46)
BARK_DARK = (84, 52, 30)
HOLLOW = (34, 20, 14)
LEAF = (95, 143, 78)
LEAF_DARK = (63, 102, 51)
CORAL = (255, 106, 77)
CORAL_DEEP = (201, 69, 44)
CREAM = (246, 238, 219)
SUN = (244, 185, 66)


def ell(d, cx, cy, rx, ry, **kw):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), **kw)


def owl(d, cx, cy, u):
    """A round coral owl standing with its feet at (cx, cy); u is 1% of the picture height."""
    w, h = 15 * u, 17 * u
    top = cy - 2 * h
    # ear tufts
    d.polygon([(cx - w * 0.95, top + 5 * u), (cx - w * 0.85, top - 6 * u), (cx - w * 0.35, top + 3 * u)], fill=CORAL_DEEP)
    d.polygon([(cx + w * 0.95, top + 5 * u), (cx + w * 0.85, top - 6 * u), (cx + w * 0.35, top + 3 * u)], fill=CORAL_DEEP)
    # body: ink shadow offset (riso misregistration), then the coral body
    ell(d, cx + 1.4 * u, cy - h + 1.4 * u, w, h, fill=INK)
    ell(d, cx, cy - h, w, h, fill=CORAL)
    # wings
    ell(d, cx - w * 0.92, cy - h * 0.85, w * 0.28, h * 0.55, fill=CORAL_DEEP)
    ell(d, cx + w * 0.92, cy - h * 0.85, w * 0.28, h * 0.55, fill=CORAL_DEEP)
    # belly with feather marks
    ell(d, cx, cy - h * 0.62, w * 0.58, h * 0.55, fill=(255, 168, 140))
    for dx, dy in [(-3, -9), (3, -9), (0, -5), (-4, -3.5), (4, -3.5)]:
        d.arc((cx + dx * u - 1.6 * u, cy + dy * u - 1.6 * u, cx + dx * u + 1.6 * u, cy + dy * u + 1.6 * u), 20, 160, fill=CORAL_DEEP, width=max(2, int(0.8 * u)))
    # eyes
    ey = cy - h * 1.42
    for sx in (-1, 1):
        ex = cx + sx * w * 0.42
        ell(d, ex, ey, 6 * u, 6 * u, fill=CREAM)
        ell(d, ex + sx * 0.6 * u, ey + 0.4 * u, 3.1 * u, 3.1 * u, fill=INK)
        ell(d, ex + sx * 0.6 * u - 1 * u, ey - 0.8 * u, 1 * u, 1 * u, fill=CREAM)
    # beak
    d.polygon([(cx - 2.2 * u, ey + 3 * u), (cx + 2.2 * u, ey + 3 * u), (cx, ey + 7 * u)], fill=SUN)
    # feet
    for sx in (-1, 1):
        ell(d, cx + sx * 4.5 * u, cy, 2.6 * u, 1.4 * u, fill=SUN)


LEAF_SPOTS = [(-5, -3, 5.5), (2, -6, 6), (7, -1, 5.5), (0, 2, 5.5), (-6, 3, 4.5), (6, 5, 4.5)]


def leaves(d, cx, cy, u):
    for col, off in ((LEAF_DARK, 1), (LEAF, 0)):
        for dx, dy, r in LEAF_SPOTS:
            ell(d, cx + dx * u + off * u, cy + dy * u + off * u, r * u, r * 0.8 * u, fill=col)


def tree(d, x, base, u, height=78, owl_on=True):
    """Bare tree whose trunk centre is x and foot is base, with an owlet in the hollow and
    one branch to the right that ends in a leaf spray."""
    tw = 9 * u
    top = base - height * u
    # trunk (tapers upward) with a darker right edge
    d.polygon([(x - tw, base), (x + tw, base), (x + tw * 0.55, top), (x - tw * 0.55, top)], fill=BARK)
    d.polygon([(x + tw * 0.35, base), (x + tw, base), (x + tw * 0.55, top), (x + tw * 0.2, top)], fill=BARK_DARK)
    # two bare twigs at the top
    d.line([(x - 2 * u, top + 6 * u), (x - 14 * u, top - 6 * u)], fill=BARK, width=int(4 * u))
    d.line([(x + 2 * u, top + 4 * u), (x + 10 * u, top - 8 * u)], fill=BARK, width=int(3.4 * u))
    # hollow, with an owlet's eyes
    hy = top + height * u * 0.62
    ell(d, x, hy, 5.2 * u, 7 * u, fill=HOLLOW)
    for sx in (-1, 1):
        ell(d, x + sx * 2.1 * u, hy - 1 * u, 1.7 * u, 1.7 * u, fill=SUN)
        ell(d, x + sx * 2.1 * u, hy - 0.8 * u, 0.7 * u, 0.7 * u, fill=INK)
    # branch to the right, ending in a leaf spray
    by = top + height * u * 0.30
    bend = x + 50 * u
    d.line([(x, by + 4 * u), (bend, by - 2 * u)], fill=BARK_DARK, width=int(6 * u))
    d.line([(x, by + 3 * u), (bend, by - 3 * u)], fill=BARK, width=int(5 * u))
    leaves(d, bend + 3 * u, by - 4 * u, u)
    if owl_on:
        owl(d, x + 30 * u, by - 1.2 * u, u)


def stars(d, W, H, u, n, seed, ymax, keep_out=None):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y, r = rnd.random() * W, rnd.random() * H * ymax, (0.5 + rnd.random() * 0.7) * u
        if keep_out and keep_out[0] < x < keep_out[2] and keep_out[1] < y < keep_out[3]:
            continue
        ell(d, x, y, r, r, fill=CREAM)


def icon(size):
    big = size * S
    u = big / 100
    img = Image.new('RGBA', (big, big), NIGHT + (255,))
    d = ImageDraw.Draw(img)
    # a lighter glow low in the sky, a crescent moon and a few stars
    ell(d, 50 * u, 110 * u, 80 * u, 70 * u, fill=NIGHT_2)
    ell(d, 86 * u, 16 * u, 7 * u, 7 * u, fill=SUN)
    ell(d, 89 * u, 13.5 * u, 6.2 * u, 6.2 * u, fill=NIGHT)
    stars(d, big, big, u, 10, seed=7, ymax=0.45)
    tree(d, 28 * u, 104 * u, u, height=74)
    return img.resize((size, size), Image.LANCZOS)


def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def feature():
    W, H = 1024 * 2, 500 * 2
    u = H / 100
    img = Image.new('RGB', (W, H), NIGHT)
    d = ImageDraw.Draw(img)
    ell(d, W * 0.5, H * 1.35, W * 0.75, H * 0.75, fill=NIGHT_2)
    ell(d, W * 0.93, 16 * u, 9 * u, 9 * u, fill=SUN)
    ell(d, W * 0.93 + 4 * u, 13 * u, 8 * u, 8 * u, fill=NIGHT)
    stars(d, W, H, u, 40, seed=3, ymax=0.6, keep_out=(0, 22 * u, W * 0.52, 70 * u))
    # trees across the right of the scene, each with an owl on its branch
    tree(d, W * 0.55, H + 2 * u, u * 0.95, height=88)
    tree(d, W * 0.80, H + 2 * u, u * 0.72, height=80)
    d.rectangle((0, H - 5 * u, W, H), fill=(14, 16, 40))
    f = font(['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'], int(16 * u))
    f2 = font(['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'], int(5.6 * u))
    tx, ty = W * 0.05, 26 * u
    d.text((tx + 1.2 * u, ty + 1.2 * u), 'Nest Rows', fill=INK, font=f)
    d.text((tx, ty), 'Nest Rows', fill=CORAL, font=f)
    d.text((tx + 0.6 * u, ty + 24 * u), 'One owl for every nest.', fill=CREAM, font=f2)
    d.text((tx + 0.6 * u, ty + 32 * u), 'No two owls touching.', fill=(190, 196, 230), font=f2)
    return img.resize((W // 2, H // 2), Image.LANCZOS)


os.makedirs(os.path.join(ROOT, 'web'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'store'), exist_ok=True)
icon(512).save(os.path.join(ROOT, 'web', 'icon-512.png'))
icon(192).save(os.path.join(ROOT, 'web', 'icon-192.png'))
icon(180).convert('RGB').save(os.path.join(ROOT, 'web', 'apple-touch-icon.png'))
feature().save(os.path.join(ROOT, 'store', 'feature-graphic-1024x500.png'))
print('icons written')
