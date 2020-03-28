import enum
from itertools import permutations
import copy

class Character:
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val):
        self.name = name
        self.str = str_val 
        self.end = end_val
        self.dex = dex_val
        self.agi = agi_val
        self.mag = mag_val


class Scope(enum.Enum):
    foe = 0
    foes = 1
    my_self = 2
    my_team = 3


class Ability(enum.Enum):
    none = 0
    str = 1
    mag = 2

class Attack(enum.Enum):
    none = 0
    phy = 1
    mag = 2

#class Attr(enum.Enum):
#    fire = 1
#    earth = 2
#    wind = 3
#    ice = 4
#    thunder = 5
#    light = 6
#    dark = 7

class Damage(enum.Enum):
    str = 0
    mag = 1
    fire = 2
    earth = 3
    wind = 4
    ice = 5
    thunder = 6
    light = 7
    dark = 8
    foe = 9
    foes = 10

class Endurance(enum.Enum):
    str = 0
    mag = 1
    fire = 2
    earth = 3
    wind = 4
    ice = 5
    thunder = 6
    light = 7
    dark = 8
    foe = 9
    foes = 10

class Power(enum.Enum):
    none = 0
    low = 1
    mid = 2
    high = 3
    super = 4
    ultra = 5

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

class SpecialPolicy(enum.Enum):
    harumime_first = 0
    single_asap = 1
    double_asap = 2
    triple_asap = 3
    max = 4


def get_coeff(scope, power):
    coeff = 0
    coeff_tmp_boost = 0
    if power == Power.none or power == None:
        return coeff, coeff_tmp_boost
    if scope == Scope.foe:
        if power == Power.low:
            coeff = 3
        elif power == Power.mid:
            coeff = 3.4
            coeff_tmp_boost = 0.2
        elif power == Power.high:
            coeff = 3.8
            coeff_tmp_boost = 0.3
        elif power == Power.super:
            coeff = 4.2
            coeff_tmp_boost = 0.3
        elif power == Power.ultra:
            coeff = 8
            coeff_tmp_boost = 0.4

    elif scope == Scope.foes:
        if power == Power.low:
            coeff = 2.2
        elif power == Power.mid:
            coeff = 2.3
            coeff_tmp_boost = 0.4
        elif power == Power.high:
            coeff = 2.4
            coeff_tmp_boost = 0.4
        elif power == Power.super:
            coeff = 2.8
            coeff_tmp_boost = 0.4
        elif power == Power.ultra:
            coeff = 7.2
            coeff_tmp_boost = 0.4
    else:
        raise ValueError
    return coeff, coeff_tmp_boost

class Skill:
    def __init__(self, scope=None, power=None, attr_dmg=None, attack=None, **kwargs ):
        self.power = power
        self.attack = attack
        self.attr_dmg = attr_dmg
        if attr_dmg:
            self.attr_end_ref = Endurance(attr_dmg.value)
        self.scope = scope
        self.temp_boost = kwargs.get("temp_boost", False)
        self.buffs = kwargs.get("buffs", None)
        self.debuffs = kwargs.get("debuffs", None)
        self.extend_buffs = kwargs.get("extend_buffs", None)
        self.extend_debuffs = kwargs.get("extend_debuffs", None)
        self.shorten_buffs = kwargs.get("shorten_buffs", None)
        self.shorten_debuffs = kwargs.get("shorten_debuffs", None)
        self.idx = None
        self.coeff = 0
        self.coeff_tmp_boost = 0
        self.coeff, self.coeff_tmp_boost = get_coeff(self.scope, self.power)

class Adventurer(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val)
        self.killer = None ## TODO
        self.one_shot = False ## TODO
        self.skills = kwargs.get("skills", None)
        #self.skills = [s for s in self.skills if s is not None]
        self.passive_skill = None ## TODO
        self.steps_record = []
        self.stages_dmg_record = []
        self.total_dmg = 0

        self.got_buff = dict()
        self.got_debuff = dict()
        self.passive_buff = dict()
        self.passive_debuff = dict()
        self.assist_buff = dict()
        self.assist_debuff = dict()
        for buffs in [Ability, Damage, Endurance]:
            for buff in buffs:
                self.got_buff[buff] = [0, 0]
                self.got_debuff[buff] = [0, 0]
                self.passive_buff[buff] = 0
                self.passive_debuff[buff] = 0
                self.assist_buff[buff] = 0
                self.assist_debuff[buff] = 0

        self.assist = None

        self.skill_policy = None
        self.my_team = None
        self.selected_skill = None

    def set_assist(self, assist):
        self.assist = assist

    def need_buff(self, kind, value):
        return self.need_skill_effect(self.got_buff, kind, value)
    
    def need_debuff(self, kind, value):
        return self.need_skill_effect(self.got_debuff, kind, value)

    def need_skill_effect(self, look_up, kind, value):
        cur_value = look_up[kind][0]
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
            if s.power == Power.ultra:
                self.selected_skill = s
            elif s.power == Power.super:
                self.selected_skill = s
            elif s.power == Power.high:
                self.selected_skill = s
            elif s.power == Power.mid:
                self.selected_skill = s
            elif s.power == Power.low:
                self.selected_skill = s
            else:
                raise ValueError

    def act(self):
        s = self.selected_skill
        dmg = 0
        if s.power != Power.none:
            foes_on_stage = self.my_team.opponent_team.members_on_stage
            foe_on_stage = foes_on_stage[0]
            atk = 0
            if s.attack == Attack.phy:
                atk = self.str
                abl_up = self.got_buff[Ability.str][0]
            elif s.attack == Attack.mag:
                atk = self.mag
                abl_up = self.got_buff[Ability.mag][0]
            else:
                raise ValueError

            attr_dmg_up = self.got_buff[s.attr_dmg][0]

            if s.scope == Scope.foe:
                scope_dmg_up = foe_on_stage.got_debuff[Damage.foe][0]
                attr_end_down = foe_on_stage.got_debuff[s.attr_end_ref][0]
                dmg = (atk * (1 + abl_up)
                           * (1 + attr_dmg_up)
                           * (1 + s.coeff_tmp_boost)
                           * (1 + scope_dmg_up)
                           * (1 + attr_end_down)
                       ) * s.coeff
            else:
                for f in foes_on_stage:
                    scope_dmg_up = f.got_debuff[Damage.foes][0]
                    attr_end_down = f.got_debuff[s.attr_end_ref][0]
                    dmg += (atk * (1 + abl_up)
                           * (1 + attr_dmg_up)
                           * (1 + s.coeff_tmp_boost)
                           * (1 + scope_dmg_up)
                           * (1 + attr_end_down)
                           ) * s.coeff
        self.stages_dmg_record.append(dmg)
        self.total_dmg += dmg
        return dmg



class Assist(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val)
        self.skill = kwargs.get("skill")


class Team:
    def __init__(self, members):
        self.opponent_team = None
        self.members = members
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
            #print(f"{m.name}\n => 招{m.selected_skill.idx}: 傷害{dmg}")
            all_dmg += dmg
        #print(f"回合總傷害: {all_dmg}")
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
                if s:
                    s.idx = idx + 1
        for i in range(self.rounds):
            #print(f"round {i}")
            self.player_team.select_skills()
            dmg = self.player_team.act()
            #print("=" * 60)
        #print("\n\n")
        #print("*" * 60)
        for p in self.player_team.members:
            pass
            #print(f"{p.name}\n 總傷害{p.total_dmg}")

my_ass_cards = [
    Assist("aa", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
    Assist("bb", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
    Assist("cc", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
    Assist("dd", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
]

my_one_shot_ass_cards = [
    Assist("ee", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
    Assist("ff", 1, 2, 3, 4, 5, skill=Skill(buffs=[] ) ),
]
my_one_shot_adv_cards = [
    Adventurer("新裝艾斯",2133, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.super, Damage.ice, Attack.phy)]
               ),
    Adventurer("英雄阿爾戈", 2108, 0, 0, 0, 0,
               skills = [Skill(Scope.foes, Power.super, Damage.fire, Attack.phy)]
               ),
]

my_adv_cards = [
    Adventurer("新裝艾斯",2133, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.super, Damage.ice, Attack.phy)]
               ),
    Adventurer("英雄阿爾戈", 2108, 0, 0, 0, 0,
               skills = [Skill(Scope.foes, Power.super, Damage.fire, Attack.phy)]
               ),
    Adventurer("聖誕千草", 2011, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.super, Damage.ice, Attack.phy)]
               ),
    Adventurer("米卡莎", 1928, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎2", 1928, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎3", 1928, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎4", 1928, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎5", 1928, 0, 0, 0, 0,
               skills = [Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
]
cnt = 0
print(f"模擬中...")
for advs in permutations(my_adv_cards, 4):
    for advs_one_shot in permutations(my_one_shot_adv_cards, 2):
        for asses in permutations(my_ass_cards, 4):
            for asses_one_shot in permutations(my_one_shot_ass_cards, 2):
                cnt += 1
                continue
                #print("")
                advs = copy.deepcopy(advs)
                advs_one_shot = copy.deepcopy(advs_one_shot)
                asses = copy.deepcopy(asses)
                asses_one_shot = copy.deepcopy(asses_one_shot)
                for adv, ass in zip(advs, asses):
                    adv.set_assist(ass)
                for adv, ass in zip(advs_one_shot, asses_one_shot):
                    adv.set_assist(ass)
                members = list(advs[0:3])
                members.extend(advs_one_shot)
                members.append(advs[3])

                my_team = Team(members)

                battle = BattleStage(1)
                battle.add_player_team(my_team)
                battle.add_enemy_team(my_team)
                battle.run()

print(f"總共{cnt}總組合.")
print(f"最佳組合是")
