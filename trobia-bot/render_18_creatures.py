"""Genera las 18 nuevas ilustraciones de Trobimons (#31 a #48) en alta resolución (640x640 JPEG)."""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

DST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "trobimons")
os.makedirs(DST_DIR, exist_ok=True)


def make_canvas(c_top, c_bot, glow_col, seed=42):
    rng = random.Random(seed)
    img = Image.new("RGBA", (640, 640))
    px = img.load()
    for y in range(640):
        t = y / 639.0
        r = int(c_top[0] * (1 - t) + c_bot[0] * t)
        g = int(c_top[1] * (1 - t) + c_bot[1] * t)
        b = int(c_top[2] * (1 - t) + c_bot[2] * t)
        for x in range(640):
            px[x, y] = (r, g, b, 255)

    glow = Image.new("RGBA", (640, 640), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((90, 90, 550, 550), fill=(*glow_col, 115))
    gd.ellipse((170, 170, 470, 470), fill=(*glow_col, 175))
    for _ in range(28):
        sx = rng.randint(40, 600)
        sy = rng.randint(40, 600)
        sr = rng.randint(4, 14)
        gd.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=(255, 255, 255, rng.randint(90, 210)))
    glow = glow.filter(ImageFilter.GaussianBlur(32))
    img = Image.alpha_composite(img, glow)

    # Particles
    pd = ImageDraw.Draw(img, "RGBA")
    for _ in range(35):
        sx = rng.randint(30, 610)
        sy = rng.randint(30, 610)
        sr = rng.randint(2, 6)
        pd.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=(*glow_col, 220))
    return img


def draw_eyes(d, x1, y1, x2, y2, col=(255, 245, 130, 255), r=18):
    d.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=col, outline=(255, 255, 255, 255), width=3)
    d.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=col, outline=(255, 255, 255, 255), width=3)
    d.ellipse((x1 - 6, y1 - 8, x1 + 4, y1 + 2), fill=(255, 255, 255, 255))
    d.ellipse((x2 - 6, y2 - 8, x2 + 4, y2 + 2), fill=(255, 255, 255, 255))


SPECS = [
    # 31. salamandrin (Brasa)
    ("salamandrin", (65, 15, 10), (180, 55, 15), (255, 145, 30), "lizard"),
    # 32. vulcanor (Brasa)
    ("vulcanor", (45, 10, 10), (150, 30, 10), (255, 95, 20), "titan_fire"),
    # 33. cangrex (Laguna)
    ("cangrex", (10, 45, 95), (25, 125, 195), (90, 220, 255), "crab"),
    # 34. krakencor (Laguna)
    ("krakencor", (6, 22, 62), (18, 78, 145), (50, 240, 255), "kraken"),
    # 35. espinach (Huerta)
    ("espinach", (15, 55, 25), (45, 135, 55), (130, 255, 95), "cactus"),
    # 36. mandragor (Huerta)
    ("mandragor", (18, 45, 32), (38, 105, 65), (160, 255, 130), "mushroom"),
    # 37. sombrilla (Sombra)
    ("sombrilla", (22, 10, 45), (65, 22, 110), (195, 95, 255), "ghost"),
    # 38. espectrovela (Sombra)
    ("espectrovela", (16, 8, 36), (52, 16, 92), (215, 110, 255), "chandelier"),
    # 39. necrodrac (Sombra)
    ("necrodrac", (10, 4, 24), (45, 10, 75), (255, 55, 145), "dragon_shadow"),
    # 40. astrobot (Astral)
    ("astrobot", (12, 24, 68), (28, 75, 155), (80, 245, 255), "drone"),
    # 41. pulsatron (Astral)
    ("pulsatron", (14, 18, 58), (35, 65, 145), (255, 215, 60), "tesla"),
    # 42. cosmolion (Astral)
    ("cosmolion", (18, 14, 62), (55, 35, 140), (110, 235, 255), "lion"),
    # 43. toporoca (Roca)
    ("toporoca", (48, 32, 18), (110, 72, 38), (255, 190, 75), "mole"),
    # 44. escarabita (Roca)
    ("escarabita", (32, 42, 24), (78, 98, 45), (195, 255, 95), "beetle"),
    # 45. pinguhelado (Escarcha)
    ("pinguhelado", (14, 42, 85), (42, 125, 195), (165, 245, 255), "penguin"),
    # 46. morsartica (Escarcha)
    ("morsartica", (10, 32, 72), (30, 95, 165), (130, 235, 255), "walrus"),
    # 47. nubecilla (Céfiro)
    ("nubecilla", (18, 65, 72), (55, 155, 145), (195, 255, 240), "cloud"),
    # 48. tempestia (Céfiro)
    ("tempestia", (12, 48, 45), (32, 125, 98), (110, 255, 195), "moth"),
]


for idx, (cid, c_top, c_bot, glow_col, shape) in enumerate(SPECS, start=31):
    img = make_canvas(c_top, c_bot, glow_col, seed=idx * 17)
    d = ImageDraw.Draw(img, "RGBA")

    # Halo / Elemental ring behind creature
    d.ellipse((115, 115, 525, 525), outline=(*glow_col, 145), width=6)
    d.ellipse((145, 145, 495, 495), outline=(255, 255, 255, 90), width=3)

    if shape == "lizard":
        # Flame tail & cute salamander body
        d.polygon([(420, 430), (560, 280), (520, 210), (465, 340)], fill=(255, 120, 20, 240), outline=(255, 230, 90, 255))
        d.ellipse((195, 250, 445, 490), fill=(235, 75, 25, 255), outline=(255, 200, 70, 255), width=5)
        d.ellipse((210, 165, 430, 355), fill=(245, 90, 30, 255), outline=(255, 215, 85, 255), width=5)
        for cx in (250, 320, 390):
            d.polygon([(cx - 22, 180), (cx, 110), (cx + 22, 180)], fill=(255, 200, 40, 255))
        draw_eyes(d, 275, 255, 365, 255, (255, 240, 90, 255), 20)

    elif shape == "titan_fire":
        # Magma volcano cannons on back + armored drake
        d.polygon([(140, 280), (220, 110), (290, 260)], fill=(90, 30, 20, 255), outline=(255, 120, 25, 255))
        d.polygon([(500, 280), (420, 110), (350, 260)], fill=(90, 30, 20, 255), outline=(255, 120, 25, 255))
        d.ellipse((135, 220, 505, 520), fill=(70, 24, 18, 255), outline=(255, 140, 30, 255), width=6)
        d.polygon([(210, 175), (320, 125), (430, 175), (400, 360), (240, 360)], fill=(115, 32, 22, 255), outline=(255, 185, 50, 255))
        d.ellipse((260, 380, 380, 480), fill=(255, 140, 20, 245))
        draw_eyes(d, 270, 245, 370, 245, (255, 220, 60, 255), 18)

    elif shape == "crab":
        # Giant water pincers + porcelain shell
        d.ellipse((70, 180, 230, 340), fill=(35, 155, 235, 255), outline=(180, 245, 255, 255), width=5)
        d.ellipse((410, 180, 570, 340), fill=(35, 155, 235, 255), outline=(180, 245, 255, 255), width=5)
        d.ellipse((175, 230, 465, 475), fill=(25, 120, 210, 255), outline=(160, 235, 255, 255), width=6)
        draw_eyes(d, 265, 240, 375, 240, (255, 245, 140, 255), 19)

    elif shape == "kraken":
        # Tentacles + abyssal mantle
        for angle in range(20, 165, 28):
            rad = math.radians(angle)
            tx = 320 + int(math.cos(rad) * 230)
            ty = 340 + int(math.sin(rad) * 200)
            d.line([(320, 360), (tx, ty)], fill=(30, 175, 230, 255), width=26)
        d.polygon([(185, 340), (240, 110), (320, 75), (400, 110), (455, 340)], fill=(20, 95, 175, 255), outline=(90, 245, 255, 255))
        draw_eyes(d, 265, 280, 375, 280, (80, 255, 245, 255), 20)

    elif shape == "cactus":
        # Cute cactus warrior with crown flower
        d.rounded_rectangle((115, 250, 215, 390), radius=40, fill=(45, 175, 75, 255), outline=(170, 255, 140, 255), width=4)
        d.rounded_rectangle((425, 230, 525, 370), radius=40, fill=(45, 175, 75, 255), outline=(170, 255, 140, 255), width=4)
        d.rounded_rectangle((205, 175, 435, 505), radius=95, fill=(38, 160, 68, 255), outline=(180, 255, 140, 255), width=5)
        d.polygon([(275, 175), (300, 105), (320, 135), (340, 105), (365, 175)], fill=(255, 210, 45, 255), outline=(255, 255, 190, 255))
        draw_eyes(d, 275, 290, 365, 290, (255, 230, 75, 255), 18)

    elif shape == "mushroom":
        # Glowing alchemical mushroom cap + nature spirit body
        d.ellipse((215, 280, 425, 515), fill=(235, 225, 195, 255), outline=(140, 245, 150, 255), width=5)
        d.pieslice((110, 110, 530, 430), 180, 360, fill=(40, 165, 95, 255), outline=(165, 255, 175, 255), width=5)
        for cx, cy, cr in [(220, 200, 26), (320, 165, 32), (420, 205, 26), (270, 235, 18), (375, 235, 18)]:
            d.ellipse((cx - cr, cy - cr, cx + cr, cy + cr), fill=(175, 255, 160, 235))
        draw_eyes(d, 275, 355, 365, 355, (90, 255, 140, 255), 18)

    elif shape == "ghost":
        # Cute violet wisp ghost with floating flame
        d.polygon([(180, 480), (205, 220), (320, 150), (435, 220), (460, 480), (390, 435), (320, 490), (250, 435)],
                  fill=(85, 35, 145, 245), outline=(215, 140, 255, 255))
        d.polygon([(290, 150), (320, 70), (350, 150)], fill=(210, 95, 255, 255))
        draw_eyes(d, 270, 285, 370, 285, (255, 90, 190, 255), 20)

    elif shape == "chandelier":
        # Ornate spectral chandelier spirit
        d.line([(140, 310), (500, 310)], fill=(215, 175, 95, 255), width=14)
        for fx in (140, 320, 500):
            d.polygon([(fx - 26, 295), (fx, 185), (fx + 26, 295)], fill=(195, 75, 255, 245), outline=(255, 210, 255, 255))
        d.ellipse((210, 235, 430, 455), fill=(62, 22, 105, 255), outline=(225, 150, 255, 255), width=5)
        draw_eyes(d, 275, 335, 365, 335, (255, 215, 80, 255), 18)

    elif shape == "dragon_shadow":
        # Legendary Eclipse Dragon
        d.polygon([(40, 140), (255, 280), (195, 455), (30, 350)], fill=(55, 15, 95, 240), outline=(245, 90, 195, 255))
        d.polygon([(600, 140), (385, 280), (445, 455), (610, 350)], fill=(55, 15, 95, 240), outline=(245, 90, 195, 255))
        d.polygon([(235, 495), (260, 195), (320, 115), (380, 195), (405, 495)], fill=(35, 12, 65, 255), outline=(255, 110, 210, 255))
        d.ellipse((275, 310, 365, 400), fill=(255, 55, 155, 235), outline=(255, 220, 245, 255), width=3)
        draw_eyes(d, 285, 225, 355, 225, (255, 55, 130, 255), 16)

    elif shape == "drone":
        # Cybernetic spherical drone with plasma ring
        d.ellipse((95, 280, 545, 370), outline=(90, 245, 255, 235), width=8)
        d.ellipse((190, 185, 450, 445), fill=(35, 65, 125, 255), outline=(110, 245, 255, 255), width=6)
        d.line([(320, 185), (320, 95)], fill=(110, 245, 255, 255), width=8)
        d.ellipse((300, 75, 340, 115), fill=(255, 230, 80, 255))
        d.ellipse((265, 260, 375, 370), fill=(0, 245, 255, 255), outline=(255, 255, 255, 255), width=4)

    elif shape == "tesla":
        # Golden Tesla sentinel with twin coils
        for tx in (165, 475):
            d.rounded_rectangle((tx - 35, 160, tx + 35, 440), radius=16, fill=(70, 90, 145, 255), outline=(255, 215, 75, 255), width=4)
            d.ellipse((tx - 45, 115, tx + 45, 205), fill=(255, 220, 70, 245), outline=(255, 255, 255, 255), width=3)
        d.polygon([(220, 210), (320, 150), (420, 210), (395, 470), (245, 470)], fill=(42, 58, 115, 255), outline=(110, 245, 255, 255))
        draw_eyes(d, 275, 275, 365, 275, (100, 250, 255, 255), 18)

    elif shape == "lion":
        # Astral Constellation Lion
        for angle in range(0, 360, 24):
            rad = math.radians(angle)
            x2 = 320 + int(math.cos(rad) * 225)
            y2 = 310 + int(math.sin(rad) * 225)
            d.polygon([(275, 310), (365, 310), (x2, y2)], fill=(65, 145, 255, 195))
        d.ellipse((195, 185, 445, 435), fill=(35, 55, 135, 255), outline=(255, 220, 90, 255), width=5)
        draw_eyes(d, 270, 285, 370, 285, (255, 235, 95, 255), 19)

    elif shape == "mole":
        # Rock excavator mole with crystal helmet
        d.ellipse((175, 235, 465, 510), fill=(115, 78, 48, 255), outline=(235, 180, 95, 255), width=5)
        d.pieslice((185, 145, 455, 345), 180, 360, fill=(245, 190, 55, 255), outline=(255, 240, 160, 255), width=4)
        d.polygon([(295, 145), (320, 75), (345, 145)], fill=(90, 245, 235, 255))
        draw_eyes(d, 270, 305, 370, 305, (255, 220, 90, 255), 17)

    elif shape == "beetle":
        # Jade & gold armored rhino beetle
        d.polygon([(285, 210), (320, 65), (355, 210)], fill=(255, 210, 65, 255), outline=(255, 250, 180, 255))
        d.ellipse((165, 200, 475, 515), fill=(45, 135, 75, 255), outline=(255, 215, 75, 255), width=6)
        d.line([(320, 260), (320, 510)], fill=(255, 215, 75, 255), width=5)
        draw_eyes(d, 260, 245, 380, 245, (255, 230, 80, 255), 17)

    elif shape == "penguin":
        # Polar crystal emperor penguin
        d.ellipse((185, 175, 455, 515), fill=(28, 78, 148, 255), outline=(165, 245, 255, 255), width=5)
        d.ellipse((225, 275, 415, 495), fill=(235, 250, 255, 255))
        d.polygon([(295, 265), (345, 265), (320, 310)], fill=(255, 195, 50, 255))
        draw_eyes(d, 270, 235, 370, 235, (110, 245, 255, 255), 17)

    elif shape == "walrus":
        # Iceberg tusk colossus
        d.ellipse((145, 200, 495, 515), fill=(55, 125, 185, 255), outline=(190, 245, 255, 255), width=6)
        d.polygon([(245, 340), (262, 485), (288, 345)], fill=(215, 250, 255, 255), outline=(255, 255, 255, 255))
        d.polygon([(395, 340), (378, 485), (352, 345)], fill=(215, 250, 255, 255), outline=(255, 255, 255, 255))
        draw_eyes(d, 265, 275, 375, 275, (140, 250, 255, 255), 18)

    elif shape == "cloud":
        # Fluffy wind cloud spirit with golden lightning crown
        for cx, cy, cr in [(220, 340, 85), (420, 340, 85), (260, 260, 90), (380, 260, 90), (320, 320, 105)]:
            d.ellipse((cx - cr, cy - cr, cx + cr, cy + cr), fill=(235, 252, 250, 255), outline=(140, 245, 225, 255), width=3)
        d.polygon([(295, 175), (320, 105), (345, 175)], fill=(255, 220, 70, 255))
        draw_eyes(d, 275, 315, 365, 315, (45, 195, 155, 255), 18)

    elif shape == "moth":
        # Emerald storm moth
        d.polygon([(55, 145), (290, 285), (220, 465), (45, 355)], fill=(45, 205, 150, 235), outline=(215, 255, 235, 255))
        d.polygon([(585, 145), (350, 285), (420, 465), (595, 355)], fill=(45, 205, 150, 235), outline=(215, 255, 235, 255))
        d.ellipse((265, 195, 375, 475), fill=(25, 95, 75, 255), outline=(180, 255, 220, 255), width=5)
        draw_eyes(d, 290, 255, 350, 255, (255, 235, 110, 255), 16)

    out_path = os.path.join(DST_DIR, f"{cid}.jpg")
    img.convert("RGB").save(out_path, "JPEG", quality=92)
    print(f"Rendered #{idx} {cid} -> {out_path}")

print("Total images in assets/trobimons:", len(os.listdir(DST_DIR)))
