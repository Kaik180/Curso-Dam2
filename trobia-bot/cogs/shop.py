"""Tienda, inventario y consumibles."""
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from data.items import COSMETIC_TYPES, ITEMS, RARITIES, TYPE_NAMES
from utils import check_achievements, error_embed, fmt, ok_embed, user_color

CATEGORY_CHOICES = [app_commands.Choice(name=name, value=key) for key, name in TYPE_NAMES.items()]


def build_shop_embed(db, uid: int, selected_type: Optional[str] = None) -> discord.Embed:
    inv = db.get_inventory(uid)
    types = [selected_type] if selected_type and selected_type != "all" else list(TYPE_NAMES)
    balance = db.get_coins(uid)

    embed = discord.Embed(
        title="🛒 Tienda Central de Trobia",
        color=config.COLOR_MAIN,
    )
    embed.description = (
        f"### Saldo disponible: {fmt(balance)}\n"
        f"-# Selecciona una categoría en el menú desplegable o compra con `/comprar <objeto> [cantidad]`\n"
        f"-# Los objetos marcados con ✨ solo pueden conseguirse en cajas de botín."
    )
    for t in types:
        lines = []
        for item_id, it in ITEMS.items():
            if it["type"] != t or it["price"] is None:
                continue
            owned = " `[EN POSESIÓN]`" if (t in COSMETIC_TYPES and inv.get(item_id)) else ""
            rarity_emoji = RARITIES[it['rarity']]['emoji']
            lines.append(f"{it['emoji']} **{it['name']}** ─ {fmt(it['price'])} {rarity_emoji}{owned}")
        exclusives = [f"{it['emoji']} {it['name']}" for it in ITEMS.values() if it["type"] == t and it["price"] is None]
        if exclusives:
            lines.append("-# ✨ *Exclusivos en cajas:* " + ", ".join(exclusives))
        if lines:
            embed.add_field(name=f"📦 {TYPE_NAMES[t]}", value="\n".join(lines)[:1024], inline=False)
    embed.set_footer(text="⚪ Común · 🔵 Raro · 🟣 Épico · 🟡 Legendario | Trobia Bot")
    return embed


class ShopCategorySelect(discord.ui.Select):
    def __init__(self, current: str = "all"):
        options = [discord.SelectOption(label="Todas las Categorías", value="all", emoji="🛒", default=(current == "all"))]
        for key, name in TYPE_NAMES.items():
            options.append(discord.SelectOption(
                label=name[:100],
                value=key,
                default=(current == key)
            ))
        super().__init__(placeholder="Elige una sección de la tienda...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        embed = build_shop_embed(self.view.db, interaction.user.id, selected)
        for opt in self.options:
            opt.default = (opt.value == selected)
        await interaction.response.edit_message(embed=embed, view=self.view)


class ShopView(discord.ui.View):
    def __init__(self, db, initial_type: str = "all"):
        super().__init__(timeout=180)
        self.db = db
        self.add_item(ShopCategorySelect(initial_type))


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    # ---------------------------------------------------------------- tienda
    @app_commands.command(name="tienda", description="Mira los objetos que puedes comprar")
    @app_commands.describe(categoria="Filtra por categoría")
    @app_commands.choices(categoria=CATEGORY_CHOICES)
    async def tienda(self, interaction: discord.Interaction, categoria: Optional[app_commands.Choice[str]] = None):
        selected = categoria.value if categoria else "all"
        embed = build_shop_embed(self.db, interaction.user.id, selected)
        view = ShopView(self.db, selected)
        await interaction.response.send_message(embed=embed, view=view)

    # --------------------------------------------------------------- comprar
    @app_commands.command(name="comprar", description="Compra un objeto de la tienda")
    @app_commands.describe(objeto="Objeto a comprar", cantidad="Cantidad (solo cajas y consumibles)")
    async def comprar(self, interaction: discord.Interaction, objeto: str,
                      cantidad: app_commands.Range[int, 1, 50] = 1):
        uid = interaction.user.id
        it = ITEMS.get(objeto)
        if not it or it["price"] is None:
            await interaction.response.send_message(embed=error_embed("Ese objeto no está a la venta."), ephemeral=True)
            return
        if it["type"] in COSMETIC_TYPES:
            if self.db.item_qty(uid, objeto) > 0:
                await interaction.response.send_message(embed=error_embed("Ya tienes ese objeto."), ephemeral=True)
                return
            cantidad = 1
        total = it["price"] * cantidad
        if not self.db.remove_coins(uid, total):
            await interaction.response.send_message(
                embed=error_embed(f"Necesitas {fmt(total)} y tienes {fmt(self.db.get_coins(uid))}."), ephemeral=True
            )
            return
        self.db.add_item(uid, objeto, cantidad)
        self.db.incr_stat(uid, "items_bought", cantidad)

        hint = ""
        if it["type"] == "box":
            hint = "\nÁbrela con `/abrir`."
        elif it["type"] == "consumable":
            hint = "\nÚsalo con `/usar`."
        elif objeto in ("huevo_comun", "huevo_mistico"):
            hint = "\nEclosiónalo con `/incubadora`."
        elif objeto.startswith("orbe_"):
            hint = "\nÚsalo para capturar criaturas en `/cazar`."
        elif objeto in ("comida_trobimon", "caramelo_raro"):
            hint = "\nAlimenta a tu compañero con `/mascota alimentar`."
        elif objeto == "piedra_evolutiva":
            hint = "\nEvoluciona a tu compañero con `/mascota evolucionar`."
        elif it["type"] == "gear":
            hint = "\nEquípaselo a tu Trobimon compañero con `/mascota objeto`."
        elif it["type"] == "scroll":
            hint = "\nEnséñaselo a tu Trobimon compañero con `/mascota habilidad`."
        elif it["type"] in COSMETIC_TYPES:
            cmd = {"color": "color", "title": "titulo", "badge": "insignia"}[it["type"]]
            hint = f"\nEquípalo con `/personalizar {cmd}`."
        await interaction.response.send_message(
            embed=ok_embed(f"Has comprado **{cantidad}x {it['emoji']} {it['name']}** por {fmt(total)}.{hint}")
        )
        await check_achievements(self.bot, interaction.user, interaction.channel)

    @comprar.autocomplete("objeto")
    async def comprar_ac(self, interaction: discord.Interaction, current: str):
        out = []
        for item_id, it in ITEMS.items():
            if it["price"] is not None and current.lower() in it["name"].lower():
                out.append(app_commands.Choice(name=f"{it['emoji']} {it['name']} — {it['price']} monedas"[:100], value=item_id))
        return out[:25]

    # ------------------------------------------------------------ inventario
    @app_commands.command(name="inventario", description="Mira tu inventario (o el de otra persona)")
    @app_commands.describe(usuario="Persona de la que quieres ver el inventario")
    async def inventario(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        inv = self.db.get_inventory(target.id)
        embed = discord.Embed(title=f"🎒 Mochila de {target.display_name}", color=user_color(self.db, target.id))
        if not inv:
            embed.description = "### 📦 Mochila vacía\n-# Pásate por `/tienda`, reclama tu `/diario` o abre `/cajas`."
        else:
            cosmetics_count = sum(1 for i in inv if ITEMS.get(i, {}).get('type') in COSMETIC_TYPES)
            cosmetics_total = sum(1 for it in ITEMS.values() if it['type'] in COSMETIC_TYPES)
            embed.description = f"-# Coleccionables desbloqueados: **{cosmetics_count}** / {cosmetics_total}"
            for t, tname in TYPE_NAMES.items():
                lines = []
                for item_id, qty in inv.items():
                    it = ITEMS.get(item_id)
                    if it and it["type"] == t:
                        q = f" `x{qty}`" if qty > 1 else ""
                        lines.append(f"{RARITIES[it['rarity']]['emoji']} {it['emoji']} **{it['name']}**{q}")
                if lines:
                    embed.add_field(name=f"📦 {tname}", value="\n".join(lines)[:1024], inline=False)
        embed.set_footer(text="Usa /usar para consumibles o /comprar para conseguir más")
        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------------------ usar
    @app_commands.command(name="usar", description="Usa un consumible de tu inventario")
    @app_commands.describe(objeto="Consumible a usar")
    async def usar(self, interaction: discord.Interaction, objeto: str):
        uid = interaction.user.id
        it = ITEMS.get(objeto)
        if not it or it["type"] != "consumable":
            await interaction.response.send_message(embed=error_embed("Eso no es un consumible."), ephemeral=True)
            return
        if not self.db.remove_item(uid, objeto, 1):
            await interaction.response.send_message(embed=error_embed("No tienes ese objeto."), ephemeral=True)
            return

        now = int(time.time())
        if objeto in ("boost_xp", "boost_monedas"):
            key = "boost_xp_until" if objeto == "boost_xp" else "boost_coins_until"
            until = max(now, self.db.get_stat(uid, key)) + 3600
            self.db.set_stat(uid, key, until)
            msg = f"{it['emoji']} **{it['name']}** activado hasta <t:{until}:t> (<t:{until}:R>)."
        elif objeto == "reset_trabajo":
            self.db.set_stat(uid, "work_last", 0)
            msg = "☕ ¡Café Cargado! Ya puedes volver a usar `/trabajar`."
        else:
            msg = "Objeto usado."
        await interaction.response.send_message(embed=ok_embed(msg))

    @usar.autocomplete("objeto")
    async def usar_ac(self, interaction: discord.Interaction, current: str):
        inv = self.db.get_inventory(interaction.user.id)
        out = []
        for item_id, qty in inv.items():
            it = ITEMS.get(item_id)
            if it and it["type"] == "consumable" and current.lower() in it["name"].lower():
                out.append(app_commands.Choice(name=f"{it['emoji']} {it['name']} (x{qty})"[:100], value=item_id))
        return out[:25]


async def setup(bot):
    await bot.add_cog(Shop(bot))
