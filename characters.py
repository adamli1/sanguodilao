import random

class Character:
    """角色基类"""
    def __init__(self, name, troops, strength, intelligence, agility):
        self.name = name
        self.max_troops = troops
        self.troops = troops
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.skills = []

    @property
    def is_alive(self):
        return self.troops > 0

class Hero(Character):
    """英雄类"""
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        self.exp = 0
        self.level = 1
        self.max_mp = 50 + 5 * intelligence
        self.mp = self.max_mp

    def level_up(self):
        """升级成长"""
        self.level += 1
        self.max_troops += 10
        self.strength += 2
        self.intelligence += 2
        self.agility += 1
        print(f"{self.name} 升级到 Lv{self.level}！")

class Enemy(Character):
    """敌人类"""
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        self.level = int(name.split("·Lv")[1]) if "·Lv" in name else 1