import random

class Character:
    """角色基类"""
    def __init__(self, name, troops, strength, intelligence, agility, skills=None, level=3):
        self.name = name
        self.level = level
        self.max_troops = self.level * 100  # 动态计算
        self.troops = min(troops, self.max_troops)  # 确保不超过上限
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.skills = skills or []
        self.exp = 0

    @property
    def is_alive(self):
        return self.troops > 0

    def add_exp(self, exp):
        self.exp += exp
        while self.exp >= self.required_exp():
            self.exp -= self.required_exp()
            self.level_up()
    
    def level_up(self):
        self.level += 1
        prev_max = self.max_troops
        self.max_troops = self.level * 100  # 更新上限
        self.troops += (self.max_troops - prev_max)  # 保持兵力差值
        self.strength += 2
        self.agility += 1
        self.intelligence += 1

    def required_exp(self):
        return 100 * self.level

class Hero(Character):
    """英雄类"""
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        self.exp = 0
        self.level = 3
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