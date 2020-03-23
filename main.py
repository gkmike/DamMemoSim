import enum


class Character:
    def __init__(self):
        self.name = ""
        self.card_name = ""
        self.STR = 0
        self.END = 0
        self.DEX = 0
        self.AGI = 0
        self.MAG = 0


class Scope(enum.Enum):
    foe = 0
    foes = 1


class Ability(enum.Enum):
    str = 0
    mag = 1


class Attack(enum.Enum):
    none = 0
    low = 1
    mid = 2
    high = 3
    super = 4
    ultra = 5


class Attr(enum.Enum):
    none = 0
    fire = 1
    earth = 2
    wind = 3
    ice = 4
    thunder = 5
    light = 6
    dark = 7


class Killer(enum.Enum):
    bull = 0
    giant = 1
    beast = 2
    fairy = 3
    plant = 4
    bug = 5
    rock = 6
    worm = 7
    dragon = 8
    aquatic = 9
    orge = 10
    undead = 11


class Buff:
    def __init__(self):
        self.abl_up = None
        self.attr_up = None


class DeBuff:
    def __init__(self):
        self.atk_end_down = None
        self.attr_end_down = None
        self.scope_end_down = None


class Skill:
    def __init__(self):
        self.attack = Attack.none
        self.attr = Attr.none
        self.temp_boost = False
        self.buff = None
        self.debuff = None


class Adventurer(Character):
    def __init__(self):
        super().__init__()
        self.killer = None
        self.one_shot = False
        self.skill = None
        self.steps = []


class Assist(Character):
    def __init__(self):
        super().__init__()
        self.skill = None


class Enemy:
    def __init__(self):
        self.type = None
        self.attr_end = None
        self.atk_end = None
        self.scope_end = None
        self.skills_predefined = None


class Team:
    def __init__(self):
        self.members = None


class ScoreBoard:
    def __init__(self):
        self.player_team = None
        self.enemy_team = None
        self.round_dmg = []
    def calc(self):
        pass


ROUNDS = 2
player_team = None
enemy_team = None

