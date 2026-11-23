"""Economía: saldo, diario, trabajar, pagar, ranking y XP por mensajes."""
import random
import time
from datetime import date, datetime, timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from data.creatures import CREATURES, PET_GEAR, RARITY_BONUS_PCT, STAR_WORK_BONUS, stars_badge
from utils import (check_achievements, error_embed, fmt, grant_xp, multiplier, user_color)

JOBS = [
    "repartiste horchata y fartons por toda la playa de la Malvarrosa",
    "hiciste una paella para 40 personas sin que se pegara el socarrat... demasiado",
    "montaste una falla de cartón piedra en tiempo récord",
    "hiciste de guía turístico por la Ciudad de las Artes y las Ciencias",
    "recogiste naranjas en un campo de La Ribera",
    "arreglaste el ordenador de tu tía (era el cable desenchufado)",
    "hiciste de streamer durante 6 horas con 3 espectadores (uno era tu madre)",
    "trabajaste de mascletero y casi te quedas sordo",
    "vendiste palomitas en el cine del centro comercial",
    "subiste de rango a un desconocido en el LoL a cambio de dinero",
    "programaste una web para la peña fallera del barrio",
    "fuiste camarero en una boda de 300 invitados",
    "paseaste a los perros de todo el bloque",
    "hiciste de extra en una serie de À Punt",
    "repartiste pizzas en patinete bajo la lluvia",
]


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self._msg_cooldown: dict[int, float] = {}

    # ------------------------------------------------------- XP por mensajes
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        uid = message.author.id
        self.db.ensure_user(uid)
        self.db.incr_stat(uid, "messages")

        now = time.time()
        if now - self._msg_cooldown.get(uid, 0) < config.MSG_COOLDOWN:
            return
        self._msg_cooldown[uid] = now

        coins = random.randint(config.MSG_COINS_MIN, config.MSG_COINS_MAX) * multiplier(self.db, uid, "coins")
        self.db.add_coins(uid, coins)
        await grant_xp(self.bot, message.author, random.randint(config.MSG_XP_MIN, config.MSG_XP_MAX), message.channel)

    # ----------------------------------------------------------------- saldo
    @app_commands.command(name="saldo", description="Mira cuántas monedas tienes (o las de otra persona)")
    @app_commands.describe(usuario="Persona de la que quieres ver el saldo")
    async def saldo(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        user = self.db.get_user(target.id)
        rank = self.db.coin_rank(target.id)
        embed = discord.Embed(
            title=f"💰 Cartera de {target.display_name}",
            color=user_color(self.db, target.id),
        )
        embed.description = (
            f"### {fmt(user['coins'])}\n"
            f"-# 🏅 Posición **#{rank}** en el ranking de riqueza\n"
            f"-# 💡 Gana más monedas usando `/trabajar`, `/diario` o jugando en el casino."
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ---------------------------------------------------------------- diario
    @app_commands.command(name="diario", description="Reclama tu recompensa diaria (¡mantén la racha!)")
    async def diario(self, interaction: discord.Interaction):
        uid = interaction.user.id
        user = self.db.get_user(uid)
        today = date.today()
        last = date.fromisoformat(user["daily_last"]) if user["daily_last"] else None

        if last == today:
            midnight = datetime.combine(today + timedelta(days=1), datetime.min.time()).astimezone()
            tomorrow = discord.utils.format_dt(midnight, "R")
            await interaction.response.send_message(
                embed=error_embed(f"Ya has reclamado tu diario hoy.\nVuelve mañana ({tomorrow})."), ephemeral=True
            )
            return

        streak = self.db.get_stat(uid, "daily_streak")
        streak = streak + 1 if last == today - timedelta(days=1) else 1
        self.db.set_stat(uid, "daily_streak", streak)
        self.db.max_stat(uid, "best_streak", streak)
        self.db.incr_stat(uid, "daily_count")
        self.db.set_field(uid, "daily_last", today.isoformat())

        amount = config.DAILY_BASE + config.DAILY_STREAK_BONUS * min(streak, config.DAILY_STREAK_CAP)
        self.db.add_coins(uid, amount)
        self.db.add_item(uid, "orbe_basico", 1)

        extra = "\n🔴 **1x Orbe Básico** gratis para `/cazar`"
        if streak % 7 == 0:
            self.db.add_item(uid, "caja_rara")
            extra += "\n🎁 **1x Caja Rara** (¡Bonus de semana completa!)"
        elif streak % 3 == 0:
            self.db.add_item(uid, "caja_comun")
            extra += "\n📦 **1x Caja Común** (¡Bonus de racha!)"

        embed = discord.Embed(
            title="🌅 Recompensa Diaria",
            color=config.COLOR_OK,
        )
        embed.description = (
            f"### +{fmt(amount)}\n"
            f"🔥 **Racha:** `{streak} día(s)` consecutivo(s)\n"
            f"{extra}\n\n"
            f"-# 💡 Vuelve cada día para conservar tu racha y multiplicar los bonus."
        )
        await interaction.response.send_message(embed=embed)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # -------------------------------------------------------------- trabajar
    @app_commands.command(name="trabajar", description="Trabaja para ganar monedas (cada 1 hora)")
    async def trabajar(self, interaction: discord.Interaction):
        uid = interaction.user.id
        self.db.ensure_user(uid)
        last = self.db.get_stat(uid, "work_last")
        now = int(time.time())
        if now - last < config.WORK_COOLDOWN:
            ready = discord.utils.format_dt(discord.utils.utcnow() + timedelta(seconds=config.WORK_COOLDOWN - (now - last)), "R")
            await interaction.response.send_message(
                embed=error_embed(f"Estás agotado/a. Podrás volver a trabajar {ready}.\n-# ☕ Un *Café Cargado* de la tienda reinicia el cooldown al instante."),
                ephemeral=True,
            )
            return

        mult = multiplier(self.db, uid, "coins")
        base_amount = random.randint(config.WORK_MIN, config.WORK_MAX) * mult
        pet = self.db.get_active_pet(uid)
        pet_bonus = 0
        pet_txt = ""
        if pet:
            sp = CREATURES[pet["species_id"]]
            stars = int(pet.get("stars") or 0)
            pct = RARITY_BONUS_PCT[sp["rarity"]] + stars * STAR_WORK_BONUS
            gear = PET_GEAR.get(pet.get("held_item") or "")
            if gear and gear.get("work_bonus_pct"):
                pct += gear["work_bonus_pct"]
            pet_bonus = int(base_amount * pct / 100)
            pet_txt = f"\n🐾 **{pet.get('nickname') or sp['name']}** {sp['emoji']}{stars_badge(stars)} te asistió: `+{pct}%` (+{fmt(pet_bonus)})"
        amount = base_amount + pet_bonus
        self.db.set_stat(uid, "work_last", now)
        self.db.incr_stat(uid, "works")
        self.db.add_coins(uid, amount)

        boost_txt = " *(Multiplicador x2 por Amuleto 🧿)*" if mult > 1 else ""
        job_story = random.choice(JOBS)
        embed = discord.Embed(
            title="💼 Jornada Laboral",
            color=config.COLOR_OK,
        )
        embed.description = (
            f"### +{fmt(amount)}\n"
            f"> *Hoy {job_story}.*\n"
            f"{boost_txt}{pet_txt}\n\n"
            f"-# ⏱️ Podrás volver a trabajar dentro de 1 hora."
        )
        await interaction.response.send_message(embed=embed)
        await grant_xp(self.bot, interaction.user, 20, interaction.channel)

    # ----------------------------------------------------------------- pagar
    @app_commands.command(name="pagar", description="Envía monedas a otra persona")
    @app_commands.describe(usuario="Quién recibe las monedas", cantidad="Cuántas monedas enviar")
    async def pagar(self, interaction: discord.Interaction, usuario: discord.Member,
                    cantidad: app_commands.Range[int, 1, 10_000_000]):
        if usuario.bot or usuario.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("No puedes transferirte monedas a ti mismo ni a un bot."), ephemeral=True)
            return
        if not self.db.remove_coins(interaction.user.id, cantidad):
            await interaction.response.send_message(embed=error_embed(f"Fondos insuficientes. No tienes {fmt(cantidad)}."), ephemeral=True)
            return
        self.db.add_coins(usuario.id, cantidad)
        embed = discord.Embed(
            title="💸 Transferencia Exitosa",
            description=f"### {fmt(cantidad)}\n{interaction.user.mention} ha transferido fondos a {usuario.mention}.",
            color=config.COLOR_OK,
        )
        embed.set_footer(text=f"ID de transacción: {int(time.time())}")
        await interaction.response.send_message(embed=embed)
        await check_achievements(self.bot, usuario, interaction.channel)

    # --------------------------------------------------------------- ranking
    @app_commands.command(name="ranking", description="Top 10 del servidor")
    @app_commands.describe(tipo="Qué ranking quieres ver")
    @app_commands.choices(tipo=[
        app_commands.Choice(name="💰 Monedas", value="monedas"),
        app_commands.Choice(name="⭐ Nivel", value="nivel"),
    ])
    async def ranking(self, interaction: discord.Interaction, tipo: Optional[app_commands.Choice[str]] = None):
        kind = tipo.value if tipo else "monedas"
        rows = self.db.leaderboard(kind, 10)
        medals = ["🥇", "🥈", "🥉"] + [f"`#{i}`" for i in range(4, 11)]
        lines = []
        for i, r in enumerate(rows):
            value = fmt(r["coins"]) if kind == "monedas" else f"Nivel **{r['level']}** ({r['xp']} XP)"
            lines.append(f"{medals[i]} <@{r['user_id']}> ─ {value}")
        embed = discord.Embed(
            title="🏆 Top 10 — " + ("Riqueza y Fortuna" if kind == "monedas" else "Nivel de Experiencia"),
            description="\n".join(lines) or "*Todavía no hay registros en este ranking.*",
            color=config.COLOR_MAIN,
        )
        embed.set_footer(text="Usa /ranking tipo:monedas o tipo:nivel para alternar")
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(Economy(bot))
