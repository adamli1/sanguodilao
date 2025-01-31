import random
import threading
import copy
from config import (
    SKILL_LIBRARY,
    HERO_POOL,
    ENEMY_TEMPLATES,
    RARITY_PROB
)
from characters import Hero, Enemy, Character
from battle import BattleSystem
from collections import defaultdict

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
            "黄金": 500,
            "木材": 1000,
            "粮草": 1500,
            "石料": 500
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
        self.materials = {}    # 改为字典存储，格式：{"英雄名": 数量}

        # 建筑系统重构
        self.buildings = {
            "农场": {
                "level": 1,
                "base_cost": {"木材": 20, "石料": 10, "粮草": 30},
                "production": {"粮草": 10},
                "unlocked": True  # 初始已解锁
            },
            "伐木场": {
                "level": 0,
                "base_cost": {"木材": 30, "石料": 15},
                "production": {"木材": 8},
                "unlocked": True
            },
            "采石场": {
                "level": 0,
                "base_cost": {"木材": 40, "石料": 20},
                "production": {"石料": 5},
                "unlocked": True
            },
            "金矿": {
                "level": 0,
                "base_cost": {"木材": 50, "石料": 30, "黄金": 20},
                "production": {"黄金": 7},
                "unlocked": False,
                "unlock_condition": {"伐木场": 2}  # 需要伐木场2级
            },
            "兵营": {
                "level": 0,
                "base_cost": {"木材": 60, "石料": 40},
                "unlocked": False,
                "unlock_condition": {"采石场": 1, "金矿": 1},
                "heal_cost": {"粮草": 50},  # 新增：每次治疗消耗
                "heal_percent": 0.2  # 新增：每次恢复最大兵力的百分比
            }
        }
        self.production_interval = 3  # 每3秒自动生产一次资源
        self.production_timer = None
    
    def heal_troops(self):
        """通过兵营恢复兵力"""
        barracks = self.buildings["兵营"]
        
        # 检查兵营等级
        if barracks["level"] == 0:
            return False, "兵营尚未建造"
        
        # 计算总消耗
        required_food = barracks["heal_cost"]["粮草"] * barracks["level"]
        
        # 检查资源是否充足
        if self.resources["粮草"] < required_food:
            return False, "粮食不足"
        
        # 检查是否有需要恢复的兵力
        total_loss = sum(h.max_troops - h.troops for h in self.party)
        if total_loss == 0:
            return False, "没有需要恢复的兵力"
        
        # 扣除资源
        self.resources["粮草"] -= required_food
        
        # 恢复兵力
        heal_amount = barracks["heal_percent"] * barracks["level"]
        for hero in self.party:
            recover = min(hero.max_troops - hero.troops, 
                        int(hero.max_troops * heal_amount))
            hero.troops += recover
        
        return True, f"消耗{required_food}粮食，恢复{heal_amount*100}%最大兵力"

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

    def generate_enemies(self, map_info):
        self.current_enemies = []
        template_names = list(ENEMY_TEMPLATES.keys())
        
        # 天干序号列表
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        # 使用字典记录每个模板的生成次数
        template_count = defaultdict(int)

        # 根据地图配置生成敌人
        enemy_count = {
            "黄巾起义": 2,
            "讨伐董卓": 3,
            "群雄割据": 3
        }.get(map_info["name"], 2)
        
        base_level = {
            "黄巾起义": 3,
            "讨伐董卓": 5,
            "群雄割据": 10
        }.get(map_info["name"], 1)
        
        for _ in range(enemy_count):
            template = random.choice(template_names)
            template_count[template] += 1
            # 获取天干序号（超过10个会循环）
            idx = (template_count[template] - 1) % 10
            suffix = tiangan[idx]
            
            enemy_data = copy.deepcopy(ENEMY_TEMPLATES[template])
            growth = enemy_data["growth"]
            
            # 根据固定等级计算属性
            enemy = Character(
                name=f"{template}{suffix}·Lv{base_level}",  # 修改名称格式
                troops=base_level * 100,
                strength=enemy_data["base"]["strength"] + growth["strength"] * (base_level-1),
                intelligence=enemy_data["base"]["intelligence"] + growth["intelligence"] * (base_level-1),
                agility=enemy_data["base"]["agility"] + growth["agility"] * (base_level-1),
                skills=[SKILL_LIBRARY[skill] for skill in enemy_data["skills"]],
                level=base_level
            )
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

        print("\n=== 英雄材料卡 ===")
        if self.materials:
            for hero, count in self.materials.items():
                print(f"{hero}材料卡：{count}张")
        else:
            print("暂无英雄材料卡")

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
        if self.resources["粮草"] < explore_cost:
            print("食物不足，无法探索！")
            return None  # 明确返回None
            
        self.resources["粮草"] -= explore_cost
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
                agility=selected_hero["agility"],
                rarity=selected_rarity  # 添加稀有度参数
            )
            new_hero.skills.append(SKILL_LIBRARY[selected_hero["skill"]])
            
            # 检查是否重复
            existing_names = [h.name for h in self.city_heroes + self.party]
            if new_hero.name in existing_names:
                # 转换为对应英雄的材料卡
                self.materials[new_hero.name] = self.materials.get(new_hero.name, 0) + 1
                print(f"获得重复名将【{new_hero.name}】，自动转化为专属材料卡x1！")
                print(f"当前{new_hero.name}材料卡数量：{self.materials[new_hero.name]}")
            else:
                self.city_heroes.append(new_hero)
                print(f"\n🌟【{selected_rarity}】获得名将：{new_hero.name}")
                print(f"典故：{selected_hero['intro']}")
                print(f"携技：{new_hero.skills[0]['name']}")
            
            self.explored_areas += 1
            return new_hero  # 成功时返回英雄实例
        else:
            print("探索未发现任何有价值的东西")
            return None  # 失败时返回None