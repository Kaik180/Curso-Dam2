"""Perfil, personalización y logros."""
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from cards import render_profile_card
from data.achievements import ACHIEVEMENTS
from data.creatures import CREATURES
from data.items import ITEMS, RARITIES
from utils import boost_active, check_achievements, error_embed, fmt, ok_embed, progress_bar, user_color

NONE_VALUE = "__ninguno__"


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    # ---------------------------------------------------------------- perfil
    @app_commands.command(name="perfil", description="Muestra tu perfil (o el de otra persona)")
    @app_commands.describe(usuario="Persona de la que quieres ver el perfil")
    async def perfil(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        db = self.db
        user = db.get_user(target.id)
        stats = db.get_stats(target.id)
        n_ach = len(db.get_achievements(target.id))

        badge = ITEMS[user["badge"]]["value"] + " " if user["badge"] in ITEMS else ""
        title = ITEMS[user["title"]]["value"] if user["title"] in ITEMS else "Sin título"
        bio = user["bio"] or "*Sin biografía. Usa `/personalizar bio` para añadir una.*"
        need = db.xp_needed(user["level"])

        embed = discord.Embed(
            title=f"{badge}{target.display_name}",
            description=f"🏷️ *{title}*\n\n{bio}",
            color=user_color(db, target.id),
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(
            name=f"⭐ Nivel {user['level']}",
            value=f"{progress_bar(user['xp'], need)}\n`{user['xp']} / {need} XP`",
            inline=False,
        )
        embed.add_field(name="💰 Monedas", value=f"{fmt(user['coins'])}\nPuesto #{db.coin_rank(target.id)}", inline=True)
        embed.add_field(name="🏅 Logros", value=f"**{n_ach} / {len(ACHIEVEMENTS)}**", inline=True)
        embed.add_field(name="🔥 Racha diaria", value=f"**{stats.get('daily_streak', 0)}** días", inline=True)
        embed.add_field(
            name="🎲 Minijuegos",
            value=f"**{stats.get('games_won', 0)}** ganadas de {stats.get('games_played', 0)}",
            inline=True,
        )
        embed.add_field(name="📦 Cajas abiertas", value=f"**{stats.get('boxes_opened', 0)}**", inline=True)
        embed.add_field(name="💬 Mensajes", value=f"**{stats.get('messages', 0)}**", inline=True)

        pet = db.get_active_pet(target.id)
        if pet and pet["species_id"] in CREATURES:
            sp = CREATURES[pet["species_id"]]
            pet_val = f"{sp['emoji']} **{pet.get('nickname') or sp['name']}** (Nv. {pet['level']})"
        else:
            pet_val = "*Ninguno (`/cazar`)*"
        embed.add_field(name="🐾 Compañero", value=pet_val, inline=True)
        embed.add_field(name="📖 Trobidex", value=f"**{stats.get('trobidex', 0)} / {len(CREATURES)}**", inline=True)

        boosts = []
        if boost_active(db, target.id, "xp"):
            boosts.append("⚗️ XP x2")
        if boost_active(db, target.id, "coins"):
            boosts.append("🧿 Monedas x2")
        if boosts:
            embed.add_field(name="✨ Potenciadores activos", value=" · ".join(boosts), inline=False)

        col_int = user_color(db, target.id)
        card_file, card_url = render_profile_card(
            display_name=target.display_name,
            title_str=title,
            bio_str=user["bio"] or "",
            level=user["level"],
            xp=user["xp"],
            xp_need=need,
            coins=user["coins"],
            rank=db.coin_rank(target.id),
            streak=stats.get("daily_streak", 0),
            n_ach=n_ach,
            total_ach=len(ACHIEVEMENTS),
            dex_count=stats.get("trobidex", 0),
            total_dex=len(CREATURES),
            tower_floor=stats.get("tower_floor", 0),
            color_int=col_int,
            active_pet=pet if (pet and pet["species_id"] in CREATURES) else None,
        )
        embed.set_image(url=card_url)
        embed.set_footer(text="trobia · /personalizar para cambiar tu estilo")
        await interaction.response.send_message(embed=embed, file=card_file)

    # ---------------------------------------------------------------- logros
    @app_commands.command(name="logros", description="Mira los logros desbloqueados y pendientes")
    @app_commands.describe(usuario="Persona de la que quieres ver los logros")
    async def logros(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        unlocked = self.db.get_achievements(target.id)
        stats = self.db.get_stats(target.id)
        done, pending = [], []
        for a in ACHIEVEMENTS:
            if a["id"] in unlocked:
                done.append(f"{a['emoji']} **{a['name']}** — {a['desc']}")
            else:
                cur = min(stats.get(a["stat"], 0), a["goal"])
                pending.append(f"🔒 **{a['name']}** — {a['desc']} `{cur}/{a['goal']}` · +{a['reward']} {config.CURRENCY}")

        desc = ""
        if done:
            desc += "### ✅ Desbloqueados\n" + "\n".join(done) + "\n"
        desc += "### 🔒 Pendientes\n" + ("\n".join(pending) if pending else "¡Los tienes todos! 👑")
        embed = discord.Embed(
            title=f"🏅 Logros de {target.display_name} ({len(unlocked)}/{len(ACHIEVEMENTS)})",
            description=desc[:4096],
            color=user_color(self.db, target.id),
        )
        await interaction.response.send_message(embed=embed)

    # --------------------------------------------------------- personalizar
    personalizar = app_commands.Group(name="personalizar", description="Personaliza tu perfil")

    def _owned_choices(self, uid: int, item_type: str, current: str) -> list[app_commands.Choice[str]]:
        inv = self.db.get_inventory(uid)
        choices = [app_commands.Choice(name="❌ Quitar / ninguno", value=NONE_VALUE)]
        for item_id in inv:
            it = ITEMS.get(item_id)
            if it and it["type"] == item_type and current.lower() in it["name"].lower():
                label = f"{it['emoji']} {it['name']} ({RARITIES[it['rarity']]['name']})"
                choices.append(app_commands.Choice(name=label[:100], value=item_id))
        return choices[:25]

    async def _equip(self, interaction: discord.Interaction, item_type: str, field: str, item_id: str, label: str):
        uid = interaction.user.id
        if item_id == NONE_VALUE:
            self.db.set_field(uid, field, None)
            await interaction.response.send_message(embed=ok_embed(f"Has quitado tu {label}."), ephemeral=True)
            return
        it = ITEMS.get(item_id)
        if not it or it["type"] != item_type or self.db.item_qty(uid, item_id) < 1:
            await interaction.response.send_message(
                embed=error_embed(f"No tienes ese {label}. Consíguelo en `/tienda` o abriendo cajas."), ephemeral=True
            )
            return
        self.db.set_field(uid, field, item_id)
        self.db.set_stat(uid, "customized", 1)
        await interaction.response.send_message(
            embed=ok_embed(f"Te has equipado {it['emoji']} **{it['name']}** como {label}."), ephemeral=True
        )
        await check_achievements(self.bot, interaction.user, interaction.channel)

    @personalizar.command(name="bio", description="Cambia la biografía de tu perfil")
    @app_commands.describe(texto="Tu nueva biografía (máx. 200 caracteres). Escribe 'borrar' para quitarla.")
    async def bio(self, interaction: discord.Interaction, texto: app_commands.Range[str, 1, 200]):
        uid = interaction.user.id
        if texto.strip().lower() == "borrar":
            self.db.set_field(uid, "bio", None)
            await interaction.response.send_message(embed=ok_embed("Biografía borrada."), ephemeral=True)
            return
        self.db.set_field(uid, "bio", texto.strip())
        self.db.set_stat(uid, "customized", 1)
        await interaction.response.send_message(embed=ok_embed("¡Biografía actualizada! Mírala con `/perfil`."), ephemeral=True)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    @personalizar.command(name="color", description="Equipa un color de perfil que tengas")
    @app_commands.describe(color="Color de tu inventario")
    async def color(self, interaction: discord.Interaction, color: str):
        await self._equip(interaction, "color", "color", color, "color de perfil")

    @color.autocomplete("color")
    async def color_ac(self, interaction: discord.Interaction, current: str):
        return self._owned_choices(interaction.user.id, "color", current)

    @personalizar.command(name="titulo", description="Equipa un título que tengas")
    @app_commands.describe(titulo="Título de tu inventario")
    async def titulo(self, interaction: discord.Interaction, titulo: str):
        await self._equip(interaction, "title", "title", titulo, "título")

    @titulo.autocomplete("titulo")
    async def titulo_ac(self, interaction: discord.Interaction, current: str):
        return self._owned_choices(interaction.user.id, "title", current)

    @personalizar.command(name="insignia", description="Equipa una insignia que tengas (sale junto a tu nombre)")
    @app_commands.describe(insignia="Insignia de tu inventario")
    async def insignia(self, interaction: discord.Interaction, insignia: str):
        await self._equip(interaction, "badge", "badge", insignia, "insignia")

    @insignia.autocomplete("insignia")
    async def insignia_ac(self, interaction: discord.Interaction, current: str):
        return self._owned_choices(interaction.user.id, "badge", current)


async def setup(bot):
    await bot.add_cog(Profile(bot))
