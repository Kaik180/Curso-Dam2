"""Capa de base de datos (SQLite) del bot."""
import os
import sqlite3
import time

import config


class Database:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id    INTEGER PRIMARY KEY,
                coins      INTEGER NOT NULL DEFAULT 0,
                xp         INTEGER NOT NULL DEFAULT 0,
                level      INTEGER NOT NULL DEFAULT 0,
                bio        TEXT,
                color      TEXT,
                title      TEXT,
                badge      TEXT,
                daily_last TEXT,
                created_at REAL NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS stats (
                user_id INTEGER NOT NULL,
                key     TEXT    NOT NULL,
                value   INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, key)
            );
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER NOT NULL,
                item_id TEXT    NOT NULL,
                qty     INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, item_id)
            );
            CREATE TABLE IF NOT EXISTS achievements (
                user_id     INTEGER NOT NULL,
                ach_id      TEXT    NOT NULL,
                unlocked_at REAL    NOT NULL,
                PRIMARY KEY (user_id, ach_id)
            );
            CREATE TABLE IF NOT EXISTS user_pets (
                pet_uid     INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                species_id  TEXT    NOT NULL,
                nickname    TEXT,
                level       INTEGER NOT NULL DEFAULT 1,
                xp          INTEGER NOT NULL DEFAULT 0,
                held_item   TEXT,
                stars       INTEGER NOT NULL DEFAULT 0,
                extra_skill TEXT,
                team_slot   INTEGER NOT NULL DEFAULT 0,
                is_active   INTEGER NOT NULL DEFAULT 0,
                caught_at   REAL    NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS trobidex (
                user_id    INTEGER NOT NULL,
                species_id TEXT    NOT NULL,
                first_at   REAL    NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, species_id)
            );
            CREATE TABLE IF NOT EXISTS processed_interactions (
                interaction_id INTEGER PRIMARY KEY,
                created_at     REAL NOT NULL
            );
            """
        )
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(user_pets)")}
        if "held_item" not in cols:
            self.conn.execute("ALTER TABLE user_pets ADD COLUMN held_item TEXT")
        if "stars" not in cols:
            self.conn.execute("ALTER TABLE user_pets ADD COLUMN stars INTEGER NOT NULL DEFAULT 0")
        if "extra_skill" not in cols:
            self.conn.execute("ALTER TABLE user_pets ADD COLUMN extra_skill TEXT")
        if "team_slot" not in cols:
            self.conn.execute("ALTER TABLE user_pets ADD COLUMN team_slot INTEGER NOT NULL DEFAULT 0")
            self.conn.execute("UPDATE user_pets SET team_slot = 1 WHERE is_active = 1 AND team_slot = 0")
        self.conn.commit()

    # ------------------------------------------------------------------ users
    def ensure_user(self, uid: int):
        self.conn.execute(
            "INSERT OR IGNORE INTO users (user_id, coins, created_at) VALUES (?, ?, ?)",
            (uid, config.STARTING_COINS, time.time()),
        )
        self.conn.commit()

    def get_user(self, uid: int) -> dict:
        self.ensure_user(uid)
        row = self.conn.execute("SELECT * FROM users WHERE user_id = ?", (uid,)).fetchone()
        return dict(row)

    _PROFILE_FIELDS = {"bio", "color", "title", "badge", "daily_last"}

    def set_field(self, uid: int, field: str, value):
        if field not in self._PROFILE_FIELDS:
            raise ValueError(f"Campo no permitido: {field}")
        self.ensure_user(uid)
        self.conn.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, uid))
        self.conn.commit()

    # ------------------------------------------------------------------ coins
    def get_coins(self, uid: int) -> int:
        return self.get_user(uid)["coins"]

    def add_coins(self, uid: int, amount: int):
        self.ensure_user(uid)
        self.conn.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (int(amount), uid))
        self.conn.commit()

    def remove_coins(self, uid: int, amount: int) -> bool:
        """Resta monedas solo si hay saldo suficiente. Devuelve True si se pudo."""
        self.ensure_user(uid)
        cur = self.conn.execute(
            "UPDATE users SET coins = coins - ? WHERE user_id = ? AND coins >= ?",
            (int(amount), uid, int(amount)),
        )
        self.conn.commit()
        return cur.rowcount == 1

    # --------------------------------------------------------------------- xp
    @staticmethod
    def xp_needed(level: int) -> int:
        return 5 * level * level + 50 * level + 100

    def add_xp(self, uid: int, amount: int) -> tuple[int, int]:
        """Añade XP. Devuelve (nivel_actual, niveles_subidos)."""
        user = self.get_user(uid)
        xp, level = user["xp"] + int(amount), user["level"]
        gained = 0
        while xp >= self.xp_needed(level):
            xp -= self.xp_needed(level)
            level += 1
            gained += 1
        self.conn.execute("UPDATE users SET xp = ?, level = ? WHERE user_id = ?", (xp, level, uid))
        self.conn.commit()
        return level, gained

    # ------------------------------------------------------------------ stats
    def get_stat(self, uid: int, key: str) -> int:
        row = self.conn.execute(
            "SELECT value FROM stats WHERE user_id = ? AND key = ?", (uid, key)
        ).fetchone()
        return row["value"] if row else 0

    def incr_stat(self, uid: int, key: str, amount: int = 1):
        self.conn.execute(
            """INSERT INTO stats (user_id, key, value) VALUES (?, ?, ?)
               ON CONFLICT(user_id, key) DO UPDATE SET value = value + excluded.value""",
            (uid, key, int(amount)),
        )
        self.conn.commit()

    def set_stat(self, uid: int, key: str, value: int):
        self.conn.execute(
            """INSERT INTO stats (user_id, key, value) VALUES (?, ?, ?)
               ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value""",
            (uid, key, int(value)),
        )
        self.conn.commit()

    def max_stat(self, uid: int, key: str, value: int):
        self.conn.execute(
            """INSERT INTO stats (user_id, key, value) VALUES (?, ?, ?)
               ON CONFLICT(user_id, key) DO UPDATE SET value = MAX(value, excluded.value)""",
            (uid, key, int(value)),
        )
        self.conn.commit()

    def get_stats(self, uid: int) -> dict:
        user = self.get_user(uid)
        stats = {r["key"]: r["value"] for r in self.conn.execute(
            "SELECT key, value FROM stats WHERE user_id = ?", (uid,)
        )}
        stats["coins"] = user["coins"]
        stats["level"] = user["level"]
        dex_row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM trobidex WHERE user_id = ?", (uid,)
        ).fetchone()
        stats["trobidex"] = dex_row["c"] if dex_row else 0
        return stats

    # -------------------------------------------------------------- inventory
    def get_inventory(self, uid: int) -> dict:
        return {r["item_id"]: r["qty"] for r in self.conn.execute(
            "SELECT item_id, qty FROM inventory WHERE user_id = ? AND qty > 0", (uid,)
        )}

    def item_qty(self, uid: int, item_id: str) -> int:
        row = self.conn.execute(
            "SELECT qty FROM inventory WHERE user_id = ? AND item_id = ?", (uid, item_id)
        ).fetchone()
        return row["qty"] if row else 0

    def add_item(self, uid: int, item_id: str, qty: int = 1):
        self.conn.execute(
            """INSERT INTO inventory (user_id, item_id, qty) VALUES (?, ?, ?)
               ON CONFLICT(user_id, item_id) DO UPDATE SET qty = qty + excluded.qty""",
            (uid, item_id, int(qty)),
        )
        self.conn.commit()

    def remove_item(self, uid: int, item_id: str, qty: int = 1) -> bool:
        cur = self.conn.execute(
            "UPDATE inventory SET qty = qty - ? WHERE user_id = ? AND item_id = ? AND qty >= ?",
            (int(qty), uid, item_id, int(qty)),
        )
        self.conn.execute("DELETE FROM inventory WHERE qty <= 0")
        self.conn.commit()
        return cur.rowcount == 1

    # ----------------------------------------------------------- achievements
    def get_achievements(self, uid: int) -> dict:
        return {r["ach_id"]: r["unlocked_at"] for r in self.conn.execute(
            "SELECT ach_id, unlocked_at FROM achievements WHERE user_id = ?", (uid,)
        )}

    def unlock_achievement(self, uid: int, ach_id: str) -> bool:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO achievements (user_id, ach_id, unlocked_at) VALUES (?, ?, ?)",
            (uid, ach_id, time.time()),
        )
        self.conn.commit()
        return cur.rowcount == 1

    # ------------------------------------------------------------ leaderboard
    def leaderboard(self, kind: str, limit: int = 10) -> list[dict]:
        bot_uid = int(config.APPLICATION_ID or 0)
        if kind == "nivel":
            sql = "SELECT user_id, level, xp, coins FROM users WHERE user_id != ? ORDER BY level DESC, xp DESC LIMIT ?"
        else:
            sql = "SELECT user_id, level, xp, coins FROM users WHERE user_id != ? ORDER BY coins DESC LIMIT ?"
        return [dict(r) for r in self.conn.execute(sql, (bot_uid, limit))]

    def coin_rank(self, uid: int) -> int:
        self.ensure_user(uid)
        bot_uid = int(config.APPLICATION_ID or 0)
        row = self.conn.execute(
            "SELECT COUNT(*) + 1 AS pos FROM users WHERE user_id != ? AND coins > (SELECT coins FROM users WHERE user_id = ?)",
            (bot_uid, uid),
        ).fetchone()
        return row["pos"]

    # --------------------------------------------------------- pets / trobidex
    def register_trobidex(self, uid: int, species_id: str) -> bool:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO trobidex (user_id, species_id, first_at) VALUES (?, ?, ?)",
            (uid, species_id, time.time()),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def get_trobidex(self, uid: int) -> set[str]:
        return {
            r["species_id"]
            for r in self.conn.execute("SELECT species_id FROM trobidex WHERE user_id = ?", (uid,))
        }

    def add_pet(self, uid: int, species_id: str, level: int = 1) -> tuple[dict, bool]:
        self.ensure_user(uid)
        has_active = self.get_active_pet(uid) is not None
        is_active = 0 if has_active else 1
        cur = self.conn.execute(
            """INSERT INTO user_pets (user_id, species_id, level, xp, is_active, caught_at)
               VALUES (?, ?, ?, 0, ?, ?)""",
            (uid, species_id, int(level), is_active, time.time()),
        )
        pet_uid = cur.lastrowid
        self.conn.commit()
        is_new_dex = self.register_trobidex(uid, species_id)
        return self.get_pet(uid, pet_uid), is_new_dex

    def get_pets(self, uid: int) -> list[dict]:
        return [
            dict(r)
            for r in self.conn.execute(
                "SELECT * FROM user_pets WHERE user_id = ? ORDER BY is_active DESC, stars DESC, level DESC, pet_uid ASC",
                (uid,),
            )
        ]

    def get_pet(self, uid: int, pet_uid: int) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM user_pets WHERE user_id = ? AND pet_uid = ?",
            (uid, int(pet_uid)),
        ).fetchone()
        return dict(row) if row else None

    def get_active_pet(self, uid: int) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM user_pets WHERE user_id = ? AND is_active = 1 LIMIT 1",
            (uid,),
        ).fetchone()
        if not row:
            row = self.conn.execute(
                "SELECT * FROM user_pets WHERE user_id = ? ORDER BY stars DESC, level DESC, pet_uid ASC LIMIT 1",
                (uid,),
            ).fetchone()
            if row:
                self.set_active_pet(uid, row["pet_uid"])
                return dict(row) | {"is_active": 1}
        return dict(row) if row else None

    def set_active_pet(self, uid: int, pet_uid: int) -> bool:
        pet = self.get_pet(uid, pet_uid)
        if not pet:
            return False
        self.conn.execute("UPDATE user_pets SET is_active = 0 WHERE user_id = ?", (uid,))
        self.conn.execute("UPDATE user_pets SET team_slot = 0 WHERE user_id = ? AND team_slot = 1", (uid,))
        self.conn.execute(
            "UPDATE user_pets SET is_active = 1, team_slot = 1 WHERE user_id = ? AND pet_uid = ?",
            (uid, int(pet_uid)),
        )
        self.conn.commit()
        return True

    def set_team_slot(self, uid: int, slot: int, pet_uid: int | None) -> bool:
        if slot not in (1, 2, 3):
            return False
        if pet_uid is not None:
            pet = self.get_pet(uid, pet_uid)
            if not pet:
                return False
            self.conn.execute(
                "UPDATE user_pets SET team_slot = 0, is_active = CASE WHEN team_slot = 1 THEN 0 ELSE is_active END WHERE user_id = ? AND (team_slot = ? OR pet_uid = ?)",
                (uid, int(slot), int(pet_uid)),
            )
            is_act = 1 if slot == 1 else 0
            if slot == 1:
                self.conn.execute("UPDATE user_pets SET is_active = 0 WHERE user_id = ?", (uid,))
            self.conn.execute(
                "UPDATE user_pets SET team_slot = ?, is_active = CASE WHEN ? = 1 THEN 1 ELSE is_active END WHERE user_id = ? AND pet_uid = ?",
                (int(slot), is_act, uid, int(pet_uid)),
            )
        else:
            if slot == 1:
                return False
            self.conn.execute(
                "UPDATE user_pets SET team_slot = 0 WHERE user_id = ? AND team_slot = ?",
                (uid, int(slot)),
            )
        self.conn.commit()
        return True

    def get_team(self, uid: int, auto_fill: bool = True) -> list[dict]:
        """Devuelve el equipo de hasta 3 Trobimons del usuario ordenado por puesto (1, 2, 3)."""
        all_pets = self.get_pets(uid)
        if not all_pets:
            return []
        by_slot: dict[int, dict] = {}
        for p in all_pets:
            s = int(p.get("team_slot") or 0)
            if s in (1, 2, 3) and s not in by_slot:
                by_slot[s] = p
        if 1 not in by_slot:
            active = self.get_active_pet(uid)
            if active:
                by_slot[1] = active
        if auto_fill:
            used_ids = {p["pet_uid"] for p in by_slot.values()}
            for s in (1, 2, 3):
                if s not in by_slot:
                    for p in all_pets:
                        if p["pet_uid"] not in used_ids:
                            by_slot[s] = p
                            used_ids.add(p["pet_uid"])
                            break
        return [by_slot[s] for s in (1, 2, 3) if s in by_slot]

    def rename_pet(self, uid: int, pet_uid: int, nickname: str | None):
        self.conn.execute(
            "UPDATE user_pets SET nickname = ? WHERE user_id = ? AND pet_uid = ?",
            (nickname, uid, int(pet_uid)),
        )
        self.conn.commit()

    def update_pet(self, uid: int, pet_uid: int, species_id: str, level: int, xp: int):
        self.conn.execute(
            "UPDATE user_pets SET species_id = ?, level = ?, xp = ? WHERE user_id = ? AND pet_uid = ?",
            (species_id, int(level), int(xp), uid, int(pet_uid)),
        )
        self.conn.commit()

    def set_pet_item(self, uid: int, pet_uid: int, item_id: str | None):
        self.conn.execute(
            "UPDATE user_pets SET held_item = ? WHERE user_id = ? AND pet_uid = ?",
            (item_id, uid, int(pet_uid)),
        )
        self.conn.commit()

    def set_pet_stars(self, uid: int, pet_uid: int, stars: int):
        self.conn.execute(
            "UPDATE user_pets SET stars = ? WHERE user_id = ? AND pet_uid = ?",
            (int(stars), uid, int(pet_uid)),
        )
        self.conn.commit()

    def set_pet_extra_skill(self, uid: int, pet_uid: int, skill_id: str | None):
        self.conn.execute(
            "UPDATE user_pets SET extra_skill = ? WHERE user_id = ? AND pet_uid = ?",
            (skill_id, uid, int(pet_uid)),
        )
        self.conn.commit()

    def delete_pet(self, uid: int, pet_uid: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM user_pets WHERE user_id = ? AND pet_uid = ?",
            (uid, int(pet_uid)),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def transfer_pet(self, from_uid: int, to_uid: int, pet_uid: int) -> bool:
        self.ensure_user(to_uid)
        cur = self.conn.execute(
            "UPDATE user_pets SET user_id = ?, is_active = 0 WHERE user_id = ? AND pet_uid = ?",
            (to_uid, from_uid, int(pet_uid)),
        )
        self.conn.commit()
        if cur.rowcount == 1:
            row = self.get_pet(to_uid, pet_uid)
            if row:
                self.register_trobidex(to_uid, row["species_id"])
            return True
        return False

    def claim_interaction(self, interaction_id: int) -> bool:
        """Garantiza atómicamente que cada interacción de Discord se procese exactamente 1 sola vez."""
        now = time.time()
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO processed_interactions (interaction_id, created_at) VALUES (?, ?)",
            (int(interaction_id), now),
        )
        if int(interaction_id) % 50 == 0:
            self.conn.execute("DELETE FROM processed_interactions WHERE created_at < ?", (now - 600,))
        self.conn.commit()
        return cur.rowcount == 1
