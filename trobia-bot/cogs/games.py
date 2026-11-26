"""Minijuegos con apuesta: moneda, dados, tragaperras, blackjack, ppt y duelo."""
import asyncio
import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_achievements, error_embed, fmt, record_game, take_bet

Bet = app_commands.Range[int, config.BET_MIN, config.BET_MAX]
DICE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# Tragaperras: (símbolo, peso, multiplicador con 3 iguales)
SLOT_SYMBOLS = [("🍒", 30, 3), ("🍋", 25, 4), ("🍊", 20, 6), ("🍇", 12, 8), ("🔔", 8, 15), ("💎", 4, 30), ("7️⃣", 1, 100)]


def result_embed(title: str, desc: str, won: Optional[bool]) -> discord.Embed:
    color = config.COLOR_OK if won else (config.COLOR_ERROR if won is False else config.COLOR_INFO)
    return discord.Embed(title=title, description=desc, color=color)


# =========================================================== BLACKJACK
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def hand_value(hand) -> int:
    total, aces = 0, 0
    for rank, _ in hand:
        if rank == "A":
            total, aces = total + 11, aces + 1
        elif rank in ("J", "Q", "K"):
            total += 10
        else:
            total += int(rank)
    while total > 21 and aces:
        total, aces = total - 10, aces - 1
    return total


def hand_str(hand) -> str:
    return " ".join(f"`{r}{s}`" for r, s in hand)


class BlackjackView(discord.ui.View):
    def __init__(self, cog, user: discord.abc.User, bet: int):
        super().__init__(timeout=90)
        self.cog, self.user, self.bet = cog, user, bet
        self.deck = [(r, s) for r in RANKS for s in SUITS] * 2
        random.shuffle(self.deck)
        self.player = [self.deck.pop(), self.deck.pop()]
        self.dealer = [self.deck.pop(), self.deck.pop()]
        self.finished = False
        self.message: Optional[discord.Message] = None

    def embed(self, reveal=False, outcome: str = "", won: Optional[bool] = None) -> discord.Embed:
        dealer_cards = hand_str(self.dealer) if reveal else f"{hand_str(self.dealer[:1])} `??`"
        dealer_val = hand_value(self.dealer) if reveal else "?"
        e = discord.Embed(
            title=f"🃏 Blackjack — apuesta {self.bet:,}".replace(",", ".") + f" {config.CURRENCY}",
            color=config.COLOR_INFO if won is None else (config.COLOR_OK if won else config.COLOR_ERROR),
        )
        e.add_field(name=f"Tu mano ({hand_value(self.player)})", value=hand_str(self.player), inline=False)
        e.add_field(name=f"Crupier ({dealer_val})", value=dealer_cards, inline=False)
        if outcome:
            e.description = outcome
        e.set_footer(text=self.user.display_name, icon_url=self.user.display_avatar.url)
        return e

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Esta partida no es tuya. Juega la tuya con `/blackjack`.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    def finish(self) -> tuple[str, Optional[bool]]:
        """Juega el crupier, paga y devuelve (texto, ganado)."""
        self.finished = True
        for child in self.children:
            child.disabled = True
        db = self.cog.db
        p = hand_value(self.player)
        if p > 21:
            won, text = False, f"💥 Te has pasado. Pierdes {fmt(self.bet)}."
        else:
            while hand_value(self.dealer) < 17:
                self.dealer.append(self.deck.pop())
            d = hand_value(self.dealer)
            if d > 21 or p > d:
                db.add_coins(self.user.id, self.bet * 2)
                won, text = True, f"🎉 ¡Ganas! Te llevas {fmt(self.bet * 2)}."
            elif p == d:
                db.add_coins(self.user.id, self.bet)
                won, text = None, "🤝 Empate. Recuperas tu apuesta."
            else:
                won, text = False, f"😢 Gana el crupier. Pierdes {fmt(self.bet)}."
        record_game(db, self.user.id, bool(won))
        self.stop()
        return text, won

    async def end(self, interaction: discord.Interaction):
        text, won = self.finish()
        await interaction.response.edit_message(embed=self.embed(True, text, won), view=self)
        await check_achievements(self.cog.bot, self.user, interaction.channel)

    @discord.ui.button(label="Pedir", emoji="➕", style=discord.ButtonStyle.primary)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.append(self.deck.pop())
        self.double.disabled = True
        if hand_value(self.player) >= 21:
            await self.end(interaction)
        else:
            await interaction.response.edit_message(embed=self.embed(), view=self)

    @discord.ui.button(label="Plantarse", emoji="✋", style=discord.ButtonStyle.secondary)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.end(interaction)

    @discord.ui.button(label="Doblar", emoji="💰", style=discord.ButtonStyle.success)
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.cog.db.remove_coins(self.user.id, self.bet):
            await interaction.response.send_message("No tienes monedas suficientes para doblar.", ephemeral=True)
            return
        self.bet *= 2
        self.player.append(self.deck.pop())
        await self.end(interaction)

    async def on_timeout(self):
        if self.finished or self.message is None:
            return
        text, won = self.finish()
        try:
            await self.message.edit(embed=self.embed(True, "⏰ Tiempo agotado, te plantas automáticamente.\n" + text, won), view=self)
        except discord.HTTPException:
            pass


# ======================================================= PIEDRA PAPEL TIJERA
PPT = {"piedra": "🪨", "papel": "📄", "tijera": "✂️"}
BEATS = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}


class PPTView(discord.ui.View):
    def __init__(self, cog, user, bet: int):
        super().__init__(timeout=60)
        self.cog, self.user, self.bet = cog, user, bet
        self.played = False
        for key, emoji in PPT.items():
            btn = discord.ui.Button(label=key.capitalize(), emoji=emoji, style=discord.ButtonStyle.primary)
            btn.callback = self.make_callback(key)
            self.add_item(btn)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Esta partida no es tuya.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    def make_callback(self, choice: str):
        async def callback(interaction: discord.Interaction):
            if self.played:
                return
            self.played = True
            bot_choice = random.choice(list(PPT))
            db = self.cog.db
            if choice == bot_choice:
                won, text = None, "🤝 ¡Empate!" + (" Recuperas tu apuesta." if self.bet else "")
                if self.bet:
                    db.add_coins(self.user.id, self.bet)
            elif BEATS[choice] == bot_choice:
                won, text = True, "🎉 ¡Ganas!" + (f" Te llevas {fmt(self.bet * 2)}." if self.bet else "")
                if self.bet:
                    db.add_coins(self.user.id, self.bet * 2)
            else:
                won, text = False, "😢 Pierdes." + (f" Adiós a {fmt(self.bet)}." if self.bet else "")
            if self.bet:
                record_game(db, self.user.id, bool(won))
            for c in self.children:
                c.disabled = True
            self.stop()
            desc = f"Tú: {PPT[choice]} **{choice}**\nBot: {PPT[bot_choice]} **{bot_choice}**\n\n{text}"
            await interaction.response.edit_message(embed=result_embed("🪨📄✂️ Piedra, papel o tijera", desc, won), view=self)
            await check_achievements(self.cog.bot, self.user, interaction.channel)
        return callback

    async def on_timeout(self):
        if self.bet and not self.played:
            self.cog.db.add_coins(self.user.id, self.bet)


# ================================================================== DUELO
class DuelView(discord.ui.View):
    def __init__(self, cog, challenger, rival, bet: int):
        super().__init__(timeout=60)
        self.cog, self.challenger, self.rival, self.bet = cog, challenger, rival, bet
        self.message: Optional[discord.Message] = None
        self.done = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.rival.id:
            await interaction.response.send_message("Solo la persona retada puede responder.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    def disable(self):
        self.done = True
        for c in self.children:
            c.disabled = True
        self.stop()

    @discord.ui.button(label="Aceptar duelo", emoji="⚔️", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.cog.db
        self.disable()
        if not db.remove_coins(self.challenger.id, self.bet):
            await interaction.response.edit_message(embed=error_embed(f"{self.challenger.mention} ya no tiene monedas suficientes."), view=self)
            return
        if not db.remove_coins(self.rival.id, self.bet):
            db.add_coins(self.challenger.id, self.bet)
            await interaction.response.edit_message(embed=error_embed(f"{self.rival.mention} no tiene monedas suficientes."), view=self)
            return

        fighters = [self.challenger, self.rival]
        hp = {f.id: 100 for f in fighters}
        attacks = ["lanza una chancla voladora 🩴", "tira un petardo de mascletà 🧨", "pega un golpe con una paellera 🥘",
                   "ataca con una naranja a 200 km/h 🍊", "hace un combo de Street Fighter 👊", "invoca a su abuela enfadada 👵"]
        log = []
        turn = random.randint(0, 1)
        embed = discord.Embed(title="⚔️ ¡Comienza el duelo!", color=config.COLOR_MAIN)
        await interaction.response.edit_message(embed=embed, view=self)
        while all(v > 0 for v in hp.values()):
            atk, dfn = fighters[turn], fighters[1 - turn]
            dmg = random.randint(8, 24)
            crit = random.random() < 0.12
            if crit:
                dmg *= 2
            hp[dfn.id] = max(0, hp[dfn.id] - dmg)
            log.append(f"**{atk.display_name}** {random.choice(attacks)} → **-{dmg}**{' 💥 ¡CRÍTICO!' if crit else ''}")
            embed.description = (
                f"❤️ {self.challenger.display_name}: **{hp[self.challenger.id]}** HP\n"
                f"❤️ {self.rival.display_name}: **{hp[self.rival.id]}** HP\n\n" + "\n".join(log[-6:])
            )
            await interaction.edit_original_response(embed=embed)
            await asyncio.sleep(1.2)
            turn = 1 - turn

        winner = self.challenger if hp[self.challenger.id] > 0 else self.rival
        loser = self.rival if winner is self.challenger else self.challenger
        db.add_coins(winner.id, self.bet * 2)
        db.incr_stat(winner.id, "duels_won")
        record_game(db, winner.id, True)
        record_game(db, loser.id, False)
        embed.title = f"🏆 ¡{winner.display_name} gana el duelo!"
        embed.color = config.COLOR_OK
        embed.description += f"\n\n{winner.mention} se lleva {fmt(self.bet * 2)}"
        await interaction.edit_original_response(embed=embed)
        await check_achievements(self.cog.bot, winner, interaction.channel)
        await check_achievements(self.cog.bot, loser, interaction.channel)

    @discord.ui.button(label="Rechazar", emoji="🏳️", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable()
        await interaction.response.edit_message(
            embed=discord.Embed(description=f"🏳️ {self.rival.mention} ha rechazado el duelo. ¡Gallina! 🐔", color=config.COLOR_ERROR),
            view=self,
        )

    async def on_timeout(self):
        if not self.done and self.message:
            self.disable()
            try:
                await self.message.edit(embed=discord.Embed(description="⏰ El duelo ha caducado.", color=config.COLOR_ERROR), view=self)
            except discord.HTTPException:
                pass


# ==================================================================== COG
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    # ---------------------------------------------------------------- moneda
    @app_commands.command(name="moneda", description="Cara o cruz: si aciertas, duplicas la apuesta")
    @app_commands.describe(apuesta="Monedas que apuestas", lado="Cara o cruz")
    @app_commands.choices(lado=[app_commands.Choice(name="🪙 Cara", value="cara"),
                                app_commands.Choice(name="❌ Cruz", value="cruz")])
    async def moneda(self, interaction: discord.Interaction, apuesta: Bet, lado: app_commands.Choice[str]):
        if not await take_bet(interaction, apuesta):
            return
        res = random.choice(["cara", "cruz"])
        won = res == lado.value
        if won:
            self.db.add_coins(interaction.user.id, apuesta * 2)
        record_game(self.db, interaction.user.id, won)
        res_emoji = "🪙" if res == "cara" else "❌"
        text = (
            f"### {res_emoji} Ha salido: **{res.upper()}**\n\n"
            f"> {'🎉 **¡Enhorabuena!** Has ganado ' + fmt(apuesta * 2) + '.' if won else '😢 **Mala suerte.** Has perdido ' + fmt(apuesta) + '.'}\n\n"
            f"-# Apostaste al lado: **{lado.name}**"
        )
        await interaction.response.send_message(embed=result_embed("🪙 Cara o Cruz", text, won))
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # ----------------------------------------------------------------- dados
    @app_commands.command(name="dados", description="Tira 2 dados contra el bot: el que saque más gana")
    @app_commands.describe(apuesta="Monedas que apuestas")
    async def dados(self, interaction: discord.Interaction, apuesta: Bet):
        if not await take_bet(interaction, apuesta):
            return
        you = [random.randint(1, 6) for _ in range(2)]
        bot = [random.randint(1, 6) for _ in range(2)]
        ys, bs = sum(you), sum(bot)
        if ys > bs:
            won = True
            self.db.add_coins(interaction.user.id, apuesta * 2)
            res = f"🎉 ¡Victoria! Has ganado **{fmt(apuesta * 2)}**."
        elif ys == bs:
            won = None
            self.db.add_coins(interaction.user.id, apuesta)
            res = "🤝 ¡Empate! Recuperas tu apuesta íntegra."
        else:
            won = False
            res = f"😢 Has perdido **{fmt(apuesta)}**."
        record_game(self.db, interaction.user.id, bool(won))
        desc = (
            f"### 🎲 Duelo de Dados de Casino\n"
            f"👤 **Tu tirada:** {DICE[you[0]-1]} {DICE[you[1]-1]} ─ **{ys} puntos**\n"
            f"🤖 **Trobia Bot:** {DICE[bot[0]-1]} {DICE[bot[1]-1]} ─ **{bs} puntos**\n\n"
            f"> {res}\n\n"
            f"-# Apuesta en juego: {fmt(apuesta)}"
        )
        await interaction.response.send_message(embed=result_embed("🎲 Duelo de Dados", desc, won))
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # ----------------------------------------------------------- tragaperras
    @app_commands.command(name="tragaperras", description="Juega a la tragaperras 🎰 (¡7️⃣7️⃣7️⃣ paga x100!)")
    @app_commands.describe(apuesta="Monedas que apuestas")
    async def tragaperras(self, interaction: discord.Interaction, apuesta: Bet):
        if not await take_bet(interaction, apuesta):
            return
        symbols = [s for s, _, _ in SLOT_SYMBOLS]
        weights = [w for _, w, _ in SLOT_SYMBOLS]
        reels = random.choices(symbols, weights=weights, k=3)

        box_spin = (
            "```text\n"
            "╔═════════════════════════╗\n"
            "║   [ ❓ ]   [ ❓ ]   [ ❓ ]   ║\n"
            "╚═════════════════════════╝\n"
            "```"
        )
        e = discord.Embed(title="🎰 Tragaperras de Trobia", description=f"### ¡Tirando de la palanca!...\n{box_spin}", color=config.COLOR_INFO)
        await interaction.response.send_message(embed=e)
        for shown in (1, 2):
            await asyncio.sleep(0.8)
            vis = reels[:shown] + ["❓"] * (3 - shown)
            spin_frame = (
                "```text\n"
                "╔═════════════════════════╗\n"
                f"║   [ {vis[0]} ]   [ {vis[1]} ]   [ {vis[2]} ]   ║\n"
                "╚═════════════════════════╝\n"
                "```"
            )
            e.description = f"### ¡Rodillos girando!...\n{spin_frame}"
            await interaction.edit_original_response(embed=e)
        await asyncio.sleep(0.8)

        uid = interaction.user.id
        payout = 0
        if reels[0] == reels[1] == reels[2]:
            mult = next(m for s, _, m in SLOT_SYMBOLS if s == reels[0])
            payout = apuesta * mult
            if reels[0] == "7️⃣":
                self.db.incr_stat(uid, "slots_jackpots")
                msg = f"🚨🚨 **¡¡JACKPOT SUPREMO!!** 🚨🚨\n¡Has ganado **{fmt(payout)}** (Multiplicador x{mult})!"
            else:
                msg = f"🎉 **¡TRES EN LÍNEA!** Has ganado **{fmt(payout)}** (Multiplicador x{mult})!"
        elif len(set(reels)) == 2:
            payout = int(apuesta * 1.5)
            msg = f"✨ **¡Doble acierto!** Te llevas **{fmt(payout)}** (Multiplicador x1.5)."
        else:
            msg = f"😢 **Nada esta vez.** Pierdes tu apuesta de {fmt(apuesta)}."
        if payout:
            self.db.add_coins(uid, payout)
        won = payout > apuesta
        record_game(self.db, uid, won)

        final_box = (
            "```text\n"
            "╔═════════════════════════╗\n"
            f"║   [ {reels[0]} ]   [ {reels[1]} ]   [ {reels[2]} ]   ║\n"
            "╚═════════════════════════╝\n"
            "```"
        )
        e.description = f"### Resultado de la Tirada:\n{final_box}\n> {msg}\n\n-# Apuesta: {fmt(apuesta)}"
        e.color = config.COLOR_OK if payout else config.COLOR_ERROR
        await interaction.edit_original_response(embed=e)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # ------------------------------------------------------------- blackjack
    @app_commands.command(name="blackjack", description="Juega al blackjack contra el crupier 🃏")
    @app_commands.describe(apuesta="Monedas que apuestas")
    async def blackjack(self, interaction: discord.Interaction, apuesta: Bet):
        if not await take_bet(interaction, apuesta):
            return
        view = BlackjackView(self, interaction.user, apuesta)
        uid = interaction.user.id
        if hand_value(view.player) == 21:  # blackjack natural
            view.finished = True
            if hand_value(view.dealer) == 21:
                self.db.add_coins(uid, apuesta)
                text, won = "🤝 ¡Los dos tenéis blackjack! Empate.", None
            else:
                payout = int(apuesta * 2.5)
                self.db.add_coins(uid, payout)
                self.db.incr_stat(uid, "bj_naturals")
                text, won = f"🃏 **¡BLACKJACK NATURAL!** Te llevas {fmt(payout)} (x2.5)", True
            record_game(self.db, uid, bool(won))
            await interaction.response.send_message(embed=view.embed(True, text, won))
            await check_achievements(self.bot, interaction.user, interaction.channel)
            return
        try:
            await interaction.response.send_message(embed=view.embed(), view=view)
            view.message = await interaction.original_response()
        except discord.HTTPException:
            view.finished = True
            self.db.add_coins(uid, apuesta)
            return

    # ------------------------------------------------------------------- ppt
    @app_commands.command(name="ppt", description="Piedra, papel o tijera contra el bot (apuesta opcional)")
    @app_commands.describe(apuesta="Monedas que apuestas (opcional)")
    async def ppt(self, interaction: discord.Interaction, apuesta: Optional[Bet] = None):
        bet = apuesta or 0
        if bet and not await take_bet(interaction, bet):
            return
        desc = "¡Elige tu jugada!" + (f"\nApuesta: {fmt(bet)}" if bet else "")
        try:
            await interaction.response.send_message(
                embed=result_embed("🪨📄✂️ Piedra, papel o tijera", desc, None), view=PPTView(self, interaction.user, bet)
            )
        except discord.HTTPException:
            if bet:
                self.db.add_coins(interaction.user.id, bet)

    # ----------------------------------------------------------------- duelo
    @app_commands.command(name="duelo", description="Reta a otra persona a un duelo con apuesta ⚔️")
    @app_commands.describe(rival="A quién retas", apuesta="Monedas que apuesta cada uno")
    async def duelo(self, interaction: discord.Interaction, rival: discord.Member, apuesta: Bet):
        if rival.bot or rival.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Elige a otra persona (ni bots ni tú mismo)."), ephemeral=True)
            return
        if self.db.get_coins(interaction.user.id) < apuesta:
            await interaction.response.send_message(embed=error_embed("No tienes monedas suficientes."), ephemeral=True)
            return
        if self.db.get_coins(rival.id) < apuesta:
            await interaction.response.send_message(embed=error_embed(f"{rival.display_name} no tiene monedas suficientes."), ephemeral=True)
            return
        view = DuelView(self, interaction.user, rival, apuesta)
        embed = discord.Embed(
            title="⚔️ ¡Desafío!",
            description=f"{interaction.user.mention} reta a {rival.mention} a un duelo por {fmt(apuesta)} cada uno.\n"
                        f"El ganador se lleva {fmt(apuesta * 2)}. Tienes 60 segundos para aceptar.",
            color=config.COLOR_MAIN,
        )
        await interaction.response.send_message(content=rival.mention, embed=embed, view=view)
        view.message = await interaction.original_response()


async def setup(bot):
    await bot.add_cog(Games(bot))
