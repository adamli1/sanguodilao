import pygame
import random
from pygame.locals import *
from game_mechanics import Game
from battle import BattleSystem

# 初始化Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 30

# 颜色定义
COLORS = {
    "background": (30, 30, 30),
    "panel": (50, 50, 60),
    "text": (200, 200, 200),
    "button": (80, 80, 90),
    "button_hover": (100, 100, 110)
}

# 在初始化部分添加图标加载
ICONS = {
    "gold": pygame.transform.scale(pygame.image.load("ui/icons/gold.png").convert_alpha(), (48, 48)),
    "wood": pygame.transform.scale(pygame.image.load("ui/icons/wood.png").convert_alpha(), (48, 48)),
    "food": pygame.transform.scale(pygame.image.load("ui/icons/food.png").convert_alpha(), (48, 48)),
    "stone": pygame.transform.scale(pygame.image.load("ui/icons/stone.png").convert_alpha(), (48, 48))
}


# 基础UI组件
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self._text = text
        self.callback = callback
        self.hover = False

    @property
    def text(self):
        return self._text() if callable(self._text) else self._text
    
    def draw(self, surface):
        color = COLORS["button_hover"] if self.hover else COLORS["button"]
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = FONT_SM.render(self.text, True, COLORS["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

# 游戏场景基类
class Scene:
    def handle_events(self, events):
        pass
    
    def update(self):
        pass
    
    def draw(self, surface):
        pass

# 初始化字体
FONT_SM = pygame.font.Font("ui/SimHei.ttf", 24)
FONT_MD = pygame.font.Font("ui/SimHei.ttf", 32)
FONT_LG = pygame.font.Font("ui/SimHei.ttf", 48)

class MainScene(Scene):
    def __init__(self):
        self.buttons = [
            Button((100, 500, 200, 50), "建筑系统", lambda: game_state.change_scene(BuildScene())),
            Button((350, 500, 200, 50), "英雄探索", self.explore),
            Button((600, 500, 200, 50), "编队管理", lambda: game_state.change_scene(PartyScene())),
            Button((850, 500, 200, 50), "开始战斗", self.start_battle)
        ]
        
    def explore(self):
        # 调用原有游戏逻辑
        game.explore()
        
    def start_battle(self):
        if not game.party:
            return
        game.generate_enemies()
        game_state.change_scene(BattleScene(game_state))  # 传递game_state参数

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn.rect.collidepoint(pos) and btn.callback:
                        btn.callback()

    def update(self):
        # 在主场景中无需特殊更新逻辑
        pass

    def draw(self, surface):
        surface.fill(COLORS["background"])
        
        # 绘制资源面板（顶部横排）
        panel_height = 80
        pygame.draw.rect(surface, COLORS["panel"], (0, 0, SCREEN_WIDTH, panel_height))
        
        # 资源项参数
        icon_size = 48
        margin = 20
        start_x = 30
        spacing = 150
        
        # 遍历资源
        for idx, (res_name, value) in enumerate(game.resources.items()):
            x = start_x + idx * spacing
            
            # 绘制图标
            if res_name in ICONS:
                icon = pygame.transform.scale(ICONS[res_name], (icon_size, icon_size))
                surface.blit(icon, (x, 15))
            
            # 绘制数值
            text_surf = FONT_MD.render(f"{value}", True, COLORS["text"])
            text_rect = text_surf.get_rect(midtop=(x + icon_size/2, 15 + icon_size + 5))
            surface.blit(text_surf, text_rect)
            
        # 绘制按钮
        for btn in self.buttons:
            btn.draw(surface)
            
        # 绘制英雄队伍
        x = 80
        for hero in game.party:
            hero_height = hero.troops / 4
            pygame.draw.rect(surface, (100,150,200), (x, 450-hero_height, 80, hero_height))
            
            # 渲染英雄名字
            text = FONT_SM.render(hero.name, True, COLORS["text"])
            
            # 获取文本的矩形区域
            text_rect = text.get_rect()
            
            # 计算文本的水平位置，使其在英雄矩形内居中
            text_x = x + (80 - text_rect.width) // 2  # 80 是英雄矩形的宽度
            text_y = 460  # 垂直位置保持不变
            
            # 绘制文本
            surface.blit(text, (text_x, text_y))
            
            # 渲染英雄的 troops 数值
            troops_text = FONT_SM.render(str(hero.troops), True, COLORS["text"])
            
            # 获取 troops 文本的矩形区域
            troops_rect = troops_text.get_rect()
            
            # 计算 troops 文本的水平位置，使其在英雄矩形内居中
            troops_x = x + (80 - troops_rect.width) // 2  # 80 是英雄矩形的宽度
            
            # 计算 troops 文本的垂直位置，使其在英雄矩形内居中
            troops_y = 450 - hero_height + (hero_height - troops_rect.height) // 2  # 垂直居中在矩形内
            
            # 绘制 troops 数值
            surface.blit(troops_text, (troops_x, troops_y))

            x += 85

class BuildScene(Scene):
    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.heal_btn = Button((200, 600, 200, 40),  # 新增恢复按钮
            lambda: f"治疗部队（需食物:{game.buildings['barracks']['heal_cost']['food']*game.buildings['barracks']['level']})",
            self.heal_troops)
        self.build_buttons = []
        self.refresh_buttons()

    def refresh_buttons(self):
        """刷新建筑按钮列表"""
        self.build_buttons = []
        y = 100
        for name in game.buildings:
            data = game.buildings[name]
            if data["unlocked"]:
                # 动态生成按钮文本（使用lambda捕获当前name值）
                text_func = lambda n=name: f"{n} Lv{game.buildings[n]['level']} (升级需: {self.get_cost_string(n)})"
                btn = Button(
                    (100, y, 600, 60),
                    text_func,
                    lambda b=name: self.upgrade_building(b)
                )
                self.build_buttons.append(btn)
                y += 70
        
        # 添加治疗按钮状态更新
        self.heal_btn.hover = self.heal_btn.rect.collidepoint(pygame.mouse.get_pos())

    def heal_troops(self):
        success, message = game.heal_troops()
        if not success:
            print(message)  # 在实际游戏中可以显示UI提示
        self.refresh_buttons()

    def get_cost_string(self, building_name):
        """生成资源需求字符串"""
        data = game.buildings[building_name]
        current_cost = {k: v * (data["level"] + 1) for k, v in data["base_cost"].items()}
        return " ".join([f"{k}:{v}" for k, v in current_cost.items()])
    
    def upgrade_building(self, building_name):
        if game.upgrade_building(building_name):
            self.refresh_buttons()  # 升级成功刷新按钮
        else:
            # 可以在这里添加资源不足的提示逻辑
            pass

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 添加治疗按钮检测
                if self.heal_btn.rect.collidepoint(pos):
                    self.heal_btn.callback()
                if self.back_btn.rect.collidepoint(pos):
                    self.back_btn.callback()
                for btn in self.build_buttons:
                    if btn.rect.collidepoint(pos) and btn.callback:
                        btn.callback()

    def update(self):
        # 在建筑场景中无需特殊更新逻辑
        pass
    
    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_btn.draw(surface)
        self.heal_btn.draw(surface)  # 绘制治疗按钮
        for btn in self.build_buttons:
            btn.hover = btn.rect.collidepoint(pygame.mouse.get_pos())
            btn.draw(surface)

class PartyScene(Scene):
    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.selection = None
        self.buttons = []
        self.refresh_ui()

    def refresh_ui(self):
        """刷新编队界面"""
        self.buttons = [self.back_btn]
        y = 100
        
        # 当前队伍
        self.buttons.append(Button((100, y, 200, 40), "当前队伍", None))
        y += 60
        for i, hero in enumerate(game.party):
            btn = Button((100, y, 300, 50), 
                        lambda h=hero: f"{h.name} Lv{h.level} (兵力: {h.troops}/经验: {h.exp}/{h.required_exp()})",
                        lambda idx=i: self.select_party_member(idx))
            self.buttons.append(btn)
            y += 60

        # 可用英雄
        y = 100
        self.buttons.append(Button((500, y, 200, 40), "可用英雄", None))
        y += 60
        for i, hero in enumerate(game.city_heroes):
            if hero not in game.party:
                btn = Button((500, y, 300, 50),
                            f"{hero.name} Lv{hero.level} (兵力: {hero.troops}/经验: {hero.exp}/{hero.required_exp()})",
                            lambda idx=i: self.select_available_hero(idx))
                self.buttons.append(btn)
                y += 60

    def select_party_member(self, index):
        """选择队伍成员进行移除"""
        if 0 <= index < len(game.party):
            removed = game.party.pop(index)
            game.city_heroes.append(removed)
            self.refresh_ui()

    def select_available_hero(self, index):
        """选择可用英雄进行添加"""
        if len(game.party) >= 3:
            return
        hero = game.city_heroes[index]
        if hero not in game.party:
            game.party.append(hero)
            game.city_heroes.remove(hero)
            self.refresh_ui()

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn.rect.collidepoint(pos) and btn.callback:
                        btn.callback()

    def draw(self, surface):
        surface.fill(COLORS["background"])
        for btn in self.buttons:
            btn.draw(surface)
        
        # 绘制提示文字
        tip_text = FONT_SM.render("点击队伍成员移出，点击可用英雄加入（最多3人）", True, COLORS["text"])
        surface.blit(tip_text, (100, 550))

class BattleScene(Scene):
    def __init__(self, game_state):
        self.battle_system = BattleSystem(game.party, game.current_enemies, game_state)  # 传递game_state
        self.game_state = game_state  # 保存引用
        self.turn_idx = 0
        self.battle_result = None  # 用于存储战斗结果
        self.back_button = Button((50, 600, 200, 50), "返回主界面", lambda: game_state.change_scene(MainScene()))
        self.battle_over = False  # 标记战斗是否结束
        self.round_count = 1  # 当前回合数
        self.damage_numbers = []  # 存储伤害数值信息 (pos, value, duration)
        self.skill_damage_numbers = []  # 存储技能伤害数值信息 (pos, value, duration)
        self.attack_animations = []  # 存储攻击动画 (start_pos, end_pos, duration)
        self.current_turn_index = 0  # 当前行动单位索引
        self.waiting_for_animation = False  # 是否正在等待动画完成
        self.action_delay = 500  # 每个动作之间的延迟（毫秒）
        self.last_action_time = 0  # 上次动作时间
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.USEREVENT:
                self.waiting_for_animation = False
                pygame.time.set_timer(pygame.USEREVENT, 0)  # 清除定时器

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.battle_over and self.back_button.rect.collidepoint(pos):
                    self.back_button.callback()
    
    def update(self):
        if self.battle_over or self.waiting_for_animation:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_action_time < self.action_delay:
            return

        try:
            # 添加安全索引检查
            fighter = self.battle_system.turn_order[self.current_turn_index]
        except IndexError:
            # 当索引超出时重置回合
            self.current_turn_index = 0
            self.round_count += 1
            self.battle_system.determine_order()
            return

        # 新增：检查行动顺序列表是否为空
        if not self.battle_system.turn_order:
            return

        # 跳过已死亡单位
        while not fighter.is_alive:
            self.current_turn_index += 1
            if self.current_turn_index >= len(self.battle_system.turn_order):
                # 新增：重置前检查是否所有单位都死亡
                alive_combatants = [c for c in self.battle_system.turn_order if c.is_alive]
                if not alive_combatants:
                    self.battle_result = "lose" if any(h.is_alive for h in self.battle_system.party) else "win"
                    self.battle_over = True
                    return
                
                self.round_count += 1
                self.current_turn_index = 0
                self.battle_system.determine_order()
                return
            fighter = self.battle_system.turn_order[self.current_turn_index]

        # 获取当前需要行动的战斗单位
        fighter = self.battle_system.turn_order[self.current_turn_index]
        
        # 执行AI行动
        self.execute_single_action(fighter)
        
        # 更新索引和时间
        self.current_turn_index += 1
        self.last_action_time = current_time
        
        # 检查回合结束
        if self.current_turn_index >= len(self.battle_system.turn_order):
            self.round_count += 1
            self.current_turn_index = 0
            self.battle_system.determine_order()  

        # 检查战斗结果（移动到此处以确保实时更新）
        if all(not e.is_alive for e in self.battle_system.enemies):
            self.battle_result = "win"
            self.battle_system.distribute_exp()
            self.battle_over = True
        elif all(not h.is_alive for h in self.battle_system.party):
            self.battle_result = "lose"
            self.battle_over = True

    def execute_single_action(self, fighter):
         # 新增：行动前再次检查存活状态
        if not fighter.is_alive:
            return
        
        # 清空上一帧的动画
        self.damage_numbers = []
        self.skill_damage_numbers = []
        self.attack_animations = []

        # 执行AI行动
        targets = [h for h in self.battle_system.party if h.is_alive] if fighter in self.battle_system.enemies else [h for h in self.battle_system.enemies if h.is_alive]
        if targets:
            target = random.choice(targets)
                       
            # 执行攻击逻辑
            self.battle_system.auto_ai_action(fighter)

        # 设置动画等待状态
        self.waiting_for_animation = True
        # 1秒后解除等待状态（根据动画持续时间调整）
        pygame.time.set_timer(pygame.USEREVENT, 1000) 
            
    def get_combatant_pos(self, combatant):
        """获取战斗单位在屏幕上的坐标"""
        if combatant in self.battle_system.party:
            index = self.battle_system.party.index(combatant)
            return (100 + index*100, 600)
        else:
            index = self.battle_system.enemies.index(combatant)
            return (100 + index*100, 100)

    def add_attack_animation(self,attacker,target):
        """添加攻击动画"""
        attacker_pos = self.get_combatant_pos(attacker)
        target_pos = self.get_combatant_pos(target)
        self.attack_animations.append((attacker_pos, target_pos, 15))

    def add_damage_number(self, target, value):
        """添加伤害数字"""
        pos = self.get_combatant_pos(target)
        self.damage_numbers.append((pos, f"-{value}", 30))

    def add_skill_damage_number(self, target, value):
        """添加伤害数字"""
        pos = self.get_combatant_pos(target)
        self.skill_damage_numbers.append((pos, f"-{value}", 30))    


    def draw(self, surface):
        surface.fill(COLORS["background"])
              
        # 绘制己方队伍
        x = 100
        for hero in game.party:
            pos = self.get_combatant_pos(hero)
            color = (0, 200, 0) if hero.is_alive else (100, 100, 100)
            pygame.draw.circle(surface, color, (x, 600), 30)
            
             # 绘制血条背景
            bar_width = 60
            bar_height = 8
            bg_rect = pygame.Rect(pos[0]-bar_width//2, pos[1]+40, bar_width, bar_height)
            pygame.draw.rect(surface, (50, 50, 50), bg_rect)
            
            # 绘制当前血量
            if hero.max_troops > 0:
                hp_width = int(bar_width * hero.troops / hero.max_troops)
                hp_rect = pygame.Rect(pos[0]-bar_width//2, pos[1]+40, hp_width, bar_height)
                pygame.draw.rect(surface, (0, 200, 0), hp_rect)
            
            # 显示兵力数值
            text = FONT_SM.render(f"{hero.troops}/{hero.max_troops}", True, (200,200,200))
            text_rect = text.get_rect(center=(pos[0], pos[1]+60))
            surface.blit(text, text_rect)

            # 绘制首字
            if hero.is_alive:
                text = FONT_SM.render(hero.name[0], True, (255, 255, 255))
                text_rect = text.get_rect(center=(x, 600))
                surface.blit(text, text_rect)
            x += 100
        
        # 绘制敌方队伍
        x = 100
        for enemy in game.current_enemies:
            pos = self.get_combatant_pos(enemy)
            color = (200, 0, 0) if enemy.is_alive else (100, 100, 100)
            pygame.draw.circle(surface, color, (x, 100), 30)
            
            # 绘制血条背景
            bar_width = 60
            bar_height = 8
            bg_rect = pygame.Rect(pos[0]-bar_width//2, pos[1]+40, bar_width, bar_height)
            pygame.draw.rect(surface, (50, 50, 50), bg_rect)
            
            # 绘制当前血量
            if enemy.max_troops > 0:
                hp_width = int(bar_width * enemy.troops / enemy.max_troops)
                hp_rect = pygame.Rect(pos[0]-bar_width//2, pos[1]+40, hp_width, bar_height)
                pygame.draw.rect(surface, (200, 0, 0), hp_rect)
            
            # 显示兵力数值
            text = FONT_SM.render(f"{enemy.troops}/{enemy.max_troops}", True, (200,200,200))
            text_rect = text.get_rect(center=(pos[0], pos[1]+60))
            surface.blit(text, text_rect)

            if enemy.is_alive:
                text = FONT_SM.render(enemy.name[0], True, (255, 255, 255))
                text_rect = text.get_rect(center=(x, 100))
                surface.blit(text, text_rect)
            x += 100

        # 绘制攻击动画
        for start_pos, end_pos, duration in self.attack_animations:
            pygame.draw.line(surface, (255, 165, 0), start_pos, end_pos, 3)

        # 绘制伤害数字
        for pos, value, d in self.damage_numbers:
            text = FONT_SM.render(value, True, (255, 50, 50))
            surface.blit(text, (pos[0]+20, pos[1]-30 - d))

        # 绘制技能伤害数字
        for pos, value, d in self.skill_damage_numbers:
            text = FONT_SM.render(value, True, (255, 0, 255))
            surface.blit(text, (pos[0]+20, pos[1]-60 - d))        

        # 绘制战斗结果
        if self.battle_over:
            result_text = "战斗胜利！" if self.battle_result == "win" else "战斗失败！"
            text_surf = FONT_LG.render(result_text, True, COLORS["text"])
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(text_surf, text_rect)
            self.back_button.draw(surface)

        # 当等待动画时显示提示
        if self.waiting_for_animation:
            text = FONT_SM.render("行动中...", True, (200, 200, 200))
            surface.blit(text, (SCREEN_WIDTH//2-50, SCREEN_HEIGHT//2))  

# 创建场景管理器
class GameState:
    def __init__(self):
        self.current_scene = MainScene()
        
    def change_scene(self, new_scene):
        self.current_scene = new_scene

game_state = GameState()

# 初始化游戏实例
game = Game()

running = True
game.start_production_timer()
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            game.stop_production_timer()
            running = False
            
    # 处理场景事件
    game_state.current_scene.handle_events(events)
    
    # 更新场景
    game_state.current_scene.update()
    
    # 绘制场景
    game_state.current_scene.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()