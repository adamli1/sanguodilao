"""
游戏全局配置数据
包含技能库、英雄池、敌人模板、概率配置等
"""

# 技能库配置
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
    "yuxuechanggong": {
        "name": "浴血长虹",
        "base": 180,
        "coef": 3.5,
        "prob": 0.07,
        "scale": "strength",
        "target": "enemy",
        "effect": "连续3回合造成流血伤害，每回合损失施放者力量20%的兵力"
    },
    "fengxixiagu": {
        "name": "风袭峡谷",
        "base": 150,
        "coef": 2.8,
        "prob": 0.09,
        "scale": "agility", 
        "target": "enemy",
        "effect": "对敌方全体造成风属性伤害，30%概率附加减速"
    },
    "longyuejiuhai": {
        "name": "龙跃九霄",
        "base": 250,
        "coef": 4.0,
        "prob": 0.05,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "召唤神龙对全体敌人造成毁灭性打击"
    },
    "qianjunpomian": {
        "name": "千军破面",
        "base": 200,
        "coef": 3.2,
        "prob": 0.06,
        "scale": "strength",
        "target": "enemy",
        "effect": "对敌方前排造成贯穿伤害，无视20%防御"
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
    "shenghouzhendi": {
    "name": "声吼震地",
    "base": 100,
    "coef": 2.0,
    "prob": 0.18,
    "scale": "strength",
    "target": "enemy",
    "effect": "范围音波攻击，30%概率眩晕"
    },
    "tianluodiwang": {
        "name": "天罗地网",
        "base": 80,
        "coef": 1.5,
        "prob": 0.18,
        "scale": "agility",
        "target": "enemy",
        "effect": "束缚敌人2回合，期间无法行动"
    },
    "jueshengqianli": {
        "name": "决胜千里",
        "base": 0,
        "coef": 0,
        "prob": 0.15,
        "scale": "intelligence",
        "target": "ally",
        "effect": "提升全体友军30%暴击率，持续3回合"
    },
    "binglinsencheng": {
        "name": "兵临城下",
        "base": 120,
        "coef": 2.0,
        "prob": 0.12,
        "scale": "strength",
        "target": "enemy",
        "effect": "召唤攻城车对城墙造成额外伤害"
    },
    "xiongyongpengpai": {
        "name": "汹涌澎湃",
        "base": 100,
        "coef": 1.8,
        "prob": 0.2,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "连续3回合的海浪冲击，每回合基础伤害递增50%"
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
    "liefengruxue": {
        "name": "烈风如血",
        "base": 90,
        "coef": 1.6,
        "prob": 0.25,
        "scale": "agility",
        "target": "enemy",
        "effect": "快速突袭造成流血伤害"
    },
    "jinshengbingjie": {
        "name": "金声兵解",
        "base": 0,
        "coef": 0,
        "prob": 0.3,
        "scale": "intelligence",
        "target": "ally",
        "effect": "为全体友军施加护盾，吸收相当于智力200%的伤害"
    },
    "yanyunbuzhi": {
        "name": "烟云布阵",
        "base": 0,
        "coef": 0,
        "prob": 0.28,
        "scale": "agility",
        "target": "ally",
        "effect": "提升全军40%闪避率，持续2回合"
    },
    "langtaoxiongzhuang": {
        "name": "浪涛汹涌",
        "base": 70,
        "coef": 1.4,
        "prob": 0.3,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "对直线上的敌人造成水属性伤害"
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
    "tuijinzhanshu": {
        "name": "推进战术",
        "base": 50,
        "coef": 0.9,
        "prob": 0.35,
        "scale": "strength",
        "target": "enemy",
        "effect": "常规推进攻击，无特殊效果"
    },
    "shouchengfanji": {
        "name": "守城反击",
        "base": 60,
        "coef": 1.0,
        "prob": 0.4,
        "scale": "strength",
        "target": "self",
        "effect": "受到攻击时反弹30%伤害，持续1回合"
    },
    "xunshantulu": {
        "name": "巡山探路",
        "base": 40,
        "coef": 0.8,
        "prob": 0.45,
        "scale": "agility",
        "target": "enemy",
        "effect": "敏捷提升时伤害增加20%"
    },
    "yexiaoxiyun": {
        "name": "夜枭袭云",
        "base": 55,
        "coef": 1.1,
        "prob": 0.5,
        "scale": "agility",
        "target": "enemy",
        "effect": "夜间战斗时触发概率翻倍"
    },
    
    # 更多技能...
    "kongchengjueji": {
        "name": "空城绝计",
        "base": 150,
        "coef": 3.0,
        "prob": 0.05,
        "scale": "intelligence",
        "target": "ally",
        "effect": "当兵力低于10%时自动触发，无敌一回合"
    },
    "huolaoxiang": {
        "name": "火烧连营",
        "base": 90,
        "coef": 1.6,
        "prob": 0.18,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "对目标及相邻单位造成持续灼烧"
    },
    "bawangxiepo": {
        "name": "霸王卸甲",
        "base": 0,
        "coef": 0,
        "prob": 0.15,
        "scale": "strength",
        "target": "enemy",
        "effect": "降低目标50%防御，持续3回合"
    },
    "qishangsangong": {
        "name": "七伤三功",
        "base": 200,
        "coef": 3.5,
        "prob": 0.1,
        "scale": "strength",
        "target": "enemy",
        "effect": "自身损失当前兵力30%，造成巨额伤害"
    },
    "bawangbieji": {
        "name": "霸王别姬",
        "base": 300,
        "coef": 5.0,
        "prob": 0.03,
        "scale": "strength",
        "target": "enemy",
        "effect": "兵力低于5%时触发，造成最终一击后自身阵亡"
    },
    "wuhuqujiang": {
        "name": "五虎群将",
        "base": 0,
        "coef": 0,
        "prob": 0.08,
        "scale": "strength",
        "target": "ally",
        "effect": "召唤五虎将幻影助战，持续2回合"
    },
    "sanguoyanyi": {
        "name": "三国演义",
        "base": 0,
        "coef": 0,
        "prob": 0.1,
        "scale": "intelligence",
        "target": "ally",
        "effect": "全属性提升20%，持续到战斗结束"
    },
    "caochuanjiejian": {
        "name": "草船借箭",
        "base": 0,
        "coef": 0,
        "prob": 0.2,
        "scale": "intelligence",
        "target": "ally",
        "effect": "免疫远程攻击并反弹伤害，持续1回合"
    },
    "nujing": {
        "name": "怒目金刚",
        "base": 120,
        "coef": 2.2,
        "prob": 0.15,
        "scale": "strength",
        "target": "enemy",
        "effect": "范围震慑降低敌方攻击力20%"
    },
    "xiongyongpengpai": {
        "name": "汹涌澎湃",
        "base": 80,
        "coef": 1.5,
        "prob": 0.25,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "三回合持续水攻，每回合伤害递增"
    },
    "yuxuechanggong": {
        "name": "浴血长虹",
        "base": 90,
        "coef": 1.6,
        "prob": 0.3,
        "scale": "strength",
        "target": "enemy",
        "effect": "自身血量越低伤害越高"
    },
    "tianluodiwang": {
        "name": "天罗地网",
        "base": 0,
        "coef": 0,
        "prob": 0.2,
        "scale": "intelligence",
        "target": "enemy",
        "effect": "束缚敌人2回合"
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

# 英雄池配置
HERO_POOL = {
    "UR": [
        {
            "name": "关羽",
            "troops": 300,
            "strength": 55,
            "intelligence": 35,
            "agility": 30,
            "skill": "qinglongyanyue",
            "intro": "温酒斩华雄，千里走单骑"
        },
        {
            "name": "吕布",
            "troops": 300,
            "strength": 60,
            "intelligence": 25,
            "agility": 40,
            "skill": "wushuang",
            "intro": "三英战吕布，辕门射戟"
        },
        {
            "name": "刘备",
            "troops": 320,
            "strength": 45,
            "intelligence": 60,
            "agility": 40,
            "skill": "sanguoyanyi",  # 全队增益
            "intro": "仁德昭烈，汉室复兴"
        },
        {
            "name": "诸葛亮",
            "troops": 280,
            "strength": 30,
            "intelligence": 68,
            "agility": 42,
            "skill": "kongchengjueji",
            "intro": "鞠躬尽瘁，星落五丈原"
        }, 
        {
            "name": "张飞",
            "troops": 380,
            "strength": 66,
            "intelligence": 25,
            "agility": 45,
            "skill": "shenghouzhendi",
            "intro": "当阳怒吼，燕人张翼德"
        } 
    ],
    "SSR": [
        {
            "name": "赵云",
            "troops": 300,
            "strength": 45,
            "intelligence": 40,
            "agility": 50,
            "skill": "qijinchu",
            "intro": "长坂坡七进七出救阿斗"
        },
        {
            "name": "马超",
            "troops": 340,
            "strength": 60,
            "intelligence": 35,
            "agility": 58,
            "skill": "longyuejiuhai",
            "intro": "西凉锦马超，狮盔银铠"
        },
        {
            "name": "黄忠",
            "troops": 300,
            "strength": 58,
            "intelligence": 40,
            "agility": 50,
            "skill": "qianjunpomian",  # 破甲攻击
            "intro": "老当益壮，百步穿杨"
        },
        {
            "name": "庞统",
            "troops": 260,
            "strength": 28,
            "intelligence": 63,
            "agility": 35,
            "skill": "tianluodiwang",  # 天罗地网
            "intro": "凤雏展翼，落凤坡殒"
        },
        {
            "name": "法正",
            "troops": 270,
            "strength": 32,
            "intelligence": 60,
            "agility": 38,
            "skill": "jueshengqianli",  # 决胜千里
            "intro": "奇谋百出，定军扬威"
        },
        {
            "name": "孟获",
            "troops": 350,
            "strength": 58,
            "intelligence": 28,
            "agility": 40,
            "skill": "nujing",  # 怒目金刚
            "intro": "七擒七纵，南中称王"
        },
        {
            "name": "典韦",
            "troops": 300,
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
            "troops": 300,
            "strength": 48,
            "intelligence": 30,
            "agility": 38,
            "skill": "bashidanjing",
            "intro": "拔矢啖睛，独目仍征战"
        },
        {
            "name": "魏延",
            "troops": 300,
            "strength": 58,
            "intelligence": 45,
            "agility": 50,
            "skill": "bawangxiepo",  # 霸王卸甲
            "intro": "子午奇谋，汉中砥柱"
        },
        {
            "name": "王平",
            "troops": 280,
            "strength": 48,
            "intelligence": 52,
            "agility": 44,
            "skill": "shouchengfanji",  # 守城反击
            "intro": "无当飞军，街亭挽歌"
        },
        {
            "name": "祝融夫人",
            "troops": 280,
            "strength": 52,
            "intelligence": 35,
            "agility": 55,
            "skill": "huolaoxiang",  # 火烧连营
            "intro": "飞刀烈马，南中女杰"
        },
        {
            "name": "关兴",
            "troops": 290,
            "strength": 54,
            "intelligence": 38,
            "agility": 50,
            "skill": "liefengruxue",  # 烈风如血
            "intro": "承父遗志，再续忠魂"
        },
        {
            "name": "张苞",
            "troops": 300,
            "strength": 56,
            "intelligence": 30,
            "agility": 48,
            "skill": "xiongyongpengpai",  # 汹涌澎湃
            "intro": "猛将之后，北伐先锋"
        },
        {
            "name": "李恢",
            "troops": 260,
            "strength": 45,
            "intelligence": 50,
            "agility": 42,
            "skill": "langtaoxiongzhuang",  # 浪涛汹涌
            "intro": "说降马超，平定南中"
        },
        {
            "name": "周仓",
            "troops": 260,
            "strength": 50,
            "intelligence": 20,
            "agility": 40,
            "skill": "tuijinzhanshu",  # 推进战术
            "intro": "青龙偃月，某来扛刀"
        },
        {
            "name": "严颜",
            "troops": 250,
            "strength": 48,
            "intelligence": 45,
            "agility": 38,
            "skill": "shouchengfanji",  # 守城反击
            "intro": "但有断头将军，无降将军"
        },
        {
            "name": "霍峻",
            "troops": 240,
            "strength": 42,
            "intelligence": 50,
            "agility": 35,
            "skill": "jinshengbingjie",  # 金声兵解
            "intro": "百日守孤城，肝胆照汉室"
        },
        {
            "name": "马岱",
            "troops": 270,
            "strength": 50,
            "intelligence": 40,
            "agility": 55,
            "skill": "yexiaoxiyun",  # 夜枭袭云
            "intro": "西凉骁骑，斩除后患"
        }
    ],
    "R": [
        {
            "name": "廖化",
            "troops": 300,
            "strength": 35,
            "intelligence": 25,
            "agility": 30,
            "skill": "xunshan",
            "intro": "蜀中无大将，廖化作先锋"
        },
        {
            "name": "关银屏",
            "troops": 260,
            "strength": 46,
            "intelligence": 35,
            "agility": 52,
            "skill": "yuxuechanggong",  # 浴血长虹
            "intro": "虎女岂能嫁犬子"
        },
        {
            "name": "罗宪",
            "troops": 220,
            "strength": 40,
            "intelligence": 48,
            "agility": 30,
            "skill": "xunshan",  # 巡山探路
            "intro": "永安保卫战，独守国门"
        },
        {
            "name": "霍弋",
            "troops": 230,
            "strength": 38,
            "intelligence": 52,
            "agility": 33,
            "skill": "shouchengfanji",  # 守城反击
            "intro": "南中最后的屏障"
        },
        # === 女性武将 ===
        {
            "name": "鲍三娘",
            "troops": 240,
            "strength": 44,
            "intelligence": 28,
            "agility": 50,
            "skill": "yexiaoxiyun",  # 夜枭袭云
            "intro": "巾帼不让须眉"
        },
        {
            "name": "花鬘",
            "troops": 220,
            "strength": 35,
            "intelligence": 40,
            "agility": 55,
            "skill": "langtaoxiongzhuang",  # 浪涛汹涌
            "intro": "南蛮公主，灵巧如鹿"
        },
        {
            "name": "诸葛瞻",
            "troops": 240,
            "strength": 30,
            "intelligence": 55,
            "agility": 40,
            "skill": "jinshengbingjie",  # 金声兵解
            "intro": "绵竹死节，以报先帝"
        },
        {
            "name": "李严",
            "troops": 250,
            "strength": 42,
            "intelligence": 55,
            "agility": 38,
            "skill": "tuijinzhanshu",  # 推进战术
            "intro": "托孤重臣，粮道之争"
        }
    ]
}

# 敌人模板配置
ENEMY_TEMPLATES = {
    "小兵": {
        "base": {
            "troops": 300,
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
            "troops": 300,
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
            "troops": 300,
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

# 稀有度概率配置
RARITY_PROB = {
    "UR": 0.05,
    "SSR": 0.15,
    "SR": 0.30,
    "R": 0.50
}

def validate_skills():
    """技能配置完整性检查"""
    missing = set()
    for rarity_level in HERO_POOL.values():
        for hero in rarity_level:
            if hero["skill"] not in SKILL_LIBRARY:
                missing.add(f"{hero['name']} -> {hero['skill']}")
    
    if missing:
        print("⚠️ 发现缺失技能配置：")
        for item in missing:
            print(f"  - {item}")
    else:
        print("✅ 所有英雄技能配置完整！")

if __name__ == "__main__":
    # 执行验证
    print("\n正在验证技能配置...")
    validate_skills()
    print("验证完成。")