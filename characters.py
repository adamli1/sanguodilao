import random

class Character:
    """角色基类"""
    def __init__(self, name, troops, strength, intelligence, agility, skills=None, level=3):
        self.name = name
        self.level = level
        self.base_max_troops = self.level * 100  # 基础值统一计算
        self.troop_bonus = 0  # 额外加成
        self.troops = min(troops, self.max_troops)  # 当前兵力
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.skills = skills or []
        self.exp = 0

    @property
    def max_troops(self):
        return self.base_max_troops + self.troop_bonus

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
        self.base_max_troops = self.level * 100  # 升级时更新基础值
        self.troops = min(self.troops, self.max_troops)  # 保持不超过上限
        self.strength += 2
        self.agility += 1
        self.intelligence += 1

    def required_exp(self):
        return 100 * self.level

class Hero(Character):
    """英雄类"""
    def __init__(self, name, troops, strength, intelligence, agility, rarity="R"):
        super().__init__(name, troops, strength, intelligence, agility)
        self.rarity = rarity  # 新增稀有度属性
        self.exp = 0
        self.level = 3
        self.base_max_troops = self.level * 100  # 确保英雄也遵守统一规则
        self.troops = self.max_troops  # 初始化时补满

    def level_up(self):
        """英雄升级需要同时处理等级和基础值"""
        super().level_up()  # 调用父类level_up方法
        # 英雄额外属性成长
        self.strength += 3
        self.intelligence += 2
        self.agility += 2
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