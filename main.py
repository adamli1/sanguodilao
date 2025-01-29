from game_mechanics import Game
from config import validate_skills
from battle import BattleSystem

def main_loop():
    game = Game()
    game.start_production_timer()

    while True:
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
            game.stop_production_timer()
            break

if __name__ == "__main__":
    validate_skills()
    main_loop()