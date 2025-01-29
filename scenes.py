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
        # 调整按钮位置和尺寸到底部
        button_width = 150
        button_height = 40
        start_y = SCREEN_HEIGHT - 70  # 底部留出空间
        horizontal_spacing = 220  # 按钮水平间距
        
        self.buttons = [
            Button((200, start_y, button_width, button_height), "建筑系统", lambda: game_state.change_scene(BuildScene())),
            Button((200 + horizontal_spacing, start_y, button_width, button_height), "英雄探索", lambda: game_state.change_scene(ExploreScene())),
            Button((200 + horizontal_spacing*2, start_y, button_width, button_height), "编队管理", lambda: game_state.change_scene(PartyScene())),
            Button((200 + horizontal_spacing*3, start_y, button_width, button_height), "开始战斗", self.start_battle)
        ]
        
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
        
        # 绘制资源面板（顶部横排） - 修改这部分
        panel_height = 40  # 进一步降低面板高度
        pygame.draw.rect(surface, COLORS["panel"], (0, 0, SCREEN_WIDTH, panel_height))
        
        # 新参数设置
        icon_size = 20       # 图标尺寸
        text_margin = 5      # 图标与数值间距
        item_spacing = 35    # 资源项间距加大
        start_margin = 15    # 左侧起始边距
        current_x = start_margin  # 当前绘制位置
        
        # 使用更小字体
        value_font = pygame.font.Font(None, 20)  # 新建小号字体
        # 或者使用预设的 FONT_SM（如果已定义合适大小）

        for res_name, value in game.resources.items():
            # 绘制图标
            if res_name in ICONS:
                icon = pygame.transform.scale(ICONS[res_name], (icon_size, icon_size))
                icon_y = (panel_height - icon_size) // 2
                surface.blit(icon, (current_x, icon_y))
            
            # 绘制数值（支持8位数）
            value_text = f"{value:8d}"  # 格式化为8位宽度
            value_surf = value_font.render(value_text, True, COLORS["text"])
            value_y = (panel_height - value_surf.get_height()) // 2
            
            # 数值位置（图标右侧）
            value_x = current_x + icon_size + text_margin
            surface.blit(value_surf, (value_x, value_y))
            
            # 更新下一个资源项位置
            current_x += icon_size + text_margin + value_surf.get_width() + item_spacing

        # 调整英雄显示位置到屏幕中部
        x = 80
        for hero in game.party:
            hero_height = hero.troops / 4
            pygame.draw.rect(surface, (100,150,200), (x, 350-hero_height, 80, hero_height))  # Y坐标上移
            
            # 调整文本位置
            text = FONT_SM.render(hero.name, True, COLORS["text"])
            text_x = x + (80 - text.get_width()) // 2
            surface.blit(text, (text_x, 360))  # 文本位置上移
            
            # 调整兵力显示位置
            troops_text = FONT_SM.render(str(hero.troops), True, COLORS["text"])
            troops_x = x + (80 - troops_text.get_width()) // 2
            troops_y = 350 - hero_height + (hero_height - troops_text.get_height()) // 2
            surface.blit(troops_text, (troops_x, troops_y))

            x += 85

        # 最后绘制按钮确保在最上层
        for btn in self.buttons:
            btn.draw(surface)

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
        self.action_delay = 0  # 每个动作之间的延迟（毫秒）
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
        pygame.time.set_timer(pygame.USEREVENT, 200) 
            
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

# 添加新的探索场景
class ExploreScene(Scene):
    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.explore_btn = Button((SCREEN_WIDTH//2 - 75, 500, 150, 50), "开始探索", self.do_explore)
        self.result = None

    def do_explore(self):
        self.result = game.explore()
        print(f"探索结果: {self.result}")  # 添加调试输出

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.back_btn.rect.collidepoint(pos):
                    self.back_btn.callback()
                elif self.explore_btn.rect.collidepoint(pos):
                    self.result = None  # 强制清空旧结果
                    self.explore_btn.callback()
                    

    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_btn.draw(surface)
        self.explore_btn.draw(surface)

        if self.result:
            # 检查英雄是否已存在
            is_existing = self.result in game.city_heroes or self.result in game.party
            
            if not is_existing:
                # 已有英雄的简单提示
                text = FONT_MD.render(f"发现 {self.result.name}", True, COLORS["text"])
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 300))
                surface.blit(text, text_rect)
            else:
                # 新英雄的完整展示
                panel_rect = pygame.Rect(100, 150, SCREEN_WIDTH-200, 300)
                pygame.draw.rect(surface, (255,255,255, 128), panel_rect, border_radius=10)
                
                text_y = 200
                title = FONT_MD.render("★ 发现新英雄！ ★", True, (200, 50, 50))
                surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, text_y))
                
                pygame.draw.rect(surface, (200,200,200), (SCREEN_WIDTH//2 - 50, text_y + 50, 100, 100))
                
                text_y += 180
                info_lines = [
                    f"姓名: {self.result.name}",
                    f"等级: {self.result.level}",
                    f"兵力: {self.result.troops}",
                    f"技能: {self.result.skills[0]['name']}"
                ]
                
                for line in info_lines:
                    text = FONT_SM.render(line, True, COLORS["text"])
                    surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, text_y))
                    text_y += 40
        else:
            # 未探索时的提示添加背景框
            prompt_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 180, 400, 80)
            pygame.draw.rect(surface, (200,200,200, 150), prompt_rect, border_radius=8)
            prompt = FONT_MD.render("点击按钮开始探索", True, (50, 50, 50))  # 深色文字
            surface.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 210))

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