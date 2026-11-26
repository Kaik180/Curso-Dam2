"""Catálogo de objetos, rarezas y cajas."""

RARITIES = {
    "comun":      {"name": "Común",      "emoji": "⚪", "color": 0x95A5A6, "dup_value": 150},
    "raro":       {"name": "Raro",       "emoji": "🔵", "color": 0x3498DB, "dup_value": 400},
    "epico":      {"name": "Épico",      "emoji": "🟣", "color": 0x9B59B6, "dup_value": 1000},
    "legendario": {"name": "Legendario", "emoji": "🟡", "color": 0xF1C40F, "dup_value": 3000},
}

COSMETIC_TYPES = ("color", "title", "badge")

# price = None -> solo se consigue en cajas
ITEMS = {
    # ------------------------------------------------------------- colores
    "color_rojo":    {"name": "Rojo Pasión",        "emoji": "🟥", "type": "color", "rarity": "comun",      "price": 800,  "value": "E74C3C"},
    "color_azul":    {"name": "Azul Mediterráneo",  "emoji": "🟦", "type": "color", "rarity": "comun",      "price": 800,  "value": "3498DB"},
    "color_verde":   {"name": "Verde Huerta",       "emoji": "🟩", "type": "color", "rarity": "comun",      "price": 800,  "value": "2ECC71"},
    "color_morado":  {"name": "Morado Real",        "emoji": "🟪", "type": "color", "rarity": "raro",       "price": 2000, "value": "9B59B6"},
    "color_rosa":    {"name": "Rosa Chicle",        "emoji": "🌸", "type": "color", "rarity": "raro",       "price": 2000, "value": "FF6FB5"},
    "color_naranja": {"name": "Naranja Valencia",   "emoji": "🟧", "type": "color", "rarity": "epico",      "price": 5000, "value": "FF7F11"},
    "color_negro":   {"name": "Negro Abismo",       "emoji": "⬛", "type": "color", "rarity": "epico",      "price": None, "value": "111111"},
    "color_dorado":  {"name": "Oro Puro",           "emoji": "🟨", "type": "color", "rarity": "legendario", "price": None, "value": "FFD700"},

    # ------------------------------------------------------------- títulos
    "titulo_novato":   {"name": "El Novato",            "emoji": "🐣", "type": "title", "rarity": "comun",      "price": 500,  "value": "El Novato"},
    "titulo_viciado":  {"name": "Viciado/a",            "emoji": "🎮", "type": "title", "rarity": "comun",      "price": 1000, "value": "Viciado/a"},
    "titulo_tryhard":  {"name": "Tryhard Profesional",  "emoji": "💢", "type": "title", "rarity": "raro",       "price": 2500, "value": "Tryhard Profesional"},
    "titulo_cinefilo": {"name": "Cinéfilo/a de Sofá",   "emoji": "🎬", "type": "title", "rarity": "raro",       "price": 2500, "value": "Cinéfilo/a de Sofá"},
    "titulo_paella":   {"name": "Maestro/a Paellero",   "emoji": "🥘", "type": "title", "rarity": "epico",      "price": 6000, "value": "Maestro/a Paellero"},
    "titulo_casino":   {"name": "Rey/Reina del Casino", "emoji": "🎰", "type": "title", "rarity": "epico",      "price": None, "value": "Rey/Reina del Casino"},
    "titulo_fallero":  {"name": "Fallero/a Mayor",      "emoji": "🔥", "type": "title", "rarity": "legendario", "price": None, "value": "Fallero/a Mayor"},
    "titulo_leyenda":  {"name": "Leyenda de trobia",    "emoji": "🌟", "type": "title", "rarity": "legendario", "price": None, "value": "Leyenda de trobia"},

    # ----------------------------------------------------------- insignias
    "insignia_naranja":   {"name": "Insignia Naranja",   "emoji": "🍊", "type": "badge", "rarity": "comun",      "price": 600,  "value": "🍊"},
    "insignia_mando":     {"name": "Insignia Gamer",     "emoji": "🎮", "type": "badge", "rarity": "comun",      "price": 600,  "value": "🎮"},
    "insignia_palomitas": {"name": "Insignia Palomitas", "emoji": "🍿", "type": "badge", "rarity": "comun",      "price": 600,  "value": "🍿"},
    "insignia_fuego":     {"name": "Insignia Fuego",     "emoji": "🔥", "type": "badge", "rarity": "raro",       "price": 1800, "value": "🔥"},
    "insignia_paella":    {"name": "Insignia Paella",    "emoji": "🥘", "type": "badge", "rarity": "raro",       "price": 1800, "value": "🥘"},
    "insignia_diamante":  {"name": "Insignia Diamante",  "emoji": "💎", "type": "badge", "rarity": "epico",      "price": None, "value": "💎"},
    "insignia_corona":    {"name": "Insignia Corona",    "emoji": "👑", "type": "badge", "rarity": "legendario", "price": None, "value": "👑"},
    "insignia_dragon":    {"name": "Insignia Dragón",    "emoji": "🐉", "type": "badge", "rarity": "legendario", "price": None, "value": "🐉"},

    # --------------------------------------------------------- consumibles
    "boost_xp":      {"name": "Poción de XP x2 (1h)",       "emoji": "⚗️", "type": "consumable", "rarity": "raro",  "price": 1200,
                      "desc": "Duplica la XP que ganas durante 1 hora."},
    "boost_monedas": {"name": "Amuleto de Monedas x2 (1h)", "emoji": "🧿", "type": "consumable", "rarity": "raro",  "price": 1500,
                      "desc": "Duplica las monedas de /trabajar y de los mensajes durante 1 hora."},
    "reset_trabajo": {"name": "Café Cargado",               "emoji": "☕", "type": "consumable", "rarity": "comun", "price": 400,
                      "desc": "Reinicia el tiempo de espera de /trabajar."},

    # --------------------------------------------------------------- cajas
    "caja_comun":      {"name": "Caja Común",      "emoji": "📦", "type": "box", "rarity": "comun",      "price": 300},
    "caja_rara":       {"name": "Caja Rara",       "emoji": "🎁", "type": "box", "rarity": "raro",       "price": 900},
    "caja_epica":      {"name": "Caja Épica",      "emoji": "💜", "type": "box", "rarity": "epico",      "price": 2500},
    "caja_legendaria": {"name": "Caja Legendaria", "emoji": "🌟", "type": "box", "rarity": "legendario", "price": 7000},

    # --------------------------------------------------- mascotas y caza
    "orbe_basico":      {"name": "Orbe Básico",       "emoji": "🔴", "type": "pet", "rarity": "comun",      "price": 150,
                         "desc": "Orbe de captura estándar (x1.0) para usar en /cazar."},
    "orbe_super":       {"name": "Súper Orbe",        "emoji": "🔵", "type": "pet", "rarity": "raro",       "price": 400,
                         "desc": "Orbe mejorado (x1.6 prob. de captura) para usar en /cazar."},
    "orbe_ultra":       {"name": "Ultra Orbe",        "emoji": "🟣", "type": "pet", "rarity": "epico",      "price": 900,
                         "desc": "Orbe de alta potencia (x2.4 prob. de captura) para /cazar."},
    "orbe_maestro":     {"name": "Orbe Maestro",      "emoji": "🟡", "type": "pet", "rarity": "legendario", "price": 4500,
                         "desc": "¡Captura 100% asegurada sin fallar nunca en /cazar!"},
    "comida_trobimon":  {"name": "Chuletón Ibérico",  "emoji": "🍖", "type": "pet", "rarity": "comun",      "price": 200,
                         "desc": "Da +60 XP a tu Trobimon compañero con /mascota alimentar."},
    "caramelo_raro":    {"name": "Caramelo Místico",  "emoji": "🍬", "type": "pet", "rarity": "raro",       "price": 750,
                         "desc": "Sube +1 nivel completo al instante a tu Trobimon compañero."},
    "piedra_evolutiva": {"name": "Piedra Evolutiva",  "emoji": "💎", "type": "pet", "rarity": "epico",      "price": 2800,
                         "desc": "Evoluciona al instante a tu Trobimon a su siguiente etapa."},
    "huevo_comun":      {"name": "Huevo Salvaje",     "emoji": "🥚", "type": "pet", "rarity": "raro",       "price": 600,
                         "desc": "Incúbalo con /incubadora para obtener un Trobimon inicial o raro."},
    "huevo_mistico":    {"name": "Huevo Místico",     "emoji": "🔮", "type": "pet", "rarity": "epico",      "price": 2200,
                         "desc": "Incúbalo con /incubadora: alta probabilidad de Trobimons raros, épicos o legendarios."},

    # --------------------------------------- objetos equipables de mascota
    "amuleto_brasa":    {"name": "Brasero Fallero",       "emoji": "🔥", "type": "gear", "rarity": "raro",       "price": 1200,
                         "desc": "+20% daño de habilidades Brasa y +15% prob. de Quemadura."},
    "perla_albufera":   {"name": "Perla de la Albufera",  "emoji": "🫧", "type": "gear", "rarity": "raro",       "price": 1200,
                         "desc": "+20% daño de habilidades Laguna y regenera 6% HP cada turno."},
    "semilla_azahar":   {"name": "Semilla de Azahar",     "emoji": "🌿", "type": "gear", "rarity": "raro",       "price": 1200,
                         "desc": "+20% daño de habilidades Huerta y +25% a todas las curaciones/drenajes."},
    "capa_nocturna":    {"name": "Capa del Ratpenat",     "emoji": "🌙", "type": "gear", "rarity": "raro",       "price": 1400,
                         "desc": "+20% daño de habilidades Sombra y 18% prob. de esquivar ataques."},
    "nucleo_plasma":    {"name": "Núcleo de Plasma",      "emoji": "⚡", "type": "gear", "rarity": "raro",       "price": 1500,
                         "desc": "+20% daño de habilidades Astrales y +20% prob. de golpe crítico."},
    "amuleto_roca":     {"name": "Runa del Penyagolosa",  "emoji": "🪨", "type": "gear", "rarity": "raro",       "price": 1400,
                         "desc": "+20% daño de habilidades Roca, +12% HP máx. y -8% daño recibido."},
    "cristal_hielo":    {"name": "Cristal de Escarcha",   "emoji": "❄️", "type": "gear", "rarity": "raro",       "price": 1400,
                         "desc": "+20% daño de habilidades Escarcha y +15% prob. de aturdir/congelar."},
    "pluma_cefiro":     {"name": "Pluma de Céfiro",       "emoji": "🌪️", "type": "gear", "rarity": "raro",       "price": 1400,
                         "desc": "+20% daño de habilidades Céfiro y 15% prob. de esquivar ataques."},
    "chaleco_titanio":  {"name": "Coraza Real",           "emoji": "🛡️", "type": "gear", "rarity": "epico",      "price": 2000,
                         "desc": "+25% de Vida máxima (HP) y reduce todo el daño recibido un 12%."},
    "garra_feroz":      {"name": "Garra Dracónica",       "emoji": "🗡️", "type": "gear", "rarity": "epico",      "price": 2200,
                         "desc": "+22% de Ataque (ATQ) y los golpes críticos hacen x1.75 de daño."},
    "espejo_espinas":   {"name": "Manto de Espinas",      "emoji": "🌵", "type": "gear", "rarity": "epico",      "price": 2100,
                         "desc": "+15% HP máx. y devuelve un 25% de todo el daño recibido al atacante."},
    "corona_fortuna":   {"name": "Cascabel Dorado",       "emoji": "👑", "type": "gear", "rarity": "legendario", "price": 3200,
                         "desc": "Regenera 5% HP por turno en combate y da +15% extra de monedas en /trabajar."},

    # ------------------------------------ pergaminos de habilidad (MT)
    "pergamino_veneno":    {"name": "Pergamino: Niebla Tóxica",     "emoji": "🧪", "type": "scroll", "rarity": "raro",       "price": 1300,
                            "desc": "Enseña 'Niebla Tóxica' (Envenena 3 turnos y baja -20% ATQ al rival)."},
    "pergamino_espejo":    {"name": "Pergamino: Cúpula Espejo",     "emoji": "🪞", "type": "scroll", "rarity": "raro",       "price": 1400,
                            "desc": "Enseña 'Cúpula Espejo' (Escudo -45% daño y devuelve 45% de daño con espinas)."},
    "pergamino_purificar": {"name": "Pergamino: Luz del Turia",     "emoji": "✨", "type": "scroll", "rarity": "raro",       "price": 1400,
                            "desc": "Enseña 'Luz del Turia' (Cura 32% HP, limpia estados negativos y sube +20% ATQ)."},
    "pergamino_helada":    {"name": "Pergamino: Ventisca Ártica",   "emoji": "❄️", "type": "scroll", "rarity": "epico",      "price": 1900,
                            "desc": "Enseña 'Ventisca Ártica' (Ralentiza CDs del rival +1t y 40% prob. de congelar)."},
    "pergamino_ejecutor":  {"name": "Pergamino: Guadaña Ejecutora", "emoji": "⚰️", "type": "scroll", "rarity": "epico",      "price": 2100,
                            "desc": "Enseña 'Guadaña Ejecutora' (Daño x2 si el rival tiene <45% HP y roba 30% vida)."},
    "pergamino_robo":      {"name": "Pergamino: Ladrón de Almas",   "emoji": "🎭", "type": "scroll", "rarity": "epico",      "price": 2200,
                            "desc": "Enseña 'Ladrón de Almas' (Roba el escudo y las mejoras de ATQ del rival y drena vida)."},
    "pergamino_equipo":    {"name": "Pergamino: Himno de Valencia", "emoji": "🎺", "type": "scroll", "rarity": "legendario", "price": 2800,
                            "desc": "Enseña 'Himno de Valencia' (Cura 25% HP y sube +20% ATQ a TODO tu equipo de 3)."},
    "pergamino_meteoros":  {"name": "Pergamino: Lluvia Estelar",    "emoji": "☄️", "type": "scroll", "rarity": "legendario", "price": 2900,
                            "desc": "Enseña 'Lluvia Estelar' (Golpea de 2 a 4 veces seguidas e ignora escudos)."},
}

# Tablas de botín. "w" = peso (probabilidad relativa)
LOOT = {
    "caja_comun": [
        {"w": 40, "type": "coins", "min": 80,  "max": 250, "rarity": "comun"},
        {"w": 15, "type": "coins", "min": 250, "max": 500, "rarity": "raro"},
        {"w": 18, "type": "cosmetic", "rarity": "comun"},
        {"w": 7,  "type": "item", "id": "orbe_super"},
        {"w": 10, "type": "item", "id": "reset_trabajo"},
        {"w": 6,  "type": "item", "id": "boost_xp"},
        {"w": 3,  "type": "item", "id": "huevo_comun"},
        {"w": 1,  "type": "cosmetic", "rarity": "raro"},
    ],
    "caja_rara": [
        {"w": 26, "type": "coins", "min": 300, "max": 800,  "rarity": "comun"},
        {"w": 15, "type": "coins", "min": 800, "max": 1600, "rarity": "raro"},
        {"w": 14, "type": "cosmetic", "rarity": "comun"},
        {"w": 14, "type": "cosmetic", "rarity": "raro"},
        {"w": 4,  "type": "item", "id": "amuleto_brasa"},
        {"w": 4,  "type": "item", "id": "pergamino_veneno"},
        {"w": 5,  "type": "item", "id": "huevo_comun"},
        {"w": 7,  "type": "item", "id": "boost_xp"},
        {"w": 6,  "type": "item", "id": "boost_monedas"},
        {"w": 4,  "type": "item", "id": "caja_epica"},
        {"w": 1,  "type": "cosmetic", "rarity": "epico"},
    ],
    "caja_epica": [
        {"w": 22, "type": "coins", "min": 1000, "max": 2500, "rarity": "raro"},
        {"w": 12, "type": "coins", "min": 2500, "max": 5000, "rarity": "epico"},
        {"w": 18, "type": "cosmetic", "rarity": "raro"},
        {"w": 15, "type": "cosmetic", "rarity": "epico"},
        {"w": 6,  "type": "item", "id": "huevo_mistico"},
        {"w": 6,  "type": "item", "id": "piedra_evolutiva"},
        {"w": 5,  "type": "item", "id": "chaleco_titanio"},
        {"w": 6,  "type": "item", "id": "pergamino_ejecutor"},
        {"w": 6,  "type": "item", "id": "boost_monedas"},
        {"w": 4,  "type": "cosmetic", "rarity": "legendario"},
    ],
    "caja_legendaria": [
        {"w": 20, "type": "coins", "min": 4000,  "max": 9000,  "rarity": "epico"},
        {"w": 10, "type": "coins", "min": 10000, "max": 20000, "rarity": "legendario"},
        {"w": 26, "type": "cosmetic", "rarity": "epico"},
        {"w": 22, "type": "cosmetic", "rarity": "legendario"},
        {"w": 8,  "type": "item", "id": "orbe_maestro"},
        {"w": 7,  "type": "item", "id": "corona_fortuna"},
        {"w": 7,  "type": "item", "id": "pergamino_meteoros"},
    ],
}

TYPE_NAMES = {
    "pet": "🐾 Mascotas y Caza (Trobimons)",
    "gear": "🎒 Objetos Equipables (Trobimons)",
    "scroll": "📜 Pergaminos de Habilidad (Trobimons)",
    "box": "🎁 Cajas",
    "consumable": "🧪 Consumibles",
    "color": "🎨 Colores de perfil",
    "title": "🏷️ Títulos",
    "badge": "🎖️ Insignias",
}


def item_label(item_id: str) -> str:
    it = ITEMS[item_id]
    return f"{it['emoji']} {it['name']}"


def cosmetics_of(rarity: str) -> list[str]:
    return [i for i, it in ITEMS.items() if it["type"] in COSMETIC_TYPES and it["rarity"] == rarity]
