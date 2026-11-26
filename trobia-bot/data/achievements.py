"""Logros: se desbloquean cuando la estadística `stat` llega a `goal`."""

ACHIEVEMENTS = [
    # Chat
    {"id": "hola_mundo",   "name": "Hola Mundo",         "emoji": "👋", "stat": "messages",       "goal": 1,      "reward": 50,    "desc": "Envía tu primer mensaje."},
    {"id": "charlatan",    "name": "Charlatán/a",        "emoji": "💬", "stat": "messages",       "goal": 500,    "reward": 500,   "desc": "Envía 500 mensajes."},
    {"id": "loro",         "name": "Más pesado que un loro", "emoji": "🦜", "stat": "messages",   "goal": 2500,   "reward": 2500,  "desc": "Envía 2.500 mensajes."},
    # Niveles
    {"id": "nivel_5",      "name": "Calentando motores", "emoji": "⭐", "stat": "level",          "goal": 5,      "reward": 300,   "desc": "Llega al nivel 5."},
    {"id": "nivel_10",     "name": "Veterano/a",         "emoji": "🌟", "stat": "level",          "goal": 10,     "reward": 1000,  "desc": "Llega al nivel 10."},
    {"id": "nivel_25",     "name": "Leyenda Viviente",   "emoji": "💫", "stat": "level",          "goal": 25,     "reward": 5000,  "desc": "Llega al nivel 25."},
    # Economía
    {"id": "madrugador",   "name": "Madrugador/a",       "emoji": "🌅", "stat": "daily_count",    "goal": 1,      "reward": 100,   "desc": "Reclama tu primera recompensa diaria."},
    {"id": "constante",    "name": "Constancia",         "emoji": "📅", "stat": "best_streak",    "goal": 7,      "reward": 1000,  "desc": "Consigue una racha diaria de 7 días."},
    {"id": "incansable",   "name": "Incansable",         "emoji": "🗓️", "stat": "best_streak",    "goal": 30,     "reward": 7500,  "desc": "Consigue una racha diaria de 30 días."},
    {"id": "currante",     "name": "Currante",           "emoji": "💼", "stat": "works",          "goal": 25,     "reward": 750,   "desc": "Trabaja 25 veces."},
    {"id": "ahorrador",    "name": "Hucha Llena",        "emoji": "🐷", "stat": "coins",          "goal": 10000,  "reward": 500,   "desc": "Ten 10.000 monedas a la vez."},
    {"id": "millonario",   "name": "Millonario/a",       "emoji": "🤑", "stat": "coins",          "goal": 100000, "reward": 5000,  "desc": "Ten 100.000 monedas a la vez."},
    {"id": "comprador",    "name": "Comprador/a Compulsivo/a", "emoji": "🛒", "stat": "items_bought", "goal": 10, "reward": 500,   "desc": "Compra 10 objetos en la tienda."},
    {"id": "estilo",       "name": "Con Estilo",         "emoji": "😎", "stat": "customized",     "goal": 1,      "reward": 200,   "desc": "Personaliza tu perfil por primera vez."},
    # Cajas
    {"id": "primera_caja", "name": "¿Qué habrá dentro?", "emoji": "📦", "stat": "boxes_opened",   "goal": 1,      "reward": 100,   "desc": "Abre tu primera caja."},
    {"id": "coleccionista","name": "Coleccionista",      "emoji": "🗃️", "stat": "boxes_opened",   "goal": 50,     "reward": 3000,  "desc": "Abre 50 cajas."},
    {"id": "suertudo",     "name": "Tocado/a por la Suerte", "emoji": "🍀", "stat": "legendary_drops", "goal": 1, "reward": 2000,  "desc": "Consigue un premio legendario en una caja."},
    # Minijuegos
    {"id": "jugador",      "name": "Jugador/a",          "emoji": "🎲", "stat": "games_played",   "goal": 10,     "reward": 200,   "desc": "Juega 10 partidas con apuesta."},
    {"id": "vicio",        "name": "Vicio Nivel Dios",   "emoji": "🕹️", "stat": "games_played",   "goal": 250,    "reward": 3000,  "desc": "Juega 250 partidas con apuesta."},
    {"id": "ganador",      "name": "Ganador/a Nato/a",   "emoji": "🏆", "stat": "games_won",      "goal": 50,     "reward": 1500,  "desc": "Gana 50 partidas con apuesta."},
    {"id": "blackjack",    "name": "¡Blackjack!",        "emoji": "🃏", "stat": "bj_naturals",    "goal": 1,      "reward": 500,   "desc": "Consigue un blackjack natural."},
    {"id": "jackpot",      "name": "JACKPOT",            "emoji": "🎰", "stat": "slots_jackpots", "goal": 1,      "reward": 5000,  "desc": "Saca 7️⃣7️⃣7️⃣ en la tragaperras."},
    {"id": "cerebrito",    "name": "Cerebrito",          "emoji": "🧠", "stat": "trivia_correct", "goal": 25,     "reward": 1000,  "desc": "Acierta 25 preguntas de trivia."},
    {"id": "detective",    "name": "Detective",          "emoji": "🔎", "stat": "guesses_won",    "goal": 5,      "reward": 500,   "desc": "Gana 5 veces a Adivina el Número."},
    {"id": "gladiador",    "name": "Gladiador/a",        "emoji": "⚔️", "stat": "duels_won",      "goal": 10,     "reward": 1500,  "desc": "Gana 10 duelos contra otros miembros."},
    # Trobimons (Mascotas y Equipos)
    {"id": "primer_trobimon",   "name": "¡Hazte con uno!",       "emoji": "🐾", "stat": "pets_caught",     "goal": 1,  "reward": 250,   "desc": "Captura o incuba tu primer Trobimon."},
    {"id": "cazador_experto",   "name": "Maestro/a Cazador/a",   "emoji": "🏹", "stat": "pets_caught",     "goal": 25, "reward": 2000,  "desc": "Captura o incuba 25 Trobimons."},
    {"id": "primera_evolucion", "name": "¡Está evolucionando!",  "emoji": "✨", "stat": "pets_evolved",    "goal": 1,  "reward": 600,   "desc": "Evoluciona a un Trobimon por primera vez."},
    {"id": "primera_fusion",    "name": "Ascensión Estelar",     "emoji": "⭐", "stat": "pets_fused",      "goal": 1,  "reward": 500,   "desc": "Fusiona un Trobimon repetido para subir de estrellas."},
    {"id": "cinco_estrellas",   "name": "Constelación Perfecta", "emoji": "🌟", "stat": "pet_max_stars",   "goal": 5,  "reward": 4000,  "desc": "Sube un Trobimon al máximo de 5 Estrellas (⭐⭐⭐⭐⭐)."},
    {"id": "entrenador_elite",  "name": "Campeón/a de trobia",   "emoji": "🥊", "stat": "pet_battles_won", "goal": 15, "reward": 2500,  "desc": "Gana 15 combates con tu equipo de Trobimons."},
    {"id": "torre_5",           "name": "Asaltante de la Torre", "emoji": "🏯", "stat": "tower_floor",     "goal": 5,  "reward": 1800,  "desc": "Supera el Piso 5 de la Torre de Campeones."},
    {"id": "torre_10",          "name": "Señor/a de la Cumbre",  "emoji": "👑", "stat": "tower_floor",     "goal": 10, "reward": 6000,  "desc": "Supera el Piso 10 de la Torre de Campeones."},
    {"id": "trobidex_10",       "name": "Investigador/a",        "emoji": "📘", "stat": "trobidex",        "goal": 10, "reward": 1500,  "desc": "Descubre 10 especies en el Trobidex."},
    {"id": "trobidex_20",       "name": "Zoólogo/a de Élite",    "emoji": "📗", "stat": "trobidex",        "goal": 20, "reward": 4000,  "desc": "Descubre 20 especies en el Trobidex."},
    {"id": "trobidex_35",       "name": "Sabio/a de la Fauna",   "emoji": "📙", "stat": "trobidex",        "goal": 35, "reward": 9000,  "desc": "Descubre 35 especies en el Trobidex."},
    {"id": "trobidex_completo", "name": "Profesor/a de trobia",  "emoji": "📖", "stat": "trobidex",        "goal": 48, "reward": 25000, "desc": "Descubre las 48 especies en el Trobidex."},
]

ACH_BY_ID = {a["id"]: a for a in ACHIEVEMENTS}
