"""Bot de trobia: economía, minijuegos, logros, cajas y personalización."""
import itertools
import logging
import os
import signal
import sys
import traceback

import discord
from discord import app_commands
from discord.ext import commands, tasks

import config
from database import Database
from utils import error_embed

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXTENSIONS = ["cogs.economy", "cogs.profile", "cogs.shop", "cogs.boxes", "cogs.games", "cogs.fun", "cogs.pets", "cogs.growth", "cogs.admin"]
PID_FILE = os.path.join(config.BASE_DIR, "data", "bot.pid")

log = logging.getLogger("trobia")


STATUS_CYCLE = itertools.cycle([
    ("playing", "🍊 /ayuda · /guia · trobia"),
    ("playing", "🐾 Cazando 48 Trobimons con /cazar"),
    ("playing", "🛡️ Equipos 3v3 en /equipo ver"),
    ("playing", "🏯 Torre de Campeones en /mascota torre"),
    ("playing", "🚀 /bump y /invitar para ganar premios"),
    ("playing", "🎰 /blackjack · /tragaperras"),
    ("playing", "🎁 Abriendo cajas con /abrir"),
    ("competing", "⚔️ Duelos en /duelo y /mascota combatir"),
    ("watching", "📖 El /trobidex de trobia"),
])


def ensure_single_instance():
    """Mata cualquier instancia previa de bot.py (y su árbol de procesos) para evitar cobros duplicados."""
    import subprocess
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    my_pid = os.getpid()
    if os.path.isfile(PID_FILE):
        try:
            with open(PID_FILE, "r", encoding="utf-8") as f:
                old_pid = int(f.read().strip())
            if old_pid != my_pid:
                if sys.platform == "win32":
                    subprocess.run(["taskkill", "/PID", str(old_pid), "/T", "/F"], capture_output=True)
                else:
                    os.kill(old_pid, signal.SIGTERM)
        except Exception:
            pass
    try:
        with open(PID_FILE, "w", encoding="utf-8") as f:
            f.write(str(my_pid))
    except Exception:
        pass


class DeduplicatedTree(app_commands.CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Evita atómicamente que una misma interacción se ejecute más de 1 vez
        return self.client.db.claim_interaction(interaction.id)


class TrobiaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()  # sin intents privilegiados
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=None,
            tree_cls=DeduplicatedTree,
        )
        self.db = Database(config.DB_PATH)

    async def setup_hook(self):
        for ext in EXTENSIONS:
            await self.load_extension(ext)
        self.tree.on_error = self.on_app_command_error

        guild = discord.Object(id=config.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        try:
            synced = await self.tree.sync(guild=guild)
            print(f"✅ {len(synced)} comandos slash sincronizados en el servidor.")
        except discord.Forbidden:
            print("❌ El bot no tiene permiso para registrar comandos slash.")
            print("   Vuelve a invitarlo con este enlace (no hace falta echarlo antes):")
            print(f"   https://discord.com/oauth2/authorize?client_id={config.APPLICATION_ID}"
                  "&permissions=8&scope=bot%20applications.commands")

    @tasks.loop(minutes=3)
    async def rotate_status(self):
        kind, text = next(STATUS_CYCLE)
        act_type = {
            "playing": discord.ActivityType.playing,
            "watching": discord.ActivityType.watching,
            "competing": discord.ActivityType.competing,
        }[kind]
        await self.change_presence(activity=discord.Activity(type=act_type, name=text))

    async def on_ready(self):
        if not self.rotate_status.is_running():
            self.rotate_status.start()
        print(f"🍊 Conectado como {self.user} — ¡listo para jugar! (Ctrl+C para apagar)")

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            return
        original = getattr(error, "original", error)
        if isinstance(original, discord.NotFound):
            return
        traceback.print_exception(type(original), original, original.__traceback__)
        msg = error_embed("Ha ocurrido un error inesperado. Inténtalo de nuevo.")
        try:
            if interaction.response.is_done():
                await interaction.followup.send(embed=msg, ephemeral=True)
            else:
                await interaction.response.send_message(embed=msg, ephemeral=True)
        except discord.HTTPException:
            pass


def main():
    if not config.TOKEN or not config.GUILD_ID:
        print("❌ Falta DISCORD_TOKEN o GUILD_ID en el archivo .env")
        sys.exit(1)
    ensure_single_instance()
    bot = TrobiaBot()
    bot.run(config.TOKEN, log_level=logging.WARNING)


if __name__ == "__main__":
    main()
