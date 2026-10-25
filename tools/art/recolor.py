import numpy as np, sys, math, random
from PIL import Image, ImageDraw, ImageFilter
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
src = Image.open('coral.png').convert('RGBA'); A = np.asarray(src).astype(float) / 255
rgb, alpha = A[:, :, :3], A[:, :, 3]
hsv = rgb_to_hsv(rgb); H, S, V = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
sat = (S > 0.45) & (alpha > 0.5)
red = sat & ((H < 16) | (H > 340))
orange = sat & (H >= 16) & (H < 31)
def soft(m, r=1.5): return np.asarray(Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(r))).astype(float) / 255
def recolor(mask, hue, s_mul, v_mul, v_add=0):
    out = hsv.copy()
    out[..., 0] = np.where(mask > 0, hue / 360, out[..., 0])
    out[..., 1] = np.clip(np.where(mask > 0, S * s_mul, S), 0, 1)
    out[..., 2] = np.clip(np.where(mask > 0, V * v_mul + v_add, V), 0, 1)
    return out
def save(h, name, extra=None):
    o = hsv_to_rgb(h)
    img = Image.fromarray((np.dstack([o, alpha]) * 255).astype('uint8'), 'RGBA')
    if extra: img = extra(img)
    img.save(name + '.png'); return img
# Tawny: chestnut body, sandy belly
h = recolor(red, 22, 0.75, 0.75); h = recolor(orange, 34, 0.45, 1.05, 0.05) if False else h
h2 = h.copy(); m = orange
h2[..., 0] = np.where(m, 36 / 360, h2[..., 0]); h2[..., 1] = np.where(m, S * 0.42, h2[..., 1]); h2[..., 2] = np.where(m, np.clip(V * 1.05 + 0.08, 0, 1), h2[..., 2])
save(h2, 'tawny')
# Ember: deep crimson body, glowing gold belly, sparks
h = hsv.copy(); h[..., 0] = np.where(red, 356 / 360, h[..., 0]); h[..., 1] = np.where(red, np.clip(S * 1.05, 0, 1), h[..., 1]); h[..., 2] = np.where(red, V * 0.62, h[..., 2])
h[..., 0] = np.where(orange, 40 / 360, h[..., 0]); h[..., 2] = np.where(orange, np.clip(V * 1.15 + 0.05, 0, 1), h[..., 2])
def sparks(img):
    W, Hh = img.size; glow = Image.new('RGBA', (W + 200, Hh + 200), (0, 0, 0, 0))
    pad = Image.new('L', glow.size, 0); pad.paste(img.split()[3], (100, 100)); a = pad.filter(ImageFilter.GaussianBlur(40)); g = Image.new('RGBA', glow.size, (255, 120, 40, 0)); ga = Image.new('L', glow.size, 0); ga.paste(a.point(lambda v: int(v * 0.6)), (0, 0)); g.putalpha(ga)
    base = Image.new('RGBA', glow.size, (0, 0, 0, 0)); base.alpha_composite(g); base.alpha_composite(img, (100, 100))
    d = ImageDraw.Draw(base); random.seed(4)
    for _ in range(26):
        x = random.choice([random.uniform(30, 260), random.uniform(W - 60, W + 170)]); y = random.uniform(60, Hh * 0.8); r = random.uniform(5, 13)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 80, 230)); d.ellipse((x - r * .45, y - r * .45, x + r * .45, y + r * .45), fill=(255, 245, 200, 255))
    return base
save(h, 'ember', sparks)
# Starry: navy body, lighter navy belly, yellow stars on the coloured parts
h = hsv.copy(); h[..., 0] = np.where(red, 228 / 360, h[..., 0]); h[..., 1] = np.where(red, 0.6, h[..., 1]); h[..., 2] = np.where(red, V * 0.45 + 0.06, h[..., 2])
h[..., 0] = np.where(orange, 232 / 360, h[..., 0]); h[..., 1] = np.where(orange, 0.45, h[..., 1]); h[..., 2] = np.where(orange, V * 0.45 + 0.14, h[..., 2])
body = red | orange
def stars(img):
    d = ImageDraw.Draw(img); random.seed(7); ys, xs = np.where(body & (np.arange(body.shape[0])[:, None] > body.shape[0] * 0.42)); n = 0; placed = []
    while n < 34:
        i = random.randrange(len(xs)); x, y = xs[i], ys[i]
        if any((x - px) ** 2 + (y - py) ** 2 < 75 ** 2 for px, py in placed): continue
        r = random.uniform(10, 22); pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
            pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
        d.polygon(pts, fill=(244, 185, 66, 255)); placed.append((x, y)); n += 1
    return img
save(h, 'starry-new', stars)

