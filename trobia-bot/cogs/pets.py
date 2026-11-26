"""Sistema completo de Trobimons: caza, huevos, equipos de 3, sinergias, 96 habilidades, duplicados, Torre de Campeones y combates."""
import asyncio
import os
import random
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from cards import (
    render_battle_banner,
    render_encounter_banner,
    render_pet_card,
    render_team_banner,
)
from data.creatures import (
    CREATURES,
    DUAL_ELEMENT_COMBOS,
    ELEMENTS,
    MAX_STARS,
    MONO_ELEMENT_COMBOS,
    ORB_MULTIPLIERS,
    PET_GEAR,
    RARITY_BONUS_PCT,
    RELEASE_REWARDS,
    SCROLL_SKILLS,
    STAR_STAT_BONUS,
    STAR_WORK_BONUS,
    calc_team_synergies,
    image_path,
    pet_power,
    pet_skills,
    pet_stats,
    pet_xp_needed,
    same_family,
    stars_badge,
)
from data.items import ITEMS, RARITIES, item_label
from utils import check_achievements, error_embed, fmt, ok_embed, progress_bar, safe_send, user_color

HUNT_COOLDOWN = 45
TRAIN_COOLDOWN = 45
TOWER_COOLDOWN = 45
UNEQUIP_VALUE = "__quitar__"


def creature_file_and_url(species_id: str) -> tuple[Optional[discord.File], Optional[str]]:
    path = image_path(species_id)
    if os.path.isfile(path):
        fname = f"{species_id}.jpg"
        return discord.File(path, filename=fname), f"attachment://{fname}"
    return None, None


def pet_display_name(pet: dict) -> str:
    sp = CREATURES[pet["species_id"]]
    stars = stars_badge(pet.get("stars", 0))
    if pet.get("nickname"):
        return f"{sp['emoji']} **{pet['nickname']}** (*{sp['name']}*){stars}"
    return f"{sp['emoji']} **{sp['name']}**{stars}"


def format_skills_block(species_id: str, extra_skill_id: Optional[str] = None) -> str:
    sp = CREATURES[species_id]
    lines = []
    pas = sp.get("passive")
    if pas:
        lines.append(f"🌟 **Pasiva — {pas['emoji']} {pas['name']}:** *{pas['desc']}*\n")
    for sk in sp["skills"]:
        cd_txt = "0t" if sk["cd"] == 0 else f"CD:{sk['cd']}t"
        role = sk.get("role", "⚔️ Asalto")
        lines.append(f"{sk['emoji']} **{sk['name']}** `[{role} · x{sk['dmg_mult']} · {cd_txt}]` — *{sk['desc']}*")
    if extra_skill_id and extra_skill_id in SCROLL_SKILLS:
        sk = SCROLL_SKILLS[extra_skill_id]
        role = sk.get("role", "📜 Secreta")
        lines.append(f"📜 {sk['emoji']} **{sk['name']}** `[{role} · x{sk['dmg_mult']} · CD:{sk['cd']}t]` — *{sk['desc']}*")
    return "\n".join(lines)


def calc_release_reward(pet: dict) -> tuple[int, str, int]:
    """Devuelve (monedas, item_id, cantidad_item) por liberar un Trobimon."""
    sp = CREATURES[pet["species_id"]]
    info = RELEASE_REWARDS[sp["rarity"]]
    stars = int(pet.get("stars") or 0)
    coins = info["base_coins"] + pet["level"] * info["per_lvl"] + stars * 200
    qty = info["qty"] + (1 if stars >= 2 else 0)
    return coins, info["item"], qty


def find_family_main(pets: list[dict], new_pet_uid: int, species_id: str) -> Optional[dict]:
    """Busca el mejor Trobimon de la misma familia evolutiva distinto a `new_pet_uid`."""
    candidates = [
        p for p in pets
        if p["pet_uid"] != new_pet_uid and same_family(p["species_id"], species_id)
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda p: (
            p.get("is_active", 0),
            1 if int(p.get("team_slot") or 0) in (1, 2, 3) else 0,
            CREATURES[p["species_id"]]["stage"],
            p.get("stars", 0),
            p["level"],
            -p["pet_uid"],
        ),
        reverse=True,
    )
    return candidates[0]


async def add_pet_xp(bot, member: discord.abc.User, pet: dict, amount: int, channel=None) -> tuple[dict, Optional[str]]:
    """Suma XP a una mascota, sube niveles y evoluciona automáticamente si toca."""
    db = bot.db
    uid = member.id
    fresh = db.get_pet(uid, pet["pet_uid"]) or pet
    xp = fresh["xp"] + int(amount)
    level = fresh["level"]
    species_id = fresh["species_id"]
    old_species = None

    while xp >= pet_xp_needed(level):
        xp -= pet_xp_needed(level)
        level += 1
        sp = CREATURES[species_id]
        if sp["evolves_to"] and sp["evolve_level"] and level >= sp["evolve_level"]:
            old_species = old_species or species_id
            species_id = sp["evolves_to"]
            db.register_trobidex(uid, species_id)
            db.incr_stat(uid, "pets_evolved")

    db.update_pet(uid, fresh["pet_uid"], species_id, level, xp)
    updated = db.get_pet(uid, fresh["pet_uid"])

    if old_species and channel is not None:
        old_sp = CREATURES[old_species]
        new_sp = CREATURES[species_id]
        file, url = creature_file_and_url(species_id)
        embed = discord.Embed(
            title="✨ ¡¡TU TROBIMON HA EVOLUCIONADO!! ✨",
            description=(
                f"{member.mention}, tu {old_sp['emoji']} **{old_sp['name']}** ha alcanzado el **Nivel {level}** "
                f"y se ha transformado en {new_sp['emoji']} **{new_sp['name']}**{stars_badge(updated.get('stars', 0))} "
                f"({RARITIES[new_sp['rarity']]['emoji']} {RARITIES[new_sp['rarity']]['name']})!\n\n"
                f"*{new_sp['desc']}*\n\n"
                f"**Nuevas habilidades desbloqueadas:**\n{format_skills_block(species_id, updated.get('extra_skill'))}"
            ),
            color=RARITIES[new_sp["rarity"]]["color"],
        )
        if url:
            embed.set_image(url=url)
        await safe_send(channel, embed=embed, file=file)

    await check_achievements(bot, member, channel)
    return updated, old_species


async def execute_fusion(bot, member: discord.abc.User, base_pet: dict, dup_pet: dict, channel=None) -> tuple[dict, int, int, Optional[str]]:
    """Fusiona `dup_pet` dentro de `base_pet`. Devuelve (updated_pet, old_stars, new_stars, returned_item)."""
    db = bot.db
    uid = member.id
    old_stars = int(base_pet.get("stars") or 0)
    dup_stars = int(dup_pet.get("stars") or 0)
    stars_gained = 1 + dup_stars
    new_stars = min(MAX_STARS, old_stars + stars_gained)

    returned_item = dup_pet.get("held_item")
    if returned_item:
        db.add_item(uid, returned_item, 1)
    if dup_pet.get("extra_skill"):
        db.add_item(uid, dup_pet["extra_skill"], 1)

    if dup_pet.get("is_active") and not base_pet.get("is_active"):
        db.set_active_pet(uid, base_pet["pet_uid"])

    db.delete_pet(uid, dup_pet["pet_uid"])
    db.set_pet_stars(uid, base_pet["pet_uid"], new_stars)
    db.incr_stat(uid, "pets_fused")
    db.max_stat(uid, "pet_max_stars", new_stars)

    xp_bonus = 120 * dup_pet["level"] + dup_pet["xp"] + (180 if old_stars >= MAX_STARS else 0)
    base_refreshed = db.get_pet(uid, base_pet["pet_uid"])
    updated, _ = await add_pet_xp(bot, member, base_refreshed, xp_bonus, channel)
    return updated, old_stars, new_stars, returned_item


# ========================================== BOTONES RÁPIDOS PARA DUPLICADOS
class DuplicateActionView(discord.ui.View):
    """Aparece cuando capturas o incubas un Trobimon cuya familia evolutiva ya tienes."""
    def __init__(self, cog, user: discord.abc.User, new_pet_uid: int, main_pet_uid: int):
        super().__init__(timeout=90)
        self.cog = cog
        self.user = user
        self.new_pet_uid = new_pet_uid
        self.main_pet_uid = main_pet_uid
        self.used = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Solo el dueño de este Trobimon puede usar estos botones.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    @discord.ui.button(label="Fusionar con mi principal (+1★ y +XP)", emoji="⭐", style=discord.ButtonStyle.success)
    async def fuse_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.used:
            return
        db = self.cog.db
        uid = self.user.id
        dup_pet = db.get_pet(uid, self.new_pet_uid)
        main_pet = db.get_pet(uid, self.main_pet_uid)
        if not dup_pet or not main_pet or dup_pet["pet_uid"] == main_pet["pet_uid"]:
            await interaction.response.send_message(embed=error_embed("Ese Trobimon ya no está disponible para fusionar."), ephemeral=True)
            return

        self.used = True
        for child in self.children:
            child.disabled = True
        self.stop()

        updated, old_s, new_s, _ = await execute_fusion(self.cog.bot, self.user, main_pet, dup_pet, interaction.channel)
        hp, atk = pet_stats(updated["species_id"], updated["level"], updated.get("held_item"), new_s)
        embed = interaction.message.embeds[0]
        embed.add_field(
            name="⭐ ¡Fusión Estelar Completada!",
            value=(
                f"Se ha fusionado con tu {pet_display_name(updated)} (`#{updated['pet_uid']}`)!\n"
                f"**Estrellas:** `{old_s}★` ➔ **`{new_s}★`** (+{new_s * 10}% HP/ATQ)\n"
                f"**Nivel actual:** Nv. {updated['level']} (❤️ {hp} HP · ⚔️ {atk} ATQ)"
            ),
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Liberar repetido (+Monedas y Comida)", emoji="🕊️", style=discord.ButtonStyle.secondary)
    async def release_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.used:
            return
        db = self.cog.db
        uid = self.user.id
        dup_pet = db.get_pet(uid, self.new_pet_uid)
        if not dup_pet or len(db.get_pets(uid)) <= 1:
            await interaction.response.send_message(embed=error_embed("No puedes liberar a tu único Trobimon."), ephemeral=True)
            return

        self.used = True
        for child in self.children:
            child.disabled = True
        self.stop()

        coins, item_id, qty = calc_release_reward(dup_pet)
        if dup_pet.get("held_item"):
            db.add_item(uid, dup_pet["held_item"], 1)
        if dup_pet.get("extra_skill"):
            db.add_item(uid, dup_pet["extra_skill"], 1)
        db.delete_pet(uid, dup_pet["pet_uid"])
        db.add_coins(uid, coins)
        db.add_item(uid, item_id, qty)

        embed = interaction.message.embeds[0]
        embed.add_field(
            name="🕊️ Trobimon Liberado",
            value=f"Has liberado a `#{dup_pet['pet_uid']}` y te ha dejado **{fmt(coins)}** y **{qty}x {item_label(item_id)}**.",
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=self)


# =========================================================== VISTA DE CAZA
class HuntView(discord.ui.View):
    def __init__(self, cog, user: discord.abc.User, species_id: str, wild_level: int):
        super().__init__(timeout=60)
        self.cog = cog
        self.user = user
        self.species_id = species_id
        self.wild_level = wild_level
        self.throws_left = 2
        self.done = False
        self.message: Optional[discord.Message] = None
        self._refresh_buttons()

    def _refresh_buttons(self):
        self.clear_items()
        inv = self.cog.db.get_inventory(self.user.id)
        sp = CREATURES[self.species_id]

        for orb_id, style in [
            ("orbe_basico", discord.ButtonStyle.secondary),
            ("orbe_super", discord.ButtonStyle.primary),
            ("orbe_ultra", discord.ButtonStyle.success),
            ("orbe_maestro", discord.ButtonStyle.danger),
        ]:
            qty = inv.get(orb_id, 0)
            it = ITEMS[orb_id]
            info = ORB_MULTIPLIERS[orb_id]
            chance = 100 if info["guaranteed"] else min(95, int(sp["catch_rate"] * info["mult"] * 100))
            btn = discord.ui.Button(
                label=f"{it['name']} (x{qty}) · {chance}%",
                emoji=it["emoji"],
                style=style,
                disabled=(qty <= 0 or self.done),
            )
            btn.callback = self._make_throw_cb(orb_id)
            self.add_item(btn)

        quick_btn = discord.ui.Button(
            label=f"Comprar + Lanzar Orbe Básico (150 {config.CURRENCY})",
            emoji="🛒",
            style=discord.ButtonStyle.secondary,
            disabled=self.done,
            row=1,
        )
        quick_btn.callback = self._quick_buy_throw
        self.add_item(quick_btn)

        flee_btn = discord.ui.Button(
            label="Huir",
            emoji="🏃",
            style=discord.ButtonStyle.secondary,
            disabled=self.done,
            row=1,
        )
        flee_btn.callback = self._flee
        self.add_item(flee_btn)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Este Trobimon salvaje no es de tu encuentro. Usa `/cazar`.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    def _make_throw_cb(self, orb_id: str):
        async def callback(interaction: discord.Interaction):
            if self.done:
                return
            if not self.cog.db.remove_item(self.user.id, orb_id, 1):
                await interaction.response.send_message(embed=error_embed("No te quedan orbes de ese tipo."), ephemeral=True)
                return
            await self._resolve_throw(interaction, orb_id)
        return callback

    async def _quick_buy_throw(self, interaction: discord.Interaction):
        if self.done:
            return
        price = ITEMS["orbe_basico"]["price"]
        if not self.cog.db.remove_coins(self.user.id, price):
            await interaction.response.send_message(
                embed=error_embed(f"Necesitas {fmt(price)} para comprar un Orbe Básico."), ephemeral=True
            )
            return
        await self._resolve_throw(interaction, "orbe_basico", bought=True)

    async def _resolve_throw(self, interaction: discord.Interaction, orb_id: str, bought: bool = False):
        db = self.cog.db
        sp = CREATURES[self.species_id]
        orb_it = ITEMS[orb_id]
        orb_info = ORB_MULTIPLIERS[orb_id]
        chance = 1.0 if orb_info["guaranteed"] else min(0.95, sp["catch_rate"] * orb_info["mult"])
        caught = random.random() <= chance
        self.throws_left -= 1

        embed = interaction.message.embeds[0]
        paid_note = f" *(comprado por {fmt(orb_it['price'])})*" if bought else ""

        if caught:
            self.done = True
            self._refresh_buttons()
            self.stop()
            pet, is_new = db.add_pet(self.user.id, self.species_id, self.wild_level)
            db.incr_stat(self.user.id, "pets_caught")
            if sp["rarity"] == "legendario":
                db.incr_stat(self.user.id, "legendary_drops")

            all_pets = db.get_pets(self.user.id)
            main_pet = find_family_main(all_pets, pet["pet_uid"], self.species_id)
            new_txt = "\n📖 **¡Nueva especie registrada en tu `/trobidex`!**" if is_new else ""
            dup_txt = ""
            next_view: discord.ui.View = self
            if main_pet:
                dup_txt = (
                    f"\n\n✨ **¡Ya tienes un {CREATURES[main_pet['species_id']]['name']} (`#{main_pet['pet_uid']}`)!** "
                    "Puedes **Fusionarlo (⭐ +10% stats y +XP)** o **Liberarlo por monedas y comida** con los botones de abajo:"
                )
                next_view = DuplicateActionView(self.cog, self.user, pet["pet_uid"], main_pet["pet_uid"])

            embed.title = f"🎉 ¡Has capturado a {sp['emoji']} {sp['name']} (Nv. {self.wild_level})!"
            embed.color = config.COLOR_OK
            embed.description = (
                f"Lanzaste {orb_it['emoji']} **{orb_it['name']}**{paid_note} y ¡clic! Captura completada.\n"
                f"🆔 ID de mascota: **`#{pet['pet_uid']}`**{new_txt}{dup_txt}"
            )
            await interaction.response.edit_message(embed=embed, view=next_view)
            await check_achievements(self.cog.bot, self.user, interaction.channel)
            return

        if self.throws_left <= 0:
            self.done = True
            self._refresh_buttons()
            self.stop()
            embed.title = f"💨 ¡{sp['name']} se ha escapado!"
            embed.color = config.COLOR_ERROR
            embed.description = (
                f"Lanzaste {orb_it['emoji']} **{orb_it['name']}**{paid_note}, pero se abrió en el último segundo "
                f"y **{sp['name']}** huyó entre la maleza."
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return

        self._refresh_buttons()
        embed.description = (
            f"¡Casi! {orb_it['emoji']} **{orb_it['name']}**{paid_note} tembló dos veces pero **{sp['name']}** salió.\n"
            f"⚠️ ¡Te queda **1 último intento** antes de que huya!"
        )
        await interaction.response.edit_message(embed=embed, view=self)

    async def _flee(self, interaction: discord.Interaction):
        self.done = True
        self._refresh_buttons()
        self.stop()
        embed = interaction.message.embeds[0]
        embed.title = "🏃 Has dejado marchar al Trobimon"
        embed.color = config.COLOR_INFO
        await interaction.response.edit_message(embed=embed, view=self)


# ========================================== MOTOR DE COMBATE DE EQUIPOS 3v3
class FighterUnit:
    """Estado individual de un Trobimon dentro de un equipo de combate."""
    def __init__(self, pet: dict, synergy: dict):
        self.pet = pet
        self.species = CREATURES[pet["species_id"]]
        self.passive = self.species.get("passive", {})
        self.element = ELEMENTS[self.species["element"]]
        self.held_id = pet.get("held_item")
        self.stars = int(pet.get("stars") or 0)
        self.gear = PET_GEAR.get(self.held_id or "", {})
        self.skills = pet_skills(pet)
        base_hp, base_atk = pet_stats(pet["species_id"], pet["level"], self.held_id, self.stars)
        self.max_hp = int(base_hp * (1.0 + synergy.get("hp_mult", 0.0)))
        self.base_atk = int(base_atk * (1.0 + synergy.get("atk_mult", 0.0)))
        self.hp = self.max_hp
        self.atk_mult = 1.0
        self.shield = max(self.passive.get("start_shield", 0.0), synergy.get("start_shield", 0.0))
        self.eva_buff = 0.0
        self.thorns_pct = 0.0
        self.thorns_turns = 0
        self.burn_turns = 0
        self.poison_turns = 0
        self.expose_turns = 0
        self.stunned = False
        self.revived = False
        self.cds = [0] * len(self.skills)

    @property
    def alive(self) -> bool:
        return self.hp > 0

    @property
    def short_name(self) -> str:
        return self.pet.get("nickname") or self.species["name"]

    @property
    def name_tag(self) -> str:
        return f"{self.species['emoji']} **{self.short_name}**{stars_badge(self.stars)} (Nv.{self.pet['level']})"

    def status_icons(self) -> str:
        tags = []
        if self.passive:
            tags.append(f"{self.passive['emoji']} {self.passive['name']}")
        if self.held_id and self.held_id in ITEMS:
            it = ITEMS[self.held_id]
            tags.append(f"{it['emoji']} {it['name']}")
        if self.shield > 0:
            tags.append(f"🛡️ Escudo (-{int(self.shield*100)}%)")
        if self.eva_buff > 0:
            tags.append(f"💨 Esquiva (+{int(self.eva_buff*100)}%)")
        total_thorns = max(
            self.thorns_pct if self.thorns_turns > 0 else 0.0,
            self.gear.get("thorns_passive", 0.0),
            self.passive.get("self_thorns", 0.0),
        )
        if total_thorns > 0:
            tags.append(f"🌵 Espinas ({int(total_thorns*100)}%)")
        if self.passive.get("berserk_atk") and self.hp <= self.max_hp * 0.50:
            tags.append(f"💢 Berserker (+{int(self.passive['berserk_atk']*100)}% ATQ)")
        if self.atk_mult > 1.01:
            tags.append(f"⬆️ +{int(round((self.atk_mult-1)*100))}% ATQ")
        elif self.atk_mult < 0.99:
            tags.append(f"🔻 -{int(round((1-self.atk_mult)*100))}% ATQ")
        if self.burn_turns > 0:
            tags.append(f"🔥 Quemado ({self.burn_turns}t)")
        if self.poison_turns > 0:
            tags.append(f"☠️ Veneno ({self.poison_turns}t)")
        if self.expose_turns > 0:
            tags.append(f"🎯 Vulnerable ({self.expose_turns}t)")
        if self.stunned:
            tags.append("💫 Aturdido")
        return " · ".join(tags) if tags else "Sin estados activos"


class TeamSide:
    """Representa el equipo completo (de 1 a 3 Trobimons) de un entrenador o jefe."""
    def __init__(self, owner_name: str, owner_user: Optional[discord.abc.User], pets: list[dict], is_ai: bool = False):
        self.owner_name = owner_name
        self.owner_user = owner_user
        self.pets = pets
        self.is_ai = is_ai
        self.synergy = calc_team_synergies(pets)
        self.units = [FighterUnit(p, self.synergy) for p in pets]
        self.active_idx = 0

    @property
    def active(self) -> FighterUnit:
        return self.units[self.active_idx]

    @property
    def has_alive(self) -> bool:
        return any(u.alive for u in self.units)

    def alive_count(self) -> int:
        return sum(1 for u in self.units if u.alive)

    def auto_advance_if_fainted(self) -> Optional[FighterUnit]:
        if self.active.alive:
            return None
        for idx, u in enumerate(self.units):
            if u.alive:
                self.active_idx = idx
                return u
        return None

    def roster_summary(self) -> str:
        parts = []
        for idx, u in enumerate(self.units):
            if not u.alive:
                parts.append(f"💀 ~~{u.species['name']}~~")
            elif idx == self.active_idx:
                parts.append(f"⚔️ **{u.species['emoji']} {u.short_name}**")
            else:
                pct = int(round(u.hp * 100 / max(1, u.max_hp)))
                parts.append(f"🟢 {u.species['emoji']} {u.short_name} (`{pct}%`)")
        return " ｜ ".join(parts)


class TacticalBattleView(discord.ui.View):
    def __init__(self, cog, side1: TeamSide, side2: TeamSide, bet: int = 0, mode: str = "train", tower_floor: int = 1):
        super().__init__(timeout=150)
        self.cog = cog
        self.sides = [side1, side2]
        self.turn = 0
        self.bet = bet
        self.mode = mode  # "train", "pvp", "tower"
        self.tower_floor = tower_floor
        self.log: list[str] = ["⚔️ ¡Comienza el combate de equipos! Usa tus habilidades o cambia de Trobimon."]
        for idx, s in enumerate(self.sides):
            opp = self.sides[1 - idx]
            if s.synergy["lines"]:
                self.log.append(f"🔗 **{s.owner_name}** activa: {s.synergy['lines'][0]}")
            debuff = min(0.35, s.synergy.get("enemy_atk_debuff", 0.0))
            if debuff > 0:
                for u in opp.units:
                    u.atk_mult = max(0.55, u.atk_mult - debuff)
                self.log.append(f"🔻 Las pasivas de **{s.owner_name}** reducen **-{int(debuff*100)}% ATQ** al equipo de **{opp.owner_name}**.")
            exp_start = s.synergy.get("enemy_expose_start", 0)
            if exp_start > 0:
                opp.active.expose_turns = max(opp.active.expose_turns, exp_start)
                self.log.append(f"🎯 **{opp.active.short_name}** empieza **Vulnerable ({exp_start}t)**.")
        self.over = False
        self._build_buttons()

    def current_side(self) -> TeamSide:
        return self.sides[self.turn]

    def opponent_side(self) -> TeamSide:
        return self.sides[1 - self.turn]

    def _build_buttons(self):
        self.clear_items()
        if self.over:
            return
        side = self.current_side()
        if side.is_ai:
            return
        cur = side.active
        # Jerarquía de botones: básica (azul) → utilidad (gris) → definitiva (verde) → secreta (azul)
        styles = [
            discord.ButtonStyle.primary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.primary,
        ]
        rows = [0, 0, 0, 1, 1]
        for idx, sk in enumerate(cur.skills):
            cd = cur.cds[idx]
            tag = "⭐ " if idx == 3 else ("📜 " if idx == 4 else "")
            label = f"{tag}{sk['name']}" + (f"  ⏳{cd}t" if cd > 0 else "")
            btn = discord.ui.Button(
                label=label[:80],
                emoji=sk["emoji"],
                style=styles[idx % len(styles)] if cd == 0 else discord.ButtonStyle.secondary,
                disabled=(cd > 0),
                row=rows[idx % len(rows)],
            )
            btn.callback = self._make_skill_cb(idx)
            self.add_item(btn)

        # Botones para relevar a otro compañero vivo del equipo
        for u_idx, u in enumerate(side.units):
            if u_idx == side.active_idx or not u.alive:
                continue
            pct = int(round(u.hp * 100 / max(1, u.max_hp)))
            sw_btn = discord.ui.Button(
                label=f"Relevo · {u.short_name} ({pct}%)"[:80],
                emoji="🔄",
                style=discord.ButtonStyle.secondary,
                row=2,
            )
            sw_btn.callback = self._make_switch_cb(u_idx)
            self.add_item(sw_btn)

        forfeit = discord.ui.Button(label="Rendirse", emoji="🏳️", style=discord.ButtonStyle.danger, row=2)
        forfeit.callback = self._forfeit_cb
        self.add_item(forfeit)

    def files(self) -> list[discord.File]:
        f, _ = render_battle_banner(self.sides[0], self.sides[1])
        return [f]

    def payload(self, title: Optional[str] = None, color: int = config.COLOR_MAIN) -> dict:
        return {"embed": self.render_embed(title, color), "view": self, "attachments": self.files()}

    def render_embed(self, title: Optional[str] = None, color: int = config.COLOR_MAIN) -> discord.Embed:
        s1, s2 = self.sides
        cur_side = self.current_side()
        cur = cur_side.active
        mode_tag = {"tower": f"🏯 TORRE · PISO {self.tower_floor}", "pvp": "⚔️ DUELO PvP", "train": "🥊 ENTRENAMIENTO"}.get(self.mode, "⚔️ COMBATE")
        t_title = title or f"{mode_tag} · Turno de {cur_side.owner_name}"
        e = discord.Embed(title=t_title, color=color)

        # Registro de combate (jerarquía moderna con última acción en bloque destacado)
        recent = self.log[-6:]
        if recent:
            head = recent[-1]
            history = "\n".join(f"-# ▫️ {l}" for l in recent[:-1])
            e.description = (f"### 💥 Última Acción:\n> **{head}**\n\n" + (f"-# 📜 Historial reciente:\n{history}\n" if history else ""))[:1500]

        # Matchups elementales
        adv_map = {
            (True, False): "⚡ ¡Súper Efectivo! (+25% Daño)",
            (False, True): "🛡️ Desventaja elemental (-25%)",
            (False, False): "⚔️ Daño Estándar (100%)",
            (True, True): "⚡ Choque Elemental Directo",
        }
        adv_s1 = (s2.active.species["element"] in s1.active.element.get("beats", []), s1.active.species["element"] in s2.active.element.get("beats", []))
        adv_s2 = (s1.active.species["element"] in s2.active.element.get("beats", []), s2.active.species["element"] in s1.active.element.get("beats", []))

        for s, adv_state in [(s1, adv_s1), (s2, adv_s2)]:
            u = s.active
            el = ELEMENTS[u.species["element"]]
            adv_txt = adv_map.get(adv_state, "")
            e.add_field(
                name=f"{el['emoji']} {u.short_name} — {s.owner_name}",
                value=f"{progress_bar(u.hp, u.max_hp, 10)} **{u.hp}/{u.max_hp} HP**\n`{adv_txt}`\n{u.status_icons()}\n{s.roster_summary()}",
                inline=True,
            )
        if not self.over and not cur_side.is_ai:
            sk_help = "\n".join(
                f"{sk['emoji']} **{sk['name']}** · `{sk.get('role', '⚔️')}`\n-# {sk['desc']}" for sk in cur.skills
            )
            e.add_field(name="✨ Arsenal de Habilidades Disponibles", value=sk_help[:1024], inline=False)
        e.set_image(url="attachment://battle_vs.jpg")
        e.set_footer(text="Usa los botones de abajo para atacar · 🔄 Relevo otorga escudo protector (-25% daño)")
        return e

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        side = self.current_side()
        if side.owner_user and interaction.user.id != side.owner_user.id:
            await interaction.response.send_message(
                f"Ahora es el turno de **{side.owner_name}**.", ephemeral=True
            )
            return False
        return self.cog.db.claim_interaction(interaction.id)

    def _execute_skill(self, atk_side: TeamSide, dfn_side: TeamSide, skill_idx: int):
        atk = atk_side.active
        dfn = dfn_side.active

        # 1. Reducir cooldowns y contadores al inicio del turno
        for i in range(len(atk.cds)):
            if atk.cds[i] > 0:
                atk.cds[i] -= 1
        if atk.thorns_turns > 0:
            atk.thorns_turns -= 1
            if atk.thorns_turns == 0:
                atk.thorns_pct = 0.0

        # 2. Regeneración por objeto equipado, pasiva propia o sinergia de equipo
        regen_pct = (
            atk.gear.get("regen_pct", 0.0)
            + atk.passive.get("self_regen_pct", 0.0)
            + atk_side.synergy.get("team_regen_pct", 0.0)
        )
        poison_heal_pen = 0.60 if atk.poison_turns > 0 else 1.0
        heal_boost_total = 1.0 + atk.gear.get("heal_boost", 0.0) + atk_side.synergy.get("heal_boost", 0.0)
        if regen_pct > 0 and atk.hp < atk.max_hp:
            reg = max(1, int(atk.max_hp * regen_pct * heal_boost_total * poison_heal_pen))
            atk.hp = min(atk.max_hp, atk.hp + reg)
            self.log.append(f"✨ **{atk.short_name}** regenera **+{reg} HP** por sus pasivas/equipo.")

        # 2b. Aura de daño pasivo al rival (`enemy_burn_aura`)
        aura_dmg_pct = atk_side.synergy.get("enemy_burn_aura", 0.0)
        if aura_dmg_pct > 0 and dfn.hp > 0:
            admg = max(1, int(dfn.max_hp * aura_dmg_pct))
            dfn.hp = max(0, dfn.hp - admg)
            self.log.append(f"☀️ El aura elemental de **{atk_side.owner_name}** abrasa **-{admg} HP** a {dfn.short_name}.")
            if dfn.hp <= 0:
                return

        # 3. Daño por Quemadura y Veneno
        if atk.burn_turns > 0:
            bdmg = max(1, int(atk.max_hp * 0.08))
            atk.hp = max(0, atk.hp - bdmg)
            atk.burn_turns -= 1
            self.log.append(f"🔥 {atk.species['emoji']} **{atk.short_name}** sufre **-{bdmg} HP** por quemadura.")
            if atk.hp <= 0:
                return

        if atk.poison_turns > 0:
            pdmg = max(1, int(atk.max_hp * 0.06))
            atk.hp = max(0, atk.hp - pdmg)
            atk.poison_turns -= 1
            self.log.append(f"☠️ {atk.species['emoji']} **{atk.short_name}** sufre **-{pdmg} HP** por veneno.")
            if atk.hp <= 0:
                return

        # 4. Comprobar Aturdimiento
        if atk.stunned:
            atk.stunned = False
            self.log.append(f"💫 {atk.species['emoji']} **{atk.short_name}** está aturdido y pierde su acción.")
            return

        sk = atk.skills[skill_idx]
        if sk["cd"] > 0:
            atk.cds[skill_idx] = sk["cd"]

        # 5. Purificar (cleanse)
        if sk.get("cleanse"):
            atk.burn_turns = 0
            atk.poison_turns = 0
            atk.expose_turns = 0
            if atk.atk_mult < 1.0:
                atk.atk_mult = 1.0
            poison_heal_pen = 1.0
            self.log.append(f"✨ **{atk.short_name}** purifica todos sus estados negativos.")

        # 6. Robo de buffs/escudos antes del impacto (`steal_buff`)
        if sk.get("steal_buff"):
            stolen_any = False
            if dfn.shield > 0:
                atk.shield = max(atk.shield, dfn.shield)
                dfn.shield = 0.0
                stolen_any = True
            if dfn.atk_mult > 1.0:
                bonus = dfn.atk_mult - 1.0
                atk.atk_mult = min(2.2, atk.atk_mult + bonus)
                dfn.atk_mult = 1.0
                stolen_any = True
            if stolen_any:
                self.log.append(f"🎭 ¡**{atk.short_name}** le roba las mejoras y escudos a {dfn.short_name}!")

        # 7. Comprobar Esquiva del defensor (objeto + pasiva propia + sinergia + eva_buff)
        dodge_chance = (
            dfn.gear.get("dodge_chance", 0.0)
            + dfn.passive.get("self_dodge", 0.0)
            + dfn_side.synergy.get("dodge_bonus", 0.0)
            + dfn.eva_buff
        )
        dfn.eva_buff = 0.0
        if random.random() < min(0.68, dodge_chance):
            self.log.append(f"💨 ¡**{dfn.short_name}** esquivó ágilmente **{sk['name']}**!")
            return

        # 8. Calcular Golpes
        hits_cfg = sk.get("hits")
        num_hits = random.randint(hits_cfg[0], hits_cfg[1]) if hits_cfg else 1
        elem_adv = dfn.species["element"] in atk.element["beats"]
        eb = atk.gear.get("elem_boost")
        crit_chance = (
            0.10
            + sk.get("crit_bonus", 0.0)
            + atk.gear.get("crit_bonus", 0.0)
            + atk.passive.get("self_crit", 0.0)
            + atk_side.synergy.get("crit_bonus", 0.0)
        )

        exec_mult = 1.0
        exec_cfg = sk.get("exec_bonus")
        if exec_cfg and (dfn.hp / max(1, dfn.max_hp)) <= exec_cfg[0]:
            exec_mult += exec_cfg[1]

        # Pasiva Berserker (<50% HP)
        berserk_mult = 1.0
        if atk.passive.get("berserk_atk") and atk.hp <= atk.max_hp * 0.50:
            berserk_mult += atk.passive["berserk_atk"]

        shield_used = False
        shield_factor = 1.0
        if dfn.shield > 0:
            if sk.get("pierce"):
                dfn.shield = 0.0
                self.log.append(f"💥 ¡**{sk['name']}** perfora el escudo de {dfn.short_name}!")
            else:
                shield_factor = 1.0 - dfn.shield
                dfn.shield = 0.0
                shield_used = True

        expose_factor = 1.30 if dfn.expose_turns > 0 else 1.0
        if dfn.expose_turns > 0:
            dfn.expose_turns -= 1

        dmg_red = min(
            0.55,
            dfn.gear.get("dmg_reduction", 0.0)
            + dfn.passive.get("self_dmg_red", 0.0)
            + dfn_side.synergy.get("dmg_reduction", 0.0),
        )

        total_dmg = 0
        crits = 0
        for _ in range(num_hits):
            raw = atk.base_atk * atk.atk_mult * berserk_mult * sk.get("dmg_mult", 1.0) * exec_mult * random.uniform(0.92, 1.08)
            if elem_adv:
                raw *= 1.25
            if eb and eb[0] == atk.species["element"]:
                raw *= 1.0 + eb[1]
            if random.random() < crit_chance:
                raw *= 1.50 + atk.gear.get("crit_dmg_bonus", 0.0)
                crits += 1
            raw *= shield_factor * expose_factor * (1.0 - dmg_red)
            total_dmg += max(1, int(raw))

        dfn.hp = max(0, dfn.hp - total_dmg)

        extras = []
        if num_hits > 1:
            extras.append(f"{num_hits} golpes")
        if elem_adv:
            extras.append("¡Súper eficaz!")
        if crits > 0:
            extras.append("¡CRÍTICO!" if crits == 1 else f"¡{crits}x CRÍTICOS!")
        if exec_mult > 1.0:
            extras.append("¡Ejecución!")
        if berserk_mult > 1.0:
            extras.append("¡Berserker!")
        if shield_used:
            extras.append("Escudo amortiguó")
        extra_str = f" *({' · '.join(extras)})*" if extras else ""
        self.log.append(
            f"{sk['emoji']} **{atk.short_name}** usa **{sk['name']}** → **-{total_dmg} HP**{extra_str}"
        )

        # Retroceso (recoil_pct)
        if sk.get("recoil_pct") and atk.hp > 1:
            rec = max(1, int(atk.hp * sk["recoil_pct"]))
            atk.hp = max(1, atk.hp - rec)
            self.log.append(f"⚡ El retroceso de **{sk['name']}** resta **-{rec} HP** a {atk.short_name}.")

        # Daño reflejado por Espinas (habilidad + objeto + pasiva + combo)
        active_thorns = max(
            dfn.thorns_pct if dfn.thorns_turns > 0 else 0.0,
            dfn.gear.get("thorns_passive", 0.0),
            dfn.passive.get("self_thorns", 0.0),
            dfn_side.synergy.get("thorns_bonus", 0.0),
        )
        if active_thorns > 0 and total_dmg > 0:
            reflected = max(1, int(total_dmg * active_thorns))
            atk.hp = max(0, atk.hp - reflected)
            self.log.append(f"🌵 Las espinas de **{dfn.short_name}** devuelven **-{reflected} HP** a {atk.short_name}.")

        # Contraataque de esporas (`counter_poison` de Arborión)
        c_poison = dfn.passive.get("counter_poison", 0.0)
        if c_poison > 0 and atk.hp > 0 and random.random() < c_poison:
            atk.poison_turns = max(atk.poison_turns, 2)
            self.log.append(f"🌳 ¡La pasiva **{dfn.passive['name']}** de {dfn.short_name} envenena a {atk.short_name} (2t)!")

        # 9. Efectos secundarios (individuales y de EQUIPO)
        heal_mult = heal_boost_total * poison_heal_pen
        lifesteal_total = (
            sk.get("lifesteal", 0.0)
            + atk.passive.get("self_lifesteal", 0.0)
            + atk_side.synergy.get("lifesteal_bonus", 0.0)
        )
        if lifesteal_total > 0 and total_dmg > 0 and atk.hp > 0:
            stolen = max(1, int(total_dmg * lifesteal_total * heal_mult))
            atk.hp = min(atk.max_hp, atk.hp + stolen)
            self.log.append(f"🩸 Drena **+{stolen} HP**.")

        if sk.get("heal_pct") and atk.hp > 0:
            healed = max(1, int(atk.max_hp * sk["heal_pct"] * heal_mult))
            atk.hp = min(atk.max_hp, atk.hp + healed)
            self.log.append(f"💚 Recupera **+{healed} HP**.")

        if sk.get("team_heal_pct") and atk.hp > 0:
            pct = sk["team_heal_pct"] * heal_mult
            for u in atk_side.units:
                if u.alive:
                    u.hp = min(u.max_hp, u.hp + max(1, int(u.max_hp * pct)))
            self.log.append(f"💚 ¡Cura un **+{int(pct*100)}% HP** a todo el equipo de **{atk_side.owner_name}**!")

        if sk.get("shield_pct"):
            atk.shield = sk["shield_pct"]
            self.log.append(f"🛡️ Activa Escudo (-{int(atk.shield*100)}% daño).")

        if sk.get("eva_buff"):
            atk.eva_buff = sk["eva_buff"]
            self.log.append(f"💨 Gana **+{int(atk.eva_buff*100)}% Esquiva** para el próximo ataque.")

        if sk.get("haste_cd"):
            dec = sk["haste_cd"]
            for i in range(len(atk.cds)):
                if i != skill_idx and atk.cds[i] > 0:
                    atk.cds[i] = max(0, atk.cds[i] - dec)
            self.log.append(f"⚡ Reduce **-{dec} turno** las recargas de sus habilidades.")

        if sk.get("thorns"):
            t_pct, t_turns = sk["thorns"]
            atk.thorns_pct = t_pct
            atk.thorns_turns = t_turns
            self.log.append(f"🌵 Se rodea de espinas ({int(t_pct*100)}% reflejo por {t_turns}t).")

        if sk.get("atk_buff"):
            atk.atk_mult = min(2.2, atk.atk_mult + sk["atk_buff"])
            self.log.append(f"⬆️ Ataque aumentado (+{int(sk['atk_buff']*100)}% ATQ).")

        if sk.get("team_atk_buff"):
            b_val = sk["team_atk_buff"]
            for u in atk_side.units:
                if u.alive:
                    u.atk_mult = min(2.2, u.atk_mult + b_val)
            self.log.append(f"🎺 ¡Sube **+{int(b_val*100)}% ATQ** a todo el equipo de **{atk_side.owner_name}**!")

        if dfn.hp > 0:
            if sk.get("weaken"):
                dfn.atk_mult = max(0.50, dfn.atk_mult - sk["weaken"])
                self.log.append(f"🔻 El ATQ de **{dfn.short_name}** se reduce un -{int(sk['weaken']*100)}%.")

            if sk.get("expose"):
                dfn.expose_turns = max(dfn.expose_turns, sk["expose"])
                self.log.append(f"🎯 ¡**{dfn.short_name}** queda Vulnerable (+30% daño recibido, {sk['expose']}t)!")

            if sk.get("freeze_cd"):
                inc = sk["freeze_cd"]
                for i in range(1, len(dfn.cds)):
                    dfn.cds[i] = min(4, dfn.cds[i] + inc)
                self.log.append(f"❄️ ¡Las recargas de **{dfn.short_name}** se retrasan +{inc} turno!")

            if sk.get("burn"):
                b_chance, b_turns = sk["burn"]
                b_chance += (
                    atk.gear.get("burn_bonus", 0.0)
                    + atk.passive.get("burn_bonus", 0.0)
                    + atk_side.synergy.get("burn_bonus", 0.0)
                )
                if random.random() < b_chance:
                    dfn.burn_turns = max(dfn.burn_turns, b_turns)
                    self.log.append(f"🔥 ¡**{dfn.short_name}** ha quedado quemado ({b_turns}t)!")

            if sk.get("poison"):
                p_chance, p_turns = sk["poison"]
                if random.random() < p_chance:
                    dfn.poison_turns = max(dfn.poison_turns, p_turns)
                    self.log.append(f"☠️ ¡**{dfn.short_name}** ha sido envenenado ({p_turns}t)!")

            stun_c = sk.get("stun_chance", 0.0)
            if stun_c > 0:
                stun_c += (
                    atk.gear.get("stun_bonus", 0.0)
                    + atk.passive.get("self_stun_bonus", 0.0)
                    + atk_side.synergy.get("stun_bonus", 0.0)
                )
                if random.random() < stun_c:
                    dfn.stunned = True
                    self.log.append(f"💫 ¡**{dfn.short_name}** ha quedado aturdido!")

    def _check_knockouts(self) -> bool:
        """Comprueba pasivas de renacimiento (Solarix) y avanza relevos si algún Trobimon cayó."""
        for s in self.sides:
            u = s.active
            if not u.alive:
                rev_pct = u.passive.get("revive_pct", 0.0)
                if rev_pct > 0 and not u.revived:
                    u.revived = True
                    u.hp = max(1, int(u.max_hp * rev_pct))
                    self.log.append(
                        f"🐦‍🔥 ¡**{u.short_name}** activa **{u.passive['name']}** y renace de sus cenizas con **{u.hp} HP**!"
                    )
                    continue
                fainted_name = u.short_name
                next_u = s.auto_advance_if_fainted()
                if next_u:
                    self.log.append(f"💀 **{fainted_name}** cayó debilitado. ¡⚡ **{next_u.short_name}** entra al relevo por **{s.owner_name}**!")
                else:
                    return True
        return False

    def _choose_ai_skill(self, ai_side: TeamSide, player_side: TeamSide) -> int:
        ai = ai_side.active
        avail = [i for i, cd in enumerate(ai.cds) if cd == 0]
        if not avail:
            return 0
        if ai.hp < ai.max_hp * 0.60:
            defensive = [
                i for i in avail
                if ai.skills[i].get("heal_pct") or ai.skills[i].get("team_heal_pct") or ai.skills[i].get("shield_pct")
            ]
            if defensive:
                return random.choice(defensive)
        best = max(avail, key=lambda i: (ai.skills[i].get("cd", 0), ai.skills[i].get("dmg_mult", 1.0)))
        return best

    def _make_skill_cb(self, idx: int):
        async def callback(interaction: discord.Interaction):
            if self.over:
                return
            atk_side, dfn_side = self.current_side(), self.opponent_side()
            self._execute_skill(atk_side, dfn_side, idx)

            if self._check_knockouts():
                await self._finish_battle(interaction)
                return

            await self._advance_turn(interaction)
        return callback

    def _make_switch_cb(self, new_idx: int):
        async def callback(interaction: discord.Interaction):
            if self.over:
                return
            side = self.current_side()
            if new_idx < 0 or new_idx >= len(side.units) or not side.units[new_idx].alive:
                return
            old_u = side.active
            side.active_idx = new_idx
            new_u = side.active
            new_u.shield = max(new_u.shield, 0.25)
            self.log.append(
                f"🔄 **{side.owner_name}** retira a **{old_u.short_name}** y saca a {new_u.species['emoji']} **{new_u.short_name}** (gana 🛡️ -25% daño)."
            )
            await self._advance_turn(interaction)
        return callback

    async def _advance_turn(self, interaction: discord.Interaction):
        self.turn = 1 - self.turn
        if self.current_side().is_ai:
            self._build_buttons()
            await interaction.response.edit_message(**self.payload())
            await asyncio.sleep(1.1)
            ai_side, pl_side = self.current_side(), self.opponent_side()
            ai_skill = self._choose_ai_skill(ai_side, pl_side)
            self._execute_skill(ai_side, pl_side, ai_skill)
            if self._check_knockouts():
                await self._finish_battle(interaction, edited=True)
                return
            self.turn = 1 - self.turn

        self._build_buttons()
        if interaction.response.is_done():
            await interaction.edit_original_response(**self.payload())
        else:
            await interaction.response.edit_message(**self.payload())

    async def _forfeit_cb(self, interaction: discord.Interaction):
        if self.over:
            return
        for u in self.current_side().units:
            u.hp = 0
        self.log.append(f"🏳️ **{self.current_side().owner_name}** se ha rendido.")
        await self._finish_battle(interaction)

    async def _finish_battle(self, interaction: discord.Interaction, edited: bool = False):
        self.over = True
        self._build_buttons()
        self.stop()
        db = self.cog.db

        s1, s2 = self.sides
        winner, loser = (s1, s2) if s1.has_alive else (s2, s1)

        if self.mode == "tower":
            uid = s1.owner_user.id
            if winner is s1:
                db.max_stat(uid, "tower_floor", self.tower_floor)
                db.incr_stat(uid, "pet_battles_won")
                coin_reward = 220 + self.tower_floor * 95
                xp_each = 45 + self.tower_floor * 8
                db.add_coins(uid, coin_reward)
                bonus_item_txt = ""
                if self.tower_floor % 5 == 0:
                    db.add_item(uid, "caja_epica", 1)
                    db.add_item(uid, "caramelo_raro", 1)
                    bonus_item_txt = "\n🎁 **¡Premio de Jefe de Piso!** Recibes **1x 💜 Caja Épica** y **1x 🍬 Caramelo Místico**."
                elif self.tower_floor % 3 == 0:
                    db.add_item(uid, "comida_trobimon", 2)
                    bonus_item_txt = "\n🍖 Recibes además **2x Chuletón Ibérico**."
                self.log.append(
                    f"\n🏆 **¡PISO {self.tower_floor} SUPERADO!** Ganas {fmt(coin_reward)} y **+{xp_each} XP** para todo tu equipo.{bonus_item_txt}"
                )
                embed = self.render_embed(f"🏯🏆 ¡Piso {self.tower_floor} de la Torre conquistado!", config.COLOR_OK)
                if edited:
                    await interaction.edit_original_response(embed=embed, view=self, attachments=self.files())
                else:
                    await interaction.response.edit_message(embed=embed, view=self, attachments=self.files())
                for p in s1.pets:
                    await add_pet_xp(self.cog.bot, s1.owner_user, p, xp_each, interaction.channel)
            else:
                self.log.append(f"\n💀 Has caído en el **Piso {self.tower_floor}**. Tu equipo gana **+20 XP** y puedes reintentarlo.")
                embed = self.render_embed(f"🏯💀 Derrota en el Piso {self.tower_floor}", config.COLOR_ERROR)
                if edited:
                    await interaction.edit_original_response(embed=embed, view=self, attachments=self.files())
                else:
                    await interaction.response.edit_message(embed=embed, view=self, attachments=self.files())
                for p in s1.pets:
                    await add_pet_xp(self.cog.bot, s1.owner_user, p, 20, interaction.channel)
            return

        if s2.is_ai:
            avg_lvl = max(1, sum(p["level"] for p in s2.pets) // len(s2.pets))
            if winner is s1:
                coin_reward = random.randint(120, 200) + avg_lvl * 18 * len(s2.pets)
                db.add_coins(s1.owner_user.id, coin_reward)
                db.incr_stat(s1.owner_user.id, "pet_battles_won")
                self.log.append(f"\n🏆 ¡Victoria de equipo! Ganas {fmt(coin_reward)} y cada Trobimon de tu equipo recibe **+50 XP**.")
                embed = self.render_embed(f"🏆 ¡El equipo de {s1.owner_name} ganó el entrenamiento!", config.COLOR_OK)
                if edited:
                    await interaction.edit_original_response(embed=embed, view=self, attachments=self.files())
                else:
                    await interaction.response.edit_message(embed=embed, view=self, attachments=self.files())
                for p in s1.pets:
                    await add_pet_xp(self.cog.bot, s1.owner_user, p, 50, interaction.channel)
            else:
                self.log.append("\n💀 Tu equipo cayó debilitado, pero cada compañero gana **+20 XP** por el esfuerzo.")
                embed = self.render_embed("💀 Derrota en el entrenamiento", config.COLOR_ERROR)
                if edited:
                    await interaction.edit_original_response(embed=embed, view=self, attachments=self.files())
                else:
                    await interaction.response.edit_message(embed=embed, view=self, attachments=self.files())
                for p in s1.pets:
                    await add_pet_xp(self.cog.bot, s1.owner_user, p, 20, interaction.channel)
            return

        # Modo PvP por equipos
        prize_txt = ""
        if self.bet:
            db.add_coins(winner.owner_user.id, self.bet * 2)
            prize_txt = f" y se lleva el bote de {fmt(self.bet * 2)}"
        db.incr_stat(winner.owner_user.id, "pet_battles_won")
        self.log.append(f"\n🏆 ¡**{winner.owner_name}** gana la batalla de equipos{prize_txt}! (+55 XP equipo ganador / +25 XP rival)")
        embed = self.render_embed(f"🏆 ¡Victoria de {winner.owner_name}!", config.COLOR_OK)
        if edited:
            await interaction.edit_original_response(embed=embed, view=self, attachments=self.files())
        else:
            await interaction.response.edit_message(embed=embed, view=self, attachments=self.files())

        for p in winner.pets:
            await add_pet_xp(self.cog.bot, winner.owner_user, p, 55, interaction.channel)
        for p in loser.pets:
            await add_pet_xp(self.cog.bot, loser.owner_user, p, 25, interaction.channel)


class PetChallengeView(discord.ui.View):
    def __init__(self, cog, p1, p2, team1: list[dict], team2: list[dict], bet: int):
        super().__init__(timeout=60)
        self.cog, self.p1, self.p2 = cog, p1, p2
        self.team1, self.team2 = team1, team2
        self.bet = bet
        self.done = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.p2.id:
            await interaction.response.send_message("Solo el entrenador retado puede aceptar.", ephemeral=True)
            return False
        return self.cog.db.claim_interaction(interaction.id)

    @discord.ui.button(label="¡Aceptar batalla de equipos!", emoji="⚔️", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.cog.db
        self.done = True
        self.stop()
        if self.bet:
            if not db.remove_coins(self.p1.id, self.bet):
                await interaction.response.edit_message(embed=error_embed(f"{self.p1.mention} ya no tiene monedas."), view=None)
                return
            if not db.remove_coins(self.p2.id, self.bet):
                db.add_coins(self.p1.id, self.bet)
                await interaction.response.edit_message(embed=error_embed(f"{self.p2.mention} no tiene monedas."), view=None)
                return

        s1 = TeamSide(self.p1.display_name, self.p1, self.team1)
        s2 = TeamSide(self.p2.display_name, self.p2, self.team2)
        battle = TacticalBattleView(self.cog, s1, s2, self.bet, mode="pvp")
        await interaction.response.edit_message(content=None, **battle.payload())

    @discord.ui.button(label="Rechazar", emoji="🏳️", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.done = True
        self.stop()
        await interaction.response.edit_message(
            content=None,
            embed=discord.Embed(description=f"🏳️ {self.p2.mention} rechazó el combate de equipos.", color=config.COLOR_ERROR),
            view=None,
        )


# ===================================================================== COG
class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self._hunt_cd: dict[int, float] = {}
        self._train_cd: dict[int, float] = {}
        self._tower_cd: dict[int, float] = {}
        self._msg_pet_cd: dict[int, float] = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        uid = message.author.id
        now = time.time()
        if now - self._msg_pet_cd.get(uid, 0) < 60:
            return
        pet = self.db.get_active_pet(uid)
        if not pet:
            return
        self._msg_pet_cd[uid] = now
        await add_pet_xp(self.bot, message.author, pet, random.randint(10, 18), message.channel)

    # ----------------------------------------------------------------- cazar
    @app_commands.command(name="cazar", description="Explora y encuentra uno de los 22 Trobimons salvajes para capturarlo 🐾")
    async def cazar(self, interaction: discord.Interaction):
        uid = interaction.user.id
        now = time.time()
        rem = int(HUNT_COOLDOWN - (now - self._hunt_cd.get(uid, 0)))
        if rem > 0:
            await interaction.response.send_message(
                embed=error_embed(f"Aún estás rastreando huellas. Espera **{rem}s** para volver a `/cazar`."),
                ephemeral=True,
            )
            return
        self._hunt_cd[uid] = now

        pool = list(CREATURES.values())
        sp = random.choices(pool, weights=[c["wild_weight"] for c in pool])[0]
        wild_level = random.randint(1, 3) if sp["stage"] == 1 else (random.randint(5, 8) if sp["stage"] == 2 else random.randint(12, 15))
        el = ELEMENTS[sp["element"]]
        rar = RARITIES[sp["rarity"]]
        hp, atk = pet_stats(sp["id"], wild_level)

        file, url = render_encounter_banner(sp, wild_level, hp, atk, sp["catch_rate"])
        embed = discord.Embed(
            title=f"🌿 ¡{sp['name']} Salvaje Detectado! (Nv. {wild_level})",
            description=(
                f"### {el['emoji']} **{sp['name']}** — {rar['name']}\n"
                f"> *{sp['desc']}*\n\n"
                f"📊 **Estadísticas:** ❤️ `{hp} HP` · ⚔️ `{atk} ATQ` · 🎯 Prob. Base: `{int(sp['catch_rate'] * 100)}%`\n"
                f"🐾 **Pasiva:** `{sp.get('passive', {}).get('name', 'Ninguna')}`\n\n"
                f"-# Tienes **2 lanzamientos**. Elige un Orbe abajo para intentar capturarlo:"
            ),
            color=rar["color"],
        )
        embed.set_image(url=url)
        embed.set_footer(text=f"Rastreo de {interaction.user.display_name} · Consigue más orbes en /tienda")

        view = HuntView(self, interaction.user, sp["id"], wild_level)
        await interaction.response.send_message(embed=embed, file=file, view=view)
        view.message = await interaction.original_response()

    # ------------------------------------------------------------ incubadora
    @app_commands.command(name="incubadora", description="Abre un Huevo Salvaje o Huevo Místico para eclosionar un Trobimon 🥚")
    @app_commands.describe(huevo="Tipo de huevo de tu inventario")
    @app_commands.choices(huevo=[
        app_commands.Choice(name="🥚 Huevo Salvaje (Comunes y Raros)", value="huevo_comun"),
        app_commands.Choice(name="🔮 Huevo Místico (Raros, Épicos y Legendarios)", value="huevo_mistico"),
    ])
    async def incubadora(self, interaction: discord.Interaction, huevo: app_commands.Choice[str]):
        uid = interaction.user.id
        egg_id = huevo.value
        if not self.db.remove_item(uid, egg_id, 1):
            await interaction.response.send_message(
                embed=error_embed(f"No tienes ningún **{item_label(egg_id)}**. Cómpralo en `/tienda`."),
                ephemeral=True,
            )
            return

        if egg_id == "huevo_comun":
            table = [
                (c["id"], 18 if c["rarity"] == "comun" else 6, 1)
                for c in CREATURES.values() if c["stage"] == 1
            ]
        else:
            w_map = {"raro": 12, "epico": 6, "legendario": 2}
            lvl_map = {"raro": 5, "epico": 8, "legendario": 12}
            table = [
                (c["id"], w_map[c["rarity"]], lvl_map[c["rarity"]])
                for c in CREATURES.values() if c["rarity"] in w_map
            ]

        species_id, _, start_lvl = random.choices(table, weights=[w for _, w, _ in table])[0]
        sp = CREATURES[species_id]
        rar = RARITIES[sp["rarity"]]
        el = ELEMENTS[sp["element"]]

        pet, is_new = self.db.add_pet(uid, species_id, start_lvl)
        self.db.incr_stat(uid, "pets_caught")
        if sp["rarity"] == "legendario":
            self.db.incr_stat(uid, "legendary_drops")

        all_pets = self.db.get_pets(uid)
        main_pet = find_family_main(all_pets, pet["pet_uid"], species_id)
        dup_txt = ""
        view = None
        if main_pet:
            dup_txt = (
                f"\n\n✨ **¡Ya tienes un {CREATURES[main_pet['species_id']]['name']} (`#{main_pet['pet_uid']}`)!** "
                "Usa los botones de abajo si quieres **Fusionarlo (+1★ y +XP)** o **Liberarlo por monedas y comida**:"
            )
            view = DuplicateActionView(self, interaction.user, pet["pet_uid"], main_pet["pet_uid"])

        card_file, card_url = render_pet_card(pet)
        new_txt = "\n📖 **¡Nueva especie descubierta en el `/trobidex`!**" if is_new else ""
        embed = discord.Embed(
            title=f"🐣 ¡El {ITEMS[egg_id]['name']} ha eclosionado!",
            description=(
                f"### ¡Ha nacido un {sp['emoji']} {sp['name']} de Nivel {start_lvl}!\n"
                f"**Rareza:** {rar['emoji']} {rar['name']} · **Elemento:** {el['emoji']} {el['name']}\n"
                f"🆔 ID de mascota: **`#{pet['pet_uid']}`**{new_txt}\n\n"
                f"> *{sp['desc']}*{dup_txt}"
            ),
            color=rar["color"],
        )
        embed.set_image(url=card_url)
        kwargs = {"embed": embed, "file": card_file}
        if view:
            kwargs["view"] = view
        await interaction.response.send_message(**kwargs)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # ============================================================== /equipo
    equipo = app_commands.Group(name="equipo", description="Forma y gestiona tu Equipo de 3 Trobimons y sus sinergias 🛡️")

    @equipo.command(name="ver", description="Muestra tu formación de 3 Trobimons, Poder Total (CP) y Sinergias Elementales 🛡️")
    @app_commands.describe(usuario="Entrenador que quieres consultar")
    async def equipo_ver(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        team = self.db.get_team(target.id, auto_fill=True)
        if not team:
            await interaction.response.send_message(
                embed=error_embed(f"{target.display_name} aún no tiene Trobimons. ¡Usa `/cazar`!"),
                ephemeral=True,
            )
            return

        syn = calc_team_synergies(team)
        total_cp = sum(pet_power(p) for p in team)
        tower_best = self.db.get_stat(target.id, "tower_floor")

        banner_file, banner_url = render_team_banner(target.display_name, team, syn, total_cp, tower_best)
        embed = discord.Embed(
            title=f"🛡️ Escuadrón de {target.display_name}",
            description=f"### ⚡ {total_cp:,} CP  ·  🏯 Torre: Piso {tower_best}",
            color=user_color(self.db, target.id),
        )
        embed.set_image(url=banner_url)

        slot_titles = ["1️⃣ Líder", "2️⃣ Vanguardia", "3️⃣ Apoyo"]
        for idx, p in enumerate(team):
            sp = CREATURES[p["species_id"]]
            el = ELEMENTS[sp["element"]]
            held_txt = item_label(p["held_item"]) if p.get("held_item") in ITEMS else "—"
            scr = SCROLL_SKILLS.get(p.get("extra_skill") or "")
            scr_txt = f"{scr['emoji']} {scr['name']}" if scr else "—"
            pas = sp.get("passive")
            pas_txt = f"{pas['emoji']} **{pas['name']}**\n-# {pas['desc']}" if pas else "—"
            embed.add_field(
                name=f"{slot_titles[idx]} · {el['emoji']} {pet_display_name(p).replace('**', '')}",
                value=f"🎒 {held_txt}\n📜 {scr_txt}\n🌟 {pas_txt}",
                inline=True,
            )

        syn_txt = "\n".join(f"• {l}" for l in syn["lines"]) if syn["lines"] else "-# Añade 2 o 3 Trobimons para activar Combinaciones Elementales."
        embed.add_field(name="🔗 Combinaciones activas", value=syn_txt[:1024], inline=False)
        embed.set_footer(text="/equipo asignar · /equipo auto · /equipo combinaciones")
        await interaction.response.send_message(embed=embed, file=banner_file)

    @equipo.command(name="combinaciones", description="Consulta todas las Combinaciones Especiales (3 del mismo elemento y parejas) 🧬")
    async def equipo_combinaciones(self, interaction: discord.Interaction):
        team = self.db.get_team(interaction.user.id, auto_fill=True)
        elems = [CREATURES[p["species_id"]]["element"] for p in team]
        unique_elems = set(elems)
        is_mono_3 = len(team) == 3 and len(unique_elems) == 1

        embed = discord.Embed(
            title="🧬 Catálogo de Combinaciones Especiales de Equipo",
            description=(
                "Forma tu equipo de 3 con `/equipo asignar` para activar **Resonancias Supremas (3 del mismo elemento)** "
                "o **Reacciones Elementales (parejas de elementos)**:"
            ),
            color=config.COLOR_MAIN,
        )

        mono_lines = []
        for el_key, combo in MONO_ELEMENT_COMBOS.items():
            mark = "✅ " if (is_mono_3 and elems[0] == el_key) else "• "
            mono_lines.append(f"{mark}**{combo['name']}**\n*{combo['desc']}*")
        embed.add_field(
            name="👑 3 del Mismo Elemento (Resonancias Supremas)",
            value="\n".join(mono_lines)[:1024],
            inline=False,
        )

        dual_lines = []
        for dc in DUAL_ELEMENT_COMBOS:
            active = (not is_mono_3) and dc["elems"].issubset(unique_elems)
            mark = "✅ " if active else "• "
            dual_lines.append(f"{mark}**{dc['name']}** — *{dc['desc']}*")
        embed.add_field(
            name="⚗️ Combinaciones de Elementos (Puedes activar varias a la vez)",
            value="\n".join(dual_lines)[:1024],
            inline=False,
        )
        embed.set_footer(text="✅ = Activa en tu /equipo actual · También existe 🌈 Triada Elemental (3 elementos distintos)")
        await interaction.response.send_message(embed=embed)

    @equipo.command(name="asignar", description="Coloca un Trobimon en el Puesto 1, 2 o 3 de tu equipo de combate")
    @app_commands.describe(puesto="Posición del equipo (1 = Líder, 2 = Vanguardia, 3 = Apoyo)", mascota="Tu Trobimon")
    @app_commands.choices(puesto=[
        app_commands.Choice(name="1️⃣ Puesto 1 — Líder (Compañero Activo)", value=1),
        app_commands.Choice(name="2️⃣ Puesto 2 — Vanguardia", value=2),
        app_commands.Choice(name="3️⃣ Puesto 3 — Apoyo", value=3),
    ])
    async def equipo_asignar(self, interaction: discord.Interaction, puesto: app_commands.Choice[int], mascota: int):
        uid = interaction.user.id
        if not self.db.set_team_slot(uid, puesto.value, mascota):
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon con ese ID."), ephemeral=True)
            return
        pet = self.db.get_pet(uid, mascota)
        team = self.db.get_team(uid, auto_fill=True)
        syn = calc_team_synergies(team)
        syn_note = ("\n\n**Sinergias activas:**\n" + "\n".join(syn["lines"])) if syn["lines"] else ""
        await interaction.response.send_message(
            embed=ok_embed(
                f"Has colocado a {pet_display_name(pet)} (`#{pet['pet_uid']}`) en el **Puesto {puesto.value}** de tu equipo.{syn_note}"
            )
        )

    @equipo_asignar.autocomplete("mascota")
    async def equipo_asignar_ac(self, interaction: discord.Interaction, current: str):
        return await self.equipar_ac(interaction, current)

    @equipo.command(name="auto", description="Forma automáticamente tu Equipo de 3 con tus Trobimons más poderosos ⚡")
    async def equipo_auto(self, interaction: discord.Interaction):
        uid = interaction.user.id
        pets = self.db.get_pets(uid)
        if not pets:
            await interaction.response.send_message(embed=error_embed("No tienes Trobimons todavía. ¡Usa `/cazar`!"), ephemeral=True)
            return

        ranked = sorted(pets, key=pet_power, reverse=True)[:3]
        for idx, p in enumerate(ranked, start=1):
            self.db.set_team_slot(uid, idx, p["pet_uid"])

        team = self.db.get_team(uid, auto_fill=False)
        syn = calc_team_synergies(team)
        lines = [
            f"**Puesto {i}:** {pet_display_name(p)} (Nv.{p['level']}) — `⚡ {pet_power(p)} CP`"
            for i, p in enumerate(team, start=1)
        ]
        if syn["lines"]:
            lines.append("\n**Sinergias activadas:**\n" + "\n".join(syn["lines"]))
        await interaction.response.send_message(
            embed=ok_embed("⚡ **¡Equipo Óptimo configurado automáticamente!**\n\n" + "\n".join(lines))
        )

    # ============================================================= /mascota
    mascota = app_commands.Group(name="mascota", description="Gestiona tus Trobimons, habilidades, objetos, duplicados, torre y combates")

    @mascota.command(name="ver", description="Muestra la tarjeta, estrellas, pasiva, habilidades, objeto e ilustración de un Trobimon")
    @app_commands.describe(mascota="ID del Trobimon que quieres ver (por defecto tu Líder activo)", usuario="Entrenador que quieres consultar")
    async def ver(self, interaction: discord.Interaction, mascota: Optional[int] = None, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        pet = self.db.get_pet(target.id, mascota) if mascota is not None else self.db.get_active_pet(target.id)
        if not pet:
            await interaction.response.send_message(
                embed=error_embed(f"No se encontró ese Trobimon en la colección de {target.display_name}."),
                ephemeral=True,
            )
            return

        sp = CREATURES[pet["species_id"]]
        el = ELEMENTS[sp["element"]]
        rar = RARITIES[sp["rarity"]]
        held_id = pet.get("held_item")
        stars = int(pet.get("stars") or 0)
        hp, atk = pet_stats(sp["id"], pet["level"], held_id, stars)
        need = pet_xp_needed(pet["level"])
        bonus = (
            RARITY_BONUS_PCT[sp["rarity"]]
            + stars * STAR_WORK_BONUS
            + PET_GEAR.get(held_id or "", {}).get("work_bonus_pct", 0)
        )

        if held_id and held_id in ITEMS:
            it = ITEMS[held_id]
            gear_summary = PET_GEAR.get(held_id, {}).get("summary", "")
            gear_txt = f"{it['emoji']} **{it['name']}** — *{gear_summary}*"
        else:
            gear_txt = "*Ninguno (`/mascota objeto`)*"

        evo_txt = "🌟 Etapa final máxima"
        if sp["evolves_to"]:
            next_sp = CREATURES[sp["evolves_to"]]
            evo_txt = f"Evoluciona a {next_sp['emoji']} **{next_sp['name']}** al **Nv. {sp['evolve_level']}** (o con 💎 Piedra Evolutiva)"

        star_txt = (
            f"{'⭐' * stars}{'☆' * (MAX_STARS - stars)} (`{stars}/{MAX_STARS}` → **+{int(stars * STAR_STAT_BONUS * 100)}% HP/ATQ**)"
            if stars > 0
            else f"☆☆☆☆☆ (`0/{MAX_STARS}` — Usa `/mascota fusionar` con repetidos)"
        )

        card_file, card_url = render_pet_card(pet, owner_name=target.display_name)
        embed = discord.Embed(
            title=f"{pet_display_name(pet).replace('**', '')}  ·  #{pet['pet_uid']}",
            description=f"### {rar['emoji']} {rar['name']} · {el['emoji']} {el['name']}\n-# {sp['desc']}",
            color=rar["color"],
        )
        embed.set_image(url=card_url)
        embed.add_field(name="🎒 Objeto", value=gear_txt, inline=True)
        embed.add_field(name="💰 Bonus /trabajar", value=f"**+{bonus}%**", inline=True)
        embed.add_field(name="🧬 Evolución", value=evo_txt, inline=False)
        embed.set_footer(text=f"Compañero de {target.display_name} · /equipo ver", icon_url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed, file=card_file)

    @ver.autocomplete("mascota")
    async def ver_ac(self, interaction: discord.Interaction, current: str):
        return await self.equipar_ac(interaction, current)

    # -------------------------------------------------------- /mascota objeto
    @mascota.command(name="objeto", description="Equipa (o quita) 1 objeto a tu Trobimon compañero 🎒")
    @app_commands.describe(objeto="Objeto equipable de tu inventario")
    async def objeto(self, interaction: discord.Interaction, objeto: str):
        uid = interaction.user.id
        pet = self.db.get_active_pet(uid)
        if not pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return

        old_item = pet.get("held_item")
        if objeto == UNEQUIP_VALUE:
            if not old_item:
                await interaction.response.send_message(embed=error_embed("Tu Trobimon no lleva ningún objeto equipado."), ephemeral=True)
                return
            self.db.set_pet_item(uid, pet["pet_uid"], None)
            self.db.add_item(uid, old_item, 1)
            await interaction.response.send_message(
                embed=ok_embed(f"Has quitado **{item_label(old_item)}** de tu compañero y ha vuelto a tu `/inventario`.")
            )
            return

        if objeto not in PET_GEAR or ITEMS.get(objeto, {}).get("type") != "gear":
            await interaction.response.send_message(embed=error_embed("Ese objeto no es un accesorio equipable de mascota."), ephemeral=True)
            return

        if not self.db.remove_item(uid, objeto, 1):
            await interaction.response.send_message(
                embed=error_embed(f"No tienes **{item_label(objeto)}** en tu inventario. Cómpralo en `/tienda`."),
                ephemeral=True,
            )
            return

        if old_item:
            self.db.add_item(uid, old_item, 1)
        self.db.set_pet_item(uid, pet["pet_uid"], objeto)
        summary = PET_GEAR[objeto]["summary"]
        returned_txt = f"\n*(El objeto anterior **{item_label(old_item)}** se ha guardado en tu inventario)*" if old_item else ""
        await interaction.response.send_message(
            embed=ok_embed(
                f"Has equipado **{item_label(objeto)}** (`{summary}`) a {pet_display_name(pet)}.{returned_txt}"
            )
        )

    @objeto.autocomplete("objeto")
    async def objeto_ac(self, interaction: discord.Interaction, current: str):
        inv = self.db.get_inventory(interaction.user.id)
        out = [app_commands.Choice(name="❌ Quitar objeto equipado (devolver al inventario)", value=UNEQUIP_VALUE)]
        for item_id, qty in inv.items():
            it = ITEMS.get(item_id)
            if it and it["type"] == "gear" and current.lower() in it["name"].lower():
                summary = PET_GEAR.get(item_id, {}).get("summary", "")
                label = f"{it['emoji']} {it['name']} (x{qty}) — {summary}"
                out.append(app_commands.Choice(name=label[:100], value=item_id))
        return out[:25]

    # ----------------------------------------------------- /mascota habilidad
    @mascota.command(name="habilidad", description="Enseña una 5ª Habilidad Secreta a tu Trobimon usando un Pergamino 📜")
    @app_commands.describe(pergamino="Pergamino de Habilidad de tu inventario")
    async def habilidad(self, interaction: discord.Interaction, pergamino: str):
        uid = interaction.user.id
        pet = self.db.get_active_pet(uid)
        if not pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return

        old_scroll = pet.get("extra_skill")
        if pergamino == UNEQUIP_VALUE:
            if not old_scroll:
                await interaction.response.send_message(embed=error_embed("Tu Trobimon no tiene ninguna habilidad secreta equipada."), ephemeral=True)
                return
            self.db.set_pet_extra_skill(uid, pet["pet_uid"], None)
            self.db.add_item(uid, old_scroll, 1)
            await interaction.response.send_message(
                embed=ok_embed(f"Has retirado **{item_label(old_scroll)}** y se ha guardado en tu `/inventario`.")
            )
            return

        if pergamino not in SCROLL_SKILLS or ITEMS.get(pergamino, {}).get("type") != "scroll":
            await interaction.response.send_message(embed=error_embed("Ese objeto no es un Pergamino de Habilidad válido."), ephemeral=True)
            return

        if not self.db.remove_item(uid, pergamino, 1):
            await interaction.response.send_message(
                embed=error_embed(f"No tienes **{item_label(pergamino)}** en tu inventario. Cómpralo en `/tienda`."),
                ephemeral=True,
            )
            return

        if old_scroll:
            self.db.add_item(uid, old_scroll, 1)
        self.db.set_pet_extra_skill(uid, pet["pet_uid"], pergamino)
        sk = SCROLL_SKILLS[pergamino]
        ret = f"\n*(El pergamino anterior **{item_label(old_scroll)}** ha vuelto a tu inventario)*" if old_scroll else ""
        await interaction.response.send_message(
            embed=ok_embed(
                f"📜 ¡{pet_display_name(pet)} ha aprendido la habilidad secreta {sk['emoji']} **{sk['name']}** (`{sk.get('role', 'Secreta')}`)!\n"
                f"*{sk['desc']}*{ret}"
            )
        )

    @habilidad.autocomplete("pergamino")
    async def habilidad_ac(self, interaction: discord.Interaction, current: str):
        inv = self.db.get_inventory(interaction.user.id)
        out = [app_commands.Choice(name="❌ Quitar pergamino equipado (devolver al inventario)", value=UNEQUIP_VALUE)]
        for item_id, qty in inv.items():
            it = ITEMS.get(item_id)
            if it and it["type"] == "scroll" and current.lower() in it["name"].lower():
                sk = SCROLL_SKILLS.get(item_id, {})
                label = f"{it['emoji']} {it['name']} (x{qty}) — {sk.get('desc', '')}"
                out.append(app_commands.Choice(name=label[:100], value=item_id))
        return out[:25]

    # ------------------------------------------------------ /mascota fusionar
    @mascota.command(name="fusionar", description="Fusiona un Trobimon repetido de la misma línea evolutiva para subir Estrellas (⭐) y XP")
    @app_commands.describe(repetido="El Trobimon repetido que quieres sacrificar en la fusión")
    async def fusionar(self, interaction: discord.Interaction, repetido: int):
        uid = interaction.user.id
        main_pet = self.db.get_active_pet(uid)
        if not main_pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return

        dup_pet = self.db.get_pet(uid, repetido)
        if not dup_pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon con ese ID."), ephemeral=True)
            return
        if dup_pet["pet_uid"] == main_pet["pet_uid"]:
            await interaction.response.send_message(
                embed=error_embed("No puedes fusionar a tu compañero activo consigo mismo. Elige otro ID duplicado."),
                ephemeral=True,
            )
            return
        if not same_family(main_pet["species_id"], dup_pet["species_id"]):
            sp_main = CREATURES[main_pet["species_id"]]
            sp_dup = CREATURES[dup_pet["species_id"]]
            await interaction.response.send_message(
                embed=error_embed(
                    f"Para fusionar deben ser de la **misma línea evolutiva**.\n"
                    f"Tu compañero activo es **{sp_main['name']}** y `#{dup_pet['pet_uid']}` es **{sp_dup['name']}**.\n"
                    f"💡 Usa `/mascota repetidos` para fusionar automáticamente todos tus repetidos con su pareja."
                ),
                ephemeral=True,
            )
            return

        updated, old_s, new_s, ret_item = await execute_fusion(self.bot, interaction.user, main_pet, dup_pet, interaction.channel)
        hp, atk = pet_stats(updated["species_id"], updated["level"], updated.get("held_item"), new_s)
        ret_txt = f"\n🎒 Se devolvió **{item_label(ret_item)}** a tu inventario." if ret_item else ""
        await interaction.response.send_message(
            embed=ok_embed(
                f"⭐ **¡Ascensión Estelar completada!**\n"
                f"Tu {pet_display_name(updated)} (`#{updated['pet_uid']}`) ha absorbido la energía de `#{repetido}`:\n"
                f"• **Estrellas:** `{old_s}★` ➔ **`{new_s}★`** (+{new_s * 10}% HP/ATQ y +{new_s * STAR_WORK_BONUS}% monedas en `/trabajar`)\n"
                f"• **Nivel y Estadísticas:** Nv. **{updated['level']}** — ❤️ **{hp}** HP · ⚔️ **{atk}** ATQ{ret_txt}"
            )
        )

    @fusionar.autocomplete("repetido")
    async def fusionar_ac(self, interaction: discord.Interaction, current: str):
        uid = interaction.user.id
        main_pet = self.db.get_active_pet(uid)
        pets = self.db.get_pets(uid)
        out = []
        for p in pets:
            if main_pet and p["pet_uid"] == main_pet["pet_uid"]:
                continue
            if main_pet and not same_family(main_pet["species_id"], p["species_id"]):
                continue
            sp = CREATURES[p["species_id"]]
            label = f"#{p['pet_uid']} {sp['emoji']} {p['nickname'] or sp['name']} (Nv.{p['level']}{stars_badge(p.get('stars', 0))})"
            if current.lower() in label.lower():
                out.append(app_commands.Choice(name=label[:100], value=p["pet_uid"]))
        return out[:25]

    # ------------------------------------------------------- /mascota liberar
    @mascota.command(name="liberar", description="Libera un Trobimon repetido a cambio de monedas y comida/caramelos 🕊️")
    @app_commands.describe(mascota="El Trobimon que quieres liberar")
    async def liberar(self, interaction: discord.Interaction, mascota: int):
        uid = interaction.user.id
        pets = self.db.get_pets(uid)
        if len(pets) <= 1:
            await interaction.response.send_message(
                embed=error_embed("No puedes liberar a tu único Trobimon."), ephemeral=True
            )
            return

        target = self.db.get_pet(uid, mascota)
        if not target:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon con ese ID."), ephemeral=True)
            return
        if target.get("is_active"):
            await interaction.response.send_message(
                embed=error_embed("No puedes liberar a tu compañero activo. Equipa otro antes con `/mascota equipar`."),
                ephemeral=True,
            )
            return

        coins, item_id, qty = calc_release_reward(target)
        ret_item = target.get("held_item")
        if ret_item:
            self.db.add_item(uid, ret_item, 1)
        if target.get("extra_skill"):
            self.db.add_item(uid, target["extra_skill"], 1)

        sp = CREATURES[target["species_id"]]
        self.db.delete_pet(uid, target["pet_uid"])
        self.db.add_coins(uid, coins)
        self.db.add_item(uid, item_id, qty)

        await interaction.response.send_message(
            embed=ok_embed(
                f"🕊️ Has liberado a {sp['emoji']} **{target.get('nickname') or sp['name']}** (`#{target['pet_uid']}`) en su hábitat.\n"
                f"Agradecido, te ha dejado **{fmt(coins)}** y **{qty}x {item_label(item_id)}**."
            )
        )

    @liberar.autocomplete("mascota")
    async def liberar_ac(self, interaction: discord.Interaction, current: str):
        pets = self.db.get_pets(interaction.user.id)
        out = []
        for p in pets:
            if p.get("is_active"):
                continue
            sp = CREATURES[p["species_id"]]
            coins, item_id, qty = calc_release_reward(p)
            label = f"#{p['pet_uid']} {sp['emoji']} {p['nickname'] or sp['name']} (Nv.{p['level']}) ➔ +{coins} monedas y {qty}x {ITEMS[item_id]['name']}"
            if current.lower() in label.lower():
                out.append(app_commands.Choice(name=label[:100], value=p["pet_uid"]))
        return out[:25]

    # ----------------------------------------------------- /mascota repetidos
    @mascota.command(name="repetidos", description="Fusiona o libera automáticamente todos tus Trobimons repetidos de golpe ✨")
    @app_commands.describe(accion="Qué hacer con tus Trobimons duplicados")
    @app_commands.choices(accion=[
        app_commands.Choice(name="⭐ Fusionar todos los repetidos (sube Estrellas y XP; libera los que sobren de 5★)", value="fusionar"),
        app_commands.Choice(name="🕊️ Liberar todos los repetidos a cambio de Monedas y Comida/Caramelos", value="liberar"),
    ])
    async def repetidos(self, interaction: discord.Interaction, accion: app_commands.Choice[str]):
        uid = interaction.user.id
        pets = self.db.get_pets(uid)
        if len(pets) <= 1:
            await interaction.response.send_message(embed=error_embed("No tienes Trobimons repetidos."), ephemeral=True)
            return

        by_family: dict[str, list[dict]] = {}
        for p in pets:
            fam = CREATURES[p["species_id"]]["family"]
            by_family.setdefault(fam, []).append(p)

        for fam_list in by_family.values():
            fam_list.sort(
                key=lambda p: (
                    p.get("is_active", 0),
                    1 if int(p.get("team_slot") or 0) in (1, 2, 3) else 0,
                    CREATURES[p["species_id"]]["stage"],
                    p.get("stars", 0),
                    p["level"],
                    -p["pet_uid"],
                ),
                reverse=True,
            )

        dups_exist = any(len(lst) > 1 for lst in by_family.values())
        if not dups_exist:
            await interaction.response.send_message(
                embed=error_embed("No tienes ningún Trobimon repetido de la misma familia evolutiva."),
                ephemeral=True,
            )
            return

        fused_count = 0
        released_count = 0
        total_coins = 0
        items_gained: dict[str, int] = {}

        for fam, fam_list in by_family.items():
            if len(fam_list) <= 1:
                continue
            main_pet = fam_list[0]
            for dup in fam_list[1:]:
                if dup.get("is_active") or int(dup.get("team_slot") or 0) in (1, 2, 3):
                    continue
                main_fresh = self.db.get_pet(uid, main_pet["pet_uid"])
                if accion.value == "fusionar" and main_fresh and int(main_fresh.get("stars") or 0) < MAX_STARS:
                    await execute_fusion(self.bot, interaction.user, main_fresh, dup, interaction.channel)
                    fused_count += 1
                else:
                    coins, item_id, qty = calc_release_reward(dup)
                    if dup.get("held_item"):
                        self.db.add_item(uid, dup["held_item"], 1)
                    if dup.get("extra_skill"):
                        self.db.add_item(uid, dup["extra_skill"], 1)
                    self.db.delete_pet(uid, dup["pet_uid"])
                    self.db.add_coins(uid, coins)
                    self.db.add_item(uid, item_id, qty)
                    total_coins += coins
                    items_gained[item_id] = items_gained.get(item_id, 0) + qty
                    released_count += 1

        if fused_count == 0 and released_count == 0:
            await interaction.response.send_message(
                embed=error_embed("Tus únicos repetidos forman parte de tu `/equipo` titular. Quítalos del equipo si deseas fusionarlos."),
                ephemeral=True,
            )
            return

        summary_lines = []
        if fused_count > 0:
            summary_lines.append(f"⭐ **{fused_count} Trobimon(s)** fusionados para subir Estrellas y XP.")
        if released_count > 0:
            items_txt = ", ".join(f"**{q}x {item_label(i)}**" for i, q in items_gained.items())
            summary_lines.append(
                f"🕊️ **{released_count} Trobimon(s)** liberados ➔ Ganaste **{fmt(total_coins)}** y {items_txt}."
            )
        await interaction.response.send_message(embed=ok_embed("\n".join(summary_lines)))

    # ---------------------------------------------------- /mascota prodigioso
    @mascota.command(name="prodigioso", description="Intercambio Prodigioso: entrega un Trobimon repetido y recibe otra especie al azar 🌀")
    @app_commands.describe(mascota="El Trobimon repetido que quieres enviar al Portal Prodigioso (cuesta 200 monedas)")
    async def prodigioso(self, interaction: discord.Interaction, mascota: int):
        uid = interaction.user.id
        pets = self.db.get_pets(uid)
        if len(pets) <= 1:
            await interaction.response.send_message(embed=error_embed("Necesitas al menos 2 Trobimons para usar el Portal Prodigioso."), ephemeral=True)
            return

        sacrificed = self.db.get_pet(uid, mascota)
        if not sacrificed:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon con ese ID."), ephemeral=True)
            return
        if sacrificed.get("is_active"):
            await interaction.response.send_message(embed=error_embed("No puedes enviar a tu compañero activo. Equipa otro primero."), ephemeral=True)
            return

        fee = 200
        if not self.db.remove_coins(uid, fee):
            await interaction.response.send_message(embed=error_embed(f"Activar el Portal Prodigioso cuesta {fmt(fee)}."), ephemeral=True)
            return

        if sacrificed.get("held_item"):
            self.db.add_item(uid, sacrificed["held_item"], 1)
        if sacrificed.get("extra_skill"):
            self.db.add_item(uid, sacrificed["extra_skill"], 1)

        old_sp = CREATURES[sacrificed["species_id"]]
        new_lvl = sacrificed["level"]
        self.db.delete_pet(uid, sacrificed["pet_uid"])

        rarity_weights = {
            "comun":      {"comun": 45, "raro": 40, "epico": 12, "legendario": 3},
            "raro":       {"comun": 15, "raro": 55, "epico": 23, "legendario": 7},
            "epico":      {"comun": 5,  "raro": 30, "epico": 50, "legendario": 15},
            "legendario": {"comun": 0,  "raro": 15, "epico": 45, "legendario": 40},
        }[old_sp["rarity"]]

        candidates = [c for c in CREATURES.values() if c["id"] != old_sp["id"]]
        weights = [rarity_weights[c["rarity"]] for c in candidates]
        new_sp = random.choices(candidates, weights=weights)[0]

        new_pet, is_new = self.db.add_pet(uid, new_sp["id"], new_lvl)
        if new_sp["rarity"] == "legendario":
            self.db.incr_stat(uid, "legendary_drops")

        rar = RARITIES[new_sp["rarity"]]
        file, url = creature_file_and_url(new_sp["id"])
        new_txt = "\n📖 **¡Nueva especie registrada en el `/trobidex`!**" if is_new else ""
        embed = discord.Embed(
            title="🌀 ¡Intercambio Prodigioso Completado!",
            description=(
                f"Enviaste a {old_sp['emoji']} **{old_sp['name']}** al vórtice dimensional y ha llegado...\n\n"
                f"✨ ¡Un {new_sp['emoji']} **{new_sp['name']}** de **Nivel {new_lvl}** "
                f"({rar['emoji']} {rar['name']})!\n"
                f"🆔 ID: **`#{new_pet['pet_uid']}`**{new_txt}\n\n"
                f"*{new_sp['desc']}*"
            ),
            color=rar["color"],
        )
        if url:
            embed.set_image(url=url)
        if file:
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    @prodigioso.autocomplete("mascota")
    async def prodigioso_ac(self, interaction: discord.Interaction, current: str):
        return await self.liberar_ac(interaction, current)

    # --------------------------------------------------------- /mascota lista
    @mascota.command(name="lista", description="Muestra todos los Trobimons que has capturado, sus estrellas y su puesto en el equipo")
    @app_commands.describe(usuario="Entrenador")
    async def lista(self, interaction: discord.Interaction, usuario: Optional[discord.Member] = None):
        target = usuario or interaction.user
        pets = self.db.get_pets(target.id)
        if not pets:
            await interaction.response.send_message(
                embed=error_embed(f"{target.display_name} no tiene Trobimons todavía. ¡Usa `/cazar`!"),
                ephemeral=True,
            )
            return

        lines = []
        for p in pets[:25]:
            sp = CREATURES[p["species_id"]]
            rar = RARITIES[sp["rarity"]]
            slot = int(p.get("team_slot") or 0)
            slot_tag = f" 🛡️`[Puesto {slot}]`" if slot in (1, 2, 3) else (" 🌟`[Activo]`" if p["is_active"] else "")
            nick = f" «{p['nickname']}»" if p.get("nickname") else ""
            stars = stars_badge(p.get("stars", 0))
            held = f" · 🎒 {ITEMS[p['held_item']]['emoji']}" if p.get("held_item") in ITEMS else ""
            scroll = f" · 📜 {SCROLL_SKILLS[p['extra_skill']]['emoji']}" if p.get("extra_skill") in SCROLL_SKILLS else ""
            lines.append(f"`#{p['pet_uid']}` {rar['emoji']} {sp['emoji']} **{sp['name']}**{nick}{stars} — **Nv. {p['level']}**{held}{scroll}{slot_tag}")

        embed = discord.Embed(
            title=f"🐾 Trobimons de {target.display_name} ({len(pets)})",
            description="\n".join(lines),
            color=user_color(self.db, target.id),
        )
        embed.set_footer(text="Usa /equipo ver para gestionar tu equipo de 3 o /mascota repetidos para fusionar duplicados")
        await interaction.response.send_message(embed=embed)

    @mascota.command(name="equipar", description="Elige cuál de tus Trobimons es tu Líder (Puesto 1)")
    @app_commands.describe(mascota="Tu Trobimon")
    async def equipar(self, interaction: discord.Interaction, mascota: int):
        uid = interaction.user.id
        if not self.db.set_active_pet(uid, mascota):
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon con ese ID."), ephemeral=True)
            return
        pet = self.db.get_pet(uid, mascota)
        await interaction.response.send_message(
            embed=ok_embed(f"Ahora tu Líder (Puesto 1) es {pet_display_name(pet)} (Nv. {pet['level']}) `#{pet['pet_uid']}`.")
        )

    @equipar.autocomplete("mascota")
    async def equipar_ac(self, interaction: discord.Interaction, current: str):
        pets = self.db.get_pets(interaction.user.id)
        out = []
        for p in pets:
            sp = CREATURES[p["species_id"]]
            label = f"#{p['pet_uid']} {sp['emoji']} {p['nickname'] or sp['name']}{stars_badge(p.get('stars', 0))} (Nv.{p['level']})"
            if current.lower() in label.lower():
                out.append(app_commands.Choice(name=label[:100], value=p["pet_uid"]))
        return out[:25]

    @mascota.command(name="apodo", description="Ponle un nombre personalizado a tu Trobimon compañero")
    @app_commands.describe(nombre="Nuevo apodo (escribe 'borrar' para quitarlo)")
    async def apodo(self, interaction: discord.Interaction, nombre: app_commands.Range[str, 1, 28]):
        uid = interaction.user.id
        pet = self.db.get_active_pet(uid)
        if not pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return
        nick = None if nombre.strip().lower() == "borrar" else nombre.strip()
        self.db.rename_pet(uid, pet["pet_uid"], nick)
        msg = "Apodo eliminado." if nick is None else f"Tu compañero ahora se llama **{nick}**."
        await interaction.response.send_message(embed=ok_embed(msg))

    @mascota.command(name="alimentar", description="Alimenta a tu Trobimon activo para subirlo de nivel y evolucionarlo 🍖🍬")
    @app_commands.describe(comida="Comida o caramelo de tu inventario", cantidad="Cuántos darle (máx. 10)")
    @app_commands.choices(comida=[
        app_commands.Choice(name="🍖 Chuletón Ibérico (+60 XP)", value="comida_trobimon"),
        app_commands.Choice(name="🍬 Caramelo Místico (+1 Nivel completo)", value="caramelo_raro"),
    ])
    async def alimentar(self, interaction: discord.Interaction, comida: app_commands.Choice[str],
                        cantidad: app_commands.Range[int, 1, 10] = 1):
        uid = interaction.user.id
        pet = self.db.get_active_pet(uid)
        if not pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return

        item_id = comida.value
        if not self.db.remove_item(uid, item_id, cantidad):
            await interaction.response.send_message(
                embed=error_embed(f"No tienes `{cantidad}x` {item_label(item_id)}. Cómpralo en `/tienda`."),
                ephemeral=True,
            )
            return

        if item_id == "comida_trobimon":
            xp_gain = 60 * cantidad
        else:
            xp_gain = sum(pet_xp_needed(pet["level"] + i) for i in range(cantidad))

        old_lvl = pet["level"]
        updated, _ = await add_pet_xp(self.bot, interaction.user, pet, xp_gain, interaction.channel)
        sp = CREATURES[updated["species_id"]]
        lvl_txt = f" y subió a **Nivel {updated['level']}**" if updated["level"] > old_lvl else ""
        await interaction.response.send_message(
            embed=ok_embed(
                f"Le diste **{cantidad}x {item_label(item_id)}** a {sp['emoji']} **{sp['name']}** (+{xp_gain} XP){lvl_txt}."
            )
        )

    @mascota.command(name="evolucionar", description="Evoluciona a tu Trobimon compañero usando una 💎 Piedra Evolutiva")
    async def evolucionar(self, interaction: discord.Interaction):
        uid = interaction.user.id
        pet = self.db.get_active_pet(uid)
        if not pet:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon activo."), ephemeral=True)
            return

        sp = CREATURES[pet["species_id"]]
        if not sp["evolves_to"]:
            await interaction.response.send_message(
                embed=error_embed(f"{sp['emoji']} **{sp['name']}** ya está en su etapa evolutiva máxima."),
                ephemeral=True,
            )
            return

        if not self.db.remove_item(uid, "piedra_evolutiva", 1):
            await interaction.response.send_message(
                embed=error_embed(
                    f"Necesitas una **💎 Piedra Evolutiva** (cómprala en `/tienda`) o subirlo a **Nivel {sp['evolve_level']}** con `/mascota alimentar`."
                ),
                ephemeral=True,
            )
            return

        new_id = sp["evolves_to"]
        new_sp = CREATURES[new_id]
        new_lvl = max(pet["level"], sp["evolve_level"] or pet["level"])
        self.db.update_pet(uid, pet["pet_uid"], new_id, new_lvl, pet["xp"])
        self.db.register_trobidex(uid, new_id)
        self.db.incr_stat(uid, "pets_evolved")

        file, url = creature_file_and_url(new_id)
        embed = discord.Embed(
            title="💎✨ ¡¡EVOLUCIÓN COMPLETADA!! ✨💎",
            description=(
                f"La **Piedra Evolutiva** ha brillado con fuerza...\n"
                f"¡Tu {sp['emoji']} **{sp['name']}** ha evolucionado en {new_sp['emoji']} **{new_sp['name']}**{stars_badge(pet.get('stars', 0))} "
                f"({RARITIES[new_sp['rarity']]['emoji']} {RARITIES[new_sp['rarity']]['name']})!\n\n"
                f"*{new_sp['desc']}*\n\n"
                f"**Nuevas habilidades desbloqueadas:**\n{format_skills_block(new_id, pet.get('extra_skill'))}"
            ),
            color=RARITIES[new_sp["rarity"]]["color"],
        )
        if url:
            embed.set_image(url=url)
        if file:
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)
        await check_achievements(self.bot, interaction.user, interaction.channel)

    # ------------------------------------------------------- /mascota entrenar
    @mascota.command(name="entrenar", description="Combate táctico por equipos (hasta 3v3) contra Guardianes Salvajes 🥊")
    async def entrenar(self, interaction: discord.Interaction):
        uid = interaction.user.id
        now = time.time()
        rem = int(TRAIN_COOLDOWN - (now - self._train_cd.get(uid, 0)))
        if rem > 0:
            await interaction.response.send_message(
                embed=error_embed(f"Tu equipo está recuperando aliento. Espera **{rem}s**."),
                ephemeral=True,
            )
            return

        team = self.db.get_team(uid, auto_fill=True)
        if not team:
            await interaction.response.send_message(
                embed=error_embed("Primero captura un Trobimon con `/cazar` o `/incubadora`."),
                ephemeral=True,
            )
            return
        self._train_cd[uid] = now

        ai_team = []
        pool = list(CREATURES.values())
        for p in team:
            enemy_sp = random.choice(pool)
            enemy_lvl = max(1, p["level"] + random.randint(-1, 1))
            ai_team.append({
                "species_id": enemy_sp["id"],
                "level": enemy_lvl,
                "nickname": None,
                "held_item": None,
                "stars": random.randint(0, max(0, int(p.get("stars") or 0) - 1)),
                "extra_skill": None,
            })

        s1 = TeamSide(interaction.user.display_name, interaction.user, team, is_ai=False)
        s2 = TeamSide("Patrulla Salvaje", None, ai_team, is_ai=True)
        battle = TacticalBattleView(self, s1, s2, bet=0, mode="train")
        await interaction.response.send_message(embed=battle.render_embed(), file=battle.files()[0], view=battle)

    # ---------------------------------------------------------- /mascota torre
    @mascota.command(name="torre", description="Desafía el siguiente piso de la Torre de Campeones con tu Equipo de 3 Trobimons 🏯")
    async def torre(self, interaction: discord.Interaction):
        uid = interaction.user.id
        now = time.time()
        rem = int(TOWER_COOLDOWN - (now - self._tower_cd.get(uid, 0)))
        if rem > 0:
            await interaction.response.send_message(
                embed=error_embed(f"Las puertas de la Torre se están recargando. Espera **{rem}s**."),
                ephemeral=True,
            )
            return

        team = self.db.get_team(uid, auto_fill=True)
        if not team:
            await interaction.response.send_message(
                embed=error_embed("Necesitas al menos 1 Trobimon (recomendado un equipo de 3 con `/equipo ver`) para entrar a la Torre."),
                ephemeral=True,
            )
            return
        self._tower_cd[uid] = now

        next_floor = self.db.get_stat(uid, "tower_floor") + 1
        boss_floor = (next_floor % 5 == 0)
        stage_pool = (
            [c for c in CREATURES.values() if c["stage"] >= 2]
            if next_floor >= 4
            else list(CREATURES.values())
        )
        if boss_floor:
            stage_pool = [c for c in CREATURES.values() if c["rarity"] in ("epico", "legendario")]

        floor_lvl = max(1, next_floor * 2)
        stars_ai = min(MAX_STARS, next_floor // 3)
        gear_keys = list(PET_GEAR.keys())
        ai_team = []
        for _ in range(3):
            sp = random.choice(stage_pool)
            ai_team.append({
                "species_id": sp["id"],
                "level": floor_lvl,
                "nickname": f"Guardián P{next_floor}" if boss_floor else None,
                "held_item": random.choice(gear_keys) if next_floor >= 3 else None,
                "stars": stars_ai,
                "extra_skill": random.choice(list(SCROLL_SKILLS.keys())) if boss_floor else None,
            })

        boss_title = f"👑 Jefe del Piso {next_floor}" if boss_floor else f"🏯 Guardián del Piso {next_floor}"
        s1 = TeamSide(interaction.user.display_name, interaction.user, team, is_ai=False)
        s2 = TeamSide(boss_title, None, ai_team, is_ai=True)
        battle = TacticalBattleView(self, s1, s2, bet=0, mode="tower", tower_floor=next_floor)
        await interaction.response.send_message(embed=battle.render_embed(), file=battle.files()[0], view=battle)

    # ------------------------------------------------------- /mascota combatir
    @mascota.command(name="combatir", description="Reta al Equipo de Trobimons de otra persona a una batalla táctica 3v3 🐾⚔️")
    @app_commands.describe(rival="Entrenador rival", apuesta="Monedas de apuesta opcional")
    async def combatir(self, interaction: discord.Interaction, rival: discord.Member,
                       apuesta: Optional[app_commands.Range[int, 10, 100_000]] = None):
        if rival.bot or rival.id == interaction.user.id:
            await interaction.response.send_message(
                embed=error_embed("Elige a otro miembro humano (o usa `/mascota entrenar` / `/mascota torre` para jugar contra la IA)."),
                ephemeral=True,
            )
            return
        team1 = self.db.get_team(interaction.user.id, auto_fill=True)
        team2 = self.db.get_team(rival.id, auto_fill=True)
        if not team1:
            await interaction.response.send_message(embed=error_embed("No tienes ningún Trobimon."), ephemeral=True)
            return
        if not team2:
            await interaction.response.send_message(embed=error_embed(f"{rival.display_name} aún no tiene ningún Trobimon."), ephemeral=True)
            return

        bet = apuesta or 0
        if bet:
            if self.db.get_coins(interaction.user.id) < bet:
                await interaction.response.send_message(embed=error_embed("No tienes suficientes monedas."), ephemeral=True)
                return
            if self.db.get_coins(rival.id) < bet:
                await interaction.response.send_message(embed=error_embed(f"{rival.display_name} no tiene suficientes monedas."), ephemeral=True)
                return

        t1_str = " · ".join(f"{CREATURES[p['species_id']]['emoji']} **{CREATURES[p['species_id']]['name']}** (Nv.{p['level']})" for p in team1)
        t2_str = " · ".join(f"{CREATURES[p['species_id']]['emoji']} **{CREATURES[p['species_id']]['name']}** (Nv.{p['level']})" for p in team2)
        bet_txt = f"\n💰 **Apuesta:** {fmt(bet)} cada uno" if bet else "\n🤝 **Combate amistoso** (da XP a todo el equipo)"
        embed = discord.Embed(
            title="🐾⚔️ ¡Desafío de Equipos de Trobimons!",
            description=(
                f"**{interaction.user.mention}** reta a **{rival.mention}** a una batalla táctica por equipos!\n\n"
                f"🛡️ **Equipo de {interaction.user.display_name}:** {t1_str}\n"
                f"🛡️ **Equipo de {rival.display_name}:** {t2_str}\n"
                f"{bet_txt}"
            ),
            color=config.COLOR_MAIN,
        )
        view = PetChallengeView(self, interaction.user, rival, team1, team2, bet)
        await interaction.response.send_message(content=rival.mention, embed=embed, view=view)

    # ------------------------------------------------------------- /trobidex
    @app_commands.command(name="trobidex", description="Enciclopedia de las 22 especies de Trobimons, sus 4 habilidades y evoluciones 📖")
    @app_commands.describe(especie="Ver la ficha, habilidades e ilustración de una especie descubierta")
    async def trobidex(self, interaction: discord.Interaction, especie: Optional[str] = None):
        discovered = self.db.get_trobidex(interaction.user.id)

        if especie:
            sp = CREATURES.get(especie)
            if not sp:
                # Permitir buscar también por nombre o número si el usuario escribió texto libre
                q = especie.strip().lower().lstrip("#")
                for cand in CREATURES.values():
                    if cand["name"].lower() == q or str(cand["num"]) == q:
                        sp = cand
                        especie = cand["id"]
                        break
            if not sp:
                await interaction.response.send_message(embed=error_embed("Esa especie no existe."), ephemeral=True)
                return
            rar = RARITIES[sp["rarity"]]
            el = ELEMENTS[sp["element"]]
            evo_info = f"Evoluciona a **{CREATURES[sp['evolves_to']]['name']}** (Nv. {sp['evolve_level']})" if sp["evolves_to"] else "Etapa evolutiva final"
            owned_status = "✅ Registrado en tu Trobidex" if especie in discovered else "🔎 Aún no capturado"
            dex_pet = {"species_id": especie, "level": 1, "xp": 0, "stars": 0, "held_item": None, "extra_skill": None, "nickname": None}
            card_file, card_url = render_pet_card(dex_pet)
            embed = discord.Embed(
                title=f"📖 Trobidex #{sp['num']:02d} · {sp['emoji']} {sp['name']}",
                description=f"### {rar['emoji']} {rar['name']} · {el['emoji']} {el['name']}\n-# {sp['desc']}",
                color=rar["color"],
            )
            embed.set_image(url=card_url)
            embed.add_field(name="🧬 Evolución", value=evo_info, inline=False)
            embed.set_footer(text=f"{owned_status} · {len(discovered)}/{len(CREATURES)} descubiertos")
            await interaction.response.send_message(embed=embed, file=card_file)
            return

        embed = discord.Embed(
            title=f"📖 Trobidex de {interaction.user.display_name} ({len(discovered)}/{len(CREATURES)})",
            description="Colecciona las **48 especies** repartidas en los **8 Elementos** (6 por elemento):",
            color=config.COLOR_MAIN,
        )
        by_elem: dict[str, list[dict]] = {}
        for sp in sorted(CREATURES.values(), key=lambda x: x["num"]):
            by_elem.setdefault(sp["element"], []).append(sp)

        for el_key, el_info in ELEMENTS.items():
            el_lines = []
            for sp in by_elem.get(el_key, []):
                rar = RARITIES[sp["rarity"]]
                if sp["id"] in discovered:
                    evo = f" *(➔ Nv.{sp['evolve_level']} {CREATURES[sp['evolves_to']]['name']})*" if sp["evolves_to"] else ""
                    el_lines.append(f"`#{sp['num']:02d}` ✅ {rar['emoji']} {sp['emoji']} **{sp['name']}**{evo}")
                else:
                    el_lines.append(f"`#{sp['num']:02d}` ❓ {rar['emoji']} *??? (Etapa {sp['stage']})*")
            embed.add_field(
                name=f"{el_info['emoji']} {el_info['name']}",
                value="\n".join(el_lines)[:1024],
                inline=True,
            )
        embed.set_footer(text="Usa /trobidex especie:<nombre> para ver pasiva, 4 habilidades e ilustración HD")
        await interaction.response.send_message(embed=embed)

    @trobidex.autocomplete("especie")
    async def trobidex_ac(self, interaction: discord.Interaction, current: str):
        discovered = self.db.get_trobidex(interaction.user.id)
        q = current.lower().strip()
        out = []
        for sp in sorted(CREATURES.values(), key=lambda x: x["num"]):
            el = ELEMENTS[sp["element"]]
            mark = "✅" if sp["id"] in discovered else "📖"
            label = f"#{sp['num']:02d} {mark} {sp['emoji']} {sp['name']} ({el['name']})"
            if not q or q in label.lower() or q in sp["id"].lower():
                out.append(app_commands.Choice(name=label[:100], value=sp["id"]))
        return out[:25]


async def setup(bot):
    await bot.add_cog(Pets(bot))
