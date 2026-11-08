"""ピン画像（1000x1500）を作る。
使い方: python3 tools/make_pin.py <slug> "<見出し1行目>" "<見出し2行目>" "<サブ見出し>" "<カテゴリ>"
出力: pins/<slug>.png
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 1500
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
SANS_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NIGHT_TOP, NIGHT_BOT = (45, 59, 110), (18, 24, 46)
INK, MUTED, GLOW, PAPER = (239, 233, 220), (185, 191, 214), (243, 199, 122), (246, 227, 184)


FALLBACK = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"  # Noto CJKが無い環境用


def font(path, size):
    if not os.path.exists(path):
        path = FALLBACK
    return ImageFont.truetype(path, size, index=0)  # index 0 = 日本語(JP)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def make(slug, line1, line2, sub, cat):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):  # 夜空のグラデーション
        t = y / H
        c = tuple(int(NIGHT_TOP[i] * (1 - t) + NIGHT_BOT[i] * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # 星は画像の下半分（見出しと重ならない位置）に置く
    for (x, y, r) in [(110, 880, 3), (300, 960, 2), (190, 1060, 3), (420, 1120, 2), (90, 1200, 2), (380, 800, 2), (950, 1050, 3)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))

    # 窓（アーチ）と月：下半分に配置して見出しと重ならないようにする
    wx0, wx1, wy0, wy1 = 500, 900, 700, 1230
    r = (wx1 - wx0) // 2
    d.rectangle([wx0, wy0 + r, wx1, wy1], fill=(26, 34, 66))
    d.pieslice([wx0, wy0, wx1, wy0 + 2 * r], 180, 360, fill=(26, 34, 66))
    d.arc([wx0, wy0, wx1, wy0 + 2 * r], 180, 360, fill=GLOW, width=4)
    d.line([(wx0, wy0 + r), (wx0, wy1)], fill=GLOW, width=4)
    d.line([(wx1, wy0 + r), (wx1, wy1)], fill=GLOW, width=4)
    cx = (wx0 + wx1) // 2
    d.line([(cx, wy0 + 4), (cx, wy1)], fill=(120, 110, 90), width=3)
    d.line([(wx0, wy0 + r + 120), (wx1, wy0 + r + 120)], fill=(120, 110, 90), width=3)
    d.ellipse([740, 770, 830, 860], fill=PAPER)
    d.ellipse([762, 756, 852, 846], fill=(26, 34, 66))
    for (x, y) in [(580, 860), (640, 980), (820, 1000)]:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))
    d.rounded_rectangle([470, 1228, 930, 1248], radius=6, fill=(59, 48, 72))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([820, 1090, 1000, 1270], fill=(243, 199, 122, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img)
    d.polygon([(895, 1180), (935, 1180), (925, 1145), (905, 1145)], fill=GLOW)
    d.rectangle([913, 1180, 917, 1228], fill=(201, 161, 90))

    # PR（右上・大きく）
    fpr = font(SANS_B, 52)
    d.rounded_rectangle([830, 50, 950, 130], radius=14, fill=GLOW)
    d.text((890, 90), "PR", font=fpr, fill=(24, 32, 58), anchor="mm")

    # カテゴリ・見出し
    d.text((70, 120), cat, font=font(SANS_B, 34), fill=GLOW)
    ft = font(SERIF, 104)
    y = 190
    for line in [line1, line2]:
        if not line:
            continue
        size = 104
        while text_w(d, line, font(SERIF, size)) > 860 and size > 60:
            size -= 4
        d.text((70, y), line, font=font(SERIF, size), fill=INK)
        y += size + 40
    size = 40
    while text_w(d, sub, font(SANS, size)) > 860 and size > 28:
        size -= 2
    d.text((70, y + 10), sub, font=font(SANS, size), fill=MUTED)

    # 下部
    d.line([(70, 1330), (930, 1330)], fill=(80, 90, 130), width=2)
    d.text((70, 1360), "パーソナル睡眠アドバイザーが選び方を解説", font=font(SANS, 34), fill=INK)
    d.text((70, 1415), "睡眠の小部屋", font=font(SERIF, 34), fill=GLOW)

    os.makedirs("pins", exist_ok=True)
    out = f"pins/{slug}.png"
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    print(make(*sys.argv[1:6]))
