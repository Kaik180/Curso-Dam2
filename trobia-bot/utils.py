"""Funciones compartidas: formato, XP, logros, apuestas."""
import time

import discord

import config
from data.achievements import ACHIEVEMENTS
from data.items import ITEMS


DIVIDER = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"


def fmt(n: int) -> str:
    return f"**{int(n):,}".replace(",", ".") + f"** {config.CURRENCY}"


def progress_bar(current: int, total: int, length: int = 12) -> str:
    filled = int(length * current / total) if total else 0
    filled = max(0, min(length, filled))
    return "▰" * filled + "▱" * (length - filled)


def error_embed(text: str) -> discord.Embed:
    return discord.Embed(description=f"### ❌ Ups…\n{text}", color=config.COLOR_ERROR)


def ok_embed(text: str) -> discord.Embed:
    return discord.Embed(description=f"### ✅ ¡Hecho!\n{text}", color=config.COLOR_OK)


def info_embed(title: str, text: str = "", color: int = config.COLOR_MAIN) -> discord.Embed:
    """Embed con jerarquía estándar: título → subtítulo destacado → detalle en texto pequeño."""
    return discord.Embed(title=title, description=text, color=color)


def boost_active(db, uid: int, kind: str) -> bool:
    """kind: 'xp' o 'coins'."""
    return db.get_stat(uid, f"boost_{kind}_until") > time.time()


def multiplier(db, uid: int, kind: str) -> int:
    return 2 if boost_active(db, uid, kind) else 1


def user_color(db, uid: int, default: int = config.COLOR_MAIN) -> int:
    item_id = db.get_user(uid)["color"]
    if item_id and item_id in ITEMS:
        return int(ITEMS[item_id]["value"], 16)
    return default


async def safe_send(channel, **kwargs):
    if channel is None:
        return
    try:
        await channel.send(**kwargs)
    except (discord.Forbidden, discord.HTTPException):
        pass


async def check_achievements(bot, member: discord.abc.User, channel=None) -> list[dict]:
    """Comprueba y desbloquea logros nuevos. Anuncia en `channel` si se pasa."""
    db = bot.db
    stats = db.get_stats(member.id)
    unlocked = db.get_achievements(member.id)
    new = []
    for ach in ACHIEVEMENTS:
        if ach["id"] in unlocked:
            continue
        if stats.get(ach["stat"], 0) >= ach["goal"]:
            if db.unlock_achievement(member.id, ach["id"]):
                db.add_coins(member.id, ach["reward"])
                new.append(ach)
    if new and channel is not None:
        lines = [f"{a['emoji']} **{a['name']}** — {a['desc']}  (+{fmt(a['reward'])})" for a in new]
        embed = discord.Embed(
            title="🏅 ¡Logro desbloqueado!" if len(new) == 1 else f"🏅 ¡{len(new)} logros desbloqueados!",
            description=f"{member.mention}\n" + "\n".join(lines),
            color=0xF1C40F,
        )
        await safe_send(channel, embed=embed)
    return new


async def grant_xp(bot, member: discord.abc.User, amount: int, channel=None):
    """Da XP, gestiona subidas de nivel (con premios) y comprueba logros."""
    db = bot.db
    amount = int(amount * multiplier(db, member.id, "xp"))
    level, gained = db.add_xp(member.id, amount)
    if gained:
        reward_coins = 0
        boxes = 0
        for lvl in range(level - gained + 1, level + 1):
            reward_coins += lvl * 50
            if lvl % 5 == 0:
                boxes += 1
        db.add_coins(member.id, reward_coins)
        extra = ""
        if boxes:
            db.add_item(member.id, "caja_rara", boxes)
            extra = f"\n🎁 ¡Y te llevas **{boxes}x Caja Rara** por llegar a un nivel múltiplo de 5!"
        embed = discord.Embed(
            description=f"🎉 {member.mention} ha subido a **nivel {level}** (+{fmt(reward_coins)}){extra}",
            color=config.COLOR_MAIN,
        )
        await safe_send(channel, embed=embed)
    await check_achievements(bot, member, channel)


def record_game(db, uid: int, won: bool):
    db.incr_stat(uid, "games_played")
    if won:
        db.incr_stat(uid, "games_won")


async def take_bet(interaction: discord.Interaction, amount: int) -> bool:
    """Cobra la apuesta por adelantado. Si no hay saldo, responde con error."""
    db = interaction.client.db
    if not db.remove_coins(interaction.user.id, amount):
        coins = db.get_coins(interaction.user.id)
        await interaction.response.send_message(
            embed=error_embed(f"No tienes suficientes monedas. Tienes {fmt(coins)}."), ephemeral=True
        )
        return False
    return True
