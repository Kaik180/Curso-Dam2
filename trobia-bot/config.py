"""Configuración general del bot de trobia."""
import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("DISCORD_TOKEN", "")
GUILD_ID = int(os.getenv("GUILD_ID", "0") or 0)
APPLICATION_ID = os.getenv("APPLICATION_ID", "")

DB_PATH = os.path.join(BASE_DIR, "data", "trobia.db")

# Moneda
CURRENCY = "🪙"
CURRENCY_NAME = "trobicoins"
STARTING_COINS = 500

# Colores
COLOR_MAIN = 0xFF7F11     # naranja valenciano
COLOR_OK = 0x2ECC71
COLOR_ERROR = 0xE74C3C
COLOR_INFO = 0x3498DB

# Economía
DAILY_BASE = 200
DAILY_STREAK_BONUS = 25     # por día de racha
DAILY_STREAK_CAP = 30       # máximo de días que suman bonus
WORK_COOLDOWN = 3600        # 1 hora
WORK_MIN, WORK_MAX = 80, 220

# XP por mensajes
MSG_COOLDOWN = 60           # segundos entre mensajes que dan XP
MSG_XP_MIN, MSG_XP_MAX = 15, 25
MSG_COINS_MIN, MSG_COINS_MAX = 3, 8

# Apuestas
BET_MIN = 10
BET_MAX = 100_000
