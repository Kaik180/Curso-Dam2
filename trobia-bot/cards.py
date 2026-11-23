"""Motor gráfico (Pillow) para renderizar tarjetas coleccionables, banners de equipo 3v3, arenas VS y perfiles."""
import io
import os
from typing import Optional
import discord
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from data.creatures import (
    CREATURES,
    ELEMENTS,
    MAX_STARS,
    PET_GEAR,
    SCROLL_SKILLS,
    image_path,
    pet_power,
    pet_skills,
    pet_stats,
    pet_xp_needed,
)
from data.items import ITEMS, RARITIES

ELEMENT_COLORS = {
    "brasa":  (255, 105, 45),
    "laguna": (45, 165, 255),
    "huerta": (65, 215, 105),
    "sombra": (175, 85, 255),
    "astral": (65, 235, 255),
    "roca":   (225, 165, 75),
    "hielo":  (125, 225, 255),
    "viento": (85, 235, 185),
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _int_to_rgb(c: int) -> tuple[int, int, int]:
    return ((c >> 16) & 255, (c >> 8) & 255, c & 255)


def _load_creature_art(species_id: str, size: tuple[int, int]) -> Image.Image:
    p = image_path(species_id)
    if os.path.isfile(p):
        try:
            return Image.open(p).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        except Exception:
            pass
    fallback = Image.new("RGBA", size, (40, 45, 65, 255))
    return fallback


def _rounded_image(img: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def _draw_bar(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    ratio: float,
    fill_col: tuple[int, int, int],
    bg_col: tuple[int, int, int, int] = (22, 26, 38, 230),
):
    ratio = max(0.0, min(1.0, float(ratio)))
    r = h // 2
    d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=bg_col, outline=(255, 255, 255, 40), width=1)
    fw = int(w * ratio)
    if fw > 0:
        fw = max(h, fw)
        d.rounded_rectangle((x, y, x + min(w, fw), y + h), radius=r, fill=(*fill_col, 255))


def _fit(text: str, font, max_w: int) -> str:
    """Recorta el texto con '…' para que quepa en max_w píxeles."""
    if font.getlength(text) <= max_w:
        return text
    while text and font.getlength(text + "…") > max_w:
        text = text[:-1]
    return text + "…"


def _draw_stars(d, x: int, y: int, filled: int, total: int = MAX_STARS, size: int = 20, gap: int = 6):
    """Dibuja estrellas vectoriales (no dependen de la fuente)."""
    import math
    for i in range(total):
        cx = x + i * (size * 2 + gap) // 2 + size // 2
        cy = y + size // 2
        pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rr = size / 2 if k % 2 == 0 else size / 4.2
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        if i < filled:
            d.polygon(pts, fill=(255, 205, 50, 255), outline=(255, 245, 160, 255))
        else:
            d.polygon(pts, fill=(40, 46, 66, 255), outline=(110, 120, 150, 255))
    return x + total * (size + gap // 2 + size // 2)


def _to_discord_file(img: Image.Image, filename: str) -> discord.File:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return discord.File(buf, filename=filename)


# =====================================================================
# 1. TARJETA COLECCIONABLE DE TROBIMON (/mascota ver y /trobidex)
# =====================================================================
def render_pet_card(pet: dict, owner_name: Optional[str] = None) -> tuple[discord.File, str]:
    sp = CREATURES[pet["species_id"]]
    rar = RARITIES[sp["rarity"]]
    el = ELEMENTS[sp["element"]]
    el_col = ELEMENT_COLORS.get(sp["element"], (255, 140, 40))
    rar_col = _int_to_rgb(rar["color"])

    W, H = 960, 540
    img = Image.new("RGBA", (W, H), (14, 17, 26, 255))

    # Glow ambiental de fondo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-80, -60, 520, 580), fill=(*el_col, 85))
    gd.ellipse((480, 40, 1020, 560), fill=(*rar_col, 65))
    glow = glow.filter(ImageFilter.GaussianBlur(55))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    # Marco exterior de la carta
    d.rounded_rectangle((12, 12, W - 12, H - 12), radius=26, fill=(20, 24, 36, 215), outline=(*rar_col, 220), width=3)
    d.rounded_rectangle((18, 18, W - 18, H - 18), radius=22, outline=(*el_col, 90), width=1)

    # Panel izquierdo: Ilustración de la criatura
    art_size = (360, 360)
    art = _rounded_image(_load_creature_art(sp["id"], art_size), 22)
    art_x, art_y = 38, 78
    d.rounded_rectangle(
        (art_x - 4, art_y - 4, art_x + art_size[0] + 4, art_y + art_size[1] + 4),
        radius=25,
        fill=(12, 15, 22, 255),
        outline=(*el_col, 230),
        width=3,
    )
    img.paste(art, (art_x, art_y), art)

    # Cabecera sobre el retrato: #ID y Rareza
    f_badge = _font(18, bold=True)
    d.rounded_rectangle((38, 32, 125, 66), radius=12, fill=(*el_col, 230))
    d.text((54, 37), f"#{sp['num']:02d}", font=f_badge, fill=(15, 18, 25, 255))

    d.rounded_rectangle((135, 32, 398, 66), radius=12, fill=(30, 36, 52, 240), outline=(*rar_col, 200), width=2)
    d.text((152, 37), f"{rar['name'].upper()}  •  {el['name'].upper()}", font=f_badge, fill=(*rar_col, 255))

    # Estrellas bajo el retrato
    stars = int(pet.get("stars") or 0)
    d.rounded_rectangle((38, 452, 398, 504), radius=14, fill=(26, 30, 44, 240), outline=(255, 205, 55, 150), width=2)
    d.text((58, 465), "ASCENSIÓN", font=_font(20, bold=True), fill=(255, 215, 65, 255))
    _draw_stars(d, 190, 465, stars, MAX_STARS, size=26, gap=10)

    # Panel derecho: Estadísticas, Pasiva y Habilidades
    rx = 426
    f_title = _font(32, bold=True)
    f_sub = _font(18, bold=False)
    f_sec = _font(17, bold=True)
    f_small = _font(15, bold=False)

    disp_name = pet.get("nickname") or sp["name"]
    d.text((rx, 30), disp_name.upper()[:20], font=f_title, fill=(255, 255, 255, 255))
    lvl = pet.get("level", 1)
    cp = pet_power(pet)

    # Pill de Nivel y CP
    d.rounded_rectangle((W - 225, 32, W - 36, 72), radius=14, fill=(*el_col, 45), outline=(*el_col, 220), width=2)
    d.text((W - 208, 40), f"NV.{lvl}  •  {cp} CP", font=_font(19, bold=True), fill=(255, 235, 140, 255))

    sub_line = f"Especie: {sp['name']}   |   " + (f"Entrenador: {owner_name}" if owner_name else "Ficha de Trobidex")
    d.text((rx, 72), sub_line[:52], font=f_sub, fill=(175, 185, 210, 255))

    # Barras de HP, ATQ y XP
    hp, atk = pet_stats(sp["id"], lvl, pet.get("held_item"), stars)
    xp = pet.get("xp", 0)
    xp_need = max(1, pet_xp_needed(lvl))

    # HP
    d.text((rx, 108), f"VIDA (HP): {hp}", font=f_sec, fill=(105, 245, 150, 255))
    _draw_bar(d, rx + 165, 112, 330, 16, min(1.0, hp / 650.0), (65, 225, 125))
    # ATQ
    d.text((rx, 136), f"ATAQUE: {atk}", font=f_sec, fill=(255, 165, 75, 255))
    _draw_bar(d, rx + 165, 140, 330, 16, min(1.0, atk / 180.0), (255, 145, 55))
    # XP
    d.text((rx, 164), f"EXP: {xp}/{xp_need}", font=f_sec, fill=(110, 215, 255, 255))
    _draw_bar(d, rx + 165, 168, 330, 16, xp / xp_need, (75, 195, 255))

    # Caja de Pasiva + Objeto Equipado
    pas = sp.get("passive", {})
    held_id = pet.get("held_item")
    held_name = ITEMS[held_id]["name"] if held_id and held_id in ITEMS else "Ninguno"
    box_w = W - 36 - rx
    d.rounded_rectangle((rx, 196, W - 36, 256), radius=14, fill=(28, 34, 52, 235), outline=(*el_col, 150), width=2)
    f_p1 = _font(15, bold=True)
    d.text((rx + 14, 202), _fit(f"PASIVA: {pas.get('name', 'Ninguna').upper()}  |  OBJETO: {held_name.upper()}", f_p1, box_w - 28), font=f_p1, fill=(255, 220, 95, 255))
    d.text((rx + 14, 227), _fit(pas.get("desc", ""), f_small, box_w - 28), font=f_small, fill=(215, 225, 245, 255))

    # Lista de Habilidades (4 + 1 secreta)
    d.text((rx, 264), "ARSENAL DE HABILIDADES", font=f_sec, fill=(*el_col, 255))
    skills = pet_skills(pet)
    sy = 288
    f_sk = _font(14, bold=True)
    f_sd = _font(12, bold=False)
    for sk in skills[:5]:
        cd_txt = "sin espera" if sk["cd"] == 0 else f"CD {sk['cd']}t"
        d.rounded_rectangle((rx, sy, W - 36, sy + 41), radius=10, fill=(26, 31, 46, 230), outline=(255, 255, 255, 35), width=1)
        d.text((rx + 12, sy + 3), _fit(f"{sk['name'].upper()}   x{sk['dmg_mult']} · {cd_txt}", f_sk, box_w - 24), font=f_sk, fill=(255, 255, 255, 255))
        d.text((rx + 12, sy + 22), _fit(sk["desc"], f_sd, box_w - 24), font=f_sd, fill=(165, 180, 208, 255))
        sy += 46

    fname = f"card_{sp['id']}.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"


# =====================================================================
# 2. BANNER GRÁFICO DE EQUIPO 3v3 (/equipo ver)
# =====================================================================
def render_team_banner(owner_name: str, team: list[dict], synergy: dict, total_cp: int, tower_floor: int) -> tuple[discord.File, str]:
    W, H = 1080, 500
    img = Image.new("RGBA", (W, H), (13, 16, 25, 255))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for idx, p in enumerate(team[:3]):
        el_col = ELEMENT_COLORS.get(CREATURES[p["species_id"]]["element"], (255, 140, 40))
        cx = 190 + idx * 350
        gd.ellipse((cx - 170, 80, cx + 170, 460), fill=(*el_col, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=24, fill=(18, 22, 34, 215), outline=(255, 165, 50, 200), width=3)

    # Header
    d.rounded_rectangle((26, 22, W - 26, 82), radius=16, fill=(28, 34, 52, 240), outline=(255, 255, 255, 45), width=1)
    d.text((44, 34), f"ESCUADRÓN 3v3 DE {owner_name.upper()[:22]}", font=_font(26, bold=True), fill=(255, 255, 255, 255))
    d.text((W - 430, 36), f"PODER: {total_cp:,} CP   •   TORRE: PISO {tower_floor}", font=_font(22, bold=True), fill=(255, 215, 75, 255))

    slot_labels = ["PUESTO 1 · LÍDER", "PUESTO 2 · VANGUARDIA", "PUESTO 3 · APOYO"]
    card_w, card_h = 326, 386

    for idx in range(3):
        cx = 26 + idx * (card_w + 25)
        cy = 96
        if idx >= len(team):
            d.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=20, fill=(22, 26, 38, 180), outline=(255, 255, 255, 35), width=2)
            d.text((cx + 75, cy + 175), "PUESTO VACÍO", font=_font(22, bold=True), fill=(110, 120, 145, 255))
            continue

        p = team[idx]
        sp = CREATURES[p["species_id"]]
        rar = RARITIES[sp["rarity"]]
        el = ELEMENTS[sp["element"]]
        el_col = ELEMENT_COLORS.get(sp["element"], (255, 140, 40))
        rar_col = _int_to_rgb(rar["color"])
        stars = int(p.get("stars") or 0)
        hp, atk = pet_stats(sp["id"], p["level"], p.get("held_item"), stars)
        hp = int(hp * (1.0 + synergy.get("hp_mult", 0.0)))
        atk = int(atk * (1.0 + synergy.get("atk_mult", 0.0)))

        d.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=20, fill=(24, 29, 44, 240), outline=(*rar_col, 220), width=3)
        d.rounded_rectangle((cx + 12, cy + 10, cx + card_w - 12, cy + 40), radius=10, fill=(*el_col, 220))
        d.text((cx + 24, cy + 14), f"{slot_labels[idx]}  (#{p['pet_uid']})", font=_font(15, bold=True), fill=(15, 18, 25, 255))

        art = _rounded_image(_load_creature_art(sp["id"], (190, 190)), 18)
        img.paste(art, (cx + 68, cy + 48), art)
        d.rounded_rectangle((cx + 66, cy + 46, cx + 260, cy + 240), radius=19, outline=(*el_col, 200), width=2)

        name_txt = (p.get("nickname") or sp["name"]).upper()[:16]
        d.text((cx + 18, cy + 248), f"{name_txt}  •  NV.{p['level']}", font=_font(20, bold=True), fill=(255, 255, 255, 255))
        d.text((cx + 18, cy + 273), f"{el['name'].upper()} · {pet_power(p)} CP", font=_font(15, bold=True), fill=(255, 215, 70, 255))
        _draw_stars(d, cx + 200, cy + 273, stars, MAX_STARS, size=16, gap=4)

        d.text((cx + 18, cy + 304), f"HP {hp}", font=_font(14, bold=True), fill=(105, 245, 150, 255))
        _draw_bar(d, cx + 95, cy + 307, 210, 12, min(1.0, hp / 650.0), (65, 225, 125))
        d.text((cx + 18, cy + 326), f"ATQ {atk}", font=_font(14, bold=True), fill=(255, 165, 75, 255))
        _draw_bar(d, cx + 95, cy + 329, 210, 12, min(1.0, atk / 180.0), (255, 145, 55))

        pas_name = sp.get("passive", {}).get("name", "")
        held_name = ITEMS[p["held_item"]]["name"] if p.get("held_item") in ITEMS else "Sin objeto"
        f_pp = _font(13, bold=False)
        d.text((cx + 18, cy + 352), _fit(f"Pasiva: {pas_name} · {held_name}", f_pp, card_w - 36), font=f_pp, fill=(185, 195, 220, 255))

    fname = "team_banner.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"


# =====================================================================
# 3. BANNER DE ARENA DE COMBATE VS (/mascota entrenar, torre, combatir)
# =====================================================================
def _hp_bar_color(ratio: float) -> tuple[int, int, int]:
    if ratio > 0.50:
        return (50, 225, 125)   # Verde esmeralda vivo
    elif ratio > 0.25:
        return (255, 195, 45)   # Ámbar advertencia
    return (255, 65, 75)       # Rojo crítico


def _get_status_pills(u) -> list[tuple[str, tuple[int, int, int]]]:
    pills = []
    if getattr(u, 'burn_turns', 0) > 0:
        pills.append(("QUEMADO", (255, 100, 45)))
    if getattr(u, 'poison_turns', 0) > 0:
        pills.append(("VENENO", (135, 230, 60)))
    if getattr(u, 'expose_turns', 0) > 0:
        pills.append(("EXPUESTO", (255, 175, 40)))
    if getattr(u, 'stunned', False):
        pills.append(("ATURDIDO", (255, 220, 50)))
    if getattr(u, 'shield', 0) > 0:
        pills.append((f"ESCUDO {int(u.shield * 100)}%", (75, 210, 255)))
    if getattr(u, 'thorns_turns', 0) > 0:
        pills.append(("ESPINAS", (95, 240, 150)))
    return pills


def render_battle_banner(side1, side2) -> tuple[discord.File, str]:
    W, H = 960, 380
    img = Image.new("RGBA", (W, H), (12, 14, 22, 255))

    u1 = side1.active
    u2 = side2.active
    el1 = ELEMENTS[u1.species["element"]]
    el2 = ELEMENTS[u2.species["element"]]
    c1 = ELEMENT_COLORS.get(u1.species["element"], (255, 110, 45))
    c2 = ELEMENT_COLORS.get(u2.species["element"], (65, 185, 255))

    # Resplandores elementales y atmósfera de arena
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-60, 10, 480, 360), fill=(*c1, 100))
    gd.ellipse((480, 10, 1020, 360), fill=(*c2, 100))
    # Resplandor central de choque
    gd.ellipse((W // 2 - 120, 70, W // 2 + 120, 270), fill=(255, 205, 55, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")

    # Rejilla de perspectiva del suelo de combate (arena stadium floor)
    floor_y = 230
    for ly in [245, 268, 298, 335]:
        alpha = int(15 + (ly - floor_y) * 0.4)
        d.line([(0, ly), (W, ly)], fill=(255, 255, 255, alpha), width=1)
    for lx in range(40, W, 70):
        alpha = 18 if abs(lx - W // 2) > 100 else 8
        d.line([(W // 2, 150), (lx, H)], fill=(255, 255, 255, alpha), width=1)

    # Marco exterior de la arena
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=24, fill=(18, 22, 34, 205), outline=(255, 255, 255, 60), width=2)

    # Pedestales luminosos bajo los combatientes
    d.ellipse((30, 225, 254, 258), fill=(*c1, 75), outline=(*c1, 190), width=2)
    d.ellipse((W - 254, 225, W - 30, 258), fill=(*c2, 75), outline=(*c2, 190), width=2)

    # Retrato Izquierdo (Jugador 1)
    art1 = _rounded_image(_load_creature_art(u1.species["id"], (210, 210)), 20)
    img.paste(art1, (36, 36), art1)
    d.rounded_rectangle((34, 34, 248, 248), radius=22, outline=(*c1, 240), width=3)

    # Datos Jugador 1
    d.text((266, 42), side1.owner_name.upper()[:18], font=_font(16, bold=True), fill=(*c1, 255))
    d.text((266, 66), f"{u1.short_name.upper()[:14]}", font=_font(25, bold=True), fill=(255, 255, 255, 255))
    d.text((266, 99), f"NV.{u1.pet['level']} · {el1['name'].upper()}", font=_font(15, bold=True), fill=(255, 215, 75, 255))
    _draw_stars(d, 395, 100, u1.stars, MAX_STARS, size=14, gap=3)

    # Barra HP Jugador 1
    hp_ratio1 = max(0.0, min(1.0, u1.hp / max(1, u1.max_hp)))
    bar_col1 = _hp_bar_color(hp_ratio1)
    _draw_bar(d, 266, 126, 175, 16, hp_ratio1, bar_col1)
    if getattr(u1, 'shield', 0) > 0:
        shield_w = int(175 * min(1.0, u1.shield))
        d.rounded_rectangle((266, 126, 266 + shield_w, 142), radius=8, outline=(90, 230, 255, 240), width=2)
    pct1_txt = f"{int(hp_ratio1 * 100)}%"
    d.text((266, 148), f"❤️ {u1.hp}/{u1.max_hp} HP ({pct1_txt})", font=_font(14, bold=True), fill=(215, 230, 248, 255))
    d.text((266, 168), f"⚔️ {int(u1.base_atk * u1.atk_mult)} ATQ", font=_font(14, bold=True), fill=(255, 180, 95, 255))

    # Pastillas de Estado Jugador 1
    pills1 = _get_status_pills(u1)
    px = 266
    f_pill = _font(11, bold=True)
    for p_name, p_col in pills1[:3]:
        pw = int(f_pill.getlength(p_name)) + 12
        d.rounded_rectangle((px, 192, px + pw, 210), radius=6, fill=(*p_col, 210), outline=(255, 255, 255, 160), width=1)
        d.text((px + 6, 194), p_name, font=f_pill, fill=(15, 18, 25, 255))
        px += pw + 6

    # Indicadores de equipo 3v3 Jugador 1 (Orbes 3D con brillo)
    for idx, unit in enumerate(side1.units):
        ox = 266 + idx * 42
        oy = 218
        if unit.alive:
            u_col = ELEMENT_COLORS.get(unit.species["element"], c1)
            d.ellipse((ox, oy, ox + 28, oy + 28), fill=(*u_col, 230), outline=(255, 255, 255, 220), width=2)
            d.ellipse((ox + 5, oy + 4, ox + 14, oy + 12), fill=(255, 255, 255, 200))
        else:
            d.ellipse((ox, oy, ox + 28, oy + 28), fill=(40, 18, 22, 230), outline=(140, 35, 45, 190), width=2)
            d.line([(ox + 7, oy + 7), (ox + 21, oy + 21)], fill=(230, 65, 65, 240), width=2)
            d.line([(ox + 21, oy + 7), (ox + 7, oy + 21)], fill=(230, 65, 65, 240), width=2)

    # Retrato Derecho (Rival / Jefe)
    art2 = _rounded_image(_load_creature_art(u2.species["id"], (210, 210)), 20)
    img.paste(art2, (W - 246, 36), art2)
    d.rounded_rectangle((W - 248, 34, W - 34, 248), radius=22, outline=(*c2, 240), width=3)

    # Datos Rival
    rx = 520
    d.text((rx, 42), side2.owner_name.upper()[:18], font=_font(16, bold=True), fill=(*c2, 255))
    d.text((rx, 66), f"{u2.short_name.upper()[:14]}", font=_font(25, bold=True), fill=(255, 255, 255, 255))
    d.text((rx, 99), f"NV.{u2.pet['level']} · {el2['name'].upper()}", font=_font(15, bold=True), fill=(255, 215, 75, 255))
    _draw_stars(d, rx + 130, 100, u2.stars, MAX_STARS, size=14, gap=3)

    # Barra HP Rival
    hp_ratio2 = max(0.0, min(1.0, u2.hp / max(1, u2.max_hp)))
    bar_col2 = _hp_bar_color(hp_ratio2)
    _draw_bar(d, rx, 126, 175, 16, hp_ratio2, bar_col2)
    if getattr(u2, 'shield', 0) > 0:
        shield_w = int(175 * min(1.0, u2.shield))
        d.rounded_rectangle((rx, 126, rx + shield_w, 142), radius=8, outline=(90, 230, 255, 240), width=2)
    pct2_txt = f"{int(hp_ratio2 * 100)}%"
    d.text((rx, 148), f"❤️ {u2.hp}/{u2.max_hp} HP ({pct2_txt})", font=_font(14, bold=True), fill=(215, 230, 248, 255))
    d.text((rx, 168), f"⚔️ {int(u2.base_atk * u2.atk_mult)} ATQ", font=_font(14, bold=True), fill=(255, 180, 95, 255))

    # Pastillas de Estado Rival
    pills2 = _get_status_pills(u2)
    px = rx
    for p_name, p_col in pills2[:3]:
        pw = int(f_pill.getlength(p_name)) + 12
        d.rounded_rectangle((px, 192, px + pw, 210), radius=6, fill=(*p_col, 210), outline=(255, 255, 255, 160), width=1)
        d.text((px + 6, 194), p_name, font=f_pill, fill=(15, 18, 25, 255))
        px += pw + 6

    # Indicadores de equipo 3v3 Rival
    for idx, unit in enumerate(side2.units):
        ox = rx + idx * 42
        oy = 218
        if unit.alive:
            u_col = ELEMENT_COLORS.get(unit.species["element"], c2)
            d.ellipse((ox, oy, ox + 28, oy + 28), fill=(*u_col, 230), outline=(255, 255, 255, 220), width=2)
            d.ellipse((ox + 5, oy + 4, ox + 14, oy + 12), fill=(255, 255, 255, 200))
        else:
            d.ellipse((ox, oy, ox + 28, oy + 28), fill=(40, 18, 22, 230), outline=(140, 35, 45, 190), width=2)
            d.line([(ox + 7, oy + 7), (ox + 21, oy + 21)], fill=(230, 65, 65, 240), width=2)
            d.line([(ox + 21, oy + 7), (ox + 7, oy + 21)], fill=(230, 65, 65, 240), width=2)

    # Emblema VS y Ventajas Elementales Centrales
    d.line([(W // 2, 24), (W // 2, 260)], fill=(255, 215, 80, 90), width=2)
    # Rombo central VS
    cx = W // 2
    cy = 135
    d.polygon([(cx, cy - 42), (cx + 46, cy), (cx, cy + 42), (cx - 46, cy)], fill=(24, 28, 44, 245), outline=(255, 210, 65, 240), width=3)
    d.text((cx - 21, cy - 17), "VS", font=_font(28, bold=True), fill=(255, 235, 110, 255))

    # Banner de Ventaja Elemental en el centro
    u1_beats_u2 = u2.species["element"] in el1.get("beats", [])
    u2_beats_u1 = u1.species["element"] in el2.get("beats", [])
    if u1_beats_u2:
        d.rounded_rectangle((cx - 105, cy + 50, cx + 105, cy + 76), radius=8, fill=(45, 215, 115, 220), outline=(255, 255, 255, 200), width=1)
        d.text((cx - 96, cy + 54), "⚡ VENTAJA JUGADOR (+25%)", font=_font(12, bold=True), fill=(12, 16, 24, 255))
    elif u2_beats_u1:
        d.rounded_rectangle((cx - 100, cy + 50, cx + 100, cy + 76), radius=8, fill=(255, 85, 75, 220), outline=(255, 255, 255, 200), width=1)
        d.text((cx - 92, cy + 54), "⚡ VENTAJA RIVAL (+25%)", font=_font(12, bold=True), fill=(12, 16, 24, 255))
    else:
        d.rounded_rectangle((cx - 75, cy + 50, cx + 75, cy + 76), radius=8, fill=(35, 42, 64, 200), outline=(255, 255, 255, 50), width=1)
        d.text((cx - 65, cy + 54), "⚔️ DUELO TÁCTICO", font=_font(12, bold=True), fill=(210, 220, 240, 255))

    # Barra inferior con Sinergias y Pasivas de ambos bandos
    d.rounded_rectangle((28, 280, W - 28, 356), radius=14, fill=(22, 27, 42, 235), outline=(255, 255, 255, 45), width=1)
    f_bp = _font(14, bold=False)
    s1_pas = f"🐾 {u1.short_name} · {u1.passive.get('name', 'Sin pasiva')}: {u1.passive.get('desc', '')}"
    s2_pas = f"🐾 {u2.short_name} · {u2.passive.get('name', 'Sin pasiva')}: {u2.passive.get('desc', '')}"
    d.text((44, 292), _fit(s1_pas, f_bp, W - 100), font=f_bp, fill=(180, 235, 255, 255))
    d.text((44, 320), _fit(s2_pas, f_bp, W - 100), font=f_bp, fill=(255, 205, 180, 255))

    fname = "battle_vs.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"


# =====================================================================
# 4. BANNER DE ENCUENTRO SALVAJE (/cazar)
# =====================================================================
def render_encounter_banner(sp: dict, wild_level: int, hp: int, atk: int, catch_chance: float) -> tuple[discord.File, str]:
    W, H = 960, 420
    img = Image.new("RGBA", (W, H), (14, 18, 28, 255))
    el = ELEMENTS[sp["element"]]
    rar = RARITIES[sp["rarity"]]
    el_col = ELEMENT_COLORS.get(sp["element"], (255, 140, 40))
    rar_col = _int_to_rgb(rar["color"])

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((30, 40, 450, 380), fill=(*el_col, 80))
    gd.ellipse((500, 30, 930, 390), fill=(*rar_col, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=22, fill=(18, 22, 34, 215), outline=(*el_col, 200), width=3)

    # Header
    d.rounded_rectangle((26, 20, W - 26, 70), radius=14, fill=(26, 32, 48, 235), outline=(255, 255, 255, 40), width=1)
    d.text((44, 30), "🌿 ¡CRIATURA SALVAJE DETECTADA!", font=_font(22, bold=True), fill=(255, 255, 255, 255))
    d.text((W - 390, 32), "ZONA SALVAJE · HUELLAS FRESCAS", font=_font(18, bold=True), fill=(*el_col, 255))

    # Retrato de la criatura
    art = _rounded_image(_load_creature_art(sp["id"], (270, 270)), 22)
    img.paste(art, (36, 88), art)
    d.rounded_rectangle((34, 86, 308, 360), radius=24, outline=(*rar_col, 240), width=3)

    # Info derecha
    rx = 335
    d.text((rx, 90), sp["name"].upper(), font=_font(34, bold=True), fill=(255, 255, 255, 255))
    d.text((rx + 340, 98), f"NV. {wild_level}", font=_font(24, bold=True), fill=(255, 215, 75, 255))

    # Badges de rareza y elemento
    d.rounded_rectangle((rx, 140, rx + 140, 172), radius=10, fill=(*rar_col, 210))
    d.text((rx + 14, 145), rar["name"].upper(), font=_font(14, bold=True), fill=(15, 18, 25, 255))

    d.rounded_rectangle((rx + 155, 140, rx + 295, 172), radius=10, fill=(*el_col, 210))
    d.text((rx + 169, 145), el["name"].upper(), font=_font(14, bold=True), fill=(15, 18, 25, 255))

    # Barra de Dificultad de Captura
    d.text((rx, 192), f"TASA BASE DE CAPTURA: {int(catch_chance * 100)}%", font=_font(15, bold=True), fill=(210, 225, 245, 255))
    _draw_bar(d, rx, 216, 570, 18, catch_chance, (65, 230, 125) if catch_chance >= 0.50 else (255, 175, 50))

    # Estadísticas
    d.rounded_rectangle((rx, 250, rx + 270, 310), radius=12, fill=(24, 29, 44, 230), outline=(255, 255, 255, 30), width=1)
    d.text((rx + 18, 258), "SALUD ESTIMADA", font=_font(12, bold=False), fill=(160, 175, 200, 255))
    d.text((rx + 18, 276), f"❤️ {hp} HP", font=_font(20, bold=True), fill=(105, 245, 150, 255))

    d.rounded_rectangle((rx + 290, 250, rx + 560, 310), radius=12, fill=(24, 29, 44, 230), outline=(255, 255, 255, 30), width=1)
    d.text((rx + 308, 258), "FUERZA ESTIMADA", font=_font(12, bold=False), fill=(160, 175, 200, 255))
    d.text((rx + 308, 276), f"⚔️ {atk} ATQ", font=_font(20, bold=True), fill=(255, 175, 95, 255))

    # Descripción y Pasiva
    pas = sp.get("passive", {})
    pas_txt = f"Pasiva de especie: {pas.get('name', 'Ninguna')} — {pas.get('desc', '')}"
    d.rounded_rectangle((rx, 324, W - 36, 396), radius=12, fill=(20, 24, 36, 230), outline=(255, 255, 255, 35), width=1)
    f_sm = _font(13, bold=False)
    d.text((rx + 14, 332), _fit(f"*{sp['desc']}*", f_sm, W - rx - 64), font=f_sm, fill=(215, 225, 245, 255))
    d.text((rx + 14, 362), _fit(pas_txt, f_sm, W - rx - 64), font=f_sm, fill=(255, 215, 75, 255))

    fname = f"wild_{sp['id']}.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"


# =====================================================================
# 4. TARJETA GRÁFICA DE PERFIL (/perfil)
# =====================================================================
def render_profile_card(
    display_name: str,
    title_str: str,
    bio_str: str,
    level: int,
    xp: int,
    xp_need: int,
    coins: int,
    rank: int,
    streak: int,
    n_ach: int,
    total_ach: int,
    dex_count: int,
    total_dex: int,
    tower_floor: int,
    color_int: int,
    active_pet: Optional[dict],
) -> tuple[discord.File, str]:
    W, H = 960, 400
    accent = _int_to_rgb(color_int)
    img = Image.new("RGBA", (W, H), (14, 17, 26, 255))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-50, -40, 520, 420), fill=(*accent, 85))
    gd.ellipse((560, 20, 980, 400), fill=(*accent, 65))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=24, fill=(20, 24, 36, 220), outline=(*accent, 230), width=3)

    # Nombre, Título y Nivel
    d.text((38, 28), display_name.upper()[:22], font=_font(34, bold=True), fill=(255, 255, 255, 255))
    d.rounded_rectangle((38, 74, 310, 104), radius=10, fill=(*accent, 45), outline=(*accent, 200), width=1)
    d.text((50, 78), f"TÍTULO: {title_str.upper()[:22]}", font=_font(15, bold=True), fill=(*accent, 255))

    d.rounded_rectangle((325, 74, 590, 104), radius=10, fill=(30, 36, 54, 240))
    d.text((340, 78), f"NIVEL {level}   •   {xp}/{xp_need} XP", font=_font(15, bold=True), fill=(120, 225, 255, 255))
    _draw_bar(d, 38, 116, 552, 16, xp / max(1, xp_need), accent)

    clean_bio = (bio_str or "Sin biografía personalizada (/personalizar bio)").replace("*", "")
    d.text((38, 142), clean_bio[:68], font=_font(16, bold=False), fill=(185, 195, 220, 255))

    # 6 Cajas de Estadísticas
    tiles = [
        ("MONEDAS", f"{coins:,}".replace(",", "."), (255, 210, 70)),
        ("RANKING RIQUEZA", f"PUESTO #{rank}", (110, 215, 255)),
        ("RACHA DIARIA", f"{streak} DÍAS", (255, 130, 65)),
        ("TROBIDEX", f"{dex_count} / {total_dex}", (85, 235, 145)),
        ("TORRE CAMPEONES", f"PISO {tower_floor}", (205, 130, 255)),
        ("LOGROS", f"{n_ach} / {total_ach}", (255, 195, 95)),
    ]
    for i, (t_label, t_val, t_col) in enumerate(tiles):
        col_i = i % 3
        row_i = i // 3
        tx = 38 + col_i * 188
        ty = 182 + row_i * 92
        d.rounded_rectangle((tx, ty, tx + 176, ty + 78), radius=14, fill=(26, 32, 48, 240), outline=(*t_col, 120), width=2)
        d.text((tx + 14, ty + 12), t_label, font=_font(13, bold=True), fill=(165, 175, 200, 255))
        d.text((tx + 14, ty + 36), t_val, font=_font(21, bold=True), fill=(*t_col, 255))

    # Panel Derecho: Compañero Trobimon Activo
    px, py = 626, 30
    d.rounded_rectangle((px, py, W - 30, H - 30), radius=20, fill=(24, 29, 44, 240), outline=(*accent, 190), width=2)
    d.text((px + 22, py + 14), "COMPAÑERO LÍDER", font=_font(16, bold=True), fill=(*accent, 255))

    if active_pet and active_pet["species_id"] in CREATURES:
        sp = CREATURES[active_pet["species_id"]]
        art = _rounded_image(_load_creature_art(sp["id"], (210, 210)), 18)
        img.paste(art, (px + 47, py + 46), art)
        d.rounded_rectangle((px + 45, py + 44, px + 259, py + 258), radius=20, outline=(*accent, 210), width=2)
        p_name = (active_pet.get("nickname") or sp["name"]).upper()[:16]
        stars = int(active_pet.get("stars") or 0)
        d.text((px + 24, py + 270), f"{p_name} (NV.{active_pet['level']})", font=_font(19, bold=True), fill=(255, 255, 255, 255))
        _draw_stars(d, px + 24, py + 300, stars, MAX_STARS, size=18, gap=4)
        d.text((px + 170, py + 298), f"{pet_power(active_pet)} CP", font=_font(16, bold=True), fill=(255, 215, 70, 255))
    else:
        d.text((px + 45, py + 160), "SIN TROBIMON\nUsa /cazar", font=_font(22, bold=True), fill=(120, 130, 155, 255))

    fname = "profile_card.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"


# =====================================================================
# 6. TARJETA DE BIENVENIDA A NUEVOS MIEMBROS (on_message new_member)
# =====================================================================
def render_welcome_card(member_name: str, member_count: int, inviter_name: Optional[str] = None) -> tuple[discord.File, str]:
    W, H = 960, 320
    img = Image.new("RGBA", (W, H), (13, 16, 25, 255))

    accent = (255, 130, 30)   # Naranja valenciano trobia
    gold = (255, 215, 75)

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-80, -60, 420, 340), fill=(*accent, 95))
    gd.ellipse((580, -40, 1040, 360), fill=(130, 80, 255, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((12, 12, W - 12, H - 12), radius=24, fill=(18, 22, 34, 215), outline=(*accent, 210), width=3)

    # Emblema izquierdo (arte de Tarongín como mascota oficial de bienvenida)
    art = _rounded_image(_load_creature_art("tarongin", (220, 220)), 24)
    img.paste(art, (42, 50), art)
    d.rounded_rectangle((40, 48, 264, 272), radius=26, outline=(*gold, 220), width=3)

    # Textos derecha
    rx = 295
    d.rounded_rectangle((rx, 42, rx + 260, 74), radius=10, fill=(*accent, 220))
    d.text((rx + 16, 48), "BIENVENIDO/A A TROBIA", font=_font(16, bold=True), fill=(15, 18, 25, 255))

    d.text((rx, 88), _fit(member_name.upper(), _font(38, bold=True), W - rx - 45), font=_font(38, bold=True), fill=(255, 255, 255, 255))
    sub = f"MIEMBRO #{member_count} DE LA COMUNIDAD"
    if inviter_name:
        sub += f"  •  INVITADO POR {inviter_name.upper()[:18]}"
    d.text((rx, 142), _fit(sub, _font(17, bold=True), W - rx - 45), font=_font(17, bold=True), fill=(*gold, 255))

    # 3 pasos rápidos en cajas limpias
    steps = [
        ("1. ROLES", "Elige juegos y zona", (80, 200, 255)),
        ("2. PRESENTATE", "Saluda en la comunidad", (110, 235, 145)),
        ("3. /CAZAR", "Captura tu 1er Trobimon", (255, 165, 60)),
    ]
    for i, (st_t, st_d, st_c) in enumerate(steps):
        sx = rx + i * 210
        sy = 188
        d.rounded_rectangle((sx, sy, sx + 196, sy + 84), radius=14, fill=(26, 32, 48, 235), outline=(*st_c, 160), width=2)
        d.text((sx + 14, sy + 14), st_t, font=_font(16, bold=True), fill=(*st_c, 255))
        d.text((sx + 14, sy + 42), st_d, font=_font(14, bold=False), fill=(215, 225, 242, 255))

    fname = "welcome_trobia.jpg"
    return _to_discord_file(img, fname), f"attachment://{fname}"
