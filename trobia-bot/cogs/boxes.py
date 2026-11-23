"""Cajas de botín."""
import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands

import config
from data.items import ITEMS, LOOT, RARITIES, cosmetics_of, item_label
from utils import check_achievements, error_embed, fmt

RARITY_ORDER = ["comun", "raro", "epico", "legendario"]


class Boxes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    def roll(self, uid: int, box_id: str) -> tuple[str, str]:
        """Tira el botín de una caja, lo entrega y devuelve (texto, rareza)."""
        table = LOOT[box_id]
        entry = random.choices(table, weights=[e["w"] for e in table])[0]

        if entry["type"] == "coins":
            amount = random.randint(entry["min"], entry["max"])
            self.db.add_coins(uid, amount)
            text, rarity = fmt(amount), entry["rarity"]
        elif entry["type"] == "item":
            self.db.add_item(uid, entry["id"])
            text, rarity = f"**{item_label(entry['id'])}**", ITEMS[entry["id"]]["rarity"]
        else:  # cosmético aleatorio de la rareza indicada, priorizando los que no tiene
            rarity = entry["rarity"]
            pool = cosmetics_of(rarity)
            inv = self.db.get_inventory(uid)
            missing = [i for i in pool if not inv.get(i)]
            item_id = random.choice(missing or pool)
            if missing:
                self.db.add_item(uid, item_id)
                text = f"**{item_label(item_id)}** *(¡nuevo!)*"
            else:
                comp = RARITIES[rarity]["dup_value"]
                self.db.add_coins(uid, comp)
                text = f"{item_label(item_id)} *(repetido → {fmt(comp)})*"

        if rarity == "legendario":
            self.db.incr_stat(uid, "legendary_drops")
        return text, rarity

    # ----------------------------------------------------------------- cajas
    @app_commands.command(name="cajas", description="Información y probabilidades de las cajas")
    async def cajas(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎁 Cajas de Botín y Probabilidades",
            description=(
                "### Consigue tesoros y cosméticos exclusivos\n"
                "-# Cómpralas en `/tienda`, consíguelas en `/diario`, subiendo de nivel o en combates.\n"
                "-# Si obtienes un cosmético repetido, se te compensará automáticamente en monedas."
            ),
            color=config.COLOR_MAIN,
        )
        for box_id, table in LOOT.items():
            total = sum(e["w"] for e in table)
            by_rarity = {r: 0 for r in RARITY_ORDER}
            for e in table:
                r = e.get("rarity") or ITEMS[e["id"]]["rarity"]
                by_rarity[r] += e["w"]
            odds = " · ".join(f"{RARITIES[r]['emoji']} **{by_rarity[r] * 100 / total:.0f}%**" for r in RARITY_ORDER if by_rarity[r])
            it = ITEMS[box_id]
            embed.add_field(name=f"{it['emoji']} {it['name']} ─ {fmt(it['price'])}", value=f"> {odds}", inline=False)
        embed.set_footer(text="Abre tus cajas con /abrir <caja> [cantidad]")
        await interaction.response.send_message(embed=embed)

    # ----------------------------------------------------------------- abrir
    @app_commands.command(name="abrir", description="Abre cajas de tu inventario")
    @app_commands.describe(caja="Caja que quieres abrir", cantidad="Cuántas abrir a la vez (máx. 10)")
    async def abrir(self, interaction: discord.Interaction, caja: str, cantidad: app_commands.Range[int, 1, 10] = 1):
        uid = interaction.user.id
        if caja not in LOOT:
            await interaction.response.send_message(embed=error_embed("Esa caja no existe."), ephemeral=True)
            return
        if not self.db.remove_item(uid, caja, cantidad):
            await interaction.response.send_message(
                embed=error_embed(f"No tienes {cantidad}x {item_label(caja)}. Tienes {self.db.item_qty(uid, caja)}."),
                ephemeral=True,
            )
            return

        box = ITEMS[caja]
        anim = discord.Embed(
            title=f"{box['emoji']} Abriendo {cantidad}x {box['name']}...",
            description="### 🪄 ✨ 🎁 ✨ 🪄\n*Preparando recompensas...*",
            color=RARITIES[box["rarity"]]["color"],
        )
        await interaction.response.send_message(embed=anim)
        await asyncio.sleep(1.0)
        anim.description = "### 💥 💫 🎁 💫 💥\n*¡Abriéndose!...*"
        await interaction.edit_original_response(embed=anim)
        await asyncio.sleep(1.0)

        results = [self.roll(uid, caja) for _ in range(cantidad)]
        self.db.incr_stat(uid, "boxes_opened", cantidad)
        best = max(results, key=lambda r: RARITY_ORDER.index(r[1]))[1]

        lines = [f"> {RARITIES[r]['emoji']} {t}" for t, r in results]
        result = discord.Embed(
            title=f"{box['emoji']} ¡{box['name']} abierta{'s' if cantidad > 1 else ''}!",
            description=f"### Recompensas obtenidas:\n" + "\n".join(lines),
            color=RARITIES[best]["color"],
        )
        if best == "legendario":
            result.title = "🌟🌟 ¡¡BOTÍN LEGENDARIO CONSEGUIDO!! 🌟🌟"
        result.set_footer(text=f"Mejor rareza: {RARITIES[best]['name']} | Trobia Bot")
        await interaction.edit_original_response(embed=result)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    @abrir.autocomplete("caja")
    async def abrir_ac(self, interaction: discord.Interaction, current: str):
        inv = self.db.get_inventory(interaction.user.id)
        out = []
        for box_id in LOOT:
            if inv.get(box_id) and current.lower() in ITEMS[box_id]["name"].lower():
                out.append(app_commands.Choice(name=f"{item_label(box_id)} (x{inv[box_id]})", value=box_id))
        return out


async def setup(bot):
    await bot.add_cog(Boxes(bot))
