import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
NAVY = (21, 24, 56, 255); RED = (196, 52, 30, 255); RING = (238, 165, 52, 255); YEL = (244, 185, 66, 255); CREAM = (246, 238, 219, 255); CORAL = (255, 106, 77, 255); BLUE = (60, 62, 134, 255)
PAD = 520
import sys
NAME, OX, OY = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
EYES = [(350 + OX, 458 + OY), (846 + OX, 458 + OY)]; RR, PR = 150, 108
SRC = Image.open(NAME + '.png').convert('RGBA')
def samp(x, y): return tuple(SRC.getpixel((x, y))[:3]) + (255,)
RING = samp(EYES[0][0] + 128, EYES[0][1]); RED = samp(EYES[0][0] - 175, EYES[0][1] + 120)
def base():
    owl = SRC; W, H = owl.size
    c = Image.new('RGBA', (W + 2 * PAD, H + PAD + 40), (0, 0, 0, 0)); c.alpha_composite(owl, (PAD, PAD)); return c
def P(x, y): return (x + PAD + OX, y + PAD + OY)
def grain(layer, amt=38):
    a = np.asarray(layer).astype(int); n = np.random.RandomState(3).randint(-amt, amt, a.shape[:2])[..., None]
    speck = np.random.RandomState(5).rand(*a.shape[:2]) > 0.985
    rgb = np.clip(a[..., :3] + n, 0, 255); rgb[speck] = rgb[speck] * 0.55
    return Image.fromarray(np.dstack([rgb, a[..., 3]]).astype('uint8'), 'RGBA')
def layer(c): return Image.new('RGBA', c.size, (0, 0, 0, 0))
def poly(d, pts, fill, w=14): d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=NAVY, width=w, joint='curve')
def finish(c, L): c.alpha_composite(grain(L)); return c
def confetti(d, W, H, seed):
    random.seed(seed)
    for _ in range(46):
        x, y = random.uniform(60, W - 60), random.uniform(60, H * 0.55); col = random.choice([CORAL, YEL, CREAM, (95, 143, 78, 255)])
        a = random.uniform(0, math.pi); l = random.uniform(22, 40); w = l * 0.45
        pts = [(x + math.cos(a) * l - math.sin(a) * w, y + math.sin(a) * l + math.cos(a) * w), (x - math.cos(a) * l - math.sin(a) * w, y - math.sin(a) * l + math.cos(a) * w), (x - math.cos(a) * l + math.sin(a) * w, y - math.sin(a) * l - math.cos(a) * w), (x + math.cos(a) * l + math.sin(a) * w, y + math.sin(a) * l - math.cos(a) * w)]
        d.polygon(pts, fill=col)
import json
BOX = {}
def crop(c, key=None):
    a = np.asarray(c)[..., 3] > 20; r = np.where(a.any(1))[0]; q = np.where(a.any(0))[0]
    out = c.crop((q[0], r[0], q[-1] + 1, r[-1] + 1)); W, H = SRC.size
    BOX[key] = [(PAD - q[0]) / out.width, (PAD - r[0]) / out.height, W / out.width, H / out.height]
    return out
# --- cheer: party hat, happy eyes, confetti
c = base(); L = layer(c); d = ImageDraw.Draw(L)
for ex, ey in EYES:
    x, y = (ex + PAD, ey + PAD); d.ellipse((x - PR - 4, y - PR - 4, x + PR + 4, y + PR + 4), fill=RING)
    d.arc((x - 70, y - 30, x + 70, y + 90), 200, 340, fill=NAVY, width=30)
hat = [P(390, 130), P(810, 130), P(620, -470)]
poly(d, hat, CORAL, 16)
for k in range(1, 4):  # stripes
    t = k / 4.0; a, b, ap = hat[0], hat[1], hat[2]
    l = (a[0] + (ap[0] - a[0]) * t, a[1] + (ap[1] - a[1]) * t); r = (b[0] + (ap[0] - b[0]) * t, b[1] + (ap[1] - b[1]) * t)
    t2 = t + 0.11; l2 = (a[0] + (ap[0] - a[0]) * t2, a[1] + (ap[1] - a[1]) * t2); r2 = (b[0] + (ap[0] - b[0]) * t2, b[1] + (ap[1] - b[1]) * t2)
    d.polygon([l, r, r2, l2], fill=YEL)
d.line(hat + [hat[0]], fill=NAVY, width=16, joint='curve')
x, y = hat[2]; d.ellipse((x - 48, y - 48, x + 48, y + 48), fill=YEL, outline=NAVY, width=12)
crop(finish(c, L), 'cheer').save(NAME + '-cheer.png')
# --- cool: sunglasses
c = base(); L = layer(c); d = ImageDraw.Draw(L)
for ex, ey in EYES:
    x, y = (ex + PAD, ey + PAD); d.rounded_rectangle((x - 175, y - 120, x + 175, y + 125), radius=95, fill=NAVY)
    d.line([(x - 95, y - 55), (x - 35, y - 85)], fill=(120, 130, 190, 255), width=22); d.line([(x - 100, y - 10), (x - 70, y - 25)], fill=(120, 130, 190, 255), width=16)
d.line([P(520, 430), P(672, 430)], fill=NAVY, width=34)
d.line([P(176, 420), P(60, 380)], fill=NAVY, width=26); d.line([P(1016, 420), P(1130, 380)], fill=NAVY, width=26)
crop(finish(c, L), 'cool').save(NAME + '-cool.png')
# --- sleepy: half-closed eyes, nightcap, z's
c = base(); L = layer(c); d = ImageDraw.Draw(L)
for ex, ey in EYES:
    x, y = (ex + PAD, ey + PAD); d.pieslice((x - RR - 6, y - RR - 6, x + RR + 6, y + RR + 6), 180, 360, fill=RED)
    d.rectangle((x - RR - 6, y - 4, x + RR + 6, y + 2), fill=RED); d.line([(x - RR + 10, y + 4), (x + RR - 10, y + 4)], fill=NAVY, width=26)
    for k in (-1, 0, 1): d.line([(x + k * 55, y + 18), (x + k * 62, y + 50)], fill=NAVY, width=12)
cap = [P(330, 150), P(900, 150), P(1180, -120), P(1330, 160), P(1250, -260), P(820, -330), P(470, -200)]
d.polygon(cap, fill=BLUE); d.line(cap + [cap[0]], fill=NAVY, width=16, joint='curve')
d.rounded_rectangle(tuple(P(300, 90)) + tuple(P(930, 190)), radius=50, fill=CREAM, outline=NAVY, width=14)
x, y = P(1330, 170); d.ellipse((x - 62, y - 62, x + 62, y + 62), fill=CREAM, outline=NAVY, width=12)
random.seed(2)
for sx, sy in [(560, -190), (720, -250), (880, -170), (1050, -150), (650, -60)]:
    x, y = P(sx, sy); r = 18; d.polygon([(x + (r if k % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + k * math.pi / 5), y + (r if k % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)], fill=YEL)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 150); f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 100)
except Exception: f = f2 = None
crop(finish(c, L), 'sleepy').save(NAME + '-sleepy.png')

json.dump(BOX, open(NAME + '-box.json', 'w'))
