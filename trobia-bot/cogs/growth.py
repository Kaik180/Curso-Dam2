"""Crecimiento y comunidad: Bump rewards (Disboard), sistema de invitaciones, bienvenidas visuales, preguntas diarias y eventos."""
import random
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

import config
from cards import render_welcome_card
from utils import check_achievements, error_embed, fmt, grant_xp, ok_embed

DISBOARD_BOT_ID = 302050872383242240
WELCOME_CHANNEL_ID = 1565494728898646157
BOT_COMMANDS_CHANNEL_ID = 1565494754006007808
CHAT_GENERAL_CHANNEL_ID = 1565494744560173096
ROLES_CHANNEL_ID = 1565494731931386037
INTRO_CHANNEL_ID = 1569863781033582704
BUMP_ROLE_ID = 1574142259274850394

BUMP_COOLDOWN = 7200       # 2 horas (cooldown oficial de Disboard)
BUMP_REWARD_COINS = 250
INVITE_REWARD_COINS = 300
NEWCOMER_BONUS_COINS = 150

DAILY_QUESTIONS = [
    "🎮 ¿Cuál es el videojuego al que más horas le has echado en toda tu vida?",
    "🍿 ¿Qué película podrías ver 10 veces seguidas sin cansarte nunca?",
    "🍊 Debate serio de la terreta: ¿Horchata con fartons o agua de Valencia?",
    "🕹️ Si solo pudieras jugar a UN juego durante todo el año, ¿cuál elegirías?",
    "🎬 ¿Cuál es la serie que todo el mundo te recomienda y todavía no has visto?",
    "🐾 Si pudieras tener un Trobimon real en casa, ¿cuál de los 48 elegirías?",
    "🍕 ¿Pizza con piña: obra maestra incomprendida o crimen contra la humanidad?",
    "🎧 ¿Qué banda sonora de videojuego o película te pone los pelos de punta?",
    "🏆 ¿Cuál ha sido tu mayor logro o momento más épico jugando online?",
    "🌙 ¿Eres más de madrugar o de trasnochar hasta las 4 AM en llamada?",
    "📺 ¿Cine en pantalla gigante con palomitas o manta y sofá en casa?",
    "🎲 ¿Qué juego cooperativo o party game siempre acaba en risas (o discusiones)?",
    "🏖️ Plan perfecto de fin de semana: ¿playa, montaña, sofá o maratón de vicio?",
    "👾 ¿Cuál fue la primera consola o PC en el que jugaste de pequeño/a?",
    "🔥 ¿Qué juego te hizo enfadar más pero aún así seguías jugándolo?",
    "🍿 ¿Cuál es el mejor giro de guion que has visto en una película?",
    "🎵 ¿Qué canción nunca te saltas cuando sale en aleatorio?",
    "⚔️ En los RPG, ¿prefieres ser tanque, DPS, healer o mago?",
    "🥘 ¿Cuál es el plato de comida que nunca falla cuando quedas con amigos?",
    "🚀 Si pudieras vivir dentro del mundo de cualquier videojuego, ¿cuál sería?",
]


class BumpPingView(discord.ui.View):
    """Botón persistente para activar/desactivar el rol 🔔 Ping Bump."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Avisarme para /bump (+250 🪙)",
        emoji="🔔",
        style=discord.ButtonStyle.primary,
        custom_id="trobia:toggle_bump_ping",
    )
    async def toggle_bump(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if not guild or not isinstance(interaction.user, discord.Member):
            return
        role = guild.get_role(BUMP_ROLE_ID)
        if not role:
            await interaction.response.send_message(embed=error_embed("No se encontró el rol de avisos de Bump."), ephemeral=True)
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, reason="Usuario desactivó aviso de Bump")
            await interaction.response.send_message(
                embed=ok_embed("🔕 Has desactivado los avisos de `/bump`."), ephemeral=True
            )
        else:
            await interaction.user.add_roles(role, reason="Usuario activó aviso de Bump")
            await interaction.response.send_message(
                embed=ok_embed(
                    f"🔔 ¡Rol {role.mention} activado!\n"
                    f"-# Te avisaremos cada 2 horas cuando puedas usar `/bump` para ganar **{fmt(BUMP_REWARD_COINS)} + 1x Orbe Básico**."
                ),
                ephemeral=True,
            )


class EventRSVPView(discord.ui.View):
    """Vista interactiva de confirmación de asistencia para /evento."""

    def __init__(self, title: str, when: str, desc: str, host_name: str):
        super().__init__(timeout=None)
        self.title_txt = title
        self.when_txt = when
        self.desc_txt = desc
        self.host_name = host_name
        self.attendees: list[int] = []

    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"📅 EVENTO · {self.title_txt}",
            description=(
                f"### 🕒 {self.when_txt}\n"
                f"> {self.desc_txt}\n\n"
                f"-# Organizado por **{self.host_name}** · Pulsa **¡Me apunto!** abajo para reservar sitio."
            ),
            color=config.COLOR_MAIN,
        )
        if self.attendees:
            mentions = " · ".join(f"<@{uid}>" for uid in self.attendees[:25])
            extra = f" *(+{len(self.attendees) - 25} más)*" if len(self.attendees) > 25 else ""
            embed.add_field(name=f"✅ Apuntados ({len(self.attendees)})", value=mentions + extra, inline=False)
        else:
            embed.add_field(name="✅ Apuntados (0)", value="*¡Sé el primero en apuntarte!*", inline=False)
        embed.set_footer(text="trobia Eventos · Invita a tus amigos con /invitar")
        return embed

    @discord.ui.button(label="¡Me apunto!", emoji="✅", style=discord.ButtonStyle.success)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = interaction.user.id
        if uid not in self.attendees:
            self.attendees.append(uid)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="No puedo ir", emoji="❌", style=discord.ButtonStyle.secondary)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = interaction.user.id
        if uid in self.attendees:
            self.attendees.remove(uid)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)


class Growth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self._invite_cache: dict[str, int] = {}
        self._last_q_ts: float = 0.0
        self.bot.add_view(BumpPingView())

    async def cog_unload(self):
        self.bump_reminder_loop.cancel()

    async def _refresh_invites(self, guild: discord.Guild):
        try:
            invs = await guild.invites()
            self._invite_cache = {inv.code: (inv.uses or 0) for inv in invs}
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(config.GUILD_ID)
        if guild:
            await self._refresh_invites(guild)
        if not self.bump_reminder_loop.is_running():
            self.bump_reminder_loop.start()

    # ---------------------------------------- Recordatorio automático de Bump
    @tasks.loop(minutes=1)
    async def bump_reminder_loop(self):
        last_ts = self.db.get_stat(0, "last_bump_ts")
        reminded = self.db.get_stat(0, "bump_reminded")
        if last_ts <= 0 or reminded:
            return
        if int(time.time()) >= last_ts + BUMP_COOLDOWN:
            self.db.set_stat(0, "bump_reminded", 1)
            ch_id = self.db.get_stat(0, "bump_channel_id") or BOT_COMMANDS_CHANNEL_ID
            ch = self.bot.get_channel(ch_id) or self.bot.get_channel(BOT_COMMANDS_CHANNEL_ID)
            if not ch:
                return
            embed = discord.Embed(
                title="🚀 ¡Ya se puede volver a hacer /bump!",
                description=(
                    "### Ayuda a subir **trobia** al Top de Disboard\n"
                    f"Usa **`/bump`** ahora mismo para atraer nuevos miembros y llévate al instante:\n"
                    f"• **{fmt(BUMP_REWARD_COINS)}**\n"
                    f"• **1x 🔴 Orbe Básico** para `/cazar`\n"
                    f"• **+40 XP** de entrenador\n\n"
                    "-# Activa o desactiva este aviso con el botón de abajo."
                ),
                color=config.COLOR_MAIN,
            )
            try:
                await ch.send(content=f"<@&{BUMP_ROLE_ID}>", embed=embed, view=BumpPingView())
            except discord.HTTPException:
                pass

    # ------------------------------------------ Listeners: Disboard + Welcome
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or message.guild.id != config.GUILD_ID:
            return

        # 1) Detectar nuevo miembro sin necesitar privileged Members Intent
        if message.type == discord.MessageType.new_member and not message.author.bot:
            await self._handle_new_member(message)
            return

        # 2) Detectar /bump exitoso de DISBOARD.org
        if message.author.id == DISBOARD_BOT_ID:
            await self._handle_disboard_message(message)

    async def _handle_disboard_message(self, message: discord.Message):
        # Extraer el usuario que ejecutó /bump (funciona sin message_content intent)
        bumper = None
        if message.interaction_metadata and message.interaction_metadata.user:
            bumper = message.interaction_metadata.user
        elif getattr(message, "interaction", None) and message.interaction.user:
            bumper = message.interaction.user
        if not bumper or bumper.bot:
            return

        # Evitar premiar mensajes de cooldown de Disboard (protección por timestamp de 110 min)
        now = int(time.time())
        last_ts = self.db.get_stat(0, "last_bump_ts")
        if now - last_ts < 6600:
            return

        # Comprobar si el embed parece error (color rojo) cuando esté disponible
        if message.embeds:
            col = message.embeds[0].color
            if col and col.value in (0xE74C3C, 0xFF0000, 0xED4245):
                return

        self.db.set_stat(0, "last_bump_ts", now)
        self.db.set_stat(0, "bump_reminded", 0)
        self.db.set_stat(0, "bump_channel_id", message.channel.id)

        uid = bumper.id
        self.db.ensure_user(uid)
        self.db.add_coins(uid, BUMP_REWARD_COINS)
        self.db.add_item(uid, "orbe_basico", 1)
        self.db.incr_stat(uid, "bumps_done", 1)
        total_bumps = self.db.get_stat(uid, "bumps_done")
        next_ts = now + BUMP_COOLDOWN

        embed = discord.Embed(
            title="🚀 ¡Gracias por impulsar trobia en Disboard!",
            description=(
                f"### {bumper.mention} ha subido el servidor al Top\n"
                f"**Recompensa recibida:**\n"
                f"• +{fmt(BUMP_REWARD_COINS)}\n"
                f"• +1x 🔴 **Orbe Básico**\n"
                f"• +40 XP\n\n"
                f"⏱️ Próximo `/bump` disponible <t:{next_ts}:R> (<t:{next_ts}:t>).\n"
                f"-# Bumps totales de {bumper.display_name}: **{total_bumps}** · ¡Pulsa el botón para recibir aviso!"
            ),
            color=config.COLOR_OK,
        )
        try:
            await message.channel.send(embed=embed, view=BumpPingView())
        except discord.HTTPException:
            pass
        await grant_xp(self.bot, bumper, 40, message.channel)

    async def _handle_new_member(self, message: discord.Message):
        member = message.author
        guild = message.guild
        inviter = None

        # Comparar invitaciones para atribuir referido
        try:
            invs = await guild.invites()
            for inv in invs:
                prev = self._invite_cache.get(inv.code, 0)
                if (inv.uses or 0) > prev:
                    inviter = inv.inviter
                    break
            self._invite_cache = {inv.code: (inv.uses or 0) for inv in invs}
        except discord.HTTPException:
            pass

        # Bonus de bienvenida al recién llegado
        self.db.ensure_user(member.id)
        self.db.add_coins(member.id, NEWCOMER_BONUS_COINS)
        self.db.add_item(member.id, "orbe_basico", 1)

        inviter_txt = ""
        inviter_name = None
        if inviter and not inviter.bot and inviter.id != member.id:
            inviter_name = inviter.display_name
            self.db.ensure_user(inviter.id)
            self.db.add_coins(inviter.id, INVITE_REWARD_COINS)
            self.db.add_item(inviter.id, "orbe_super", 1)
            self.db.incr_stat(inviter.id, "invites_count", 1)
            inv_total = self.db.get_stat(inviter.id, "invites_count")
            inviter_txt = (
                f"\n🤝 Invitado/a por {inviter.mention} "
                f"(+{fmt(INVITE_REWARD_COINS)} + 1x 🔵 Súper Orbe · **{inv_total}** invitados)"
            )

        member_count = guild.member_count or 1
        card_file, card_url = render_welcome_card(member.display_name, member_count, inviter_name)

        embed = discord.Embed(
            title=f"🍊 ¡Bienvenido/a a trobia, {member.display_name}!",
            description=(
                f"### ¡Qué alegría tenerte por aquí, {member.mention}!{inviter_txt}\n\n"
                f"🎁 **Regalo de bienvenida entregado:** +{fmt(NEWCOMER_BONUS_COINS)} y **1x 🔴 Orbe Básico**.\n\n"
                f"**Primeros pasos rápidos:**\n"
                f"1️⃣ Elige tus juegos y zona en <#{ROLES_CHANNEL_ID}>\n"
                f"2️⃣ Preséntate en <#{INTRO_CHANNEL_ID}> y saluda en <#{CHAT_GENERAL_CHANNEL_ID}>\n"
                f"3️⃣ Captura tu primer **Trobimon** usando `/cazar` en <#{BOT_COMMANDS_CHANNEL_ID}>"
            ),
            color=config.COLOR_MAIN,
        )
        embed.set_image(url=card_url)
        embed.set_footer(text=f"trobia · Miembro #{member_count} · Usa /invitar para traer amigos y ganar premios")
        try:
            await message.channel.send(embed=embed, file=card_file, view=BumpPingView())
        except discord.HTTPException:
            pass
        if inviter and not inviter.bot:
            await check_achievements(self.bot, inviter, message.channel)

    # --------------------------------------------------------------- /invitar
    @app_commands.command(name="invitar", description="Consigue tu enlace personal de invitación y gana premios por cada amigo 🎁")
    async def invitar(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            return
        uid = interaction.user.id
        personal_url = None

        # Buscar si el usuario ya tiene una invitación permanente creada
        try:
            invs = await guild.invites()
            for inv in invs:
                if inv.inviter and inv.inviter.id == uid and inv.max_age == 0 and inv.max_uses == 0:
                    personal_url = inv.url
                    break
            if not personal_url:
                ch = guild.get_channel(WELCOME_CHANNEL_ID) or interaction.channel
                new_inv = await ch.create_invite(max_age=0, max_uses=0, unique=True, reason=f"Invitación personal de {interaction.user}")
                personal_url = new_inv.url
                self._invite_cache[new_inv.code] = 0
        except discord.HTTPException:
            personal_url = "https://discord.gg/XCYchd9jgp"

        count = self.db.get_stat(uid, "invites_count")
        embed = discord.Embed(
            title="💌 Tu Enlace de Invitación Personal",
            description=(
                f"### Comparte este enlace y trae gente nueva a **trobia**:\n"
                f"{personal_url}\n\n"
                f"**🎁 Recompensas automáticas por cada amigo que entre:**\n"
                f"• **Para ti:** +{fmt(INVITE_REWARD_COINS)} + **1x 🔵 Súper Orbe**\n"
                f"• **Para tu amigo:** +{fmt(NEWCOMER_BONUS_COINS)} + **1x 🔴 Orbe Básico** de bienvenida\n\n"
                f"📊 **Tus invitados confirmados:** `{count}`\n"
                f"-# Consulta el ranking de promotores con `/top_crecimiento`."
            ),
            color=config.COLOR_MAIN,
        )
        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------- /top_crecimiento
    @app_commands.command(name="top_crecimiento", description="Ranking de los miembros que más ayudan a crecer el servidor 🚀")
    async def top_crecimiento(self, interaction: discord.Interaction):
        bumps_rows = self.db.conn.execute(
            "SELECT user_id, value FROM stats WHERE key = 'bumps_done' AND user_id > 0 AND value > 0 ORDER BY value DESC LIMIT 10"
        ).fetchall()
        inv_rows = self.db.conn.execute(
            "SELECT user_id, value FROM stats WHERE key = 'invites_count' AND user_id > 0 AND value > 0 ORDER BY value DESC LIMIT 10"
        ).fetchall()

        medals = ["🥇", "🥈", "🥉"] + [f"`#{i}`" for i in range(4, 11)]
        b_lines = [f"{medals[i]} <@{r['user_id']}> ─ **{r['value']}** bumps" for i, r in enumerate(bumps_rows)]
        i_lines = [f"{medals[i]} <@{r['user_id']}> ─ **{r['value']}** invitados" for i, r in enumerate(inv_rows)]

        embed = discord.Embed(
            title="🚀 Top Crecimiento de trobia",
            description="-# ¡Ayuda a crecer la comunidad haciendo `/bump` en Disboard o compartiendo tu `/invitar`!",
            color=config.COLOR_MAIN,
        )
        embed.add_field(
            name="📣 Top Bumpers (Disboard)",
            value="\n".join(b_lines) or "*Nadie ha hecho `/bump` todavía. ¡Sé el primero!*",
            inline=True,
        )
        embed.add_field(
            name="💌 Top Invitadores",
            value="\n".join(i_lines) or "*Aún no hay invitaciones registradas. Usa `/invitar`.*",
            inline=True,
        )
        embed.set_footer(text="Cada /bump da +250 🪙 + 1 Orbe · Cada invitado da +300 🪙 + 1 Súper Orbe")
        await interaction.response.send_message(embed=embed, view=BumpPingView(), allowed_mentions=discord.AllowedMentions.none())

    # ------------------------------------------------------------- /ping_bump
    @app_commands.command(name="ping_bump", description="Activa o desactiva el aviso cada 2h para hacer /bump y ganar monedas 🔔")
    async def ping_bump(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild or not isinstance(interaction.user, discord.Member):
            return
        role = guild.get_role(BUMP_ROLE_ID)
        if not role:
            await interaction.response.send_message(embed=error_embed("No existe el rol de aviso de Bump."), ephemeral=True)
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=ok_embed("🔕 Avisos de `/bump` desactivados."), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                embed=ok_embed(f"🔔 Rol {role.mention} activado. Te avisaremos cada 2h para ganar **{fmt(BUMP_REWARD_COINS)} + 1x Orbe Básico**."),
                ephemeral=True,
            )

    # -------------------------------------------------------------- /pregunta
    @app_commands.command(name="pregunta", description="Lanza una Pregunta del Día para activar el chat 💬")
    async def pregunta(self, interaction: discord.Interaction):
        now = time.time()
        if now - self._last_q_ts < 600 and not interaction.user.guild_permissions.manage_messages:
            rem = int(600 - (now - self._last_q_ts))
            await interaction.response.send_message(
                embed=error_embed(f"Ya se lanzó una pregunta hace poco. Espera **{rem}s** para lanzar otra."),
                ephemeral=True,
            )
            return
        self._last_q_ts = now
        q = random.choice(DAILY_QUESTIONS)
        embed = discord.Embed(
            title="💬 Pregunta del Día — trobia",
            description=f"### {q}\n\n-# ¡Responde en el chat y debate con la comunidad!",
            color=config.COLOR_INFO,
        )
        embed.set_footer(text=f"Lanzada por {interaction.user.display_name} · ¡Anímate a participar!")
        await interaction.response.send_message(embed=embed)

    # ---------------------------------------------------------------- /evento
    @app_commands.command(name="evento", description="[Staff] Publica un evento con botón interactivo de asistencia 📅")
    @app_commands.default_permissions(manage_events=True)
    @app_commands.describe(
        titulo="Nombre del evento (ej: Noche de Cine: Interestelar)",
        cuando="Día y hora (ej: Viernes 22:00h España)",
        descripcion="Detalles del plan y premios si los hay",
        mencionar="Rol opcional al que avisar del evento",
    )
    async def evento(
        self,
        interaction: discord.Interaction,
        titulo: str,
        cuando: str,
        descripcion: str,
        mencionar: Optional[discord.Role] = None,
    ):
        view = EventRSVPView(titulo, cuando, descripcion, interaction.user.display_name)
        content = mencionar.mention if mencionar else None
        await interaction.response.send_message(content=content, embed=view.build_embed(), view=view)


async def setup(bot):
    await bot.add_cog(Growth(bot))
