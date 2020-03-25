import enum


class Character:
    def __init__(self):
        self.name = ""
        self.card_name = ""
        self.str = 0
        self.end = 0
        self.dex = 0
        self.agi = 0
        self.mag = 0


class Scope(enum.Enum):
    foe = 0
    foes = 1


class Ability(enum.Enum):
    none = 0
    str = 1
    mag = 2


class Endurance(enum.Enum):
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


class SkillPolicy(enum.Enum):
    buff = 0
    debuff = 1
    extend_buff = 2
    extend_debuff = 3

class Skill:
    def __init__(self):
        self.attack = Attack.none
        self.ability = None
        self.attr = Attr.none
        self.scope = None
        self.temp_boost = False
        self.buffs = None
        self.debuffs = None
        self.idx = None

def get_coeff(scope, attack):
    coeff = 0
    coeff_tmp = 0
    if scope == Scope.foe:
        if attack == Attack.low:
            coeff = 3
        elif attack == Attack.mid:
            coeff = 3.4
            coeff_tmp = 0.2
        elif attack == Attack.high:
            coeff = 3.8
            coeff_tmp = 0.3
        elif attack == Attack.super:
            coeff = 4.2
            coeff_tmp = 0.3
        elif attack == Attack.ultra:
            coeff = 8
            coeff_tmp = 0.4

    elif scope == Scope.foes:
        if attack == Attack.low:
            coeff = 2.2
        elif attack == Attack.mid:
            coeff = 2.3
            coeff_tmp = 0.4
        elif attack == Attack.high:
            coeff = 2.4
            coeff_tmp = 0.4
        elif attack == Attack.super:
            coeff = 2.8
            coeff_tmp = 0.4
        elif attack == Attack.ultra:
            coeff = 7.2
            coeff_tmp = 0.4
    else:
        raise ValueError
    return coeff, coeff_tmp

class Adventurer(Character):
    def __init__(self):
        super().__init__()
        self.killer = None
        self.one_shot = False
        self.skills = None
        self.passive_skill = None
        self.steps = []
        self.stages_dmg = []
        self.total_dmg = 0

        self.got_buff = dict()
        self.got_buff[Ability.str] = [0, 0]
        self.got_buff[Ability.mag] = [0, 0]
        self.got_buff[Attr.fire] = [0, 0]
        self.got_buff[Attr.earth] = [0, 0]
        self.got_buff[Attr.wind] = [0, 0]
        self.got_buff[Attr.ice] = [0, 0]
        self.got_buff[Attr.thunder] = [0, 0]
        self.got_buff[Attr.light] = [0, 0]
        self.got_buff[Attr.dark] = [0, 0]

        self.passive_buff = dict()
        self.passive_buff[Ability.str] = 0
        self.passive_buff[Ability.mag] = 0
        self.passive_buff[Attr.fire] = 0
        self.passive_buff[Attr.earth] = 0
        self.passive_buff[Attr.wind] = 0
        self.passive_buff[Attr.ice] = 0
        self.passive_buff[Attr.thunder] = 0
        self.passive_buff[Attr.light] = 0
        self.passive_buff[Attr.dark] = 0

        self.got_debuff = dict()
        self.got_debuff[Scope.foe] = [0, 0]
        self.got_debuff[Scope.foes] = [0, 0]
        self.got_debuff[Endurance.str] = [0, 0]
        self.got_debuff[Endurance.mag] = [0, 0]
        self.got_debuff[Attr.fire] = [0, 0]
        self.got_debuff[Attr.earth] = [0, 0]
        self.got_debuff[Attr.wind] = [0, 0]
        self.got_debuff[Attr.ice] = [0, 0]
        self.got_debuff[Attr.thunder] = [0, 0]
        self.got_debuff[Attr.light] = [0, 0]
        self.got_debuff[Attr.dark] = [0, 0]

        self.passive_debuff = dict()
        self.passive_debuff[Endurance.str] = 0
        self.passive_debuff[Endurance.mag] = 0
        self.passive_debuff[Attr.fire] = 0
        self.passive_debuff[Attr.earth] = 0
        self.passive_debuff[Attr.wind] = 0
        self.passive_debuff[Attr.ice] = 0
        self.passive_debuff[Attr.thunder] = 0
        self.passive_debuff[Attr.light] = 0
        self.passive_debuff[Attr.dark] = 0

        self.skill_policy = None
        self.my_team = None
        self.selected_skill = None

    def need_buf(self, buff):
        kind = buff[0]
        value = buff[1]
        round = buff[2]
        cur_value = self.got_buff[kind][0]
        if value > cur_value:
            return True
        else:
            return False

    def select_skill(self):
        if self.skill_policy == SkillPolicy.buff:
            for s in self.skills:
                if s.buffs:
                    for b in s.buffs:
                        if b.scope == Scope.foes:
                            if self.my_team.need_buff(b):
                                self.selected_skill = s
                                return
                        else:
                            if self.need_buf(b):
                                self.selected_skill = s
                                return
        for s in self.skills:
            if s.attack == Attack.ultra:
                self.selected_skill = s
            elif s.attack == Attack.super:
                self.selected_skill = s
            elif s.attack == Attack.high:
                self.selected_skill = s
            elif s.attack == Attack.mid:
                self.selected_skill = s
            elif s.attack == Attack.low:
                self.selected_skill = s
            else:
                raise ValueError


    def act(self):
        s = self.selected_skill
        dmg = 0
        if s.attack != Attack.none:
            foes_on_stage = self.my_team.opponent_team.members_on_stage
            foe_on_stage = foes_on_stage[0]
            atk = 0
            if s.ability == Ability.str:
                atk = self.str
            elif s.ability == Ability.mag:
                atk = self.mag
            else:
                raise ValueError

            abl_up = self.got_buff[s.ability][0]
            attr_up = self.got_buff[s.attr][0]
            coeff, coeff_tmp = get_coeff(s.scope, s.attack)

            if s.scope == Scope.foe:
                scope_dmg_up = foe_on_stage.got_debuff[s.scope][0]
                attr_dmg_up = foe_on_stage.got_debuff[s.attr][0]
                dmg = (atk * (1 + abl_up)
                           * (1 + attr_up)
                           * (1 + coeff_tmp)
                           * (1 + scope_dmg_up)
                           * (1 + attr_dmg_up)
                       ) * coeff
            else:
                for f in foes_on_stage:
                    scope_dmg_up = f.got_debuff[s.scope][0]
                    attr_dmg_up = f.got_debuff[s.attr][0]
                    dmg += (atk * (1 + abl_up)
                           * (1 + attr_up)
                           * (1 + coeff_tmp)
                           * (1 + scope_dmg_up)
                           * (1 + attr_dmg_up)
                           ) * coeff
        self.stages_dmg.append(dmg)
        self.total_dmg += dmg
        return dmg



class Assist(Character):
    def __init__(self):
        super().__init__()
        self.passive_skill = None


class Team:
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.opponent_team = None
        self.members = [p1, p2, p3, p4, p5, p6]
        for m in self.members:
            m.my_team = self
        self.members_on_stage = self.members[0: 4]
        self.hit_dmg_rounds = []
        self.got_dmg_rounds = []

    def select_skills(self):
        for m in self.members_on_stage:
            m.select_skill()

    def need_buff(self, buff):
        for m in self.members_on_stage:
            if m.need_buff(buff):
                return True
        return False

    def act(self):
        all_dmg = 0
        for m in self.members_on_stage:
            dmg = m.act()
            print(f"{m.name}({m.card_name})\n => 招{m.selected_skill.idx}: 傷害{dmg}")
            all_dmg += dmg
        print(f"回合總傷害: {all_dmg}")
        return all_dmg


class BattleStage:
    def __init__(self, rounds):
        self.rounds = rounds
        self.player_team = None
        self.enemy_team = None

    def add_player_team(self, team):
        self.player_team = team

    def add_enemy_team(self, team):
        self.enemy_team = team

    def run(self):
        self.player_team.opponent_team = self.enemy_team
        self.enemy_team.opponent_team = self.player_team
        for p in self.player_team.members:
            for idx, s in enumerate(p.skills):
                s.idx = idx + 1
        for i in range(self.rounds):
            print(f"round {i}")
            self.player_team.select_skills()
            dmg = self.player_team.act()
            print("=" * 60)
        print("\n\n")
        print("*" * 60)
        for p in self.player_team.members:
            print(f"{p.name}({p.card_name})\n 總傷害{p.total_dmg}")


p1 = Adventurer()
p1.name = "艾斯"
p1.card_name = "新裝銳氣"
p1.str = 2133
skill_1 = Skill()
skill_1.attack = Attack.super
skill_1.ability = Ability.str
skill_1.scope = Scope.foe
skill_1.attr = Attr.ice
p1.skills = [skill_1]

p2 = Adventurer()
p2.name = "阿爾戈"
p2.card_name = "始源英雄"
p2.str = 2108
skill_1 = Skill()
skill_1.attack = Attack.super
skill_1.ability = Ability.str
skill_1.scope = Scope.foes
skill_1.attr = Attr.fire
p2.skills = [skill_1]

p3 = Adventurer()
p3.name = "千草"
p3.card_name = "聖誕"
p3.str = 2011
skill_1 = Skill()
skill_1.attack = Attack.super
skill_1.ability = Ability.str
skill_1.scope = Scope.foes
skill_1.attr = Attr.ice
p3.skills = [skill_1]

p4 = Adventurer()
p4.name = "米卡莎"
p4.card_name = "訓練兵首席"
p4.str = 1928
skill_1 = Skill()
skill_1.attack = Attack.high
skill_1.ability = Ability.str
skill_1.scope = Scope.foe
skill_1.attr = Attr.dark
p4.skills = [skill_1]

my_team = Team(p1, p2, p3, p4, p1, p1)

battle = BattleStage(16)
battle.add_player_team(my_team)
battle.add_enemy_team(my_team)
battle.run()
