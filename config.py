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
    """验证技能配置完整性"""
    missing = set()
    for rarity, heroes in HERO_POOL.items():
        for hero in heroes:
            if hero["skill"] not in SKILL_LIBRARY:
                missing.add(hero["skill"])
    if missing:
        print(f"缺失技能配置：{', '.join(missing)}")
    else:
        print("所有技能配置完整！")