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
        self.base_max_troops = troops  # 新增基础兵力


    def level_up(self):
        """升级成长"""
        self.level += 1
        # 属性成长
        self.strength += 3
        self.intelligence += 2
        self.agility += 2
        self.base_max_troops += 50
        self.max_troops = self.base_max_troops
        self.troops = self.max_troops  # 升级时恢复全部兵力
        print(f"{self.name} 升级到 Lv{self.level}！")

    def add_exp(self, amount):
        """获得经验"""
        self.exp += amount
        print(f"{self.name} 获得 {amount} 经验值")
        while self.exp >= self.required_exp():
            self.exp -= self.required_exp()
            self.level_up()
    
    def required_exp(self):
        """升级所需经验公式"""
        return 100 * (2 ** (self.level - 1))
    
class Enemy(Character):
    """敌人类"""
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        self.level = int(name.split("·Lv")[1]) if "·Lv" in name else 1