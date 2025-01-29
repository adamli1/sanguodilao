import random
import threading
from config import (
    SKILL_LIBRARY,
    HERO_POOL,
    ENEMY_TEMPLATES,
    RARITY_PROB
)
from characters import Hero, Enemy
from battle import BattleSystem

        # 保持原Game类初始化内容不变
        # 包括资源、队伍、建筑等初始化

    # 保持原Game类的方法不变
    # 包括 show_status, produce_resources, upgrade_building, 
    # explore, manage_party, generate_enemies 等方法
    # （由于篇幅限制，具体方法实现此处省略，保持原样即可）

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
        self.production_interval = 3  # 每3秒自动生产一次资源
        self.production_timer = None

    def produce_resources(self):
        """根据所有建筑等级进行资源生产"""
        # print("\n[资源生产]")
        for building_name, data in self.buildings.items():
            if "production" in data:
                for resource, amount in data["production"].items():
                    produced = amount * data["level"]
                    self.resources[resource] += produced
                    # print(f"{building_name} 生产了 {produced} {resource}，当前库存{self.resources[resource]}")

        # 重新启动定时器
        self.start_production_timer()

    def start_production_timer(self):
        """启动资源生产的定时器"""
        if self.production_timer:
            self.production_timer.cancel()
        self.production_timer = threading.Timer(self.production_interval, self.produce_resources)
        self.production_timer.start()

    def stop_production_timer(self):
        """停止资源生产的定时器"""
        if self.production_timer:
            self.production_timer.cancel()

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

    def upgrade_building(self, building_name):
        """升级指定建筑"""
        if building_name not in self.buildings:
            return False
        
        building = self.buildings[building_name]
        if not building["unlocked"]:
            return False
        
        # 计算升级所需资源
        current_cost = {k: v * (building["level"] + 1) for k, v in building["base_cost"].items()}
        
        # 检查资源是否足够
        if any(self.resources[r] < v for r, v in current_cost.items()):
            return False
        
        # 扣除资源
        for r, v in current_cost.items():
            self.resources[r] -= v
        
        # 升级建筑
        building["level"] += 1
        self.check_unlocks()  # 检查是否解锁新内容
        return True
    
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