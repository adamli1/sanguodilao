"""
author: Yadong Li
version: 0.001
----------------------------
核心玩法验证目标：
1. 资源生产与建筑升级的数值平衡
2. 英雄探索与战斗的流程体验
3. 资源消耗与战斗收益的合理性
"""

# game.py
import random
import time

# 放在所有类定义之前

# 修改技能库（完全替换为三国主题四字技能）
SKILL_LIBRARY = {
    # UR级技能
    "qinglongyanyue": {
        "name": "青龙偃月",
        "base": 100,
        "coef": 2.0,
        "prob": 0.15,
        "scale": "strength",
        "target": "enemy"
    },
    "wushuang": {
        "name": "天下无双",
        "base": 120,
        "coef": 2.2,
        "prob": 0.1,
        "scale": "strength",
        "target": "enemy" 
    },
    
    # SSR级技能
    "qijinchu": {
        "name": "七进七出",
        "base": 80,
        "coef": 1.8,
        "prob": 0.2,
        "scale": "agility",
        "target": "enemy"
    },
    "nujing": {
    "name": "怒目金刚",
    "base": 75,
    "coef": 1.7,
    "prob": 0.2,
    "scale": "strength",
    "target": "enemy"
    },

    # SR级技能
    "bashidanjing": {
        "name": "拔矢啖睛",
        "base": 70,
        "coef": 1.5,
        "prob": 0.25,
        "scale": "strength",
        "target": "enemy"
    },
    
    # R级技能 
    "xunshan": {
        "name": "巡山探路",
        "base": 40,
        "coef": 0.8,
        "prob": 0.3,
        "scale": "agility",
        "target": "enemy"
    },
    
    # 更多技能...
    "kongchengji": {
        "name": "空城绝计",
        "base": 150,
        "coef": 3.0,
        "prob": 0.05,
        "scale": "intelligence",
        "target": "ally"
    },
    "huolaoxiang": {
        "name": "火烧连营",
        "base": 90,
        "coef": 1.6,
        "prob": 0.18,
        "scale": "intelligence",
        "target": "enemy"
    },
   
    # 敌人专属技能
    "looting": {
        "name": "劫掠四方",
        "base": 30,
        "coef": 0.5,
        "prob": 0.25,
        "scale": "strength",
        "target": "enemy"
    },
    "corrupt": {
        "name": "中饱私囊",
        "base": 50,
        "coef": 1.2,
        "prob": 0.3,
        "scale": "intelligence",
        "target": "ally"
    },
    "swarm": {
        "name": "人海战术",
        "base": 20,
        "coef": 0.3,
        "prob": 0.4,
        "scale": "agility",
        "target": "enemy"
    }
}

# 扩展三国英雄池（示例30个）
HERO_POOL = {
    "UR": [
        {
            "name": "关羽",
            "troops": 400,
            "strength": 55,
            "intelligence": 35,
            "agility": 30,
            "skill": "qinglongyanyue",
            "intro": "温酒斩华雄，千里走单骑"
        },
        {
            "name": "吕布",
            "troops": 450,
            "strength": 60,
            "intelligence": 25,
            "agility": 40,
            "skill": "wushuang",
            "intro": "三英战吕布，辕门射戟"
        }
    ],
    "SSR": [
        {
            "name": "赵云",
            "troops": 350,
            "strength": 45,
            "intelligence": 40,
            "agility": 50,
            "skill": "qijinchu",
            "intro": "长坂坡七进七出救阿斗"
        },
        {
            "name": "典韦",
            "troops": 380,
            "strength": 58,
            "intelligence": 20,
            "agility": 35,
            "skill": "nujing",  # 需在SKILL_LIBRARY添加对应技能
            "intro": "古之恶来，护主捐躯"
        }
    ],
    "SR": [
        {
            "name": "夏侯惇",
            "troops": 280,
            "strength": 48,
            "intelligence": 30,
            "agility": 38,
            "skill": "bashidanjing",
            "intro": "拔矢啖睛，独目仍征战"
        }
    ],
    "R": [
        {
            "name": "廖化",
            "troops": 200,
            "strength": 35,
            "intelligence": 25,
            "agility": 30,
            "skill": "xunshan",
            "intro": "蜀中无大将，廖化作先锋"
        }
    ]
}

ENEMY_TEMPLATES = {
    "小兵": {
        "base": {
            "troops": 100,
            "strength": 20,
            "intelligence": 15,
            "agility": 18
        },
        "growth": {
            "troops": 20,
            "strength": 3,
            "intelligence": 2,
            "agility": 2
        },
        "skills": ["swarm"]
    },
    "贼将": {
        "base": {
            "troops": 80,
            "strength": 35,
            "intelligence": 10,
            "agility": 15
        },
        "growth": {
            "troops": 15,
            "strength": 5,
            "intelligence": 1,
            "agility": 3
        },
        "skills": ["looting"]
    },
    "贪官": {
        "base": {
            "troops": 70,
            "strength": 10,
            "intelligence": 30,
            "agility": 12
        },
        "growth": {
            "troops": 10,
            "strength": 1,
            "intelligence": 6,
            "agility": 1
        },
        "skills": ["corrupt"]
    }
}

# 稀有度概率（总和应<=1）
RARITY_PROB = {
    "UR": 0.05,
    "SSR": 0.15,
    "SR": 0.30,
    "R": 0.50
}

class Game:
    def __init__(self):
        # 初始资源
        self.resources = {
            "gold": 500,
            "wood": 1000,
            "food": 1500,
            "stone": 500
        }
        
        # 英雄队伍
        self.party = []
        
        # 探索进度
        self.explored_areas = 0       
        
        # 当前遭遇的敌人
        self.current_enemies = []  
        
        # 英雄系统重构
        self.city_heroes = []  # 城池中的所有英雄
        self.party = []        # 出战队伍（最多3人）
        self.materials = {}    # 材料卡（同名卡转换）

        # 建筑系统重构
        self.buildings = {
            "farm": {
                "level": 1,
                "base_cost": {"wood": 20, "stone": 10, "food": 30},
                "production": {"food": 10},
                "unlocked": True  # 初始已解锁
            },
            "lumber_camp": {
                "level": 0,
                "base_cost": {"wood": 30, "stone": 15},
                "production": {"wood": 8},
                "unlocked": True
            },
            "stone_quarry": {
                "level": 0,
                "base_cost": {"wood": 40, "stone": 20},
                "production": {"stone": 5},
                "unlocked": True
            },
            "gold_mine": {
                "level": 0,
                "base_cost": {"wood": 50, "stone": 30, "gold": 20},
                "production": {"gold": 7},
                "unlocked": False,
                "unlock_condition": {"lumber_camp": 2}  # 需要伐木场2级
            },
            "barracks": {
                "level": 0,
                "base_cost": {"wood": 60, "stone": 40},
                "unlocked": False,
                "unlock_condition": {"stone_quarry": 1, "gold_mine": 1}
            }
        }

    def show_hero_details(self):
            print("\n=== 英雄详情 ===")
            for hero in self.party:
                print(f"{hero.name} Lv{hero.level}")
                print(f"兵力: {hero.troops}/{hero.max_troops}")
                print(f"力量: {hero.strength} 智力: {hero.intelligence} 敏捷: {hero.agility}")
                print("技能：" + ", ".join([s["name"] for s in hero.skills]))
                print("----------------")

    def generate_enemies(self):
        """根据队伍等级生成敌人"""
        avg_level = sum(h.level for h in self.party)/len(self.party) if self.party else 1
        enemy_level = max(1, int(avg_level))
        
        # 随机生成敌人组合（示例组合）
        enemy_types = random.choice([
            ["小兵", "小兵"],
            ["小兵", "贼将"],
            ["贪官", "贼将"],
            ["贪官", "贪官", "小兵"]
        ])
        
        self.current_enemies = []
        for etype in enemy_types:
            template = ENEMY_TEMPLATES[etype]
            level = enemy_level
            
            # 计算成长后属性
            troops = template["base"]["troops"] + template["growth"]["troops"] * (level-1)
            strength = template["base"]["strength"] + template["growth"]["strength"] * (level-1)
            intelligence = template["base"]["intelligence"] + template["growth"]["intelligence"] * (level-1)
            agility = template["base"]["agility"] + template["growth"]["agility"] * (level-1)
            
            enemy = Enemy(
                name=f"{etype}·Lv{level}",
                troops=troops,
                strength=strength,
                intelligence=intelligence,
                agility=agility
            )
            
            # 添加技能
            for skill_key in template["skills"]:
                enemy.skills.append(SKILL_LIBRARY[skill_key])
            
            self.current_enemies.append(enemy)
    
    def manage_party(self):
        """管理出战队伍"""
        while True:
            print("\n=== 编队管理 ===")
            print("当前出战队伍（最多3人）：")
            for i, hero in enumerate(self.party, 1):
                print(f"{i}. {hero.name} (兵力: {hero.troops})")
            
            print("\n城池中的英雄：")
            for i, hero in enumerate(self.city_heroes, 1):
                print(f"{i+len(self.party)}. {hero.name} (兵力: {hero.troops})")
            
            print("\n操作：")
            print("a.添加英雄到队伍  r.从队伍移除  q.返回")
            choice = input("请选择操作：").lower()
            
            if choice == 'a':
                if len(self.party) >= 3:
                    print("❌ 出战队伍已满！")
                    continue
                    
                available = [h for h in self.city_heroes if h not in self.party]
                if not available:
                    print("❌ 没有可添加的英雄")
                    continue
                    
                print("选择要添加的英雄：")
                for i, h in enumerate(available, 1):
                    print(f"{i}. {h.name}（兵力：{h.troops}）")
                    
                try:
                    idx = int(input("请输入编号：")) - 1
                    selected = available[idx]
                    self.party.append(selected)
                    print(f"✅ {selected.name} 已加入出战队伍！")
                except:
                    print("❌ 无效输入")
                    
            elif choice == 'r':
                if not self.party:
                    print("❌ 出战队伍为空")
                    continue
                    
                print("选择要移除的英雄：")
                for i, h in enumerate(self.party, 1):
                    print(f"{i}. {h.name}")
                    
                try:
                    idx = int(input("请输入编号：")) - 1
                    removed = self.party.pop(idx)
                    print(f"✅ {removed.name} 已移除出队伍")
                except:
                    print("❌ 无效输入")
                    
            elif choice == 'q':
                break
    
    def check_unlocks(self):
        """检查所有建筑的解锁条件"""
        for building_name, data in self.buildings.items():
            # 如果已经解锁则跳过
            if data.get("unlocked", False):
                continue
            
            # 检查解锁条件是否满足
            required = data.get("unlock_condition", {})
            meet_condition = True
            for req_building, req_level in required.items():
                if self.buildings[req_building]["level"] < req_level:
                    meet_condition = False
                    break
            
            if meet_condition and required:
                data["unlocked"] = True
                print(f"\n[系统] 新建筑已解锁：{building_name}！")

    def show_status(self):
        """显示当前状态"""
        print(f"\n=== 当前资源 ===")
        print(" | ".join([f"{k}:{v}" for k, v in self.resources.items()]))
        
        print("\n=== 材料卡 ===")
        if self.materials:
            print(" ".join([f"{k}x{v}" for k, v in self.materials.items()]))
        else:
            print("无")

        print("\n=== 建筑状态 ===")
        building_status = []
        for name, data in self.buildings.items():
            prod_str = ""
            if "production" in data:
                prod_str = "->" + " ".join([f"+{v*data['level']}{k}" for k,v in data["production"].items()])
            building_status.append(f"{name}(Lv{data['level']}){prod_str}")
        print("\n".join(building_status))
        print(f"\n=== 英雄队伍 ===")
        print("无" if not self.party else "\n".join([f"{h.name} (Troops:{h.troops})" for h in self.party]))

    def show_hero_details(self):
        """显示所有英雄详情"""
        print("\n=== 出战英雄详情 ===")
        if not self.party:
            print("无")
        else:
            for hero in self.party:
                print(f"{hero.name} Lv{hero.level}")
                print(f"兵力: {hero.troops}/{hero.max_troops}")
                print(f"力量: {hero.strength} 智力: {hero.intelligence} 敏捷: {hero.agility}")
                print("技能：" + ", ".join([s["name"] for s in hero.skills]))
                print("----------------")
        
        print("\n=== 城池英雄详情 ===")
        if not self.city_heroes:
            print("无")
        else:
            for hero in self.city_heroes:
                print(f"{hero.name} Lv{hero.level}")
                print(f"兵力: {hero.troops}/{hero.max_troops}")
                print(f"力量: {hero.strength} 智力: {hero.intelligence} 敏捷: {hero.agility}")
                print("技能：" + ", ".join([s["name"] for s in hero.skills]))
                print("----------------")

    def produce_resources(self):
        """根据所有建筑等级进行资源生产"""
        print("\n[资源生产]")
        
        # 遍历所有生产型建筑
        for building_name, data in self.buildings.items():
            if "production" in data:
                for resource, amount in data["production"].items():
                    produced = amount * data["level"]
                    self.resources[resource] += produced
                    print(f"{building_name} 生产了 {produced} {resource}")
  
    def upgrade_building(self):
        self.check_unlocks()
        available_buildings = [(n, d) for n, d in self.buildings.items() if d["unlocked"]]
        
        print("\n=== 可升级建筑 ===")
        for i, (name, data) in enumerate(available_buildings, 1):
            # 计算动态成本：基础成本 * 当前等级
            current_cost = {k: v * (data["level"] + 1) for k, v in data["base_cost"].items()}
            cost_str = " ".join([f"{k}:{v}" for k, v in current_cost.items()])
            print(f"{i}. {name}(Lv{data['level']}) 需求: {cost_str}")

        try:
            choice = int(input("选择要升级的建筑编号: ")) - 1
            selected = available_buildings[choice]
            building_name, building_data = selected
            
            # 计算实际需要的资源
            current_cost = {k: v * (building_data["level"] + 1) for k, v in building_data["base_cost"].items()}
            missing = [r for r, v in current_cost.items() if self.resources[r] < v]
            
            if not missing:
                for r, v in current_cost.items():
                    self.resources[r] -= v
                building_data["level"] += 1
                print(f"{building_name} 升级到 Lv{building_data['level']}！")
            else:
                print(f"资源不足！缺少：{', '.join(missing)}")
                
        except (ValueError, IndexError):
            print("无效输入")

    # 在main_loop的choice=="1"时调用

    def explore(self):
        explore_cost = 50
        if self.resources["food"] < explore_cost:
            print("食物不足，无法探索！")
            return
        
        self.resources["food"] -= explore_cost
        print(f"消耗了 {explore_cost} 食物进行探索。")
        
        success_chance = 0.8 
        
        if random.random() < success_chance:
            # 确定获得的稀有度
            rand = random.random()
            cumulative = 0
            for rarity, prob in RARITY_PROB.items():
                cumulative += prob
                if rand <= cumulative:
                    selected_rarity = rarity
                    break
            else:  # 防止浮点误差
                selected_rarity = "R"
            
            # 从对应池中随机选择英雄
            selected_hero = random.choice(HERO_POOL[selected_rarity])
            
            # 创建英雄实例
            new_hero = Hero(
                name=selected_hero["name"],
                troops=selected_hero["troops"],
                strength=selected_hero["strength"],
                intelligence=selected_hero["intelligence"],
                agility=selected_hero["agility"]
            )
            new_hero.skills.append(SKILL_LIBRARY[selected_hero["skill"]])
            
            # 检查是否重复
            existing_names = [h.name for h in self.city_heroes + self.party]
            if new_hero.name in existing_names:
                self.materials[new_hero.name] = self.materials.get(new_hero.name, 0) + 1
                print(f"获得重复名将【{new_hero.name}】，自动转化为材料卡x1！")
                print(f"当前材料：{self.materials[new_hero.name]}张")
            else:
                self.city_heroes.append(new_hero)
                print(f"\n🌟【{selected_rarity}】获得名将：{new_hero.name}")
                print(f"典故：{selected_hero['intro']}")
                print(f"携技：{new_hero.skills[0]['name']}")
            
            self.explored_areas += 1
        else:
            print("探索未发现任何有价值的东西")


# 角色基类
class Character:
    def __init__(self, name, troops, strength, intelligence, agility):
        self.name = name
        self.max_troops = troops
        self.troops = troops      # 当前兵力
        self.max_troops = troops  # 记录最大兵力
        self.strength = strength  # 力量
        self.intelligence = intelligence  # 智力
        self.agility = agility    # 敏捷
        self.skills = []          # 技能列表

    @property
    def is_alive(self):
        return self.troops > 0

# 英雄类继承
class Hero(Character):
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        self.exp = 0
        self.max_mp = 50 + 5 * intelligence  # 示例MP计算公式
        self.mp = self.max_mp
        self.skills = []
        self.level = 1

    def level_up(self):
        # 升级时的属性成长
        self.level += 1
        self.max_troops += 10
        self.strength += 2
        self.intelligence += 2
        self.agility += 1
        print(f"{self.name} 升级到 Lv{self.level}！") 

# 敌人类
class Enemy(Character):
    def __init__(self, name, troops, strength, intelligence, agility):
        super().__init__(name, troops, strength, intelligence, agility)
        # 从名字中解析等级
        if "·Lv" in name:
            self.level = int(name.split("·Lv")[1])
        else:
            self.level = 1
            
class BattleSystem:
    def __init__(self, party, enemies):
        self.party = party
        self.enemies = enemies
        self.turn_order = []  # 行动顺序队列
    
    def basic_attack(self, attacker, defender):
        """普通攻击并概率触发技能"""
        # 普通攻击
        damage = max(1, attacker.strength - defender.agility//2)
        defender.troops = max(0, defender.troops - damage)
        print(f"{attacker.name} 对 {defender.name} 造成 {damage} 伤害")
        self.print_combatant_status(defender)
        
        # 概率触发技能
        for skill in attacker.skills:
            if random.random() < skill["prob"]:
                self.trigger_skill(attacker, defender, skill)

    def trigger_skill(self, attacker, defender, skill):
        """处理技能效果"""
        # 选择目标
        if skill["target"] == "ally":
            target = self.select_ally_target(attacker)
        else:
            target = defender
        
        if not target:
            return

        # 计算效果值
        scale_value = attacker.strength if skill["scale"] == "strength" else attacker.intelligence
        effect_value = int(skill["base"] + scale_value * skill["coef"])
        
        # 应用效果
        if skill["target"] == "enemy":
            target.troops = max(0, target.troops - effect_value)
            print(f"✨ {attacker.name} 触发 {skill['name']} 对 {target.name} 造成 {effect_value} 伤害！")
        else:
            target.troops = min(target.max_troops, target.troops + int(effect_value))
            print(f"✨ {attacker.name} 触发 {skill['name']} 为 {target.name} 恢复 {effect_value} 兵力！")
        
        self.print_combatant_status(target)

    def select_ally_target(self, attacker):
        """选择友方目标"""
        allies = self.party if attacker in self.party else self.enemies
        alive_allies = [a for a in allies if a.is_alive]
        
        if not alive_allies:
            return None
            
        # 优先选择兵力最少的单位
        return min(alive_allies, key=lambda x: x.troops)
    
    
    
    
    
    def determine_order(self):
        """根据敏捷生成行动顺序"""
        all_combatants = self.party + self.enemies
        # 按敏捷降序排序，相同敏捷时随机
        self.turn_order = sorted(
            all_combatants,
            key=lambda x: (-x.agility, random.random())
        )
    
        
    def print_combatant_status(self, combatant):
        """打印角色状态"""
        print(f"{combatant.name} 的兵力：{combatant.troops}/{combatant.max_troops}")
    
    def auto_ai_action(self, character):
        """AI的自动行为"""
        targets = [h for h in self.party if h.is_alive] if character in self.enemies else [h for h in self.enemies if h.is_alive]
        if not targets:
            return
            
        target = random.choice(targets)
        self.basic_attack(character, target)
 
    def battle_loop(self):
        """主战斗循环"""
        round_count = 1
        while True:
            print(f"\n=== 第 {round_count} 回合 ===")
            time.sleep(1)
            self.determine_order()
            
            for fighter in self.turn_order:
                if not fighter.is_alive:
                    continue
                    
                print(f"\n{fighter.name} 的行动：")
                self.auto_ai_action(fighter)
                
                # 检查战斗结果
                if all(not e.is_alive for e in self.enemies):
                    print("🎉 战斗胜利！")
                    return "win"
                if all(not h.is_alive for h in self.party):
                    print("💀 队伍全灭...")
                    return "lose"
            
            round_count += 1

# 在代码中添加验证函数
def validate_skills():
    missing_skills = set()
    for rarity, heroes in HERO_POOL.items():
        for hero in heroes:
            if hero["skill"] not in SKILL_LIBRARY:
                missing_skills.add(hero["skill"])
    if missing_skills:
        print(f"缺失技能配置：{', '.join(missing_skills)}")
    else:
        print("所有技能配置完整！")

def main_loop():
    game = Game()
    
    while True:
        game.produce_resources()  # 自动生产资源
        game.show_status()
        print("\n=== 选择操作 ===")
        print("1. 升级建筑  2. 探索  3. 编队管理  4. 英雄详情  5. 战斗  q.退出")
        choice = input("请输入选项: ").lower()
        
        # 处理玩家选择
        if choice == "1":
            # 建筑升级逻辑
            game.upgrade_building()
        elif choice == "2":
            # 探索逻辑
            game.explore()
        elif choice == "3":
            game.manage_party()
        elif choice == "4":
            game.show_hero_details()
        elif choice == "5":
            if not game.party:
                print("❌ 请先编组出战队伍！")
                continue
                
            game.generate_enemies()  # 生成当前敌人
            battle = BattleSystem(game.party, game.current_enemies)
            result = battle.battle_loop()
            
            if result == "win":
                # 胜利奖励
                game.resources["gold"] += 100 * game.explored_areas
                print(f"获得 {100*game.explored_areas} 黄金！")
            else:
                # 失败惩罚
                game.resources["food"] = max(0, game.resources["food"] - 50)     
        elif choice == "q":
            break

if __name__ == "__main__":
    validate_skills()
    main_loop()