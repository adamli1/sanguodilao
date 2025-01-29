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
    "黄金": pygame.transform.scale(pygame.image.load("ui/icons/gold.png").convert_alpha(), (48, 48)),
    "木材": pygame.transform.scale(pygame.image.load("ui/icons/wood.png").convert_alpha(), (48, 48)),
    "粮草": pygame.transform.scale(pygame.image.load("ui/icons/food.png").convert_alpha(), (48, 48)),
    "石料": pygame.transform.scale(pygame.image.load("ui/icons/stone.png").convert_alpha(), (48, 48))
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
        horizontal_spacing = 150  # 缩小间距以适应更多按钮
        
        self.buttons = [
            Button((200, start_y, button_width, button_height), "建筑系统", lambda: game_state.change_scene(BuildScene())),
            Button((200 + horizontal_spacing, start_y, button_width, button_height), "英雄探索", lambda: game_state.change_scene(ExploreScene())),
            Button((200 + horizontal_spacing*2, start_y, button_width, button_height), "编队管理", lambda: game_state.change_scene(PartyScene())),
            Button((200 + horizontal_spacing*3, start_y, button_width, button_height), "开始战斗", self.start_battle),
            Button((200 + horizontal_spacing*4, start_y, button_width, button_height), "英雄详情", lambda: game_state.change_scene(HeroScene())),
            Button((200 + horizontal_spacing*5, start_y, button_width, button_height), "背包", lambda: game_state.change_scene(InventoryScene()))
        ]
        
        self.player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]  # 新增：玩家初始位置
        self.move_speed = 5  # 移动速度
        self.city_rect = pygame.Rect(100, 100, 200, 200)  # 新增：城池区域（x, y, width, height）
        self.in_city = False  # 是否在城池范围内

    def start_battle(self):
        if not game.party:
            return
        game.generate_enemies()
        game_state.change_scene(BattleScene(game_state))  # 传递game_state参数

    def handle_events(self, events):
        # 检测玩家是否在城池范围内
        self.in_city = self.city_rect.collidepoint(self.player_pos)
        
        # 处理键盘输入（WSAD移动）
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.player_pos[1] -= self.move_speed
        if keys[K_s]:
            self.player_pos[1] += self.move_speed
        if keys[K_a]:
            self.player_pos[0] -= self.move_speed
        if keys[K_d]:
            self.player_pos[0] += self.move_speed
        
        # 边界限制
        self.player_pos[0] = max(50, min(SCREEN_WIDTH-50, self.player_pos[0]))
        self.player_pos[1] = max(50, min(SCREEN_HEIGHT-150, self.player_pos[1]))  # 底部留出按钮空间
        
        # 处理空格键进入建筑场景
        if keys[K_SPACE] and self.in_city:
            game_state.change_scene(BuildScene())
        
        # 原有鼠标事件处理
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
        
        # 绘制城池区域
        pygame.draw.rect(surface, (150, 100, 50), self.city_rect)  # 棕色矩形表示城池
        city_text = FONT_SM.render("长安", True, (255, 255, 200))
        text_rect = city_text.get_rect(center=self.city_rect.center)
        surface.blit(city_text, text_rect)
        
        # 当玩家在城池内时显示提示
        if self.in_city:
            tip_text = FONT_SM.render("进入主城", True, (200, 200, 0))
            surface.blit(tip_text, (self.city_rect.centerx - 100, self.city_rect.bottom + 10))
        
        # 绘制玩家角色
        pygame.draw.circle(surface, (0, 200, 255), self.player_pos, 20)  # 蓝色圆形表示玩家
        pygame.draw.circle(surface, (255, 255, 0), self.player_pos, 5)  # 黄色前向指示
        
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

        # 调整英雄显示到右上角（资源栏下方）
        panel_height = 40  # 资源栏高度
        start_x = SCREEN_WIDTH - 200  # 从右侧200像素开始
        start_y = panel_height + 10   # 资源栏下方10像素
        icon_size = 40  # 头像尺寸

        # 横向排列
        x = start_x
        for hero in game.party:
            # 头像背景
            pygame.draw.rect(surface, (80, 80, 100), (x, start_y, icon_size, icon_size), border_radius=5)
            
            # 显示首字（临时替代头像）
            initial = hero.name[0]  # 取名字首字
            initial_surf = FONT_MD.render(initial, True, (255,255,255))
            initial_rect = initial_surf.get_rect(center=(x + icon_size//2, start_y + icon_size//2))
            surface.blit(initial_surf, initial_rect)
            
            # 简化兵力显示（小进度条）
            troop_bar_height = 5
            troop_width = int(icon_size * (hero.troops / hero.max_troops))
            pygame.draw.rect(surface, (0, 200, 0), (x, start_y + icon_size, troop_width, troop_bar_height))
            
            # 显示兵力数字
            troops_text = FONT_SM.render(str(hero.troops), True, COLORS["text"])
            surface.blit(troops_text, (x + 2, start_y + icon_size + troop_bar_height))
            
            # 显示等级徽章
            level_bg = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(level_bg, (200, 200, 100), (10, 10), 10)
            surface.blit(level_bg, (x + icon_size - 20, start_y))
            level_text = FONT_SM.render(str(hero.level), True, (50, 50, 50))
            surface.blit(level_text, (x + icon_size - 15, start_y + 2))
            
            x -= (icon_size + 10)  # 向左排列，间距10像素

        # 最后绘制按钮确保在最上层
        for btn in self.buttons:
            btn.draw(surface)

class BuildScene(Scene):
    BUILDING_NAMES = {
        "农场": "农场",
        "伐木场": "伐木场", 
        "采石场": "采石场",
        "金矿": "金矿",
        "兵营": "兵营"
    }
    
    RESOURCE_NAMES = {
        "gold": "黄金",
        "wood": "木材",
        "food": "粮草",
        "stone": "石料"
    }

    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.heal_btn = Button((200, 600, 200, 40), 
            lambda: f"治疗部队（需食物:{game.buildings['兵营']['heal_cost']['粮草']*game.buildings['兵营']['level']})",
            self.heal_troops)
        self.selected_building = None
        self.confirm_rect = None
        self.confirm_buttons = []
        self.unlock_rect = None  # 新增解锁需求弹窗

    def heal_troops(self):
        """治疗部队方法（保持原有逻辑）"""
        success, message = game.heal_troops()
        if not success:
            print(message)
        self.refresh_buttons()

    def refresh_buttons(self):
        """仅更新治疗按钮状态"""
        self.heal_btn.hover = self.heal_btn.rect.collidepoint(pygame.mouse.get_pos())

    def draw_building(self, surface, name, data, pos):
        """绘制单个建筑元素（包含解锁状态）"""
        zh_name = self.BUILDING_NAMES.get(name, name)
        
        # 根据解锁状态调整颜色
        main_color = (100, 100, 150) if data['unlocked'] else (60, 60, 80)
        pygame.draw.rect(surface, main_color, (pos[0], pos[1], 120, 120), border_radius=10)
        
        # 未解锁建筑的特殊处理
        if not data['unlocked']:
            # 绘制锁定图标
            lock_icon = FONT_SM.render("🔒", True, (200, 200, 200))
            surface.blit(lock_icon, (pos[0]+40, pos[1]+40))
            
            # 显示建筑名称（灰色）
            name_text = FONT_SM.render(zh_name, True, (150,150,150))
            surface.blit(name_text, (pos[0]+(120-name_text.get_width())//2, pos[1]+130))
        else:
            # 等级徽章
            pygame.draw.circle(surface, (200, 200, 100), (pos[0]+100, pos[1]+20), 16)
            level_text = FONT_SM.render(str(data['level']), True, (50, 50, 50))
            surface.blit(level_text, (pos[0]+100 - level_text.get_width()//2, pos[1]+20 - level_text.get_height()//2))
            
            # 建筑名称
            name_text = FONT_SM.render(zh_name, True, COLORS["text"])
            surface.blit(name_text, (pos[0]+(120-name_text.get_width())//2, pos[1]+130))

    def draw_confirmation(self, surface):
        """绘制升级确认弹窗（新增产出变化显示）"""
        dialog_rect = pygame.Rect(300, 200, 600, 350)
        pygame.draw.rect(surface, (80, 80, 100), dialog_rect, border_radius=10)
        
        building = game.buildings[self.selected_building]
        current_level = building["level"]
        next_level = current_level + 1
        
        # 初始化y坐标
        y = 280  # 所有建筑通用的起始Y坐标
        
        # 标题
        title = FONT_MD.render(
            f"升级 {self.BUILDING_NAMES.get(self.selected_building, self.selected_building)} 到 Lv.{next_level}", 
            True, 
            (255,255,200)
        )
        surface.blit(title, (dialog_rect.centerx - title.get_width()//2, 220))
        
        # 当前和升级后的生产量（仅生产型建筑）
        if "production" in building:
            # 当前产出
            current_prod = building["production"]
            curr_text = FONT_SM.render("当前产出:", True, (200,200,200))
            surface.blit(curr_text, (320, y))
            
            # 升级后产出
            next_prod = {k: v * next_level for k, v in building["production"].items()}
            next_text = FONT_SM.render("升级后:", True, (0,200,0))
            surface.blit(next_text, (500, y))
            y += 30
            
            for res, amount in current_prod.items():
                # 当前值
                curr_amount = amount * current_level
                curr_surf = FONT_SM.render(f"{curr_amount}/s", True, (200,200,200))
                surface.blit(curr_surf, (340, y))
                
                # 升级后值
                next_amount = amount * next_level
                next_surf = FONT_SM.render(f"+{next_amount - curr_amount} → {next_amount}/s", True, (0,200,0))
                surface.blit(next_surf, (500, y))
                
                # 图标
                icon = pygame.transform.scale(ICONS[res], (25,25))
                surface.blit(icon, (300, y))
                y += 40
            y += 20  # 增加间距
        else:
            # 非生产型建筑的说明
            desc_text = FONT_SM.render("该建筑不产生资源", True, (200,200,200))
            surface.blit(desc_text, (350, y))
            y += 60

        # 资源消耗（所有建筑通用）
        cost_title = FONT_SM.render("升级需要:", True, (200,200,200))
        surface.blit(cost_title, (320, y))
        y += 30
        
        cost = {k: v * next_level for k,v in building["base_cost"].items()}
        for res, amount in cost.items():
            icon = pygame.transform.scale(ICONS[res], (25,25))
            surface.blit(icon, (320, y))
            
            color = (0,200,0) if game.resources[res] >= amount else (200,0,0)
            text = FONT_SM.render(f"{amount}", True, color)
            surface.blit(text, (350, y))
            y += 40
        
        # 确认按钮位置调整
        confirm_btn = Button((400, y+20, 120, 40), "确认升级", self.do_upgrade)
        cancel_btn = Button((600, y+20, 120, 40), "取消", self.cancel_upgrade)
        confirm_btn.draw(surface)
        cancel_btn.draw(surface)
        self.confirm_buttons = [confirm_btn, cancel_btn]

    def do_upgrade(self):
        """执行升级"""
        if game.upgrade_building(self.selected_building):
            self.selected_building = None
        self.confirm_rect = None

    def cancel_upgrade(self):
        """取消升级"""
        self.selected_building = None
        self.confirm_rect = None

    def draw_unlock_requirement(self, surface):
        """绘制解锁需求弹窗"""
        dialog_rect = pygame.Rect(300, 200, 600, 300)
        pygame.draw.rect(surface, (80, 80, 100), dialog_rect, border_radius=10)
        
        # 标题
        title = FONT_MD.render(f"解锁需求", True, (255,255,200))
        surface.blit(title, (dialog_rect.centerx - title.get_width()//2, 220))
        
        # 显示解锁条件
        y = 280
        building = game.buildings[self.selected_building]
        for req_name, req_level in building['unlock_condition'].items():
            current_level = game.buildings[req_name]['level']
            color = (0,200,0) if current_level >= req_level else (200,0,0)
            
            text = FONT_SM.render(f"{req_name} Lv{req_level}（当前：{current_level}）", True, color)
            surface.blit(text, (350, y))
            y += 40

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # 优先处理确认弹窗的按钮
                if self.confirm_buttons:
                    for btn in self.confirm_buttons:
                        if btn.rect.collidepoint(pos):
                            btn.callback()
                            return  # 确保点击弹窗按钮后不触发其他操作
                
                # 处理解锁需求弹窗
                if self.unlock_rect and self.unlock_rect.collidepoint(pos):
                    self.selected_building = None
                    self.unlock_rect = None
                    continue
                
                # 检测建筑点击（遍历所有建筑）
                col_count = 4
                start_x, start_y = 100, 100
                for i, (name, data) in enumerate(game.buildings.items()):
                    col = i % col_count
                    row = i // col_count
                    x = start_x + col * 180
                    y = start_y + row * 180
                    building_rect = pygame.Rect(x, y, 120, 150)
                    
                    if building_rect.collidepoint(pos):
                        self.selected_building = name
                        if data['unlocked']:
                            self.confirm_rect = pygame.Rect(300, 200, 600, 300)
                            self.unlock_rect = None
                        else:
                            self.unlock_rect = pygame.Rect(300, 200, 600, 300)
                            self.confirm_rect = None
                        break
                
                # 处理治疗和返回按钮
                if self.heal_btn.rect.collidepoint(pos) and game.buildings['兵营']['unlocked']:
                    self.heal_btn.callback()
                if self.back_btn.rect.collidepoint(pos):
                    self.back_btn.callback()

    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_btn.draw(surface)
        self.heal_btn.draw(surface)
        
        # 绘制所有建筑（不再过滤unlocked）
        col_count = 4
        start_x, start_y = 100, 100
        for i, (name, data) in enumerate(game.buildings.items()):
            col = i % col_count
            row = i // col_count
            x = start_x + col * 180
            y = start_y + row * 180
            self.draw_building(surface, name, data, (x, y))
        
        # 绘制解锁需求弹窗
        if self.selected_building and not game.buildings[self.selected_building]['unlocked']:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0,0))
            self.draw_unlock_requirement(surface)

        # 绘制升级确认弹窗（新增这部分）
        if self.selected_building and game.buildings[self.selected_building]['unlocked']:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0,0))
            self.draw_confirmation(surface)  # 确保调用绘制确认弹窗的方法

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

# 在Scene类之后添加新的英雄场景
class HeroScene(Scene):
    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.selected_hero = None
        self.hero_buttons = []
        self.refresh_hero_list()

    def refresh_hero_list(self):
        """刷新英雄列表"""
        self.hero_buttons = []
        y = 100
        for hero in game.party + game.city_heroes:
            btn = Button((100, y, 400, 50),
                        lambda h=hero: f"{h.name} Lv{h.level} 兵力:{h.troops} 技能:{h.skills[0]['name']}",
                        lambda h=hero: self.select_hero(h))
            self.hero_buttons.append(btn)
            y += 60

    def select_hero(self, hero):
        """选择查看英雄详情"""
        self.selected_hero = hero

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.back_btn.rect.collidepoint(pos):
                    self.back_btn.callback()
                for btn in self.hero_buttons:
                    if btn.rect.collidepoint(pos) and btn.callback:
                        btn.callback()

    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_btn.draw(surface)
        for btn in self.hero_buttons:
            btn.draw(surface)
        
        # 绘制选中英雄的详细信息
        if self.selected_hero:
            hero = self.selected_hero
            panel_rect = pygame.Rect(500, 100, 600, 500)
            pygame.draw.rect(surface, COLORS["panel"], panel_rect, border_radius=10)
            
            y = 120
            # 英雄名称
            name_text = FONT_MD.render(f"{hero.name} Lv{hero.level}", True, (255, 215, 0))
            surface.blit(name_text, (520, y))
            y += 50
            
            # 基础属性
            attrs = [
                f"兵力: {hero.troops}/{hero.max_troops}",
                f"力量: {hero.strength}",
                f"智力: {hero.intelligence}",
                f"敏捷: {hero.agility}",
                f"经验: {hero.exp}/{hero.required_exp()}"
            ]
            for attr in attrs:
                text = FONT_SM.render(attr, True, COLORS["text"])
                surface.blit(text, (520, y))
                y += 40
            
            # 技能信息
            y += 20
            skill_title = FONT_SM.render("技能列表:", True, COLORS["text"])
            surface.blit(skill_title, (520, y))
            y += 40
            for skill in hero.skills:
                skill_text = FONT_SM.render(f"{skill['name']} - {skill['scale']}", True, COLORS["text"])
                surface.blit(skill_text, (540, y))
                y += 30

class InventoryScene(Scene):
    def __init__(self):
        self.back_btn = Button((50, 600, 100, 40), "返回", lambda: game_state.change_scene(MainScene()))
        self.tabs = [
            {"name": "材料卡", "rect": pygame.Rect(150, 100, 150, 40)},
            {"name": "消耗品", "rect": pygame.Rect(350, 100, 150, 40)},
            {"name": "其他", "rect": pygame.Rect(550, 100, 150, 40)}
        ]
        self.current_tab = 0  # 当前选中标签页

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 检测标签切换
                for i, tab in enumerate(self.tabs):
                    if tab["rect"].collidepoint(pos):
                        self.current_tab = i
                # 检测返回按钮
                if self.back_btn.rect.collidepoint(pos):
                    self.back_btn.callback()

    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_btn.draw(surface)
        
        # 绘制标题
        title = FONT_MD.render("背 包", True, COLORS["text"])
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # 绘制标签页
        for i, tab in enumerate(self.tabs):
            color = (100, 100, 150) if i == self.current_tab else (60, 60, 90)
            pygame.draw.rect(surface, color, tab["rect"], border_radius=5)
            text = FONT_SM.render(tab["name"], True, (255,255,200))
            surface.blit(text, (tab["rect"].centerx - text.get_width()//2, tab["rect"].centery - text.get_height()//2))
        
        # 根据当前标签绘制内容
        if self.current_tab == 0:  # 材料卡
            self._draw_materials(surface)
        else:  # 其他标签预留位置
            tip_text = FONT_MD.render("空空如也", True, (150,150,150))
            surface.blit(tip_text, (SCREEN_WIDTH//2-60, 300))

    def _draw_materials(self, surface):
        """绘制材料卡内容（原逻辑）"""
        start_x, start_y = 100, 150
        col_spacing = 250
        row_spacing = 150
        materials = list(game.materials.items())
        
        for i, (hero_name, quantity) in enumerate(materials):
            col = i % 3
            row = i // 3
            x = start_x + col * col_spacing
            y = start_y + row * row_spacing
            
            # 材料卡背景
            pygame.draw.rect(surface, (80, 80, 100), (x, y, 200, 120), border_radius=8)
            
            # 英雄名称
            name_text = FONT_SM.render(hero_name, True, (255, 255, 200))
            surface.blit(name_text, (x + 10, y + 10))
            
            # 材料数量
            count_text = FONT_MD.render(f"×{quantity}", True, (200, 200, 0))
            surface.blit(count_text, (x + 150 - count_text.get_width(), y + 90))
            
            # 占位图标
            pygame.draw.circle(surface, (150, 150, 200), (x + 40, y + 60), 30)

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