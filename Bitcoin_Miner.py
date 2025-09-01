#!/usr/bin/env python3
"""
Coin minor game (totally-not-real Bitcoin) — made with tkinter
Single file. No external assets. Python 3.9+ recommended.

Features
- Click Mine to discover coins of varying rarities with different values
- Buy assets (hitarthss, nirvanss, Farms, Quantum rigs, aanshs) for auto-mining
- Upgrades: Luck Booster (rarer drops) & Power Upgrade (coin value multiplier)
- Inventory + Sell Coins to convert to balance = 🤑
- Save/Load to save.json

Tip: Keep this fun & educational. It's fake crypto money, ITS FAKE NOT REAL VALUE
"""
import json
import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass, asdict, field

# --------------------------- Game Data --------------------------- #
RARITIES = [
    {"name": "Common",     "weight": 75.0,   "base_value": 1},
    {"name": "Uncommon",   "weight": 18.0,   "base_value": 5},
    {"name": "Rare",       "weight": 5.0,    "base_value": 25},
    {"name": "Epic",       "weight": 1.5,    "base_value": 100},
    {"name": "Legendary",  "weight": 0.4,    "base_value": 400},
    {"name": "Mythic",     "weight": 0.09,   "base_value": 2000},
    {"name": "Satoshi",    "weight": 0.01,   "base_value": 10000},
]

ASSETS = [
    {
        "key": "toa",
        "name": "Toaster Miner",
        "base_cost": 250,
        "cost_mult": 1.15,
        "per_sec": 0.8,
        "desc": "+0.8 mines/sec"
    },
    {
        "key": "hit",
        "name": "Hitarth Miner",
        "base_cost": 1500,
        "cost_mult": 1.17,
        "per_sec": 3.5,
        "desc": "+3.5 mines/sec"
    },
    {
        "key": "shl",
        "name": "Nirvan Miner",
        "base_cost": 8000,
        "cost_mult": 1.20,
        "per_sec": 15,
        "desc": "+15 mines/sec"
    },
    {
        "key": "aansh",
        "name": "Aansh Miner",
        "base_cost": 120000,
        "cost_mult": 1.25,
        "per_sec": 120,
        "desc": "+120 mines/sec (woah)"
    },
]

UPGRADES = [
    {
        "key": "luck",
        "name": "Luck Booster",
        "base_cost": 2000,
        "cost_mult": 2.2,
        "desc": "Rarer drops (+15% effective luck each level)",
        "effect_per_level": 0.15,
    },
    {
        "key": "power",
        "name": "Power Upgrade",
        "base_cost": 3000,
        "cost_mult": 2.4,
        "desc": "Increase coin value (+10% each level)",
        "effect_per_level": 0.10,
    },
]

SAVE_FILE_DEFAULT = "save.json"
TICK_MS = 100  # 10 ticks/sec

# --------------------------- Helpers --------------------------- #

def weighted_choice(entries, weight_key="weight"):
    total = sum(e[weight_key] for e in entries)
    r = random.random() * total
    upto = 0.0
    for e in entries:
        upto += e[weight_key]
        if upto >= r:
            return e
    return entries[-1]


def format_money(x):
    # Compact number formatting
    for unit in ["", "K", "M", "B", "T", "Q"]:
        if abs(x) < 1000:
            return f"{x:,.0f}{unit}"
        x /= 1000
    return f"{x:.1f}Q+"

# --------------------------- Data Model --------------------------- #

@dataclass
class GameState:
    balance: float = 0.0
    inventory: dict = field(default_factory=lambda: {r["name"]: 0 for r in RARITIES})
    assets: dict = field(default_factory=lambda: {a["key"]: 0 for a in ASSETS})
    upgrades: dict = field(default_factory=lambda: {u["key"]: 0 for u in UPGRADES})
    mines_per_click: float = 1.0
    mines_buffer: float = 0.0  # accumulates from auto mining between rolls
    total_mined: float = 0.0
    created_at: float = field(default_factory=time.time)
    last_tick: float = field(default_factory=time.time)

    def total_mines_per_sec(self) -> float:
        rate = 0.0
        for a in ASSETS:
            owned = self.assets.get(a["key"], 0)
            rate += owned * a["per_sec"]
        return rate

    def luck_multiplier(self) -> float:
        lvl = self.upgrades.get("luck", 0)
        return 1.0 + lvl * next(u for u in UPGRADES if u["key"] == "luck")["effect_per_level"]

    def value_multiplier(self) -> float:
        lvl = self.upgrades.get("power", 0)
        return 1.0 + lvl * next(u for u in UPGRADES if u["key"] == "power")["effect_per_level"]

# --------------------------- Core Logic --------------------------- #

class CryptoMinerGame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.state = GameState()
        self.random = random.Random()

        self._build_ui()
        self._schedule_tick()
        self._update_all_labels()

    # ----- UI ----- #
    def _build_ui(self):
        self.master.title("Crypto Miner Tycoon — totally-not-real BTC")
        self.master.minsize(980, 560)
        self.grid(sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Top bar
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        top.columnconfigure(4, weight=1)

        self.balance_var = tk.StringVar()
        ttk.Label(top, textvariable=self.balance_var, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=8)

        self.rate_var = tk.StringVar()
        ttk.Label(top, textvariable=self.rate_var).grid(row=0, column=1, padx=8)

        self.mined_var = tk.StringVar()
        ttk.Label(top, textvariable=self.mined_var).grid(row=0, column=2, padx=8)

        ttk.Button(top, text="Save", command=self.save).grid(row=0, column=5, padx=4)
        ttk.Button(top, text="Load", command=self.load).grid(row=0, column=6, padx=4)
        ttk.Button(top, text="Reset", command=self.reset_confirm).grid(row=0, column=7, padx=4)

        # Main columns
        main = ttk.Frame(self)
        main.grid(row=1, column=0, sticky="nsew")
        for c in range(3):
            main.columnconfigure(c, weight=1)
        main.rowconfigure(1, weight=1)

        # Left: Mining
        mine_card = ttk.LabelFrame(main, text="Mining")
        mine_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=8)
        mine_card.columnconfigure(0, weight=1)

        self.mine_result = tk.StringVar(value="Click MINE to start digging for coins!")
        ttk.Label(mine_card, textvariable=self.mine_result, wraplength=260, justify="center").grid(row=0, column=0, padx=8, pady=8)

        self.mine_btn = ttk.Button(mine_card, text="⛏️  MINE", command=self.mine_click)
        self.mine_btn.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.sell_btn = ttk.Button(mine_card, text="💰 Sell Coins", command=self.sell_all)
        self.sell_btn.grid(row=2, column=0, padx=8, pady=(0,10), sticky="ew")

        inv_card = ttk.LabelFrame(mine_card, text="Inventory (Coins)")
        inv_card.grid(row=3, column=0, sticky="nsew", padx=8, pady=8)
        inv_card.columnconfigure(0, weight=1)
        self.inventory_box = tk.Listbox(inv_card, height=10)
        self.inventory_box.grid(row=0, column=0, sticky="nsew")

        # Middle: Shop — Assets
        shop_assets = ttk.LabelFrame(main, text="Shop — Assets (Auto-Mining)")
        shop_assets.grid(row=0, column=1, sticky="nsew", padx=10, pady=8)
        shop_assets.columnconfigure(1, weight=1)

        self.asset_rows = {}
        for i, a in enumerate(ASSETS):
            name_lbl = ttk.Label(shop_assets, text=a["name"])
            name_lbl.grid(row=i, column=0, sticky="w", padx=6, pady=3)

            info_var = tk.StringVar()
            info_lbl = ttk.Label(shop_assets, textvariable=info_var)
            info_lbl.grid(row=i, column=1, sticky="w")

            btn = ttk.Button(shop_assets, text="Buy", command=lambda key=a["key"]: self.buy_asset(key))
            btn.grid(row=i, column=2, padx=6)
            self.asset_rows[a["key"]] = (info_var, btn)

        # Middle bottom: Upgrades
        shop_up = ttk.LabelFrame(main, text="Upgrades")
        shop_up.grid(row=1, column=1, sticky="nsew", padx=10, pady=8)
        shop_up.columnconfigure(1, weight=1)

        self.upgrade_rows = {}
        for i, u in enumerate(UPGRADES):
            name_lbl = ttk.Label(shop_up, text=u["name"])
            name_lbl.grid(row=i, column=0, sticky="w", padx=6, pady=3)

            info_var = tk.StringVar()
            info_lbl = ttk.Label(shop_up, textvariable=info_var)
            info_lbl.grid(row=i, column=1, sticky="w")

            btn = ttk.Button(shop_up, text="Buy", command=lambda key=u["key"]: self.buy_upgrade(key))
            btn.grid(row=i, column=2, padx=6)
            self.upgrade_rows[u["key"]] = (info_var, btn)

        # Right: Info
        info_card = ttk.LabelFrame(main, text="Info")
        info_card.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=8)
        info_card.columnconfigure(0, weight=1)

        self.info_text = tk.Text(info_card, height=20, width=40, wrap="word")
        self.info_text.grid(row=0, column=0, sticky="nsew")
        self._write_info()

        # Status bar
        self.status_var = tk.StringVar(value="Welcome!")
        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.grid(row=2, column=0, sticky="ew", padx=10, pady=(0,8))

        # Nice padding
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

    def _write_info(self):
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END,
            "This is a purely-for-fun idle/clicker game.\n\n"
            "• Click MINE to roll for a coin. Rarer coins are worth more.\n"
            "• Buy Assets for auto-mining (mines/sec).\n"
            "• Luck Booster increases odds of rarer coins.\n"
            "• Power Upgrade increases the value of all coins.\n"
            "• Sell Coins converts inventory to balance, used to buy more stuff.\n"
            "• Save/Load keeps your progress in save.json.\n\n"
            "None of this is real cryptocurrency — it's just a game. Have fun!"
        )
        self.info_text.configure(state="disabled")

    # ----- Game Mechanics ----- #
    def roll_coin(self, mines: float = 1.0):
        """Perform a coin drop roll for a given number of mines (clicks)."""
        # Effective luck weights: multiply weights by luck multiplier, but only for rarities except Common.
        luck = self.state.luck_multiplier()
        entries = []
        for r in RARITIES:
            w = r["weight"]
            if r["name"] != "Common":
                w *= luck
            entries.append({**r, "weight": w})

        # Roll once per whole mine
        drops = []
        whole = int(mines)
        for _ in range(whole):
            coin = weighted_choice(entries)
            drops.append(coin)
        return drops

    def grant_drops(self, drops):
        for coin in drops:
            self.state.inventory[coin["name"]] += 1
        if drops:
            last = drops[-1]
            self.mine_result.set(f"Found {len(drops)} coin(s)! Last: {last['name']}")
            self.status_var.set(f"Inventory updated. Total coins: {sum(self.state.inventory.values())}")
        self.refresh_inventory_box()
        self._update_all_labels()

    def mine_click(self):
        self.state.total_mined += self.state.mines_per_click
        drops = self.roll_coin(self.state.mines_per_click)
        self.grant_drops(drops)

    def auto_mine_tick(self, dt_sec: float):
        per_sec = self.state.total_mines_per_sec()
        gain = per_sec * dt_sec
        self.state.mines_buffer += gain
        whole = int(self.state.mines_buffer)
        if whole > 0:
            self.state.total_mined += whole
            drops = self.roll_coin(whole)
            self.grant_drops(drops)
            self.state.mines_buffer -= whole

    def coins_value(self) -> float:
        mult = self.state.value_multiplier()
        total = 0.0
        for r in RARITIES:
            count = self.state.inventory.get(r["name"], 0)
            total += count * r["base_value"] * mult
        return total

    def sell_all(self):
        value = self.coins_value()
        if value <= 0:
            self.status_var.set("You have no coins to sell.")
            return
        for r in RARITIES:
            self.state.inventory[r["name"]] = 0
        self.state.balance += value
        self.status_var.set(f"Sold all coins for {format_money(value)} ⓑ.")
        self.refresh_inventory_box()
        self._update_all_labels()

    # ----- Shop ----- #
    def asset_cost(self, key: str) -> float:
        a = next(x for x in ASSETS if x["key"] == key)
        owned = self.state.assets.get(key, 0)
        return a["base_cost"] * (a["cost_mult"] ** owned)

    def buy_asset(self, key: str):
        cost = self.asset_cost(key)
        if self.state.balance >= cost:
            self.state.balance -= cost
            self.state.assets[key] += 1
            a = next(x for x in ASSETS if x["key"] == key)
            self.status_var.set(f"Bought {a['name']} for {format_money(cost)} ⓑ.")
            self._update_all_labels()
        else:
            self.status_var.set("Not enough balance.")

    def upgrade_cost(self, key: str) -> float:
        u = next(x for x in UPGRADES if x["key"] == key)
        lvl = self.state.upgrades.get(key, 0)
        return u["base_cost"] * (u["cost_mult"] ** lvl)

    def buy_upgrade(self, key: str):
        cost = self.upgrade_cost(key)
        if self.state.balance >= cost:
            self.state.balance -= cost
            self.state.upgrades[key] += 1
            u = next(x for x in UPGRADES if x["key"] == key)
            self.status_var.set(f"Bought {u['name']} (Lv.{self.state.upgrades[key]}) for {format_money(cost)} ⓑ.")
            self._update_all_labels()
        else:
            self.status_var.set("Not enough balance for upgrade.")

    # ----- UI Updates ----- #
    def refresh_inventory_box(self):
        self.inventory_box.delete(0, tk.END)
        mult = self.state.value_multiplier()
        for r in RARITIES:
            n = self.state.inventory.get(r["name"], 0)
            val_each = r["base_value"] * mult
            self.inventory_box.insert(tk.END, f"{r['name']}: {n}  (each worth {val_each:.0f})")

    def _update_all_labels(self):
        self.balance_var.set(f"Balance: {format_money(self.state.balance)} ⓑ")
        self.rate_var.set(f"Rate: {self.state.total_mines_per_sec():.1f} mines/sec")
        self.mined_var.set(f"Total Mines: {format_money(self.state.total_mined)}")

        # Update assets rows
        for a in ASSETS:
            key = a["key"]
            owned = self.state.assets.get(key, 0)
            cost = self.asset_cost(key)
            info_var, btn = self.asset_rows[key]
            info_var.set(f"Owned: {owned}  |  Cost: {format_money(cost)}  |  {a['desc']}")
            btn.state(["!disabled"]) if self.state.balance >= cost else btn.state(["disabled"])

        # Update upgrades rows
        for u in UPGRADES:
            key = u["key"]
            lvl = self.state.upgrades.get(key, 0)
            cost = self.upgrade_cost(key)
            info_var, btn = self.upgrade_rows[key]
            info_var.set(f"Lv.{lvl}  |  Cost: {format_money(cost)}  |  {u['desc']}")
            btn.state(["!disabled"]) if self.state.balance >= cost else btn.state(["disabled"])

        self.refresh_inventory_box()
    # ----- Loop ----- #
    def _schedule_tick(self):
        self.master.after(TICK_MS, self._tick)

    def _tick(self):
        now = time.time()
        dt = now - self.state.last_tick
        self.state.last_tick = now
        self.auto_mine_tick(dt)
        self._update_all_labels()
        self._schedule_tick()

    # ----- Save/Load/Reset ----- #
    def save(self):
        path = filedialog.asksaveasfilename(initialfile=SAVE_FILE_DEFAULT, defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        data = asdict(self.state)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.status_var.set(f"Saved to {os.path.basename(path)}")

    def load(self):
        path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Sanity merge
            s = GameState()
            s.__dict__.update({k: data.get(k, getattr(s, k)) for k in s.__dict__.keys()})
            # Ensure all keys exist
            for r in RARITIES:
                s.inventory.setdefault(r["name"], 0)
            for a in ASSETS:
                s.assets.setdefault(a["key"], 0)
            for u in UPGRADES:
                s.upgrades.setdefault(u["key"], 0)
            self.state = s
            self.status_var.set(f"Loaded {os.path.basename(path)}")
            self._update_all_labels()
        except Exception as e:
            messagebox.showerror("Load Failed", str(e))

    def reset_confirm(self):
        if messagebox.askyesno("Reset Game", "Are you sure you want to wipe your progress?"):
            self.state = GameState()
            self._update_all_labels()
            self.status_var.set("Game reset.")

# --------------------------- Run --------------------------- #

def main():
    root = tk.Tk()
    # High-DPI scaling on Windows
    try:
        if os.name == "nt":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = CryptoMinerGame(root)
    app.mainloop()

if __name__ == "__main__":
    main()
