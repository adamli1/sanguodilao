import random
import time
from characters import Character
from collections import defaultdict

    # 保持原BattleSystem类的方法不变
    # 包括 basic_attack, trigger_skill, select_ally_target, 
    # determine_order, print_combatant_status, auto_ai_action, battle_loop
    # （由于篇幅限制，具体方法实现此处省略，保持原样即可）

class BattleSystem:
    def __init__(self, party, enemies, game_state):
        self.party = party
        self.enemies = enemies
        self.game_state = game_state  # 保存引用
        self.turn_order = []  # 行动顺序队列
        self.last_action = None  # 新增属性记录最后动作
        # 新增战斗报告数据
        self.battle_report = {
            'rounds': 0,
            'participants': {},  # 改为字典存储每个参与者的详细数据
            'skills_used': defaultdict(int)
        }
        # 记录初始兵力
        self._record_initial_troops(party + enemies)

    def _record_initial_troops(self, combatants):
        """记录初始兵力"""
        for c in combatants:
            self.battle_report['participants'][c.name] = {
                'obj': c,
                'initial_troops': c.troops,
                'basic_damage': 0,
                'skill_damage': defaultdict(int),
                'total_dealt': 0,
                'total_taken': 0
            }

    def _record_damage(self, attacker, defender, amount, is_skill=False, skill_name=None):
        """记录伤害统计"""
        # 攻击者数据
        if attacker.name in self.battle_report['participants']:
            self.battle_report['participants'][attacker.name]['total_dealt'] += amount
            if is_skill:
                self.battle_report['participants'][attacker.name]['skill_damage'][skill_name] += amount
            else:
                self.battle_report['participants'][attacker.name]['basic_damage'] += amount
        
        # 防御者数据
        if defender.name in self.battle_report['participants']:
            self.battle_report['participants'][defender.name]['total_taken'] += amount

    def basic_attack(self, attacker, defender):
        """普通攻击并概率触发技能"""
        # 普通攻击
        base_damage = max(1, attacker.strength - defender.agility//2)
        
        # 平滑后的兵力比例系数（使用平方根函数）
        ratio = (attacker.troops / max(1, defender.troops)) ** 0.5  # 修改点
        damage = int(base_damage * ratio)
        
        defender.troops = max(0, defender.troops - damage)

        # 添加伤害数字显示
        if self.game_state.current_scene.__class__.__name__ == "BattleScene":
            self.game_state.current_scene.add_damage_number(defender, damage)
            self.game_state.current_scene.add_attack_animation(attacker, defender)

        print(f"{attacker.name} 对 {defender.name} 造成 {damage} 伤害")
        self.print_combatant_status(defender)
        
        # 概率触发技能
        for skill in attacker.skills:
            if random.random() < skill["prob"]:
                self.trigger_skill(attacker, defender, skill)

        # 记录伤害数据
        self._record_damage(attacker, defender, damage)

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
        
        # 添加平滑后的兵力比例系数（仅对敌方生效）
        if skill["target"] == "enemy":
            ratio = (attacker.troops / max(1, defender.troops)) ** 0.5  # 修改点
            effect_value = int(effect_value * ratio)
        
        # 添加伤害数字显示
        if skill["target"] == "enemy":
            target.troops = max(0, target.troops - effect_value)
            print(f"✨ {attacker.name} 触发 {skill['name']} 对 {target.name} 造成 {effect_value} 伤害！")
            if self.game_state.current_scene.__class__.__name__ == "BattleScene":
                self.game_state.current_scene.add_skill_damage_number(target, effect_value)
               
        else:
            # 治疗数值显示
            target.troops = min(target.max_troops, target.troops + effect_value)
            print(f"✨ {attacker.name} 触发 {skill['name']} 为 {target.name} 恢复 {effect_value} 兵力！")
            if self.game_state.current_scene.__class__.__name__ == "BattleScene":              
                self.game_state.current_scene.add_skill_damage_number(target, effect_value)
               
        
        self.print_combatant_status(target)

        # 记录技能使用
        self.battle_report['skills_used'][skill['name']] += 1

        # 记录伤害数据
        self._record_damage(attacker, defender, effect_value, is_skill=True, skill_name=skill['name'])

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

    def distribute_exp(self):
        """战斗胜利后分配经验"""
        if not self.party:
            return
        
        # 计算总经验值（根据敌人等级和数量）
        total_exp = sum(e.level * 50 for e in self.enemies)
        exp_per_hero = total_exp // len(self.party)
        
        # 分配经验并升级
        for hero in self.party:
            if hero.is_alive:
                hero.add_exp(exp_per_hero)
            else:
                hero.add_exp(exp_per_hero // 2)  # 阵亡获得一半经验

    def battle_loop(self):
        self.determine_order()
        while True:
            self.battle_report['rounds'] += 1
            battle_over = False
            
            # 检查战斗结果
            if all(not e.is_alive for e in self.enemies):
                self.battle_report['result'] = '胜利'  # 明确设置结果
                self.game_state.change_scene(MainScene())
                return
            elif all(not h.is_alive for h in self.party):
                self.battle_report['result'] = '失败'  # 明确设置结果
                self.game_state.change_scene(MainScene())
                return
            
            # ... 原有战斗循环代码 ...
 