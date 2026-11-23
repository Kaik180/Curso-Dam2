"""Catálogo de Trobimons: 30 criaturas, 8 elementos, pasivas únicas, combinaciones elementales de equipo, 128 habilidades y objetos."""
import os
import config

ASSETS_DIR = os.path.join(config.BASE_DIR, "assets", "trobimons")

MAX_STARS = 5
STAR_STAT_BONUS = 0.10  # +10% HP y +10% ATQ por cada estrella (hasta +50% en 5★)
STAR_WORK_BONUS = 3     # +3% monedas extra en /trabajar por cada estrella

ELEMENTS = {
    "brasa":  {"name": "Brasa",    "emoji": "🔥", "beats": ["huerta", "sombra", "hielo"]},
    "laguna": {"name": "Laguna",   "emoji": "💧", "beats": ["brasa", "astral", "roca"]},
    "huerta": {"name": "Huerta",   "emoji": "🌿", "beats": ["laguna", "astral", "roca"]},
    "sombra": {"name": "Sombra",   "emoji": "🌙", "beats": ["huerta", "laguna", "viento"]},
    "astral": {"name": "Astral",   "emoji": "⚡", "beats": ["brasa", "sombra", "viento"]},
    "roca":   {"name": "Roca",     "emoji": "🪨", "beats": ["brasa", "astral", "hielo"]},
    "hielo":  {"name": "Escarcha", "emoji": "❄️", "beats": ["huerta", "roca", "viento"]},
    "viento": {"name": "Céfiro",   "emoji": "🌪️", "beats": ["huerta", "laguna", "roca"]},
}

RARITY_BONUS_PCT = {
    "comun": 5,
    "raro": 12,
    "epico": 22,
    "legendario": 35,
}

RELEASE_REWARDS = {
    "comun":      {"base_coins": 160,  "per_lvl": 25,  "item": "comida_trobimon", "qty": 1},
    "raro":       {"base_coins": 400,  "per_lvl": 45,  "item": "comida_trobimon", "qty": 2},
    "epico":      {"base_coins": 950,  "per_lvl": 70,  "item": "caramelo_raro",   "qty": 1},
    "legendario": {"base_coins": 2500, "per_lvl": 110, "item": "caramelo_raro",   "qty": 2},
}

PET_GEAR = {
    "amuleto_brasa": {
        "elem_boost": ("brasa", 0.20),
        "burn_bonus": 0.15,
        "summary": "+20% daño Brasa · +15% prob. Quemadura",
    },
    "perla_albufera": {
        "elem_boost": ("laguna", 0.20),
        "regen_pct": 0.06,
        "summary": "+20% daño Laguna · Regenera 6% HP/turno",
    },
    "semilla_azahar": {
        "elem_boost": ("huerta", 0.20),
        "heal_boost": 0.25,
        "summary": "+20% daño Huerta · +25% curación y drenaje",
    },
    "capa_nocturna": {
        "elem_boost": ("sombra", 0.20),
        "dodge_chance": 0.18,
        "summary": "+20% daño Sombra · 18% prob. de esquivar",
    },
    "nucleo_plasma": {
        "elem_boost": ("astral", 0.20),
        "crit_bonus": 0.20,
        "summary": "+20% daño Astral · +20% prob. crítico",
    },
    "amuleto_roca": {
        "elem_boost": ("roca", 0.20),
        "hp_mult": 0.12,
        "dmg_reduction": 0.08,
        "summary": "+20% daño Roca · +12% HP · -8% daño recibido",
    },
    "cristal_hielo": {
        "elem_boost": ("hielo", 0.20),
        "stun_bonus": 0.15,
        "summary": "+20% daño Escarcha · +15% prob. de congelar/aturdir",
    },
    "pluma_cefiro": {
        "elem_boost": ("viento", 0.20),
        "dodge_chance": 0.15,
        "summary": "+20% daño Céfiro · 15% prob. de esquivar",
    },
    "chaleco_titanio": {
        "hp_mult": 0.25,
        "dmg_reduction": 0.12,
        "summary": "+25% HP máx. · -12% daño recibido",
    },
    "garra_feroz": {
        "atk_mult": 0.22,
        "crit_dmg_bonus": 0.25,
        "summary": "+22% ATQ · Críticos hacen x1.75",
    },
    "espejo_espinas": {
        "hp_mult": 0.15,
        "thorns_passive": 0.25,
        "summary": "+15% HP máx. · Devuelve 25% del daño recibido",
    },
    "corona_fortuna": {
        "regen_pct": 0.05,
        "work_bonus_pct": 15,
        "summary": "Regenera 5% HP/turno · +15% monedas en /trabajar",
    },
}

SCROLL_SKILLS = {
    "pergamino_veneno": {
        "name": "Niebla Tóxica", "emoji": "🧪", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.90,
        "poison": (0.85, 3), "weaken": 0.20,
        "desc": "Nube corrosiva: 85% prob. de envenenar (3t) y reduce -20% el ATQ rival.",
    },
    "pergamino_espejo": {
        "name": "Cúpula Espejo", "emoji": "🪞", "role": "🛡️ Tanque", "cd": 3, "dmg_mult": 0.55,
        "shield_pct": 0.45, "thorns": (0.45, 2),
        "desc": "Escudo (-45% daño) y Espinas que devuelven el 45% del daño durante 2 turnos.",
    },
    "pergamino_purificar": {
        "name": "Luz del Turia", "emoji": "✨", "role": "💚 Soporte", "cd": 3, "dmg_mult": 0.40,
        "heal_pct": 0.32, "cleanse": True, "atk_buff": 0.20,
        "desc": "Purifica quemaduras/venenos/debilitamientos, cura 32% HP y sube +20% ATQ.",
    },
    "pergamino_helada": {
        "name": "Ventisca Ártica", "emoji": "❄️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.25,
        "freeze_cd": 1, "stun_chance": 0.40,
        "desc": "Aumenta +1 turno las recargas del rival y tiene 40% prob. de congelarlo.",
    },
    "pergamino_ejecutor": {
        "name": "Guadaña Ejecutora", "emoji": "⚰️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.25,
        "exec_bonus": (0.45, 0.75), "lifesteal": 0.30,
        "desc": "Inflige +75% de daño si el rival tiene <45% HP y roba 30% de vida.",
    },
    "pergamino_robo": {
        "name": "Ladrón de Almas", "emoji": "🎭", "role": "🎭 Táctica", "cd": 3, "dmg_mult": 1.15,
        "steal_buff": True, "lifesteal": 0.28,
        "desc": "Roba el Escudo y las subidas de ATQ del enemigo para ti y drena 28% de vida.",
    },
    "pergamino_equipo": {
        "name": "Himno de Valencia", "emoji": "🎺", "role": "👥 Equipo", "cd": 3, "dmg_mult": 0.50,
        "team_heal_pct": 0.25, "team_atk_buff": 0.20, "cleanse": True,
        "desc": "Purifica, cura 25% HP a TODO tu equipo vivo y sube +20% ATQ a tus 3 Trobimons.",
    },
    "pergamino_meteoros": {
        "name": "Lluvia Estelar", "emoji": "☄️", "role": "⚡ Ráfaga", "cd": 3, "dmg_mult": 0.58,
        "hits": (2, 4), "pierce": True, "expose": 2,
        "desc": "Golpea de 2 a 4 veces ignorando escudos y deja Vulnerable (+30% daño) 2t.",
    },
}

# =====================================================================
# COMBINACIONES DE EQUIPO (3 DEL MISMO ELEMENTO + PAREJAS ELEMENTALES)
# =====================================================================
MONO_ELEMENT_COMBOS = {
    "brasa": {
        "name": "🔥👑 Supernova de la Cremà (3x Brasa)",
        "atk_mult": 0.30, "burn_bonus": 0.20, "enemy_burn_aura": 0.06,
        "desc": "+30% ATQ al equipo, +20% prob. de Quemadura y abrasa al rival un -6% HP cada turno.",
    },
    "laguna": {
        "name": "💧👑 Abismo del Mediterráneo (3x Laguna)",
        "hp_mult": 0.25, "atk_mult": 0.18, "team_regen_pct": 0.07,
        "desc": "+25% HP, +18% ATQ y todo tu equipo regenera +7% HP al inicio de cada turno.",
    },
    "huerta": {
        "name": "🌿👑 Jardín Sagrado del Turia (3x Huerta)",
        "hp_mult": 0.28, "heal_boost": 0.35, "lifesteal_bonus": 0.15,
        "desc": "+28% HP, +35% efectividad de curación y todos tus ataques drenan +15% de vida.",
    },
    "sombra": {
        "name": "🌙👑 Corte del Eclipse Eterno (3x Sombra)",
        "atk_mult": 0.25, "dodge_bonus": 0.16, "lifesteal_bonus": 0.15, "enemy_expose_start": 2,
        "desc": "+25% ATQ, +16% Esquiva, +15% Drenaje y el equipo rival empieza Vulnerable (2t).",
    },
    "astral": {
        "name": "⚡👑 Singularidad Cibernética (3x Astral)",
        "atk_mult": 0.28, "crit_bonus": 0.25, "start_shield": 0.35,
        "desc": "+28% ATQ, +25% Prob. de Crítico y tus 3 Trobimons empiezan con Escudo (-35% daño).",
    },
    "roca": {
        "name": "🪨👑 Cordillera Inmortal (3x Roca)",
        "hp_mult": 0.35, "dmg_reduction": 0.20, "thorns_bonus": 0.25,
        "desc": "+35% HP, -20% daño recibido para todo el equipo y refleja un 25% de daño con Espinas.",
    },
    "hielo": {
        "name": "❄️👑 Era Glacial Absoluta (3x Escarcha)",
        "hp_mult": 0.20, "atk_mult": 0.20, "stun_bonus": 0.20, "enemy_atk_debuff": 0.18,
        "desc": "+20% HP/ATQ, +20% prob. de Congelar/Aturdir y reduce -18% el ATQ del equipo enemigo.",
    },
    "viento": {
        "name": "🌪️👑 Ojo del Huracán (3x Céfiro)",
        "atk_mult": 0.25, "dodge_bonus": 0.22, "crit_bonus": 0.20,
        "desc": "+25% ATQ, +22% Prob. de Esquiva y +20% Prob. de Crítico para todo el equipo.",
    },
}

DUAL_ELEMENT_COMBOS = [
    {
        "elems": {"brasa", "viento"},
        "name": "🔥🌪️ Tormenta Ígnea (Brasa + Céfiro)",
        "atk_mult": 0.18, "burn_bonus": 0.15, "crit_bonus": 0.12,
        "desc": "El viento aviva las llamas: +18% ATQ, +15% prob. Quemadura y +12% Crítico.",
    },
    {
        "elems": {"roca", "brasa"},
        "name": "🪨🔥 Corazón de Magma (Roca + Brasa)",
        "hp_mult": 0.18, "atk_mult": 0.15, "thorns_bonus": 0.15,
        "desc": "Roca fundida: +18% HP, +15% ATQ y +15% reflejo de daño por Espinas.",
    },
    {
        "elems": {"laguna", "hielo"},
        "name": "💧❄️ Marea Ártica (Laguna + Escarcha)",
        "hp_mult": 0.16, "dmg_reduction": 0.12, "stun_bonus": 0.15,
        "desc": "Aguas bajo cero: +16% HP, -12% daño recibido y +15% prob. de Congelar.",
    },
    {
        "elems": {"laguna", "astral"},
        "name": "💧⚡ Electrocución Marina (Laguna + Astral)",
        "atk_mult": 0.16, "crit_bonus": 0.20,
        "desc": "El agua conduce el plasma: +16% ATQ y +20% probabilidad de Crítico.",
    },
    {
        "elems": {"huerta", "laguna"},
        "name": "🌿💧 Oasis de la Albufera (Huerta + Laguna)",
        "hp_mult": 0.20, "team_regen_pct": 0.05, "heal_boost": 0.20,
        "desc": "Florecimiento vital: +20% HP, +20% curaciones y regenera +5% HP/turno.",
    },
    {
        "elems": {"huerta", "sombra"},
        "name": "🌿🌙 Bosque Embrujado (Huerta + Sombra)",
        "lifesteal_bonus": 0.18, "enemy_atk_debuff": 0.14,
        "desc": "Drenaje maldito: +18% Robo de Vida en ataques y -14% ATQ al equipo enemigo.",
    },
    {
        "elems": {"astral", "viento"},
        "name": "⚡🌪️ Tempestad Supersónica (Astral + Céfiro)",
        "atk_mult": 0.16, "dodge_bonus": 0.15, "crit_bonus": 0.12,
        "desc": "Velocidad del rayo: +16% ATQ, +15% Esquiva y +12% Crítico.",
    },
    {
        "elems": {"roca", "hielo"},
        "name": "🪨❄️ Glaciar Acorazado (Roca + Escarcha)",
        "hp_mult": 0.22, "dmg_reduction": 0.15,
        "desc": "Muralla polar: +22% HP máximo y -15% daño recibido para todo el equipo.",
    },
    {
        "elems": {"sombra", "astral"},
        "name": "🌙⚡ Nebulosa Cuántica (Sombra + Astral)",
        "atk_mult": 0.22, "dodge_bonus": 0.12, "enemy_expose_start": 1,
        "desc": "Materia oscura: +22% ATQ, +12% Esquiva y el rival empieza Vulnerable (1t).",
    },
]

# =====================================================================
# CATÁLOGO DE LAS 30 CRIATURAS (CON HABILIDAD PASIVA ÚNICA + 4 ACTIVAS)
# =====================================================================
CREATURES = {
    # ===================== LÍNEA 1: BRASA (Fuego / Fallas) =====================
    "masclet": {
        "id": "masclet", "num": 1, "name": "Mascletín", "emoji": "🧨",
        "element": "brasa", "rarity": "comun", "stage": 1, "family": "masclet",
        "base_hp": 90, "base_atk": 22, "catch_rate": 0.65, "wild_weight": 30,
        "evolves_to": "pirodrac", "evolve_level": 5,
        "desc": "Pequeño espíritu travieso de brasa y pólvora. Cuando se emociona suelta chispas naranjas.",
        "passive": {
            "name": "Mecha Corta", "emoji": "🧨", "scope": "self",
            "burn_bonus": 0.15, "atk_mult": 0.08,
            "desc": "[Propia] +8% ATQ propio y +15% probabilidad de Quemadura.",
        },
        "skills": [
            {"name": "Chispazo", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "burn": (0.25, 2),
             "desc": "Ataque rápido de brasas (25% prob. de quemar 2 turnos)."},
            {"name": "Ráfaga de Petardos", "emoji": "🧨", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.48, "hits": (2, 3), "expose": 2,
             "desc": "Lanza 2-3 petardos seguidos y deja Vulnerable al rival (+30% daño recibido)."},
            {"name": "Pólvora Viva", "emoji": "♨️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.60, "team_atk_buff": 0.18, "burn": (0.50, 2),
             "desc": "Enciende al equipo (+18% ATQ a tus 3 Trobimons) y 50% prob. de quemar."},
            {"name": "Traca Valenciana", "emoji": "💥", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.50, "crit_bonus": 0.30, "pierce": True,
             "desc": "Definitiva: explosión perforante con +30% prob. de golpe crítico."},
        ],
    },
    "pirodrac": {
        "id": "pirodrac", "num": 2, "name": "Pirodrac", "emoji": "🐉",
        "element": "brasa", "rarity": "raro", "stage": 2, "family": "masclet",
        "base_hp": 150, "base_atk": 38, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "ignifoc", "evolve_level": 12,
        "desc": "Draconiano de fuego con alas de bengala dorada. Surca el cielo nocturno dejando estelas de luz.",
        "passive": {
            "name": "Calor de Falla", "emoji": "🔥", "scope": "team",
            "team_atk_mult": 0.10, "team_burn_bonus": 0.12,
            "desc": "[Equipo] Otorga +10% ATQ y +12% prob. de Quemadura a todo tu equipo.",
        },
        "skills": [
            {"name": "Colmillo Ígneo", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.05, "burn": (0.35, 2),
             "desc": "Mordisco ardiente (35% prob. de quemar 2 turnos)."},
            {"name": "Escamas Candentes", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.70, "shield_pct": 0.45, "thorns": (0.35, 2),
             "desc": "Activa Escudo (-45% daño) y quema al atacante devolviendo 35% de daño."},
            {"name": "Vuelo de Bengala", "emoji": "🚀", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.52, "hits": (2, 3), "team_atk_buff": 0.18,
             "desc": "Bombardeo de 2-3 impactos que inspira +18% ATQ a todo tu equipo."},
            {"name": "Aliento de Mascletà", "emoji": "🌋", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.60, "burn": (0.70, 3), "pierce": True, "expose": 2,
             "desc": "Definitiva: llamarada que ignora escudos, quema 3t y deja Vulnerable."},
        ],
    },
    "ignifoc": {
        "id": "ignifoc", "num": 3, "name": "Ignifoc", "emoji": "🌋",
        "element": "brasa", "rarity": "legendario", "stage": 3, "family": "masclet",
        "base_hp": 255, "base_atk": 68, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Soberano ancestral de la Cremà envuelto en llamas solares y armadura de obsidiana y oro.",
        "passive": {
            "name": "Aura de la Cremà", "emoji": "☀️", "scope": "team",
            "team_atk_mult": 0.16, "enemy_burn_aura": 0.05,
            "desc": "[Equipo/Rival] +16% ATQ a tu equipo y quema al rival activo un -5% HP cada turno.",
        },
        "skills": [
            {"name": "Garra Solar", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.12, "burn": (0.40, 2),
             "desc": "Zarpazo incandescente (40% prob. de quemar 2 turnos)."},
            {"name": "Coraza de Magma", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.55, "heal_pct": 0.20, "cleanse": True,
             "desc": "Purifica estados, cura 20% HP y activa Escudo de obsidiana (-55% daño)."},
            {"name": "Juicio de Ceniza", "emoji": "☄️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 1.25, "exec_bonus": (0.50, 0.55), "team_atk_buff": 0.22,
             "desc": "Sube +22% ATQ a todo tu equipo e inflige +55% daño si el rival tiene <50% HP."},
            {"name": "Nit de la Cremà", "emoji": "☀️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.85, "burn": (0.90, 3), "pierce": True, "crit_bonus": 0.30,
             "desc": "Definitiva: cataclismo solar que ignora escudos y abrasa al enemigo."},
        ],
    },

    # ===================== LÍNEA 2: LAGUNA (Agua / Albufera) =====================
    "goris": {
        "id": "goris", "num": 4, "name": "Goris", "emoji": "🫧",
        "element": "laguna", "rarity": "comun", "stage": 1, "family": "goris",
        "base_hp": 100, "base_atk": 19, "catch_rate": 0.65, "wild_weight": 30,
        "evolves_to": "mariscor", "evolve_level": 5,
        "desc": "Criatura anfibia cristalina que habita en aguas tranquilas y brilla bajo la luna.",
        "passive": {
            "name": "Piel Húmeda", "emoji": "💧", "scope": "self",
            "self_regen_pct": 0.05,
            "desc": "[Propia] Regenera automáticamente un 5% de su HP máximo en cada turno.",
        },
        "skills": [
            {"name": "Chorro Cristalino", "emoji": "💧", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0,
             "desc": "Disparo de agua pura a presión."},
            {"name": "Escarcha Salina", "emoji": "❄️", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.85, "weaken": 0.20, "freeze_cd": 1,
             "desc": "Enfría al rival: baja su ATQ -20% y retrasa +1 turno sus habilidades."},
            {"name": "Rocío de la Albufera", "emoji": "🫧", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.35, "shield_pct": 0.45, "team_heal_pct": 0.18, "cleanse": True,
             "desc": "Limpia estados, activa Escudo (-45%) y cura 18% HP a TODO tu equipo."},
            {"name": "Torbellino Albufera", "emoji": "🌊", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.45, "stun_chance": 0.35,
             "desc": "Definitiva: remolino acuático con 35% prob. de aturdir al rival."},
        ],
    },
    "mariscor": {
        "id": "mariscor", "num": 5, "name": "Mariscor", "emoji": "🌊",
        "element": "laguna", "rarity": "raro", "stage": 2, "family": "goris",
        "base_hp": 165, "base_atk": 35, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "leviamar", "evolve_level": 12,
        "desc": "Guardián del arrecife protegido por placas de coral turquesa y chorros de agua a presión.",
        "passive": {
            "name": "Coraza de Arrecife", "emoji": "🪸", "scope": "team",
            "team_dmg_reduction": 0.08, "self_regen_pct": 0.04,
            "desc": "[Equipo] Reduce -8% el daño que recibe tu equipo y se regenera 4% HP/turno.",
        },
        "skills": [
            {"name": "Lanza de Coral", "emoji": "💧", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.05,
             "desc": "Estocada acuática reforzada con coral."},
            {"name": "Arrecife Espinoso", "emoji": "🪸", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.75, "thorns": (0.40, 2), "weaken": 0.20,
             "desc": "Baja -20% ATQ al rival y refleja 40% del daño recibido durante 2 turnos."},
            {"name": "Marea Sanadora", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.22, "shield_pct": 0.45, "cleanse": True,
             "desc": "Purifica, restaura 22% HP a todo tu equipo y levanta Escudo (-45% daño)."},
            {"name": "Cañón Hidráulico", "emoji": "🌊", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.60, "stun_chance": 0.42, "expose": 2,
             "desc": "Definitiva: impacto abisal (42% aturdir) que deja Vulnerable al rival."},
        ],
    },
    "leviamar": {
        "id": "leviamar", "num": 6, "name": "Leviamar", "emoji": "🔱",
        "element": "laguna", "rarity": "legendario", "stage": 3, "family": "goris",
        "base_hp": 270, "base_atk": 64, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Leviatán mítico del Mediterráneo con aletas bioluminiscentes y perlas abisales.",
        "passive": {
            "name": "Bendición Abisal", "emoji": "🔱", "scope": "team",
            "team_regen_pct": 0.05, "team_dmg_reduction": 0.10,
            "desc": "[Equipo] Todo tu equipo regenera +5% HP por turno y recibe -10% de daño.",
        },
        "skills": [
            {"name": "Azote Abisal", "emoji": "💧", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.10, "lifesteal": 0.22,
             "desc": "Golpe de marea que absorbe un 22% del daño como vida."},
            {"name": "Presión de Fosa", "emoji": "❄️", "role": "🎯 Control", "cd": 2, "dmg_mult": 1.15, "weaken": 0.25, "freeze_cd": 1, "expose": 2,
             "desc": "Aplasta al enemigo: -25% ATQ rival, +1t a sus recargas y Vulnerable."},
            {"name": "Santuario Marino", "emoji": "🫧", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.55, "team_heal_pct": 0.28, "shield_pct": 0.55, "cleanse": True,
             "desc": "Purifica, cura 28% HP a TODO tu equipo y envuelve en Escudo (-55% daño)."},
            {"name": "Ira de Poseidón", "emoji": "🔱", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.75, "stun_chance": 0.55, "pierce": True,
             "desc": "Definitiva: tsunami colosal que perfora escudos (55% prob. de aturdir)."},
        ],
    },

    # ===================== LÍNEA 3: HUERTA (Naturaleza / Azahar) =====================
    "tarongin": {
        "id": "tarongin", "num": 7, "name": "Tarongín", "emoji": "🍊",
        "element": "huerta", "rarity": "comun", "stage": 1, "family": "tarongin",
        "base_hp": 95, "base_atk": 20, "catch_rate": 0.65, "wild_weight": 30,
        "evolves_to": "citrioso", "evolve_level": 5,
        "desc": "Espíritu redondo de azahar y cítrico. Desprende un aroma dulce que revitaliza al equipo.",
        "passive": {
            "name": "Esencia Cítrica", "emoji": "🍊", "scope": "team",
            "team_heal_boost": 0.18,
            "desc": "[Equipo] Aumenta un +18% todas las curaciones y robos de vida de tu equipo.",
        },
        "skills": [
            {"name": "Látigo de Hoja", "emoji": "🌿", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.0, "lifesteal": 0.22,
             "desc": "Corte vegetal que drena un 22% del daño en salud."},
            {"name": "Esporas de Azahar", "emoji": "🧪", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.80, "poison": (0.75, 3), "weaken": 0.15,
             "desc": "75% prob. de envenenar 3 turnos (reduce curación rival) y -15% ATQ."},
            {"name": "Aroma de Huerta", "emoji": "🍊", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.35, "team_heal_pct": 0.22, "atk_buff": 0.18, "cleanse": True,
             "desc": "Purifica estados, cura 22% HP a todo tu equipo y sube +18% ATQ."},
            {"name": "Bomba Cítrica", "emoji": "💥", "role": "🩸 Drenaje", "cd": 3, "dmg_mult": 1.50, "lifesteal": 0.38, "expose": 2,
             "desc": "Definitiva: estallido ácido que te cura el 38% del daño y deja Vulnerable."},
        ],
    },
    "citrioso": {
        "id": "citrioso", "num": 8, "name": "Citrioso", "emoji": "🍃",
        "element": "huerta", "rarity": "raro", "stage": 2, "family": "tarongin",
        "base_hp": 160, "base_atk": 36, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "arborion", "evolve_level": 12,
        "desc": "Bestia feroz del bosque con pelaje de musgo, garras de corteza y hombreras de cristal ámbar.",
        "passive": {
            "name": "Instinto Salvaje", "emoji": "🐾", "scope": "self",
            "berserk_atk": 0.35,
            "desc": "[Propia] Cuando tiene menos del 50% de vida, su ATQ aumenta un +35%.",
        },
        "skills": [
            {"name": "Zarpazo de Corteza", "emoji": "🌿", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.05, "lifesteal": 0.25,
             "desc": "Ataque salvaje que roba un 25% del daño infligido."},
            {"name": "Zarzal Venenoso", "emoji": "🌵", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.85, "poison": (0.80, 3), "thorns": (0.35, 2),
             "desc": "Envenena 3 turnos (80% prob.) y envuelve en zarzas que reflejan 35% de daño."},
            {"name": "Raíces Vivas", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.50, "team_heal_pct": 0.24, "shield_pct": 0.45,
             "desc": "Se enraíza: cura 24% HP a todo tu equipo y gana Escudo (-45% daño)."},
            {"name": "Furia de la Huerta", "emoji": "🌳", "role": "🩸 Drenaje", "cd": 3, "dmg_mult": 1.60, "lifesteal": 0.45, "atk_buff": 0.22,
             "desc": "Definitiva: embestida natural que drena 45% de vida y aumenta ATQ +22%."},
        ],
    },
    "arborion": {
        "id": "arborion", "num": 9, "name": "Arborión", "emoji": "🌳",
        "element": "huerta", "rarity": "epico", "stage": 3, "family": "tarongin",
        "base_hp": 245, "base_atk": 57, "catch_rate": 0.14, "wild_weight": 2,
        "evolves_to": None, "evolve_level": None,
        "desc": "Coloso milenario de raíces doradas y runas esmeralda que protege los huertos sagrados.",
        "passive": {
            "name": "Corteza de Esporas", "emoji": "🌳", "scope": "enemy",
            "counter_poison": 0.40, "team_hp_mult": 0.12,
            "desc": "[Equipo/Rival] +12% HP a tu equipo y 40% prob. de envenenar al rival cuando te golpea.",
        },
        "skills": [
            {"name": "Mazo Ancestral", "emoji": "🌿", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.10, "lifesteal": 0.30,
             "desc": "Golpe sísmico con raíces que drena un 30% del daño en vida."},
            {"name": "Polen Maldito", "emoji": "☠️", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.90, "poison": (0.90, 3), "weaken": 0.25, "thorns": (0.40, 2),
             "desc": "Envenena 3t, reduce -25% ATQ rival y activa Espinas (40% reflejo)."},
            {"name": "Bendición del Bosque", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.50, "team_heal_pct": 0.30, "shield_pct": 0.50, "cleanse": True,
             "desc": "Purifica estados, restaura 30% HP a TODO tu equipo y activa Escudo (-50%)."},
            {"name": "Juicio del Árbol Sagrado", "emoji": "🌳", "role": "🩸 Drenaje", "cd": 3, "dmg_mult": 1.70, "lifesteal": 0.50, "stun_chance": 0.40,
             "desc": "Definitiva: atrapa con raíces doradas, drena 50% del daño y puede aturdir."},
        ],
    },

    # ===================== LÍNEA 4: SOMBRA (Noche / Murciélago) =====================
    "ratpenat": {
        "id": "ratpenat", "num": 10, "name": "Ratpenat", "emoji": "🦇",
        "element": "sombra", "rarity": "comun", "stage": 1, "family": "ratpenat",
        "base_hp": 85, "base_atk": 24, "catch_rate": 0.60, "wild_weight": 25,
        "evolves_to": "noctulord", "evolve_level": 8,
        "desc": "Murciélago místico de terciopelo morado con una luna creciente dorada en la frente.",
        "passive": {
            "name": "Hijo de la Noche", "emoji": "🦇", "scope": "self",
            "self_dodge": 0.12, "self_lifesteal": 0.10,
            "desc": "[Propia] Tiene +12% de Esquiva natural y +10% de Robo de Vida en sus ataques.",
        },
        "skills": [
            {"name": "Mordisco Vampírico", "emoji": "🦇", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.0, "lifesteal": 0.32,
             "desc": "Colmillos sombríos que absorben un 32% del daño causado."},
            {"name": "Colmillo Venenoso", "emoji": "☠️", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.95, "poison": (0.75, 3), "expose": 2,
             "desc": "Inyecta toxina nocturna (75% veneno 3t) y deja Vulnerable al rival."},
            {"name": "Robo de Sombra", "emoji": "🎭", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.80, "steal_buff": True, "eva_buff": 0.30,
             "desc": "Roba el Escudo y mejoras de ATQ del rival y gana 30% esquiva por 1 turno."},
            {"name": "Chillido Ultrasónico", "emoji": "🟣", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.55, "pierce": True, "stun_chance": 0.35,
             "desc": "Definitiva: onda sónica que ignora escudos (35% prob. de aturdir)."},
        ],
    },
    "noctulord": {
        "id": "noctulord", "num": 11, "name": "Noctulord", "emoji": "🌑",
        "element": "sombra", "rarity": "epico", "stage": 2, "family": "ratpenat",
        "base_hp": 215, "base_atk": 61, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Caballero alado de la medianoche con capa de nebulosa estelar y garras de neón violeta.",
        "passive": {
            "name": "Terror Nocturno", "emoji": "🌑", "scope": "enemy",
            "enemy_atk_debuff": 0.15, "self_lifesteal": 0.12,
            "desc": "[Rival] Intimida al equipo enemigo reduciendo su ATQ un -15% y gana +12% Drenaje.",
        },
        "skills": [
            {"name": "Guadaña Umbría", "emoji": "🌙", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.10, "lifesteal": 0.35, "crit_bonus": 0.15,
             "desc": "Tajo sombrío que drena 35% de vida (+15% prob. crítico)."},
            {"name": "Danza de Sombras", "emoji": "🗡️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.55, "hits": (2, 3), "poison": (0.75, 3), "expose": 2,
             "desc": "2-3 cortes fugaces que envenenan (75%) y dejan Vulnerable al enemigo."},
            {"name": "Usurpación Oscura", "emoji": "🌑", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.90, "steal_buff": True, "atk_buff": 0.25, "eva_buff": 0.35,
             "desc": "Roba escudos/buffs rivales, sube +25% ATQ y gana 35% esquiva."},
            {"name": "Pesadilla Carmesí", "emoji": "🦇", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "lifesteal": 0.45, "pierce": True, "exec_bonus": (0.50, 0.55),
             "desc": "Definitiva: perfora defensas, drena 45% vida y hace +55% si el rival tiene <50% HP."},
        ],
    },

    # ===================== LÍNEA 5: ASTRAL (Cyber / Plasma) =====================
    "voltbit": {
        "id": "voltbit", "num": 12, "name": "Voltbit", "emoji": "⚡",
        "element": "astral", "rarity": "raro", "stage": 1, "family": "voltbit",
        "base_hp": 120, "base_atk": 32, "catch_rate": 0.35, "wild_weight": 10,
        "evolves_to": "cyberkitsune", "evolve_level": 10,
        "desc": "Zorro espiritual cibernético con pelaje de plasma cian y anillos de energía flotantes.",
        "passive": {
            "name": "Núcleo de Plasma", "emoji": "⚡", "scope": "self",
            "self_crit": 0.15, "start_shield": 0.25,
            "desc": "[Propia] Empieza el combate con un Escudo (-25% daño) y +15% prob. de Crítico.",
        },
        "skills": [
            {"name": "Pulso de Plasma", "emoji": "⚡", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.05, "crit_bonus": 0.20,
             "desc": "Descarga veloz de energía (+20% prob. de crítico)."},
            {"name": "Descarga Binaria", "emoji": "💠", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.45, "hits": (2, 4), "expose": 2,
             "desc": "Dispara de 2 a 4 pulsos láser y aplica Vulnerable (+30% daño) por 2 turnos."},
            {"name": "Overclock", "emoji": "🔋", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.80, "atk_buff": 0.30, "haste_cd": 1,
             "desc": "Acelera circuitos: sube +30% ATQ y reduce -1 turno tus recargas."},
            {"name": "Rayo Orbital", "emoji": "💫", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "pierce": True, "crit_bonus": 0.35,
             "desc": "Definitiva: láser astral que perfora escudos con +35% prob. crítica."},
        ],
    },
    "cyberkitsune": {
        "id": "cyberkitsune", "num": 13, "name": "Cyberkitsune", "emoji": "🦊",
        "element": "astral", "rarity": "legendario", "stage": 2, "family": "voltbit",
        "base_hp": 260, "base_atk": 70, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Zorro astral de nueve colas de relámpago y armadura dorada capaz de doblar el espacio.",
        "passive": {
            "name": "Matriz Nueve Colas", "emoji": "🦊", "scope": "team",
            "team_crit_bonus": 0.16, "start_shield": 0.35,
            "desc": "[Equipo] Da +16% Prob. de Crítico a todo tu equipo y empieza con Escudo (-35%).",
        },
        "skills": [
            {"name": "Relámpago Nueve Colas", "emoji": "⚡", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.12, "crit_bonus": 0.25,
             "desc": "Ráfaga de plasma cian y oro (+25% prob. de crítico)."},
            {"name": "Andanada Cuántica", "emoji": "☄️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.50, "hits": (3, 4), "freeze_cd": 1,
             "desc": "Ataca de 3 a 4 veces seguidas y retrasa +1 turno las recargas del rival."},
            {"name": "Salto Temporal", "emoji": "✨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.80, "shield_pct": 0.50, "team_atk_buff": 0.22, "haste_cd": 1,
             "desc": "Escudo (-50%), sube +22% ATQ a todo tu equipo y reduce -1t tus recargas."},
            {"name": "Tormenta Cósmica", "emoji": "🦊", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.85, "stun_chance": 0.48, "pierce": True, "crit_bonus": 0.30,
             "desc": "Definitiva: tempestad astral que ignora escudos y puede paralizar."},
        ],
    },

    # ===================== LÍNEA 6: ROCA (Montaña / Penyagolosa) =====================
    "pedrisca": {
        "id": "pedrisca", "num": 14, "name": "Pedrisca", "emoji": "🪨",
        "element": "roca", "rarity": "comun", "stage": 1, "family": "pedrisca",
        "base_hp": 115, "base_atk": 18, "catch_rate": 0.65, "wild_weight": 28,
        "evolves_to": "rocafort", "evolve_level": 5,
        "desc": "Pequeño gólem de piedra caliza con cristales de cuarzo turquesa que rueda por las laderas del Penyagolosa.",
        "passive": {
            "name": "Cuerpo de Cuarzo", "emoji": "🪨", "scope": "self",
            "self_dmg_red": 0.10, "self_thorns": 0.15,
            "desc": "[Propia] Recibe -10% de daño y devuelve un 15% del daño recibido como Espinas.",
        },
        "skills": [
            {"name": "Pedrada Sísmica", "emoji": "🪨", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "stun_chance": 0.18,
             "desc": "Impacto rocoso contundente (18% prob. de aturdir)."},
            {"name": "Bastión de Cuarzo", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.55, "shield_pct": 0.55, "thorns": (0.40, 2),
             "desc": "Se endurece: Escudo (-55% daño) y Espinas de cuarzo (40% reflejo por 2t)."},
            {"name": "Temblor de Tierra", "emoji": "⛰️", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.95, "weaken": 0.22, "expose": 2,
             "desc": "Sacude el suelo: reduce -22% el ATQ rival y lo deja Vulnerable."},
            {"name": "Avalancha Caliza", "emoji": "💥", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.55, "stun_chance": 0.40,
             "desc": "Definitiva: derrumbe de rocas con 40% prob. de aturdir al rival."},
        ],
    },
    "rocafort": {
        "id": "rocafort", "num": 15, "name": "Rocafort", "emoji": "⛰️",
        "element": "roca", "rarity": "raro", "stage": 2, "family": "pedrisca",
        "base_hp": 185, "base_atk": 33, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "titangolosa", "evolve_level": 12,
        "desc": "Guardián acorazado de granito y gemas brillantes con puños sísmicos capaces de partir montañas.",
        "passive": {
            "name": "Muro de Granito", "emoji": "⛰️", "scope": "team",
            "team_dmg_reduction": 0.10, "self_thorns": 0.20,
            "desc": "[Equipo] Reduce -10% el daño recibido por todo tu equipo y tiene 20% Espinas.",
        },
        "skills": [
            {"name": "Puño de Granito", "emoji": "🪨", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.05, "stun_chance": 0.22,
             "desc": "Puñetazo tectónico (22% prob. de aturdir)."},
            {"name": "Muralla de Cristal", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.60, "shield_pct": 0.60, "thorns": (0.45, 2), "heal_pct": 0.18,
             "desc": "Cura 18% HP, levanta Muralla (-60% daño) y refleja 45% del daño."},
            {"name": "Falla Tectónica", "emoji": "⛰️", "role": "🎯 Control", "cd": 2, "dmg_mult": 1.10, "weaken": 0.25, "expose": 2,
             "desc": "Abre una grieta bajo el rival: -25% ATQ y Vulnerable por 2 turnos."},
            {"name": "Impacto Meteórico", "emoji": "☄️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.85, "recoil_pct": 0.10, "pierce": True,
             "desc": "Definitiva: embestida colosal que perfora escudos (cuesta 10% de tu HP actual)."},
        ],
    },
    "titangolosa": {
        "id": "titangolosa", "num": 16, "name": "Titangolosa", "emoji": "🏔️",
        "element": "roca", "rarity": "legendario", "stage": 3, "family": "pedrisca",
        "base_hp": 300, "base_atk": 60, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Coloso ancestral de la cumbre sagrada con núcleo de diamante y armadura de basalto dorado.",
        "passive": {
            "name": "Bastión del Penyagolosa", "emoji": "🏔️", "scope": "team",
            "team_dmg_reduction": 0.15, "team_hp_mult": 0.15,
            "desc": "[Equipo] Otorga +15% HP máximo y -15% daño recibido a TODO tu equipo.",
        },
        "skills": [
            {"name": "Martillo de Basalto", "emoji": "🪨", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.12, "stun_chance": 0.25,
             "desc": "Golpe de monolito que hace temblar la tierra (25% aturdir)."},
            {"name": "Égida de Diamante", "emoji": "💎", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.65, "thorns": (0.55, 2), "team_heal_pct": 0.20,
             "desc": "Escudo de diamante (-65% daño), 55% Espinas y cura 20% HP a todo tu equipo."},
            {"name": "Rugido de la Cumbre", "emoji": "🏔️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 1.10, "team_atk_buff": 0.22, "weaken": 0.25, "expose": 2,
             "desc": "Sube +22% ATQ a tu equipo, baja -25% ATQ al rival y lo deja Vulnerable."},
            {"name": "Cataclismo del Penyagolosa", "emoji": "🌋", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.95, "pierce": True, "stun_chance": 0.50, "recoil_pct": 0.08,
             "desc": "Definitiva: lanza una montaña entera ignorando escudos (50% prob. de aturdir)."},
        ],
    },

    # ===================== LÍNEA 7: ESCARCHA (Hielo / Glaciar) =====================
    "granizet": {
        "id": "granizet", "num": 17, "name": "Granizet", "emoji": "🍧",
        "element": "hielo", "rarity": "comun", "stage": 1, "family": "granizet",
        "base_hp": 92, "base_atk": 21, "catch_rate": 0.65, "wild_weight": 28,
        "evolves_to": "gelidrak", "evolve_level": 5,
        "desc": "Espíritu helado de escarcha y chufa cristalizada que congela el aire a su alrededor.",
        "passive": {
            "name": "Frío Dulce", "emoji": "🍧", "scope": "enemy",
            "enemy_atk_debuff": 0.08, "self_stun_bonus": 0.10,
            "desc": "[Rival] El aire helado reduce un -8% el ATQ del rival y da +10% prob. de congelar.",
        },
        "skills": [
            {"name": "Esquirla Helada", "emoji": "❄️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "crit_bonus": 0.15,
             "desc": "Lanza cristales afilados de hielo (+15% prob. crítico)."},
            {"name": "Ráfaga de Granizo", "emoji": "🌨️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.46, "hits": (2, 3), "freeze_cd": 1,
             "desc": "Golpea 2-3 veces con granizo y retrasa +1 turno las recargas del rival."},
            {"name": "Velo Polar", "emoji": "🧊", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.50, "shield_pct": 0.50, "heal_pct": 0.22,
             "desc": "Se recubre de hielo puro: cura 22% HP y activa Escudo (-50% daño)."},
            {"name": "Cero Absoluto", "emoji": "❄️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.48, "stun_chance": 0.42, "expose": 2,
             "desc": "Definitiva: congela al enemigo (42% aturdir) y lo deja Vulnerable."},
        ],
    },
    "gelidrak": {
        "id": "gelidrak", "num": 18, "name": "Gelidrak", "emoji": "❄️",
        "element": "hielo", "rarity": "raro", "stage": 2, "family": "granizet",
        "base_hp": 152, "base_atk": 37, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "glaciorex", "evolve_level": 12,
        "desc": "Wyvern de hielo cristalino con alas de ventisca ártica y cuernos de zafiro congelado.",
        "passive": {
            "name": "Escarcha Entumecedora", "emoji": "❄️", "scope": "enemy",
            "enemy_atk_debuff": 0.12, "self_stun_bonus": 0.12,
            "desc": "[Rival] Entumece al enemigo (-12% ATQ rival) y gana +12% prob. de congelar.",
        },
        "skills": [
            {"name": "Colmillo Glaciar", "emoji": "❄️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.06, "crit_bonus": 0.20,
             "desc": "Mordisco bajo cero (+20% prob. crítico)."},
            {"name": "Lluvia de Carámbanos", "emoji": "🌨️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.50, "hits": (2, 4), "freeze_cd": 1,
             "desc": "Dispara de 2 a 4 carámbanos y retrasa +1 turno las habilidades del rival."},
            {"name": "Armadura de Escarcha", "emoji": "🧊", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.50, "thorns": (0.35, 2), "weaken": 0.20,
             "desc": "Escudo (-50%), Espinas de hielo (35%) y baja -20% ATQ al rival."},
            {"name": "Aliento Boreal", "emoji": "🌬️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.62, "stun_chance": 0.48, "pierce": True,
             "desc": "Definitiva: ventisca perforante con 48% prob. de congelar al enemigo."},
        ],
    },
    "glaciorex": {
        "id": "glaciorex", "num": 19, "name": "Glaciorex", "emoji": "🧊",
        "element": "hielo", "rarity": "epico", "stage": 3, "family": "granizet",
        "base_hp": 240, "base_atk": 60, "catch_rate": 0.14, "wild_weight": 2,
        "evolves_to": None, "evolve_level": None,
        "desc": "Emperador de la ventisca eterna con armadura de cristal polar y aliento de cero absoluto.",
        "passive": {
            "name": "Presencia bajo Cero", "emoji": "🧊", "scope": "enemy",
            "enemy_atk_debuff": 0.16, "self_stun_bonus": 0.15,
            "desc": "[Rival] Reduce un -16% el ATQ de todo el equipo rival y +15% prob. de congelar.",
        },
        "skills": [
            {"name": "Garra del Ártico", "emoji": "❄️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.10, "crit_bonus": 0.22,
             "desc": "Zarpazo de hielo imperial (+22% prob. crítico)."},
            {"name": "Tormenta de Zafiro", "emoji": "🌨️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.52, "hits": (3, 4), "freeze_cd": 1, "weaken": 0.22,
             "desc": "3-4 impactos helados que retrasan +1t los CDs rivales y bajan -22% su ATQ."},
            {"name": "Trono Glacial", "emoji": "🧊", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.60, "shield_pct": 0.55, "heal_pct": 0.28, "cleanse": True,
             "desc": "Purifica estados, restaura 28% HP y activa Escudo polar (-55% daño)."},
            {"name": "Era Glacial", "emoji": "❄️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.75, "stun_chance": 0.55, "pierce": True, "exec_bonus": (0.50, 0.45),
             "desc": "Definitiva: congela el campo ignorando escudos (55% congelar y +45% daño si <50% HP)."},
        ],
    },

    # ===================== LÍNEA 8: CÉFIRO (Viento / Cielo Mediterráneo) =====================
    "brisolin": {
        "id": "brisolin", "num": 20, "name": "Brisolín", "emoji": "🍃",
        "element": "viento", "rarity": "comun", "stage": 1, "family": "brisolin",
        "base_hp": 88, "base_atk": 23, "catch_rate": 0.65, "wild_weight": 28,
        "evolves_to": "vendaval", "evolve_level": 6,
        "desc": "Pequeño grifo alado de las brisas mediterráneas con plumas blancas y doradas.",
        "passive": {
            "name": "Pluma Ligera", "emoji": "🍃", "scope": "self",
            "self_dodge": 0.14,
            "desc": "[Propia] Las corrientes de aire le dan un +14% de probabilidad de Esquiva.",
        },
        "skills": [
            {"name": "Picotazo Veloz", "emoji": "🌪️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.02, "crit_bonus": 0.18,
             "desc": "Ataque aéreo relámpago (+18% prob. de crítico)."},
            {"name": "Corriente Ascendente", "emoji": "🍃", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.75, "eva_buff": 0.35, "haste_cd": 1, "atk_buff": 0.18,
             "desc": "Gana 35% de esquiva, sube +18% ATQ y reduce -1 turno tus recargas."},
            {"name": "Viento de Levante", "emoji": "🌬️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.60, "team_heal_pct": 0.18, "team_atk_buff": 0.15,
             "desc": "Brisa revitalizante: cura 18% HP y sube +15% ATQ a TODO tu equipo."},
            {"name": "Ciclón Costero", "emoji": "🌪️", "role": "⚡ Ráfaga", "cd": 3, "dmg_mult": 0.55, "hits": (2, 3), "pierce": True,
             "desc": "Definitiva: tornado que golpea 2-3 veces ignorando escudos."},
        ],
    },
    "vendaval": {
        "id": "vendaval", "num": 21, "name": "Vendaval", "emoji": "🌪️",
        "element": "viento", "rarity": "raro", "stage": 2, "family": "brisolin",
        "base_hp": 148, "base_atk": 39, "catch_rate": 0.32, "wild_weight": 7,
        "evolves_to": "huracanor", "evolve_level": 13,
        "desc": "Halcón imperial de las tormentas costeras que genera ciclones con cada batir de alas.",
        "passive": {
            "name": "Brisa de Cola", "emoji": "🌪️", "scope": "team",
            "team_dodge_bonus": 0.10, "team_crit_bonus": 0.08,
            "desc": "[Equipo] Otorga +10% Esquiva y +8% Prob. de Crítico a todo tu equipo.",
        },
        "skills": [
            {"name": "Ala Cortante", "emoji": "🌪️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.06, "crit_bonus": 0.22,
             "desc": "Ráfaga cortante de aire comprimido (+22% prob. crítico)."},
            {"name": "Evasión Supersónica", "emoji": "💨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.85, "eva_buff": 0.42, "haste_cd": 1, "atk_buff": 0.22,
             "desc": "Otorga 42% prob. de esquivar, +22% ATQ y reduce -1t tus enfriamientos."},
            {"name": "Impulso de Cola", "emoji": "🦅", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.70, "team_heal_pct": 0.20, "team_atk_buff": 0.20, "cleanse": True,
             "desc": "Purifica, cura 20% HP y aumenta +20% ATQ a todo tu equipo de 3."},
            {"name": "Tifón Esmeralda", "emoji": "🌪️", "role": "⚡ Ráfaga", "cd": 3, "dmg_mult": 0.58, "hits": (3, 3), "pierce": True, "crit_bonus": 0.25,
             "desc": "Definitiva: triple embestida aérea que perfora escudos (+25% crítico)."},
        ],
    },
    "huracanor": {
        "id": "huracanor", "num": 22, "name": "Huracanor", "emoji": "🦅",
        "element": "viento", "rarity": "legendario", "stage": 3, "family": "brisolin",
        "base_hp": 250, "base_atk": 71, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Señor supremo de los cielos mediterráneos con cuatro alas de relámpago esmeralda y armadura eólica.",
        "passive": {
            "name": "Señor de los Vientos", "emoji": "🦅", "scope": "team",
            "team_dodge_bonus": 0.14, "team_crit_bonus": 0.14,
            "desc": "[Equipo] Otorga +14% de Esquiva y +14% de Crítico a tus 3 Trobimons.",
        },
        "skills": [
            {"name": "Garra del Céfiro", "emoji": "🌪️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.14, "crit_bonus": 0.25,
             "desc": "Picado celestial a velocidad del sonido (+25% prob. crítico)."},
            {"name": "Danza del Huracán", "emoji": "💨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.90, "eva_buff": 0.48, "haste_cd": 1, "steal_buff": True,
             "desc": "Roba escudos/buffs rivales, gana 48% esquiva y reduce -1t tus recargas."},
            {"name": "Bendición de los Vientos", "emoji": "🦅", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.70, "team_heal_pct": 0.26, "team_atk_buff": 0.25, "cleanse": True,
             "desc": "Purifica, cura 26% HP y otorga +25% ATQ a TODO tu equipo de 3 Trobimons."},
            {"name": "Juicio de la Tempestad", "emoji": "⚡", "role": "⚡ Ráfaga", "cd": 3, "dmg_mult": 0.58, "hits": (3, 4), "pierce": True, "crit_bonus": 0.30, "expose": 2,
             "desc": "Definitiva: 3-4 impactos divinos que perforan escudos y dejan Vulnerable."},
        ],
    },

    # =====================================================================
    # 8 NUEVAS CRIATURAS ESPECIALISTAS (PARA FORMAR EQUIPOS DEL MISMO ELEMENTO)
    # =====================================================================
    "solarix": {
        "id": "solarix", "num": 23, "name": "Solarix", "emoji": "🐦‍🔥",
        "element": "brasa", "rarity": "epico", "stage": 2, "family": "solarix",
        "base_hp": 210, "base_atk": 63, "catch_rate": 0.16, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Ave fénix de fuego solar y ceniza dorada que renace de sus propias brasas en mitad del combate.",
        "passive": {
            "name": "Renacer del Fénix", "emoji": "🐦‍🔥", "scope": "self",
            "revive_pct": 0.40,
            "desc": "[Propia] La primera vez que cae a 0 HP en combate, ¡revive con el 40% de su HP!",
        },
        "skills": [
            {"name": "Ala Solar", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.08, "burn": (0.35, 2),
             "desc": "Barrido de plumas ígneas (35% prob. de quemar 2 turnos)."},
            {"name": "Plumaje de Ceniza", "emoji": "✨", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.65, "team_heal_pct": 0.22, "cleanse": True,
             "desc": "Purifica estados y cura un 22% HP a todos tus aliados vivos."},
            {"name": "Llamarada Imperial", "emoji": "☀️", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 1.15, "expose": 2, "atk_buff": 0.22,
             "desc": "Sube +22% tu ATQ y deja Vulnerable al rival por 2 turnos."},
            {"name": "Nova del Fénix", "emoji": "🐦‍🔥", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.75, "burn": (0.85, 3), "lifesteal": 0.35,
             "desc": "Definitiva: explosión de renacimiento que quema 3t y drena 35% de vida."},
        ],
    },
    "dracmar": {
        "id": "dracmar", "num": 24, "name": "Dracmar", "emoji": "🐲",
        "element": "laguna", "rarity": "epico", "stage": 2, "family": "dracmar",
        "base_hp": 230, "base_atk": 59, "catch_rate": 0.16, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Dragón serpiente de las fosas mediterráneas con escamas de zafiro luminoso y remolinos abisales.",
        "passive": {
            "name": "Furia de Marea", "emoji": "🐲", "scope": "team",
            "team_atk_mult": 0.12, "self_lifesteal": 0.12,
            "desc": "[Equipo] Da +12% ATQ a todo tu equipo y sus ataques drenan +12% de vida.",
        },
        "skills": [
            {"name": "Fauce Marina", "emoji": "💧", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.08, "crit_bonus": 0.18,
             "desc": "Mordisco dracónico de alta presión (+18% prob. crítico)."},
            {"name": "Vórtice de Zafiro", "emoji": "🌀", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.50, "hits": (2, 3), "expose": 2,
             "desc": "Golpea 2-3 veces con chorros gemelos y deja Vulnerable al enemigo."},
            {"name": "Escama Reflectante", "emoji": "🪞", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.50, "thorns": (0.40, 2),
             "desc": "Escudo de escamas (-50% daño) y devuelve 40% del daño recibido."},
            {"name": "Maelstrom Dracónico", "emoji": "🌊", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.72, "pierce": True, "stun_chance": 0.45,
             "desc": "Definitiva: abismo giratorio que perfora escudos (45% prob. de aturdir)."},
        ],
    },
    "florabella": {
        "id": "florabella", "num": 25, "name": "Florabella", "emoji": "🌸",
        "element": "huerta", "rarity": "epico", "stage": 2, "family": "florabella",
        "base_hp": 225, "base_atk": 56, "catch_rate": 0.16, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Dríade ancestral de flor de azahar y lianas esmeralda que envuelve al equipo en un aura de vida.",
        "passive": {
            "name": "Jardín Viviente", "emoji": "🌸", "scope": "team",
            "team_regen_pct": 0.06, "team_heal_boost": 0.20,
            "desc": "[Equipo] Regenera +6% HP cada turno a todo tu equipo y aumenta +20% las curaciones.",
        },
        "skills": [
            {"name": "Danza de Pétalos", "emoji": "🌸", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.06, "lifesteal": 0.28,
             "desc": "Torbellino floral que drena un 28% del daño causado."},
            {"name": "Lianas Atrapadoras", "emoji": "🌿", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.90, "weaken": 0.22, "stun_chance": 0.35,
             "desc": "Reduce -22% el ATQ del enemigo con 35% prob. de inmovilizarlo."},
            {"name": "Sinfonía de Primavera", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.30, "team_atk_buff": 0.18, "cleanse": True,
             "desc": "Purifica, cura 30% HP a TODO tu equipo y sube +18% su ATQ."},
            {"name": "Floración Celestial", "emoji": "🌺", "role": "🩸 Drenaje", "cd": 3, "dmg_mult": 1.68, "lifesteal": 0.48, "expose": 2,
             "desc": "Definitiva: explosión de azahar que roba 48% de vida y deja Vulnerable."},
        ],
    },
    "umbrawolf": {
        "id": "umbrawolf", "num": 26, "name": "Umbrawolf", "emoji": "🐺",
        "element": "sombra", "rarity": "epico", "stage": 2, "family": "umbrawolf",
        "base_hp": 210, "base_atk": 65, "catch_rate": 0.16, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Lobo espectral de niebla púrpura y colmillos de luna carmesí que lidera la caza nocturna.",
        "passive": {
            "name": "Líder de la Manada", "emoji": "🐺", "scope": "team",
            "team_atk_mult": 0.14, "team_crit_bonus": 0.10,
            "desc": "[Equipo] Su aullido otorga +14% ATQ y +10% Prob. de Crítico a todo tu equipo.",
        },
        "skills": [
            {"name": "Colmillo Lunar", "emoji": "🐺", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.10, "lifesteal": 0.25, "crit_bonus": 0.20,
             "desc": "Dentellada feroz (+20% crítico y 25% robo de vida)."},
            {"name": "Aullido de Eclipse", "emoji": "🌕", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.70, "team_atk_buff": 0.24, "weaken": 0.20,
             "desc": "Sube +24% el ATQ de todo tu equipo y reduce -20% el ATQ rival."},
            {"name": "Paso Fantasma", "emoji": "💨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.90, "eva_buff": 0.40, "steal_buff": True,
             "desc": "Roba las mejoras/escudos del rival y gana +40% de Esquiva."},
            {"name": "Cacería Sangrienta", "emoji": "🩸", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "exec_bonus": (0.55, 0.65), "pierce": True,
             "desc": "Definitiva: ignora escudos e inflige +65% de daño si el rival tiene <55% HP."},
        ],
    },
    "mechatron": {
        "id": "mechatron", "num": 27, "name": "Mechatron", "emoji": "🤖",
        "element": "astral", "rarity": "epico", "stage": 2, "family": "mechatron",
        "base_hp": 250, "base_atk": 58, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Coloso cibernético de plasma cuántico equipado con escudos de energía y cañones orbitales.",
        "passive": {
            "name": "Campo de Fuerza Cuántico", "emoji": "🤖", "scope": "team",
            "start_shield": 0.35, "team_dmg_reduction": 0.10,
            "desc": "[Equipo] Reduce -10% el daño recibido por tu equipo y empieza con Escudo (-35%).",
        },
        "skills": [
            {"name": "Cañón de Positrones", "emoji": "⚡", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.08, "crit_bonus": 0.18,
             "desc": "Disparo de energía concentrada (+18% prob. crítico)."},
            {"name": "Barrera Holográfica", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.60, "shield_pct": 0.60, "thorns": (0.45, 2), "haste_cd": 1,
             "desc": "Escudo (-60% daño), 45% Espinas láser y reduce -1t tus recargas."},
            {"name": "Bomba Electromagnética", "emoji": "💣", "role": "🎯 Control", "cd": 2, "dmg_mult": 1.05, "freeze_cd": 1, "expose": 2,
             "desc": "Retrasa +1 turno los CDs del enemigo y lo deja Vulnerable (2t)."},
            {"name": "Láser Satelital", "emoji": "🛰️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.80, "pierce": True, "stun_chance": 0.45,
             "desc": "Definitiva: impacto desde la órbita que ignora escudos (45% paralizar)."},
        ],
    },
    "geodino": {
        "id": "geodino", "num": 28, "name": "Geodino", "emoji": "🦖",
        "element": "roca", "rarity": "epico", "stage": 2, "family": "geodino",
        "base_hp": 255, "base_atk": 59, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Saurio prehistórico acorazado con placas de obsidiana volcánica y maza de cristal ámbar.",
        "passive": {
            "name": "Escamas de Obsidiana", "emoji": "🦖", "scope": "self",
            "self_thorns": 0.30, "berserk_atk": 0.35,
            "desc": "[Propia] Devuelve siempre un 30% de daño por Espinas y gana +35% ATQ con <50% HP.",
        },
        "skills": [
            {"name": "Maza de Ámbar", "emoji": "🪨", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.10, "stun_chance": 0.22,
             "desc": "Golpe brutal con su cola cristalina (22% prob. de aturdir)."},
            {"name": "Rugido Jurásico", "emoji": "🦖", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.80, "team_atk_buff": 0.22, "weaken": 0.22,
             "desc": "Aumenta +22% el ATQ de tu equipo y reduce -22% el ATQ rival."},
            {"name": "Fortaleza Fósil", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.60, "shield_pct": 0.55, "heal_pct": 0.25,
             "desc": "Recupera 25% de su HP máximo y levanta un Escudo (-55% daño)."},
            {"name": "Extinción Cretácica", "emoji": "☄️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.90, "pierce": True, "recoil_pct": 0.08,
             "desc": "Definitiva: embestida sísmica que perfora escudos con daño devastador."},
        ],
    },
    "borealis": {
        "id": "borealis", "num": 29, "name": "Borealis", "emoji": "🐅",
        "element": "hielo", "rarity": "legendario", "stage": 2, "family": "borealis",
        "base_hp": 250, "base_atk": 69, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Tigre dientes de sable mítico forjado en hielo estelar y envuelto en la luz de la aurora boreal.",
        "passive": {
            "name": "Cazador de la Aurora", "emoji": "🐅", "scope": "enemy",
            "enemy_atk_debuff": 0.15, "team_crit_bonus": 0.14,
            "desc": "[Equipo/Rival] Reduce -15% el ATQ enemigo y da +14% Crítico a todo tu equipo.",
        },
        "skills": [
            {"name": "Colmillo de Cristal", "emoji": "❄️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.14, "crit_bonus": 0.25,
             "desc": "Mordisco letal a velocidad polar (+25% prob. de crítico)."},
            {"name": "Asalto de Escarcha", "emoji": "🐾", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.54, "hits": (2, 3), "expose": 2, "freeze_cd": 1,
             "desc": "2-3 zarpazos que dejan Vulnerable al rival y retrasan +1t sus recargas."},
            {"name": "Velo de Aurora", "emoji": "🌌", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.60, "team_heal_pct": 0.24, "shield_pct": 0.50, "cleanse": True,
             "desc": "Purifica, cura 24% HP a todo tu equipo y activa Escudo (-50% daño)."},
            {"name": "Devastación Polar", "emoji": "🧊", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.85, "stun_chance": 0.52, "pierce": True, "exec_bonus": (0.50, 0.50),
             "desc": "Definitiva: perfora defensas, 52% congelar y +50% daño si el rival tiene <50% HP."},
        ],
    },
    "cefirion": {
        "id": "cefirion", "num": 30, "name": "Cefirión", "emoji": "🐉",
        "element": "viento", "rarity": "epico", "stage": 2, "family": "cefirion",
        "base_hp": 225, "base_atk": 62, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Dragón celeste de las cumbres nubladas que controla esferas de vacío y tormentas esmeralda.",
        "passive": {
            "name": "Vórtice de Vacío", "emoji": "🌪️", "scope": "enemy",
            "enemy_burn_aura": 0.05, "team_dodge_bonus": 0.12,
            "desc": "[Equipo/Rival] Da +12% Esquiva a tu equipo y corta al rival un -5% HP cada turno.",
        },
        "skills": [
            {"name": "Esfera de Vacío", "emoji": "🌪️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.08, "crit_bonus": 0.20,
             "desc": "Proyectil de aire comprimido (+20% prob. de crítico)."},
            {"name": "Ráfaga Ciclónica", "emoji": "💨", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.50, "hits": (2, 4), "haste_cd": 1,
             "desc": "Golpea de 2 a 4 veces seguidas y reduce -1 turno tus recargas."},
            {"name": "Ojo de la Tormenta", "emoji": "🌀", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.80, "steal_buff": True, "eva_buff": 0.40,
             "desc": "Roba los escudos/mejoras del enemigo y gana +40% de Esquiva."},
            {"name": "Ira del Firmamento", "emoji": "🐉", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.75, "pierce": True, "stun_chance": 0.42, "expose": 2,
             "desc": "Definitiva: tornado celestial que perfora escudos, aturde (42%) y deja Vulnerable."},
        ],
    },

    # =====================================================================
    # 18 NUEVAS CRIATURAS (#31 A #48 — 6 ESPECIES POR ELEMENTO EN TOTAL)
    # =====================================================================
    # --- BRASA (#31 Salamandrín ➔ #32 Vulcanor) ---
    "salamandrin": {
        "id": "salamandrin", "num": 31, "name": "Salamandrín", "emoji": "🦎",
        "element": "brasa", "rarity": "comun", "stage": 1, "family": "salamandrin",
        "base_hp": 102, "base_atk": 21, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "vulcanor", "evolve_level": 7,
        "desc": "Lagartija ígnea de lava naranja que habita en los hornos antiguos y escupe brasas.",
        "passive": {
            "name": "Sangre Volcánica", "emoji": "🦎", "scope": "self",
            "hp_mult": 0.12, "burn_bonus": 0.15,
            "desc": "[Propia] +12% HP máximo y +15% probabilidad de Quemadura.",
        },
        "skills": [
            {"name": "Lengüetazo de Lava", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "burn": (0.28, 2),
             "desc": "Golpe ardiente con 28% prob. de quemar 2 turnos."},
            {"name": "Piel de Magma", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.60, "shield_pct": 0.45, "thorns": (0.35, 2),
             "desc": "Escudo (-45% daño) y Espinas de lava (35% reflejo por 2t)."},
            {"name": "Humo Asfixiante", "emoji": "💨", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.85, "weaken": 0.20, "expose": 2,
             "desc": "Baja -20% el ATQ rival y lo deja Vulnerable por 2 turnos."},
            {"name": "Géiser Ígneo", "emoji": "🌋", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.52, "burn": (0.65, 3),
             "desc": "Definitiva: columna de magma con 65% prob. de quemar 3 turnos."},
        ],
    },
    "vulcanor": {
        "id": "vulcanor", "num": 32, "name": "Vulcanor", "emoji": "🦕",
        "element": "brasa", "rarity": "epico", "stage": 2, "family": "salamandrin",
        "base_hp": 238, "base_atk": 58, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Salamandra acorazada de magma fundido con cañones dorsales que disparan ceniza incandescente.",
        "passive": {
            "name": "Erupción Interna", "emoji": "🌋", "scope": "team",
            "team_atk_mult": 0.14, "self_thorns": 0.25,
            "desc": "[Equipo] Otorga +14% ATQ a todo tu equipo y devuelve 25% de daño por Espinas.",
        },
        "skills": [
            {"name": "Mordisco Piroclástico", "emoji": "🔥", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.08, "burn": (0.38, 2),
             "desc": "Fauces de roca fundida (38% prob. de quemar 2 turnos)."},
            {"name": "Bombardeo de Caldera", "emoji": "☄️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.52, "hits": (2, 3), "burn": (0.50, 2),
             "desc": "Dispara 2-3 obuses de magma con 50% prob. de quemar."},
            {"name": "Coraza Volcánica", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.55, "heal_pct": 0.22,
             "desc": "Cura 22% HP y activa un Escudo volcánico (-55% daño)."},
            {"name": "Despertar del Vesubio", "emoji": "🌋", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.75, "pierce": True, "burn": (0.85, 3),
             "desc": "Definitiva: erupción que perfora escudos y abrasa al enemigo (85% quemadura)."},
        ],
    },

    # --- LAGUNA (#33 Cangrex ➔ #34 Krakencor) ---
    "cangrex": {
        "id": "cangrex", "num": 33, "name": "Cangrex", "emoji": "🦀",
        "element": "laguna", "rarity": "comun", "stage": 1, "family": "cangrex",
        "base_hp": 106, "base_atk": 20, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "krakencor", "evolve_level": 7,
        "desc": "Cangrejo de caparazón de porcelana azul y tenazas de espuma marina.",
        "passive": {
            "name": "Pinza Férrea", "emoji": "🦀", "scope": "self",
            "self_crit": 0.14, "self_dmg_red": 0.10,
            "desc": "[Propia] Tiene +14% prob. de Crítico y recibe -10% de daño.",
        },
        "skills": [
            {"name": "Tenaza Marina", "emoji": "🦀", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.02, "crit_bonus": 0.20,
             "desc": "Pellizco a presión (+20% prob. de crítico)."},
            {"name": "Doble Pinza", "emoji": "⚡", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.54, "hits": (2, 2), "expose": 2,
             "desc": "Golpea 2 veces seguidas y deja Vulnerable al rival (2t)."},
            {"name": "Guardia de Concha", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.55, "shield_pct": 0.55, "atk_buff": 0.20,
             "desc": "Se protege (-55% daño) y afila sus pinzas (+20% ATQ)."},
            {"name": "Martillo de Marea", "emoji": "🌊", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.52, "crit_bonus": 0.30, "pierce": True,
             "desc": "Definitiva: golpe perforante con +30% prob. de crítico."},
        ],
    },
    "krakencor": {
        "id": "krakencor", "num": 34, "name": "Krakencor", "emoji": "🐙",
        "element": "laguna", "rarity": "epico", "stage": 2, "family": "cangrex",
        "base_hp": 240, "base_atk": 58, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "Kraken colosal del puerto con tentáculos bioluminiscentes y armadura de galeón hundido.",
        "passive": {
            "name": "Tentáculos del Abismo", "emoji": "🐙", "scope": "enemy",
            "enemy_atk_debuff": 0.15, "self_lifesteal": 0.15,
            "desc": "[Rival] Reduce -15% el ATQ del equipo enemigo y gana +15% Robo de Vida.",
        },
        "skills": [
            {"name": "Latigazo Tentacular", "emoji": "🐙", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.08, "lifesteal": 0.25,
             "desc": "Azote abisal que drena 25% de vida."},
            {"name": "Tinta Cegadora", "emoji": "🌑", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.85, "weaken": 0.25, "eva_buff": 0.35,
             "desc": "Baja -25% el ATQ rival y te otorga +35% de Esquiva."},
            {"name": "Abrazo del Kraken", "emoji": "🌊", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.48, "hits": (2, 4), "stun_chance": 0.35,
             "desc": "Golpea de 2 a 4 veces con sus tentáculos (35% prob. de aturdir)."},
            {"name": "Terror del Naufragio", "emoji": "🔱", "role": "🩸 Drenaje", "cd": 3, "dmg_mult": 1.72, "lifesteal": 0.40, "pierce": True,
             "desc": "Definitiva: arrastra al fondo ignorando escudos y drena 40% del daño."},
        ],
    },

    # --- HUERTA (#35 Espinach ➔ #36 Mandrágor) ---
    "espinach": {
        "id": "espinach", "num": 35, "name": "Espinach", "emoji": "🌵",
        "element": "huerta", "rarity": "comun", "stage": 1, "family": "espinach",
        "base_hp": 105, "base_atk": 20, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "mandragor", "evolve_level": 7,
        "desc": "Pequeño guerrero cactus con corona de flores amarillas y espinas esmeralda.",
        "passive": {
            "name": "Púas Verdes", "emoji": "🌵", "scope": "self",
            "self_thorns": 0.25,
            "desc": "[Propia] Devuelve automáticamente un 25% de todo el daño recibido.",
        },
        "skills": [
            {"name": "Dardo Espinoso", "emoji": "🌵", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "poison": (0.30, 2),
             "desc": "Dispara espinas con 30% prob. de envenenar 2 turnos."},
            {"name": "Lluvia de Agujas", "emoji": "⚡", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.48, "hits": (2, 3), "expose": 2,
             "desc": "2-3 impactos de agujas que dejan Vulnerable al enemigo."},
            {"name": "Savia del Desierto", "emoji": "💚", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.50, "heal_pct": 0.28, "thorns": (0.45, 2),
             "desc": "Cura 28% HP y aumenta sus Espinas al 45% durante 2 turnos."},
            {"name": "Explosión de Cactus", "emoji": "💥", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.55, "poison": (0.80, 3), "pierce": True,
             "desc": "Definitiva: estallido de púas que ignora escudos y envenena 3t."},
        ],
    },
    "mandragor": {
        "id": "mandragor", "num": 36, "name": "Mandrágor", "emoji": "🍄",
        "element": "huerta", "rarity": "raro", "stage": 2, "family": "espinach",
        "base_hp": 175, "base_atk": 38, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Guardián fúngico ancestral de esporas luminosas y raíces alquímicas.",
        "passive": {
            "name": "Alquimia del Bosque", "emoji": "🍄", "scope": "team",
            "team_regen_pct": 0.04, "team_heal_boost": 0.15,
            "desc": "[Equipo] Todo tu equipo regenera +4% HP/turno y recibe +15% de curación.",
        },
        "skills": [
            {"name": "Golpe de Micelio", "emoji": "🍄", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.05, "lifesteal": 0.28,
             "desc": "Absorbe nutrientes drenando un 28% del daño."},
            {"name": "Nube Alucinógena", "emoji": "🧪", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.85, "poison": (0.85, 3), "stun_chance": 0.35,
             "desc": "85% prob. de envenenar 3t y 35% prob. de aturdir al rival."},
            {"name": "Elixir de Raíz", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.26, "cleanse": True,
             "desc": "Purifica estados y restaura un 26% HP a TODO tu equipo."},
            {"name": "Grito de Mandrágora", "emoji": "🌳", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.62, "weaken": 0.25, "pierce": True,
             "desc": "Definitiva: grito sónico que perfora escudos y baja -25% el ATQ rival."},
        ],
    },

    # --- SOMBRA (#37 Sombrilla ➔ #38 Espectrovela, y #39 Necrodrac) ---
    "sombrilla": {
        "id": "sombrilla", "num": 37, "name": "Sombrilla", "emoji": "🕯️",
        "element": "sombra", "rarity": "comun", "stage": 1, "family": "sombrilla",
        "base_hp": 88, "base_atk": 23, "catch_rate": 0.62, "wild_weight": 26,
        "evolves_to": "espectrovela", "evolve_level": 6,
        "desc": "Pequeño fantasma de llama violeta que flota por los callejones antiguos de noche.",
        "passive": {
            "name": "Fuego Fatuo", "emoji": "🕯️", "scope": "enemy",
            "enemy_burn_aura": 0.04,
            "desc": "[Rival] Su llama espectral consume un -4% HP al rival activo cada turno.",
        },
        "skills": [
            {"name": "Llama Violeta", "emoji": "🕯️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "burn": (0.28, 2),
             "desc": "Fuego fantasmal con 28% prob. de quemar 2 turnos."},
            {"name": "Susurro del Carmen", "emoji": "👻", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.85, "weaken": 0.22, "freeze_cd": 1,
             "desc": "Asusta al rival: -22% ATQ y retrasa +1 turno sus habilidades."},
            {"name": "Drenaje de Cera", "emoji": "🩸", "role": "🩸 Drenaje", "cd": 2, "dmg_mult": 0.95, "lifesteal": 0.38, "shield_pct": 0.40,
             "desc": "Drena 38% de vida y activa Escudo espiritual (-40% daño)."},
            {"name": "Pira Espectral", "emoji": "🟣", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.52, "burn": (0.75, 3), "pierce": True,
             "desc": "Definitiva: explosión de almas que ignora escudos y quema 3t."},
        ],
    },
    "espectrovela": {
        "id": "espectrovela", "num": 38, "name": "Espectrovela", "emoji": "👻",
        "element": "sombra", "rarity": "raro", "stage": 2, "family": "sombrilla",
        "base_hp": 162, "base_atk": 41, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Espíritu candelabro de fuego fatuo morado que absorbe la vitalidad para iluminar a su equipo.",
        "passive": {
            "name": "Cosecha de Almas", "emoji": "👻", "scope": "team",
            "lifesteal_bonus": 0.12, "enemy_burn_aura": 0.04,
            "desc": "[Equipo/Rival] Da +12% Robo de Vida a tu equipo y quita -4% HP/turno al rival.",
        },
        "skills": [
            {"name": "Antorcha de Ánimas", "emoji": "👻", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.06, "lifesteal": 0.30,
             "desc": "Llama etérea que absorbe un 30% del daño en salud."},
            {"name": "Maldición de Cera", "emoji": "🎭", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.90, "steal_buff": True, "expose": 2,
             "desc": "Roba escudos/mejoras del enemigo y lo deja Vulnerable (2t)."},
            {"name": "Luz del Más Allá", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.55, "team_heal_pct": 0.24, "cleanse": True,
             "desc": "Purifica y cura un 24% HP a TODO tu equipo."},
            {"name": "Réquiem Violeta", "emoji": "🕯️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "burn": (0.80, 3), "lifesteal": 0.35, "pierce": True,
             "desc": "Definitiva: perfora defensas, quema 3t y drena 35% del daño."},
        ],
    },
    "necrodrac": {
        "id": "necrodrac", "num": 39, "name": "Necrodrac", "emoji": "💀",
        "element": "sombra", "rarity": "legendario", "stage": 2, "family": "necrodrac",
        "base_hp": 265, "base_atk": 70, "catch_rate": 0.08, "wild_weight": 1,
        "evolves_to": None, "evolve_level": None,
        "desc": "Dragón soberano del eclipse eterno con alas de sombra abisal y núcleo de estrella oscura.",
        "passive": {
            "name": "Monarca del Eclipse", "emoji": "💀", "scope": "enemy",
            "team_atk_mult": 0.16, "enemy_atk_debuff": 0.15,
            "desc": "[Equipo/Rival] Sube +16% el ATQ de tu equipo y reduce -15% el ATQ rival.",
        },
        "skills": [
            {"name": "Aliento de Vacío", "emoji": "🌙", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.14, "lifesteal": 0.30,
             "desc": "Llamarada de materia oscura que roba 30% de vida."},
            {"name": "Trono de Sombras", "emoji": "💀", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.90, "steal_buff": True, "team_atk_buff": 0.22,
             "desc": "Roba las mejoras del rival y otorga +22% ATQ a todo tu equipo."},
            {"name": "Plaga Abisal", "emoji": "☠️", "role": "🎯 Control", "cd": 2, "dmg_mult": 1.05, "poison": (0.90, 3), "expose": 2,
             "desc": "Envenena 3 turnos (90%) y aplica Vulnerable al enemigo."},
            {"name": "Apocalipsis Umbrío", "emoji": "🌑", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.88, "pierce": True, "exec_bonus": (0.50, 0.55), "lifesteal": 0.35,
             "desc": "Definitiva: perfora escudos, drena 35% vida y hace +55% daño si el rival tiene <50% HP."},
        ],
    },

    # --- ASTRAL (#40 Astrobot ➔ #41 Pulsatrón, y #42 Cosmolión) ---
    "astrobot": {
        "id": "astrobot", "num": 40, "name": "Astrobot", "emoji": "🛸",
        "element": "astral", "rarity": "comun", "stage": 1, "family": "astrobot",
        "base_hp": 96, "base_atk": 22, "catch_rate": 0.62, "wild_weight": 26,
        "evolves_to": "pulsatron", "evolve_level": 6,
        "desc": "Pequeño dron esférico de neón cian con antenas de energía estelar y escáner táctico.",
        "passive": {
            "name": "Radar Cuántico", "emoji": "🛸", "scope": "team",
            "team_crit_bonus": 0.10,
            "desc": "[Equipo] Su escáner otorga +10% Prob. de Crítico a todo tu equipo.",
        },
        "skills": [
            {"name": "Láser Óptico", "emoji": "⚡", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "crit_bonus": 0.22,
             "desc": "Disparo de precisión (+22% prob. de crítico)."},
            {"name": "Escaneo de Punto Débil", "emoji": "🎯", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.70, "expose": 2, "team_atk_buff": 0.18,
             "desc": "Deja Vulnerable al enemigo (2t) y sube +18% el ATQ de tu equipo."},
            {"name": "Nano-Reparación", "emoji": "💚", "role": "💚 Soporte", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.20, "shield_pct": 0.40,
             "desc": "Cura 20% HP a todo tu equipo y activa Escudo (-40% daño)."},
            {"name": "Cañón de Fotones", "emoji": "💫", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.55, "pierce": True, "crit_bonus": 0.30,
             "desc": "Definitiva: haz lumínico que ignora escudos (+30% crítico)."},
        ],
    },
    "pulsatron": {
        "id": "pulsatron", "num": 41, "name": "Pulsatrón", "emoji": "⚡",
        "element": "astral", "rarity": "raro", "stage": 2, "family": "astrobot",
        "base_hp": 168, "base_atk": 40, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Centinela magnético de bobinas Tesla doradas que descarga tormentas de plasma.",
        "passive": {
            "name": "Bobina Tesla", "emoji": "⚡", "scope": "self",
            "start_shield": 0.30, "atk_mult": 0.12,
            "desc": "[Propia] Empieza con Escudo (-30% daño) y tiene +12% ATQ base.",
        },
        "skills": [
            {"name": "Arco Voltaico", "emoji": "⚡", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.06, "stun_chance": 0.20,
             "desc": "Descarga magnética (20% prob. de paralizar)."},
            {"name": "Campo Magnético", "emoji": "🛡️", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.65, "shield_pct": 0.50, "thorns": (0.40, 2),
             "desc": "Escudo (-50% daño) y devuelve 40% del daño como descarga."},
            {"name": "Pulso Acelerador", "emoji": "🔋", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.75, "team_atk_buff": 0.20, "haste_cd": 1,
             "desc": "Sube +20% ATQ a todo tu equipo y reduce -1t tus recargas."},
            {"name": "Tormenta de Tesla", "emoji": "🌩️", "role": "⚡ Ráfaga", "cd": 3, "dmg_mult": 0.56, "hits": (3, 3), "stun_chance": 0.42, "pierce": True,
             "desc": "Definitiva: 3 relámpagos que perforan escudos (42% paralizar)."},
        ],
    },
    "cosmolion": {
        "id": "cosmolion", "num": 42, "name": "Cosmolión", "emoji": "🦁",
        "element": "astral", "rarity": "epico", "stage": 2, "family": "cosmolion",
        "base_hp": 235, "base_atk": 64, "catch_rate": 0.15, "wild_weight": 3,
        "evolves_to": None, "evolve_level": None,
        "desc": "León astral de melena de constelaciones y armadura de luz estelar.",
        "passive": {
            "name": "Rugido Estelar", "emoji": "🦁", "scope": "team",
            "team_atk_mult": 0.15, "team_crit_bonus": 0.12,
            "desc": "[Equipo] Otorga +15% ATQ y +12% Prob. de Crítico a todo tu equipo.",
        },
        "skills": [
            {"name": "Zarpazo de Orión", "emoji": "🦁", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.10, "crit_bonus": 0.25,
             "desc": "Garra de plasma estelar (+25% prob. de crítico)."},
            {"name": "Melena de Supernova", "emoji": "✨", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.75, "team_atk_buff": 0.24, "shield_pct": 0.45,
             "desc": "Sube +24% el ATQ de todo tu equipo y activa Escudo (-45% daño)."},
            {"name": "Cometa Cazador", "emoji": "☄️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.54, "hits": (2, 3), "expose": 2,
             "desc": "Embiste 2-3 veces como un cometa y deja Vulnerable al rival."},
            {"name": "Furia del Zodíaco", "emoji": "💫", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.78, "pierce": True, "crit_bonus": 0.35,
             "desc": "Definitiva: impacto de constelación que ignora escudos (+35% crítico)."},
        ],
    },

    # --- ROCA (#43 Toporoca ➔ #44 Escarabita) ---
    "toporoca": {
        "id": "toporoca", "num": 43, "name": "Toporoca", "emoji": "🦔",
        "element": "roca", "rarity": "comun", "stage": 1, "family": "toporoca",
        "base_hp": 110, "base_atk": 20, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "escarabita", "evolve_level": 7,
        "desc": "Topo excavador con garras de mineral de hierro y casco minero de cuarzo brillante.",
        "passive": {
            "name": "Excavador", "emoji": "🦔", "scope": "self",
            "self_dodge": 0.12, "hp_mult": 0.10,
            "desc": "[Propia] Gana +12% Esquiva subterránea y +10% HP máximo.",
        },
        "skills": [
            {"name": "Garra Taladro", "emoji": "🪨", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.02, "pierce": True,
             "desc": "Ataque giratorio que ignora los escudos del rival."},
            {"name": "Túnel Subterráneo", "emoji": "💨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.85, "eva_buff": 0.45, "atk_buff": 0.20,
             "desc": "Excava bajo tierra: +45% Esquiva en el próximo turno y +20% ATQ."},
            {"name": "Lluvia de Escombros", "emoji": "⛰️", "role": "🎯 Control", "cd": 2, "dmg_mult": 0.90, "weaken": 0.20, "stun_chance": 0.30,
             "desc": "Baja -20% el ATQ rival con 30% prob. de aturdir."},
            {"name": "Perforadora Sísmica", "emoji": "💥", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.58, "pierce": True, "crit_bonus": 0.25,
             "desc": "Definitiva: barrena tectónica que perfora cualquier escudo."},
        ],
    },
    "escarabita": {
        "id": "escarabita", "num": 44, "name": "Escarabita", "emoji": "🪲",
        "element": "roca", "rarity": "raro", "stage": 2, "family": "toporoca",
        "base_hp": 195, "base_atk": 36, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Escarabajo rinoceronte acorazado en jade esmeralda y oro antiguo.",
        "passive": {
            "name": "Caparazón de Jade", "emoji": "🪲", "scope": "team",
            "team_dmg_reduction": 0.12,
            "desc": "[Equipo] Su aura mineral reduce un -12% el daño recibido por todo tu equipo.",
        },
        "skills": [
            {"name": "Cuerno de Jade", "emoji": "🪲", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.06, "lifesteal": 0.20,
             "desc": "Embestida con su cuerno real que recupera 20% del daño."},
            {"name": "Égida Esmeralda", "emoji": "🛡️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.55, "team_heal_pct": 0.22, "shield_pct": 0.55,
             "desc": "Cura 22% HP a todo tu equipo y activa Escudo de jade (-55% daño)."},
            {"name": "Coraza Reflectante", "emoji": "🪞", "role": "🛡️ Tanque", "cd": 2, "dmg_mult": 0.70, "thorns": (0.50, 2), "atk_buff": 0.20,
             "desc": "Refleja el 50% del daño recibido por 2 turnos y sube +20% ATQ."},
            {"name": "Catapulta Imperial", "emoji": "⛰️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "stun_chance": 0.45, "pierce": True,
             "desc": "Definitiva: lanza al rival por los aires ignorando escudos (45% aturdir)."},
        ],
    },

    # --- ESCARCHA (#45 Pinguhelado ➔ #46 Morsártica) ---
    "pinguhelado": {
        "id": "pinguhelado", "num": 45, "name": "Pinguhelado", "emoji": "🐧",
        "element": "hielo", "rarity": "comun", "stage": 1, "family": "pinguhelado",
        "base_hp": 98, "base_atk": 21, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "morsartica", "evolve_level": 7,
        "desc": "Pingüino emperador de cristal polar que se desliza a toda velocidad sobre el hielo.",
        "passive": {
            "name": "Deslizamiento Helado", "emoji": "🐧", "scope": "self",
            "self_dodge": 0.14, "self_stun_bonus": 0.10,
            "desc": "[Propia] Tiene +14% de Esquiva y +10% prob. de congelar/aturdir.",
        },
        "skills": [
            {"name": "Tobogán Polar", "emoji": "🐧", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.02, "crit_bonus": 0.18,
             "desc": "Embestida deslizante sobre hielo (+18% prob. crítico)."},
            {"name": "Bolas de Nieve", "emoji": "⛄", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.48, "hits": (2, 3), "weaken": 0.18,
             "desc": "Lanza 2-3 bolas de nieve compacta y baja -18% el ATQ rival."},
            {"name": "Iglú Protector", "emoji": "🧊", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.20, "shield_pct": 0.45,
             "desc": "Refugia al equipo: cura 20% HP grupal y activa Escudo (-45% daño)."},
            {"name": "Torpedo Ártico", "emoji": "❄️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.52, "stun_chance": 0.40, "pierce": True,
             "desc": "Definitiva: impacto helado que perfora escudos (40% congelar)."},
        ],
    },
    "morsartica": {
        "id": "morsartica", "num": 46, "name": "Morsártica", "emoji": "🦭",
        "element": "hielo", "rarity": "raro", "stage": 2, "family": "pinguhelado",
        "base_hp": 190, "base_atk": 37, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Coloso marino de colmillos de iceberg y coraza de nieve eterna.",
        "passive": {
            "name": "Muro de Iceberg", "emoji": "🦭", "scope": "team",
            "team_hp_mult": 0.14, "team_dmg_reduction": 0.08,
            "desc": "[Equipo] Otorga +14% HP máximo y -8% daño recibido a todo tu equipo.",
        },
        "skills": [
            {"name": "Colmillo de Iceberg", "emoji": "❄️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.06, "stun_chance": 0.22,
             "desc": "Golpe pesado con sus colmillos helados (22% congelar)."},
            {"name": "Rompehielos", "emoji": "💥", "role": "⚔️ Asalto", "cd": 2, "dmg_mult": 1.15, "pierce": True, "expose": 2,
             "desc": "Destroza el escudo del rival y lo deja Vulnerable por 2 turnos."},
            {"name": "Banquisa Sanadora", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.50, "team_heal_pct": 0.25, "shield_pct": 0.50, "cleanse": True,
             "desc": "Purifica, cura 25% HP a todo tu equipo y levanta Escudo (-50% daño)."},
            {"name": "Alud Glaciar", "emoji": "🏔️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.68, "stun_chance": 0.48, "weaken": 0.25,
             "desc": "Definitiva: aplasta con un iceberg (48% congelar y -25% ATQ rival)."},
        ],
    },

    # --- CÉFIRO (#47 Nubecilla ➔ #48 Tempestia) ---
    "nubecilla": {
        "id": "nubecilla", "num": 47, "name": "Nubecilla", "emoji": "☁️",
        "element": "viento", "rarity": "comun", "stage": 1, "family": "nubecilla",
        "base_hp": 94, "base_atk": 21, "catch_rate": 0.65, "wild_weight": 26,
        "evolves_to": "tempestia", "evolve_level": 7,
        "desc": "Espíritu esponjoso de nube mediterránea con destellos de brisa dorada.",
        "passive": {
            "name": "Cuerpo de Nube", "emoji": "☁️", "scope": "self",
            "self_dodge": 0.16,
            "desc": "[Propia] Su cuerpo gaseoso le otorga +16% de Esquiva natural.",
        },
        "skills": [
            {"name": "Soplo Esponjoso", "emoji": "☁️", "role": "⚔️ Asalto", "cd": 0, "dmg_mult": 1.0, "weaken": 0.12,
             "desc": "Ráfaga suave que reduce -12% el ATQ del enemigo."},
            {"name": "Niebla Ilusoria", "emoji": "💨", "role": "🎭 Táctica", "cd": 2, "dmg_mult": 0.70, "eva_buff": 0.45, "cleanse": True,
             "desc": "Purifica tus estados negativos y te da +45% de Esquiva."},
            {"name": "Lluvia de Verano", "emoji": "🌦️", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.50, "team_heal_pct": 0.22, "haste_cd": 1,
             "desc": "Cura 22% HP a todo tu equipo y reduce -1t tus recargas."},
            {"name": "Cumulonimbo", "emoji": "⛈️", "role": "🎯 Control", "cd": 3, "dmg_mult": 1.50, "stun_chance": 0.38, "expose": 2,
             "desc": "Definitiva: descarga de tormenta (38% aturdir) que deja Vulnerable."},
        ],
    },
    "tempestia": {
        "id": "tempestia", "num": 48, "name": "Tempestia", "emoji": "🦋",
        "element": "viento", "rarity": "raro", "stage": 2, "family": "nubecilla",
        "base_hp": 170, "base_atk": 40, "catch_rate": 0.30, "wild_weight": 6,
        "evolves_to": None, "evolve_level": None,
        "desc": "Polilla mística de las tormentas con alas de esmeralda y polvo de vendaval curativo.",
        "passive": {
            "name": "Polvo de Vendaval", "emoji": "🦋", "scope": "team",
            "team_dodge_bonus": 0.12, "team_regen_pct": 0.04,
            "desc": "[Equipo] Otorga +12% Esquiva y regenera +4% HP/turno a todo tu equipo.",
        },
        "skills": [
            {"name": "Aleteo Esmeralda", "emoji": "🦋", "role": "🩸 Drenaje", "cd": 0, "dmg_mult": 1.05, "lifesteal": 0.25,
             "desc": "Onda de viento que absorbe un 25% del daño en salud."},
            {"name": "Escamas de Huracán", "emoji": "🌪️", "role": "⚡ Ráfaga", "cd": 2, "dmg_mult": 0.50, "hits": (2, 3), "weaken": 0.20,
             "desc": "Golpea 2-3 veces y reduce -20% el ATQ del enemigo."},
            {"name": "Brisa Sanadora", "emoji": "💚", "role": "👥 Equipo", "cd": 2, "dmg_mult": 0.45, "team_heal_pct": 0.28, "team_atk_buff": 0.18, "cleanse": True,
             "desc": "Purifica, cura 28% HP a todo tu equipo y sube +18% su ATQ."},
            {"name": "Danza de la Tormenta", "emoji": "⛈️", "role": "⚔️ Asalto", "cd": 3, "dmg_mult": 1.65, "pierce": True, "eva_buff": 0.40,
             "desc": "Definitiva: ciclón que ignora escudos y te otorga +40% de Esquiva."},
        ],
    },
}

ORB_MULTIPLIERS = {
    "orbe_basico":  {"mult": 1.0, "guaranteed": False},
    "orbe_super":   {"mult": 1.6, "guaranteed": False},
    "orbe_ultra":   {"mult": 2.4, "guaranteed": False},
    "orbe_maestro": {"mult": 999.0, "guaranteed": True},
}


def image_path(species_id: str) -> str:
    return os.path.join(ASSETS_DIR, f"{species_id}.jpg")


def same_family(sp1: str, sp2: str) -> bool:
    """Devuelve True si dos especies pertenecen a la misma línea evolutiva."""
    c1, c2 = CREATURES.get(sp1), CREATURES.get(sp2)
    return bool(c1 and c2 and c1["family"] == c2["family"])


def stars_badge(stars: int) -> str:
    if not stars or stars <= 0:
        return ""
    return " " + "⭐" * min(MAX_STARS, stars)


def pet_skills(pet: dict) -> list[dict]:
    """Devuelve las 4 habilidades base de la especie + la 5ª habilidad secreta si tiene pergamino."""
    sp = CREATURES[pet["species_id"]]
    skills = list(sp["skills"])
    extra = pet.get("extra_skill")
    if extra and extra in SCROLL_SKILLS:
        skills.append(SCROLL_SKILLS[extra])
    return skills


def pet_stats(species_id: str, level: int, held_item: str | None = None, stars: int = 0) -> tuple[int, int]:
    """Devuelve (hp, atk) escalados con el nivel, las estrellas (⭐), la pasiva propia y el objeto equipado."""
    sp = CREATURES[species_id]
    star_mult = 1.0 + STAR_STAT_BONUS * min(MAX_STARS, max(0, int(stars or 0)))
    passive = sp.get("passive", {})
    hp = sp["base_hp"] * (1 + 0.12 * (level - 1)) * star_mult * (1.0 + passive.get("hp_mult", 0.0))
    atk = sp["base_atk"] * (1 + 0.12 * (level - 1)) * star_mult * (1.0 + passive.get("atk_mult", 0.0))
    gear = PET_GEAR.get(held_item or "")
    if gear:
        hp *= 1 + gear.get("hp_mult", 0.0)
        atk *= 1 + gear.get("atk_mult", 0.0)
    return int(hp), int(atk)


def pet_power(pet: dict) -> int:
    """Calcula el Poder de Combate (CP) individual de un Trobimon."""
    hp, atk = pet_stats(pet["species_id"], pet["level"], pet.get("held_item"), int(pet.get("stars") or 0))
    extra = 60 if pet.get("extra_skill") else 0
    return int(hp + atk * 3.5 + extra)


def calc_team_synergies(team: list[dict]) -> dict:
    """
    Calcula TODOS los bonus pasivos de equipo:
    1) Las Habilidades Pasivas (`passive`) de cada criatura del equipo.
    2) Las Combinaciones Especiales al juntar 3 del MISMO elemento (`MONO_ELEMENT_COMBOS`).
    3) Las Combinaciones Especiales al juntar ciertos elementos (`DUAL_ELEMENT_COMBOS` y Triada).
    """
    res = {
        "hp_mult": 0.0,
        "atk_mult": 0.0,
        "crit_bonus": 0.0,
        "dmg_reduction": 0.0,
        "dodge_bonus": 0.0,
        "burn_bonus": 0.0,
        "stun_bonus": 0.0,
        "heal_boost": 0.0,
        "lifesteal_bonus": 0.0,
        "thorns_bonus": 0.0,
        "team_regen_pct": 0.0,
        "enemy_burn_aura": 0.0,
        "enemy_atk_debuff": 0.0,
        "enemy_expose_start": 0,
        "start_shield": 0.0,
        "lines": [],
        "passive_lines": [],
    }
    if not team:
        return res

    # 1. Acumular las pasivas de equipo/rival de cada miembro del equipo
    for p in team:
        sp = CREATURES[p["species_id"]]
        pas = sp.get("passive")
        if not pas:
            continue
        res["hp_mult"] += pas.get("team_hp_mult", 0.0)
        res["atk_mult"] += pas.get("team_atk_mult", 0.0)
        res["crit_bonus"] += pas.get("team_crit_bonus", 0.0)
        res["dmg_reduction"] += pas.get("team_dmg_reduction", 0.0)
        res["dodge_bonus"] += pas.get("team_dodge_bonus", 0.0)
        res["burn_bonus"] += pas.get("team_burn_bonus", 0.0)
        res["heal_boost"] += pas.get("team_heal_boost", 0.0)
        res["team_regen_pct"] += pas.get("team_regen_pct", 0.0)
        res["enemy_burn_aura"] += pas.get("enemy_burn_aura", 0.0)
        res["enemy_atk_debuff"] += pas.get("enemy_atk_debuff", 0.0)
        res[" passive_lines" if False else "passive_lines"].append(
            f"{pas['emoji']} **{sp['name']} — {pas['name']}:** {pas['desc']}"
        )

    if len(team) < 2:
        return res

    elems = [CREATURES[p["species_id"]]["element"] for p in team]
    unique_elems = set(elems)

    # 2. Combinación Suprema al juntar 3 del MISMO elemento
    if len(team) == 3 and len(unique_elems) == 1:
        el = elems[0]
        combo = MONO_ELEMENT_COMBOS[el]
        for k in (
            "hp_mult", "atk_mult", "crit_bonus", "dmg_reduction", "dodge_bonus",
            "burn_bonus", "stun_bonus", "heal_boost", "lifesteal_bonus",
            "thorns_bonus", "team_regen_pct", "enemy_burn_aura", "enemy_atk_debuff",
            "enemy_expose_start", "start_shield",
        ):
            if k in combo:
                res[k] += combo[k]
        res["lines"].append(f"**{combo['name']}**: {combo['desc']}")
        return res

    # 3. Si hay 2 del mismo elemento
    for el in unique_elems:
        if elems.count(el) == 2:
            el_info = ELEMENTS[el]
            res["atk_mult"] += 0.14
            res["hp_mult"] += 0.08
            res["lines"].append(
                f"{el_info['emoji']} **Dúo de {el_info['name']}** (2x {el_info['name']}): `+14% ATQ` y `+8% HP` a todo el equipo."
            )

    # 4. Si los 3 son de elementos distintos: Triada Elemental
    if len(team) == 3 and len(unique_elems) == 3:
        res["hp_mult"] += 0.12
        res["atk_mult"] += 0.12
        res["lines"].append("🌈 **Triada Elemental** (3 elementos distintos): `+12% HP` y `+12% ATQ` a todo el equipo.")

    # 5. Combinaciones Elementales Especiales al juntar ciertos elementos
    for dc in DUAL_ELEMENT_COMBOS:
        if dc["elems"].issubset(unique_elems):
            for k in (
                "hp_mult", "atk_mult", "crit_bonus", "dmg_reduction", "dodge_bonus",
                "burn_bonus", "stun_bonus", "heal_boost", "lifesteal_bonus",
                "thorns_bonus", "team_regen_pct", "enemy_burn_aura", "enemy_atk_debuff",
                "enemy_expose_start", "start_shield",
            ):
                if k in dc:
                    res[k] += dc[k]
            res["lines"].append(f"**{dc['name']}**: {dc['desc']}")

    return res


def pet_xp_needed(level: int) -> int:
    return 40 + level * 35
