"""Minijuegos sin apuesta: trivia y adivina el número."""
import random
import time

import discord
from discord import app_commands
from discord.ext import commands

import config
from data.trivia import QUESTIONS
from utils import check_achievements, error_embed, fmt, grant_xp

TRIVIA_COOLDOWN = 30
GUESS_COOLDOWN = 60


# ===================================================================== TRIVIA
class TriviaView(discord.ui.View):
    def __init__(self, cog, user, correct: str, options: list[str]):
        super().__init__(timeout=20)
        self.cog, self.user, self.correct = cog, user, correct
        self.answered = False
        self.message = None
        for i, opt in enumerate(options):
            btn = discord.ui.Button(label=opt[:80], style=discord.ButtonStyle.secondary, emoji=["🇦", "🇧", "🇨", "🇩"][i])
            btn.callback = self.make_callback(btn, opt)
            self.add_item(btn)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Esta pregunta no es tuya. Pide la tuya con `/trivia`.", ephemeral=True)
            return False
        return True

    def reveal(self, chosen_btn=None):
        for c in self.children:
            c.disabled = True
            if c.label == self.correct[:80]:
                c.style = discord.ButtonStyle.success
            elif c is chosen_btn:
                c.style = discord.ButtonStyle.danger

    def make_callback(self, btn, option: str):
        async def callback(interaction: discord.Interaction):
            if self.answered:
                return
            self.answered = True
            self.stop()
            self.reveal(btn)
            embed = interaction.message.embeds[0]
            if option == self.correct:
                reward = random.randint(60, 120)
                self.cog.db.add_coins(self.user.id, reward)
                self.cog.db.incr_stat(self.user.id, "trivia_correct")
                embed.color = config.COLOR_OK
                embed.add_field(name="✅ ¡Respuesta Correcta!", value=f"### +{fmt(reward)}\nHas ganado **30 XP** de experiencia.", inline=False)
                await interaction.response.edit_message(embed=embed, view=self)
                await grant_xp(self.cog.bot, self.user, 30, interaction.channel)
            else:
                embed.color = config.COLOR_ERROR
                embed.add_field(name="❌ Respuesta Incorrecta", value=f"La solución correcta era: **{self.correct}**.", inline=False)
                await interaction.response.edit_message(embed=embed, view=self)
        return callback

    async def on_timeout(self):
        if self.answered or self.message is None:
            return
        self.reveal()
        embed = self.message.embeds[0]
        embed.color = config.COLOR_ERROR
        embed.add_field(name="⏰ Tiempo Agotado", value=f"Se acabó el tiempo. La respuesta era: **{self.correct}**.", inline=False)
        try:
            await self.message.edit(embed=embed, view=self)
        except discord.HTTPException:
            pass


# ============================================================ ADIVINA NÚMERO
class GuessModal(discord.ui.Modal, title="🔢 Adivina el número"):
    number = discord.ui.TextInput(label="Tu número (1-100)", placeholder="Ej: 50", min_length=1, max_length=3)

    def __init__(self, game: "GuessView"):
        super().__init__()
        self.game = game

    async def on_submit(self, interaction: discord.Interaction):
        g = self.game
        if g.over:
            await interaction.response.send_message("La partida ya ha terminado.", ephemeral=True)
            return
        try:
            n = int(self.number.value.strip())
            if not 1 <= n <= 100:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("Escribe un número entre 1 y 100.", ephemeral=True)
            return

        g.attempts_left -= 1
        if n == g.secret:
            g.over = True
            reward = 50 + 40 * g.attempts_left + 40
            g.cog.db.add_coins(g.user.id, reward)
            g.cog.db.incr_stat(g.user.id, "guesses_won")
            g.history.append(f"`{n}` ✅")
            g.finish_buttons()
            await interaction.response.edit_message(
                embed=g.embed(f"🎉 ¡Correcto! Era el **{g.secret}**. Ganas {fmt(reward)}.", config.COLOR_OK), view=g
            )
            await check_achievements(g.cog.bot, g.user, interaction.channel)
            return

        g.history.append(f"`{n}` {'⬆️' if n < g.secret else '⬇️'}")
        if g.attempts_left <= 0:
            g.over = True
            g.finish_buttons()
            await interaction.response.edit_message(
                embed=g.embed(f"💀 Sin intentos. El número era el **{g.secret}**.", config.COLOR_ERROR), view=g
            )
            return
        hint = "más ALTO ⬆️" if n < g.secret else "más BAJO ⬇️"
        await interaction.response.edit_message(embed=g.embed(f"El número es {hint}"), view=g)


class GuessView(discord.ui.View):
    MAX_ATTEMPTS = 7

    def __init__(self, cog, user):
        super().__init__(timeout=180)
        self.cog, self.user = cog, user
        self.secret = random.randint(1, 100)
        self.attempts_left = self.MAX_ATTEMPTS
        self.history: list[str] = []
        self.over = False
        self.message = None

    def embed(self, status: str = "", color: int = config.COLOR_INFO) -> discord.Embed:
        e = discord.Embed(
            title="🔢 Adivina el Número Oculto",
            description=f"### Estoy pensando un número del 1 al 100\n> {status}",
            color=color,
        )
        e.add_field(name="🎯 Intentos restantes", value=f"`{self.attempts_left} / {self.MAX_ATTEMPTS}`", inline=True)
        if self.history:
            e.add_field(name="📜 Pistas anteriores", value=" · ".join(self.history), inline=False)
        e.set_footer(text=f"Partida de {self.user.display_name} · Cuantos menos intentos uses, mayor será el premio")
        return e

    def finish_buttons(self):
        for c in self.children:
            c.disabled = True
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Esta partida no es tuya. Empieza la tuya con `/adivina`.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Adivinar", emoji="🔢", style=discord.ButtonStyle.primary)
    async def guess(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GuessModal(self))

    @discord.ui.button(label="Rendirse", emoji="🏳️", style=discord.ButtonStyle.danger)
    async def give_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.over = True
        self.finish_buttons()
        await interaction.response.edit_message(embed=self.embed(f"🏳️ Te has rendido. Era el **{self.secret}**.", config.COLOR_ERROR), view=self)

    async def on_timeout(self):
        if self.over or self.message is None:
            return
        self.over = True
        for c in self.children:
            c.disabled = True
        try:
            await self.message.edit(embed=self.embed(f"⏰ Se acabó el tiempo. Era el **{self.secret}**.", config.COLOR_ERROR), view=self)
        except discord.HTTPException:
            pass


# ======================================================================= COG
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self._cooldowns: dict[tuple[str, int], float] = {}

    def _on_cooldown(self, key: str, uid: int, seconds: int) -> int:
        now = time.time()
        last = self._cooldowns.get((key, uid), 0)
        if now - last < seconds:
            return int(seconds - (now - last)) + 1
        self._cooldowns[(key, uid)] = now
        return 0

    @app_commands.command(name="trivia", description="Responde una pregunta de trivia y gana monedas 🧠")
    async def trivia(self, interaction: discord.Interaction):
        wait = self._on_cooldown("trivia", interaction.user.id, TRIVIA_COOLDOWN)
        if wait:
            await interaction.response.send_message(embed=error_embed(f"Espera {wait}s para otra pregunta."), ephemeral=True)
            return
        cat, question, correct, wrong = random.choice(QUESTIONS)
        options = [correct] + list(wrong)
        random.shuffle(options)
        embed = discord.Embed(title=f"🧠 Trivia · {cat}", description=f"**{question}**\n\n⏱️ Tienes 20 segundos.", color=config.COLOR_INFO)
        embed.set_footer(text=f"Pregunta para {interaction.user.display_name}")
        view = TriviaView(self, interaction.user, correct, options)
        await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response()

    @app_commands.command(name="adivina", description="Adivina el número del 1 al 100 en 7 intentos 🔢")
    async def adivina(self, interaction: discord.Interaction):
        wait = self._on_cooldown("adivina", interaction.user.id, GUESS_COOLDOWN)
        if wait:
            await interaction.response.send_message(embed=error_embed(f"Espera {wait}s para otra partida."), ephemeral=True)
            return
        view = GuessView(self, interaction.user)
        await interaction.response.send_message(embed=view.embed("Pulsa **Adivinar** para escribir tu número."), view=view)
        view.message = await interaction.original_response()


async def setup(bot):
    await bot.add_cog(Fun(bot))
