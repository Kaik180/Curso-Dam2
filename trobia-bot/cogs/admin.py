"""Comandos de administración y Enciclopedia/Guía interactiva completa (/ayuda y /guia)."""
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import config
from data.creatures import (
    CREATURES,
    DUAL_ELEMENT_COMBOS,
    ELEMENTS,
    MONO_ELEMENT_COMBOS,
    PET_GEAR,
    SCROLL_SKILLS,
)
from data.items import ITEMS, RARITIES, item_label
from utils import check_achievements, error_embed, fmt, ok_embed

HELP_SECTIONS = [
    ("general",       "📋 Vista General (Todos los comandos)",        "Resumen completo de todos los comandos del bot"),
    ("criaturas",     "🐾 Las 48 Criaturas (6 por Elemento)",         "Catálogo de las 48 especies por elemento y evolución"),
    ("pasivas",       "🌟 Las 48 Habilidades Pasivas",                "Pasivas Propias, de Equipo y contra el Rival"),
    ("combinaciones", "🧬 Combinaciones de Equipo (3 iguales y dúos)", "Las 8 Resonancias 3x y 9 Reacciones Elementales"),
    ("objetos",       "🎒 Objetos Equipables y Pergaminos (MT)",       "Los 12 accesorios equipables y 8 habilidades secretas"),
    ("combate",       "⚔️ Combate 3v3, Torre, Efectos y Elementos",   "Reglas del combate 3v3, relevos, estados y 8 elementos"),
    ("duplicados",    "⭐ Trobimons Repetidos (Estrellas y Portal)",   "Fusión 1★-5★, liberar por recompensas y Prodigioso"),
    ("economia",      "💰 Economía, Tienda, Cajas y Casino",           "Monedas, trabajo, cajas, minijuegos, perfil y logros"),
]


def build_help_embed(section: str = "general") -> discord.Embed:
    c = config.CURRENCY
    cname = config.CURRENCY_NAME

    # --------------------------------------------------------- 2. CRIATURAS (48)
    if section == "criaturas":
        e = discord.Embed(
            title="🐾 Catálogo Completo de las 48 Criaturas (6 por Elemento)",
            description=(
                "Existen **48 especies originales** repartidas en **8 elementos** (**6 especies distintas en cada elemento**). "
                "Usa `/cazar`, `/incubadora` o `/mascota prodigioso` para conseguirlas todas y `/trobidex` para ver su ilustración:"
            ),
            color=0x2ECC71,
        )
        by_elem: dict[str, list[dict]] = {}
        for sp in sorted(CREATURES.values(), key=lambda x: x["num"]):
            by_elem.setdefault(sp["element"], []).append(sp)

        for el_key, el_info in ELEMENTS.items():
            sp_list = by_elem.get(el_key, [])
            lines = []
            for sp in sp_list:
                rar = RARITIES[sp["rarity"]]
                evo = f" ➔ *(Nv.{sp['evolve_level']} {CREATURES[sp['evolves_to']]['name']})*" if sp["evolves_to"] else ""
                lines.append(
                    f"`#{sp['num']:02d}` {rar['emoji']} {sp['emoji']} **{sp['name']}** "
                    f"(❤️{sp['base_hp']} · ⚔️{sp['base_atk']}){evo}"
                )
            beats_txt = ", ".join(f"{ELEMENTS[b]['emoji']}{ELEMENTS[b]['name']}" for b in el_info["beats"])
            e.add_field(
                name=f"{el_info['emoji']} {el_info['name']} ({len(sp_list)} especies · Vence a: {beats_txt})",
                value="\n".join(lines)[:1024],
                inline=False,
            )
        e.set_footer(text="Usa /trobidex especie:<nombre> para ver la ilustración HD y las 4 habilidades de cada criatura")
        return e

    # --------------------------------------------------------- 3. PASIVAS (48)
    if section == "pasivas":
        e = discord.Embed(
            title="🌟 Guía de las 48 Habilidades Pasivas Únicas",
            description=(
                "Cada Trobimon tiene una **Habilidad Pasiva innata** que se activa automáticamente en combate:\n"
                "• **`[Propia]`**: Mejora al propio Trobimon · **`[Equipo]`**: Potencia a **tus 3 Trobimons** · **`[Rival]`**: Debilita/daña al enemigo."
            ),
            color=0x3498DB,
        )
        by_elem: dict[str, list[dict]] = {}
        for sp in sorted(CREATURES.values(), key=lambda x: x["num"]):
            by_elem.setdefault(sp["element"], []).append(sp)

        for el_key, el_info in ELEMENTS.items():
            lines = []
            for sp in by_elem.get(el_key, []):
                pas = sp.get("passive", {})
                lines.append(f"• {sp['emoji']} **{sp['name']}** — {pas['emoji']} **{pas['name']}:** {pas['desc']}")
            e.add_field(
                name=f"{el_info['emoji']} Pasivas de {el_info['name']}",
                value="\n".join(lines)[:1024],
                inline=False,
            )
        e.set_footer(text="Las pasivas de [Equipo] y [Rival] de tus 3 Trobimons se suman entre sí en /equipo ver")
        return e

    # --------------------------------------------------------- 4. COMBINACIONES
    if section == "combinaciones":
        e = discord.Embed(
            title="🧬 Combinaciones Especiales de Equipo (3 Iguales y Parejas)",
            description=(
                "Al formar tu equipo de 3 Trobimons con `/equipo asignar`, activas poderosos bonus según los elementos que combines. "
                "Puedes comprobar las tuyas en vivo con `/equipo combinaciones`:"
            ),
            color=0x9B59B6,
        )
        mono_lines = [
            f"• **{combo['name']}**\n  *{combo['desc']}*"
            for combo in MONO_ELEMENT_COMBOS.values()
        ]
        e.add_field(
            name="👑 1. Juntar 3 del MISMO Elemento (8 Resonancias Supremas)",
            value="\n".join(mono_lines)[:1024],
            inline=False,
        )
        dual_lines = [
            f"• **{dc['name']}** — *{dc['desc']}*"
            for dc in DUAL_ELEMENT_COMBOS
        ]
        e.add_field(
            name="⚗️ 2. Juntar Ciertos Elementos (9 Reacciones Elementales — Acumulables)",
            value="\n".join(dual_lines)[:1024],
            inline=False,
        )
        e.add_field(
            name="🌈 3. Otras Sinergias de Formación",
            value=(
                "• **🌈 Triada Elemental (3 elementos distintos):** `+12% HP` y `+12% ATQ` a todo el equipo (se suma a las Reacciones Elementales que tengas).\n"
                "• **🔥 Dúo Elemental (2 del mismo elemento + 1 distinto):** `+14% ATQ` y `+8% HP` a todo el equipo."
            ),
            inline=False,
        )
        return e

    # --------------------------------------------------------- 5. OBJETOS Y PERGAMINOS
    if section == "objetos":
        e = discord.Embed(
            title="🎒 Objetos Equipables (12) y Pergaminos de Habilidad (8)",
            description="Todos se pueden comprar en `/tienda` o conseguir abriendo cajas con `/abrir`.",
            color=0xE67E22,
        )
        gear_lines = []
        for gid, ginfo in PET_GEAR.items():
            it = ITEMS[gid]
            rar = RARITIES[it["rarity"]]
            gear_lines.append(
                f"• {rar['emoji']} {it['emoji']} **{it['name']}** ({fmt(it['price'])}) — `{ginfo['summary']}`"
            )
        e.add_field(
            name="🎒 12 Objetos Equipables (`/mascota objeto` — 1 por Trobimon)",
            value="\n".join(gear_lines)[:1024],
            inline=False,
        )

        scroll_lines = []
        for sid, sk in SCROLL_SKILLS.items():
            it = ITEMS[sid]
            rar = RARITIES[it["rarity"]]
            scroll_lines.append(
                f"• {rar['emoji']} {sk['emoji']} **{sk['name']}** `[{sk['role']} · x{sk['dmg_mult']} · CD:{sk['cd']}t]` ({fmt(it['price'])})\n"
                f"  *{sk['desc']}*"
            )
        e.add_field(
            name="📜 8 Pergaminos de 5ª Habilidad Secreta (`/mascota habilidad`)",
            value="\n".join(scroll_lines)[:1024],
            inline=False,
        )
        return e

    # --------------------------------------------------------- 6. COMBATE 3V3 Y TORRE
    if section == "combate":
        e = discord.Embed(
            title="⚔️ Combate de Equipos 3v3, Torre de Campeones y Estados",
            description="Los combates enfrentan a **2 equipos de hasta 3 Trobimons** por turnos interactivos con botones.",
            color=0xE74C3C,
        )
        e.add_field(
            name="🥊 Modos de Combate y Relevos",
            value=(
                "• **`/mascota entrenar`** — Batalla 3v3 contra una Patrulla Salvaje (monedas + **50 XP a tus 3 Trobimons**).\n"
                "• **`/mascota torre`** — **🏯 Torre de Campeones:** Sube pisos infinitos contra Guardianes y **👑 Jefes cada 5 pisos** (da Cajas Épicas, Caramelos y miles de monedas).\n"
                "• **`/mascota combatir [@rival] [apuesta]`** — Duelo táctico 3v3 PvP contra otro jugador.\n"
                "• **🔄 Relevos en Vivo:** En tu turno puedes pulsar `Relevar` para cambiar de Trobimon activo (el que entra gana un **Escudo de `-25%` daño** ese turno)."
            ),
            inline=False,
        )
        e.add_field(
            name="✨ Diccionario de Efectos de Combate",
            value=(
                "• 🔥 **Quemadura:** `-8% HP` máx. por turno.\n"
                "• ☠️ **Veneno:** `-6% HP` máx. por turno y **reduce un `-40%` las curaciones** del afectado.\n"
                "• 🛡️ **Escudo:** Reduce el daño del próximo ataque enemigo (a menos que sea **💥 Perforante**).\n"
                "• 🌵 **Espinas:** Devuelve un porcentaje del daño recibido al atacante.\n"
                "• 🎯 **Vulnerable:** El objetivo recibe un **`+30%` de daño extra**.\n"
                "• 🔻 **Debilitar / ⬆️ Subir ATQ:** Modifica el ataque de un Trobimon o de **🎺 todo el equipo**.\n"
                "• ❄️ **Escarcha (+CD) / ⚡ Prisa (-CD):** Retrasa `+1t` las recargas rivales o acelera `-1t` las tuyas.\n"
                "• 💨 **Esquiva:** Probabilidad de evadir por completo el ataque enemigo.\n"
                "• 🎭 **Robo de Buffs:** Roba el escudo y las subidas de ATQ del enemigo para ti.\n"
                "• ☄️ **Multigolpe (2-4x)** · ⚰️ **Ejecución** (daño extra a rivales con poca vida) · 🐦‍🔥 **Renacer** (revive al caer)."
            ),
            inline=False,
        )
        return e

    # --------------------------------------------------------- 7. DUPLICADOS
    if section == "duplicados":
        e = discord.Embed(
            title="⭐ Guía de Trobimons Repetidos: Estrellas, Liberar y Portal",
            description="Cuando capturas o incubas un Trobimon cuya familia evolutiva ya tienes, salen botones rápidos y tienes **4 comandos** para aprovecharlo:",
            color=0xF1C40F,
        )
        e.add_field(
            name="1️⃣ Ascensión Estelar (`/mascota fusionar` — ⭐ a ⭐⭐⭐⭐⭐)",
            value=(
                "• Fusiona cualquier repetido de la **misma línea evolutiva** (ej. un *Mascletín* sirve para subir a tu *Ignifoc*).\n"
                "• Sube **+1 Estrella (`⭐`)** hasta **`5★` (`⭐⭐⭐⭐⭐`)** y le transfiere toda su XP.\n"
                "• **Tabla de Bonus por Estrellas:**\n"
                "  `⭐ (1★)` ➔ **+10% HP/ATQ** y **+3%** monedas en `/trabajar`\n"
                "  `⭐⭐ (2★)` ➔ **+20% HP/ATQ** y **+6%** monedas en `/trabajar`\n"
                "  `⭐⭐⭐ (3★)` ➔ **+30% HP/ATQ** y **+9%** monedas en `/trabajar`\n"
                "  `⭐⭐⭐⭐ (4★)` ➔ **+40% HP/ATQ** y **+12%** monedas en `/trabajar`\n"
                "  `⭐⭐⭐⭐⭐ (5★)` ➔ **+50% HP/ATQ** y **+15%** monedas en `/trabajar`"
            ),
            inline=False,
        )
        e.add_field(
            name="2️⃣ Liberar (`/mascota liberar`) y Gestión Masiva (`/mascota repetidos`)",
            value=(
                "• **Liberar Común:** `160 + 25/nv` monedas + `1x 🍖 Chuletón Ibérico`.\n"
                "• **Liberar Raro:** `400 + 45/nv` monedas + `2x 🍖 Chuletón Ibérico`.\n"
                "• **Liberar Épico:** `950 + 70/nv` monedas + `1x 🍬 Caramelo Místico`.\n"
                "• **Liberar Legendario:** `2.500 + 110/nv` monedas + `2x 🍬 Caramelo Místico`.\n"
                "• **`/mascota repetidos`** fusiona o libera **todos tus duplicados de golpe** en 1 clic (respetando tu `/equipo`)."
            ),
            inline=False,
        )
        e.add_field(
            name="3️⃣ Portal de Intercambio Prodigioso (`/mascota prodigioso`)",
            value="• Entrega un Trobimon repetido (+`200` monedas) y recibe al instante **otra especie distinta del mismo nivel**, con probabilidad mejorada de que salga Épico o Legendario.",
            inline=False,
        )
        return e

    # --------------------------------------------------------- 8. ECONOMÍA Y CASINO
    if section == "economia":
        e = discord.Embed(
            title=f"💰 Economía, Tienda, Cajas, Casino y Perfil ({c} {cname})",
            description=f"Todo lo que puedes hacer para ganar {c} **{cname}**, abrir cajas y personalizar tu perfil.",
            color=0xF39C12,
        )
        e.add_field(
            name="💵 Economía y Tienda",
            value=(
                "• **`/saldo [usuario]`** — Consulta tu cartera y puesto en el ranking.\n"
                "• **`/diario`** — Recompensa diaria + **1x 🔴 Orbe Básico gratis** (cajas gratis cada 3 y 7 días de racha).\n"
                "• **`/trabajar`** — Trabaja cada hora (tu Líder suma hasta **+65% monedas extra**).\n"
                "• **`/pagar`** · **`/ranking`** · **`/tienda`** · **`/comprar`** · **`/inventario`** · **`/usar`** · **`/cajas`** · **`/abrir`**."
            ),
            inline=False,
        )
        e.add_field(
            name="🎰 Casino y Minijuegos",
            value=(
                "• **Con apuesta:** `/moneda` (x2) · `/dados` (x2/x3) · `/tragaperras` (hasta x25) · `/blackjack` · `/duelo` · `/ppt`.\n"
                "• **Gratis (dan monedas y XP):** `/trivia` · `/adivina` · `/ppt` (sin apuesta)."
            ),
            inline=False,
        )
        e.add_field(
            name="👤 Perfil, Personalización y 35 Logros",
            value=(
                "• **`/perfil [usuario]`** — Nivel, XP, racha, logros y cosméticos.\n"
                "• **`/logros [usuario]`** — Consulta los **35 logros** con premios de hasta `18.000` monedas.\n"
                "• **`/personalizar [bio|color|titulo|insignia]`** — Equipa tus colores, títulos e insignias."
            ),
            inline=False,
        )
        return e

    # --------------------------------------------------------- 1. VISTA GENERAL
    e = discord.Embed(
        title="🍊 Enciclopedia y Centro de Ayuda de Trobia Bot",
        description=(
            "¡Bienvenido/a! Aquí tienes **toda la información del bot guardada y organizada**.\n"
            "👇 **Usa el menú desplegable de abajo** para consultar las **30 criaturas**, las **30 pasivas**, "
            "las **17 combinaciones de equipo**, los **objetos/pergaminos** y todos los comandos:"
        ),
        color=config.COLOR_MAIN,
    )
    e.add_field(
        name="🛡️ Equipo de 3, Pasivas y Combinaciones",
        value="`/equipo ver` `/equipo asignar` `/equipo auto` `/equipo combinaciones`",
        inline=False,
    )
    e.add_field(
        name="🐾 Trobimons: Caza, Huevos y Colección (30 especies)",
        value="`/cazar` `/incubadora` `/trobidex` `/mascota ver` `/mascota lista` `/mascota equipar` `/mascota alimentar` `/mascota evolucionar` `/mascota apodo`",
        inline=False,
    )
    e.add_field(
        name="⭐ Trobimons Repetidos (Estrellas 1★-5★ y Portal)",
        value="`/mascota fusionar` `/mascota liberar` `/mascota repetidos` `/mascota prodigioso`",
        inline=False,
    )
    e.add_field(
        name="⚔️ Combate 3v3, Torre de Campeones, Objetos y Pergaminos",
        value="`/mascota entrenar` `/mascota torre` `/mascota combatir` `/mascota objeto` `/mascota habilidad`",
        inline=False,
    )
    e.add_field(
        name="💰 Economía, Tienda y Cajas",
        value="`/saldo` `/diario` `/trabajar` `/pagar` `/ranking` `/tienda` `/comprar` `/inventario` `/usar` `/cajas` `/abrir`",
        inline=False,
    )
    e.add_field(
        name="🎰 Casino, Minijuegos, Perfil y Guía",
        value="`/moneda` `/dados` `/tragaperras` `/blackjack` `/duelo` `/ppt` `/trivia` `/adivina` `/perfil` `/logros` `/personalizar` `/ayuda` `/guia`",
        inline=False,
    )
    e.set_footer(text="Selecciona cualquier sección en el desplegable de abajo para consultar todos los datos 👇")
    return e


def help_embed(section: str) -> discord.Embed:
    """Embed de ayuda con pie de navegación 'Sección N/M' (usado por los botones ◀ ▶)."""
    e = build_help_embed(section)
    keys = [k for k, _, _ in HELP_SECTIONS]
    idx = keys.index(section) if section in keys else 0
    label = HELP_SECTIONS[idx][1]
    e.set_footer(text=f"📚 Sección {idx + 1}/{len(keys)} · {label} · Usa ◀ ▶ o el desplegable")
    return e


def _current_section_index(message: Optional[discord.Message]) -> int:
    import re
    try:
        txt = message.embeds[0].footer.text or ""
        m = re.search(r"Sección (\d+)/", txt)
        if m:
            return max(0, int(m.group(1)) - 1)
    except Exception:
        pass
    return 0


class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=title.split(" ", 1)[1][:95],
                value=key,
                emoji=title.split(" ", 1)[0],
                description=desc[:100],
            )
            for key, title, desc in HELP_SECTIONS
        ]
        super().__init__(
            placeholder="📚 Elige una sección de la guía…",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="trobia_help_select",
            row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=help_embed(self.values[0]), view=self.view)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

    async def _go(self, interaction: discord.Interaction, idx: int):
        keys = [k for k, _, _ in HELP_SECTIONS]
        idx %= len(keys)
        await interaction.response.edit_message(embed=help_embed(keys[idx]), view=self)

    @discord.ui.button(label="Anterior", emoji="◀️", style=discord.ButtonStyle.secondary, custom_id="trobia_help_prev", row=1)
    async def prev_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, _current_section_index(interaction.message) - 1)

    @discord.ui.button(label="Inicio", emoji="🏠", style=discord.ButtonStyle.primary, custom_id="trobia_help_home", row=1)
    async def home_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, 0)

    @discord.ui.button(label="Siguiente", emoji="▶️", style=discord.ButtonStyle.secondary, custom_id="trobia_help_next", row=1)
    async def next_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, _current_section_index(interaction.message) + 1)


SECTION_CHOICES = [
    app_commands.Choice(name=title[:100], value=key)
    for key, title, _ in HELP_SECTIONS
]


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    admin = app_commands.Group(
        name="admin",
        description="Comandos de administración de la economía y guía",
        default_permissions=discord.Permissions(administrator=True),
        guild_only=True,
    )

    @admin.command(name="monedas", description="Da (o quita, con número negativo) monedas a alguien")
    @app_commands.describe(usuario="Persona", cantidad="Cantidad (negativa para quitar)")
    async def monedas(self, interaction: discord.Interaction, usuario: discord.Member, cantidad: int):
        if cantidad < 0:
            current = self.db.get_coins(usuario.id)
            take = min(current, -cantidad)
            self.db.remove_coins(usuario.id, take)
            msg = f"Quitadas {fmt(take)} a {usuario.mention}."
        else:
            self.db.add_coins(usuario.id, cantidad)
            msg = f"Dadas {fmt(cantidad)} a {usuario.mention}."
        await interaction.response.send_message(embed=ok_embed(msg), ephemeral=True)
        await check_achievements(self.bot, usuario, interaction.channel)

    @admin.command(name="objeto", description="Da un objeto, pergamino o caja a alguien")
    @app_commands.describe(usuario="Persona", objeto="Objeto", cantidad="Cantidad")
    async def objeto(self, interaction: discord.Interaction, usuario: discord.Member, objeto: str,
                     cantidad: app_commands.Range[int, 1, 100] = 1):
        if objeto not in ITEMS:
            await interaction.response.send_message(embed=error_embed("Ese objeto no existe."), ephemeral=True)
            return
        self.db.add_item(usuario.id, objeto, cantidad)
        await interaction.response.send_message(
            embed=ok_embed(f"Dado **{cantidad}x {item_label(objeto)}** a {usuario.mention}."), ephemeral=True
        )

    @objeto.autocomplete("objeto")
    async def objeto_ac(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=item_label(i)[:100], value=i)
            for i, it in ITEMS.items() if current.lower() in it["name"].lower()
        ][:25]

    @admin.command(name="evento", description="Lanza un drop: la primera persona en pulsar el botón gana el premio")
    @app_commands.describe(monedas="Monedas de premio")
    async def evento(self, interaction: discord.Interaction, monedas: app_commands.Range[int, 1, 1_000_000]):
        view = DropView(self, monedas)
        embed = discord.Embed(
            title="🎉 ¡DROP SORPRESA!",
            description=f"¡La primera persona que pulse el botón se lleva {fmt(monedas)}!",
            color=0xF1C40F,
        )
        await interaction.response.send_message(embed=embed, view=view)

    @admin.command(name="publicar_guia", description="Publica el panel interactivo permanente de la Guía en un canal 📚")
    @app_commands.describe(canal="Canal donde publicar la guía interactiva")
    async def publicar_guia(self, interaction: discord.Interaction, canal: Optional[discord.TextChannel] = None):
        target_ch = canal or interaction.channel
        await target_ch.send(embed=help_embed("general"), view=HelpView())
        await interaction.response.send_message(
            embed=ok_embed(f"Guía interactiva publicada en {target_ch.mention}."), ephemeral=True
        )

    # --------------------------------------------------------- /ayuda y /guia
    @app_commands.command(name="ayuda", description="Abre la Enciclopedia y Guía interactiva con toda la información del bot 📚")
    @app_commands.describe(seccion="Ir directamente a una sección (criaturas, pasivas, combinaciones, objetos...)")
    @app_commands.choices(seccion=SECTION_CHOICES)
    async def ayuda(self, interaction: discord.Interaction, seccion: Optional[app_commands.Choice[str]] = None):
        sec = seccion.value if seccion else "general"
        await interaction.response.send_message(embed=help_embed(sec), view=HelpView())

    @app_commands.command(name="guia", description="Consulta la Guía completa: las 30 criaturas, pasivas, combinaciones de equipo y objetos 📖")
    @app_commands.describe(seccion="Qué apartado de la guía quieres consultar")
    @app_commands.choices(seccion=SECTION_CHOICES)
    async def guia(self, interaction: discord.Interaction, seccion: Optional[app_commands.Choice[str]] = None):
        sec = seccion.value if seccion else "combinaciones"
        await interaction.response.send_message(embed=help_embed(sec), view=HelpView())


class DropView(discord.ui.View):
    def __init__(self, cog, amount: int):
        super().__init__(timeout=300)
        self.cog, self.amount = cog, amount
        self.claimed = False

    @discord.ui.button(label="¡Reclamar!", emoji="🎁", style=discord.ButtonStyle.success)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.claimed:
            await interaction.response.send_message("¡Demasiado tarde! Alguien ya lo ha reclamado.", ephemeral=True)
            return
        self.claimed = True
        button.disabled = True
        self.stop()
        self.cog.db.add_coins(interaction.user.id, self.amount)
        await interaction.response.edit_message(
            embed=discord.Embed(
                title="🎉 ¡Drop reclamado!",
                description=f"{interaction.user.mention} ha sido el más rápido y se lleva {fmt(self.amount)}",
                color=config.COLOR_OK,
            ),
            view=self,
        )
        await check_achievements(self.cog.bot, interaction.user, interaction.channel)


async def setup(bot):
    bot.add_view(HelpView())
    await bot.add_cog(Admin(bot))
