import enum
from itertools import permutations, combinations
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
    energy_bar = 3


class Attack(enum.Enum):
    none = 0
    phy = 1
    mag = 2


# class Attr(enum.Enum):
#    fire = 1
#    earth = 2
#    wind = 3
#    ice = 4
#    thunder = 5
#    light = 6
#    dark = 7


class Damage(enum.Enum):
    phy = 0
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
    if power is None:
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


class Effect:
    def __init__(self, scope, effect_enum, value, turns=None):
        self.scope = scope
        self.effect_enum = effect_enum
        self.value = value
        self.turns = turns


class Skill:
    def __init__(self, scope=None, power=None, attr_dmg=None, attack=None, **kwargs):
        self.power = power
        self.attack = attack
        self.attr_dmg = attr_dmg
        if attr_dmg:
            self.attr_end_ref = Endurance(attr_dmg.value)
        self.scope = scope
        self.temp_boost = kwargs.get("temp_boost", False)
        self.buffs = kwargs.get("buffs", [])
        self.debuffs = kwargs.get("debuffs", [])
        self.extend_buffs = kwargs.get("extend_buffs", None)
        self.extend_debuffs = kwargs.get("extend_debuffs", None)
        self.shorten_buffs = kwargs.get("shorten_buffs", None)
        self.shorten_debuffs = kwargs.get("shorten_debuffs", None)
        self.is_special = kwargs.get("is_special", False)
        self.idx = None
        self.coeff = 0
        self.coeff_tmp_boost = 0
        self.coeff, self.coeff_tmp_boost = get_coeff(self.scope, self.power)


class Adventurer(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val)
        self.killer = None  ## TODO
        self.one_shot = False  ## TODO
        self.skills = kwargs.get("skills", None)
        # self.skills = [s for s in self.skills if s is not None]
        self.passive_skill = None  ## TODO
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

        self.skill_policy = None ## TODO
        self.my_team = None
        self.selected_skill = None

    def reset(self):
        self.steps_record = []
        self.stages_dmg_record = []
        self.total_dmg = 0
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
        self.selected_skill = None

    def set_assist(self, assist):
        self.assist = assist
        assist.my_adv = self
        assist.my_team = self.my_team

    def need_buff(self, effect):
        return self.need_skill_effect(self.got_buff, effect)

    def need_debuff(self, effect):
        return self.need_skill_effect(self.got_debuff, effect)

    def need_skill_effect(self, look_up, effect):
        kind = effect.effect_enum
        value = effect.value
        cur_value = look_up[kind][0]
        if value > cur_value:
            return True
        else:
            return False

    def select_skill(self, special_avail):
        if self.skill_policy == SkillPolicy.buff:
            for s in self.skills:
                if special_avail is False and s.is_special:
                    continue
                for effect in s.buffs:
                    if effect.scope == Scope.foes:
                        if self.my_team.need_buff(effect):
                            self.selected_skill = s
                            return
                    else:
                        if self.need_buff(effect):
                            self.selected_skill = s
                            return
        for s in self.skills:
            if s.power == Power.ultra:
                if special_avail:
                    self.selected_skill = s
            elif s.power == Power.super:
                self.selected_skill = s
            elif s.power == Power.high:
                self.selected_skill = s
            elif s.power == Power.mid:
                self.selected_skill = s
            elif s.power == Power.low:
                self.selected_skill = s
            elif s.power is None:
                self.selected_skill = s
            else:
                raise ValueError

    def act(self):
        s = self.selected_skill
        self.steps_record.append(s.idx)
        dmg = 0
        foes_on_stage = self.my_team.opponent_team.members_on_stage
        foe_on_stage = foes_on_stage[0]
        if s.power is not None:
            if s.attack == Attack.phy:
                atk = self.str + self.assist.str
                abl_up = self.calc_buff_value(Ability.str)
                enum_atk_end = Damage.phy
            elif s.attack == Attack.mag:
                atk = self.mag + self.assist.mag
                abl_up = self.calc_buff_value(Ability.mag)
                enum_atk_end = Damage.mag
            else:
                raise ValueError

            attr_dmg_up = self.calc_buff_value(s.attr_dmg)

            if s.scope == Scope.foe:
                foe_end_down = foe_on_stage.calc_debuff_value(Damage.foe)
                attr_end_down = foe_on_stage.calc_debuff_value(s.attr_end_ref)
                attr_end_up = foe_on_stage.calc_buff_value(s.attr_end_ref)
                atk_end_down = foe_on_stage.calc_debuff_value(enum_atk_end)
                end = foe_on_stage.end
                dmg = ((atk * (1 + abl_up) * (1 + s.coeff_tmp_boost) - end * (1 + attr_end_up))
                       * s.coeff
                       * (1 + attr_dmg_up)
                       * (1 + attr_end_down + atk_end_down)
                       * (1 + foe_end_down)
                       )
            else:
                for f in foes_on_stage:
                    foe_end_down = f.calc_debuff_value(Damage.foe)
                    attr_end_down = f.calc_debuff_value(s.attr_end_ref)
                    attr_end_up = f.calc_buff_value(s.attr_end_ref)
                    atk_end_down = f.calc_debuff_value(enum_atk_end)
                    end = f.end
                    dmg = ((atk * (1 + abl_up) * (1 + s.coeff_tmp_boost) - end * (1 + attr_end_up))
                           * s.coeff
                           * (1 + attr_dmg_up)
                           * (1 + attr_end_down + atk_end_down)
                           * (1 + foe_end_down)
                           )
        self.stages_dmg_record.append(dmg)
        self.total_dmg += dmg

        for buff in s.buffs:
            if buff.scope == Scope.my_team:
                for m in self.my_team.members_on_stage:
                    m.set_buff(buff)
            elif buff.scope == Scope.my_self:
                self.set_buff(buff)
            else:
                raise ValueError

        for debuff in s.debuffs:
            if debuff.scope == Scope.foes:
                for f in foes_on_stage:
                    f.set_debuff(debuff)
            elif debuff.scope == Scope.foe:
                foe_on_stage.set_debuff(debuff)
            else:
                raise ValueError

        energy_bar_boost = self.got_buff[Ability.energy_bar][0]
        self.my_team.inc_energy_bar(1 + energy_bar_boost)

        return dmg

    def calc_buff_value(self, effect):
        v0 = self.got_buff[effect][0]
        v1 = self.passive_buff[effect]
        v2 = self.assist_buff[effect]
        return v0 + v1 + v2

    def calc_debuff_value(self, effect):
        v0 = self.got_debuff[effect][0]
        v1 = self.passive_debuff[effect]
        v2 = self.assist_debuff[effect]
        return v0 + v1 + v2

    def set_effect(self, item, effect):
        kind = effect.effect_enum
        value = effect.value
        turns = effect.turns
        if turns is None:
            if value > item[kind]:
                item[kind] = value
        else:
            cur_value = item[kind][0]
            cur_turns = item[kind][1]
            if value > cur_value:
                item[kind] = [value, turns]
            else:
                if turns > cur_turns:
                    item[kind] = [value, turns]

    def set_buff(self, effect):
        self.set_effect(self.got_buff, effect)

    def set_assit_buff(self, effect):
        self.set_effect(self.assist_buff, effect)

    def set_debuff(self, effect):
        self.set_effect(self.got_debuff, effect)

    def set_assist_debuff(self, effect):
        self.set_effect(self.assist_debuff, effect)

    def effect_next(self, item):
        item_val = item[0]
        item_turn = item[1]
        if item_turn == 0:
            return
        elif item_turn == 1:
            item[0] = 0
            item[1] = 0
        else:
            item[0] = item_val
            item[1] = item_turn - 1

    def next_turn(self):
        for effects_enum in [Ability, Damage, Endurance]:
            for effect_enum in effects_enum:
                buff = self.got_buff[effect_enum]
                debuff = self.got_debuff[effect_enum]
                self.effect_next(buff)
                self.effect_next(debuff)


class Assist(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val)
        self.skill = kwargs.get("skill")
        self.my_team = None
        self.my_adv = None

    def act(self):
        for buff in self.skill.buffs:
            if buff.scope == Scope.my_team:
                for m in self.my_team.members_on_stage:
                    m.set_assit_buff(buff)
            elif buff.scope == Scope.my_self:
                self.my_adv.set_assit_buff(buff)
            else:
                raise ValueError

        for debuff in self.skill.debuffs:
            if debuff.scope == Scope.foes:
                for f in self.my_team.opponent_team.members_on_stage:
                    f.set_assist_debuff(debuff)
            elif debuff.scope == Scope.foe:
                raise ValueError
            else:
                raise ValueError


class Team:
    def __init__(self, members):
        self.opponent_team = None
        self.members = members
        for m in self.members:
            m.my_team = self
        self.members_on_stage = self.members[0: 4]
        self.hit_dmg_rounds = []
        self.got_dmg_rounds = []
        self.total_dmg = 0
        self.energy_bar = 0

    def select_skills(self):
        for m in self.members_on_stage:
            sv = self.max_special_moves()
            if sv > 0:
                has_sv = True
            else:
                has_sv = False
            m.select_skill(has_sv)
            if m.selected_skill.is_special:
                self.dec_energy_bar()

    def need_buff(self, buff):
        for m in self.members_on_stage:
            if m.need_buff(buff):
                return True
        return False

    def act(self):
        all_dmg = 0
        for m in self.members_on_stage:
            dmg = m.act()
            # print(f"{m.name}\n => 招{m.selected_skill.idx}: 傷害{dmg}")
            all_dmg += dmg
        # print(f"回合總傷害: {all_dmg}")
        self.total_dmg += all_dmg
        return all_dmg

    def show_result(self):
        for i, m in enumerate(members):
            print(f"{i + 1}:")
            print(f"    {m.name} + {m.assist.name} : {int(m.total_dmg):,} ({m.total_dmg / self.total_dmg * 100:,.0f}%)")
            print(f"    招式順序: {m.steps_record}")
        print(f"\n總傷害:{int(self.total_dmg):,}")
        print("=" * 60)

    def next_turn(self):
        for m in self.members_on_stage:
            m.next_turn()

    def reset(self):
        for m in self.members:
            m.reset()

    def inc_energy_bar(self, num):
        self.energy_bar += num
        if self.energy_bar > 60:
            self.energy_bar = 60

    def max_special_moves(self):
        return int(self.energy_bar / 15)

    def dec_energy_bar(self):
        self.energy_bar -= 15
        if self.energy_bar < 0:
            raise ValueError

    def init(self):
        for m in self.members_on_stage:
            if m.assist:
                m.assist.act()


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
        self.player_team.init()
        self.enemy_team.init()
        for p in self.player_team.members:
            for idx, s in enumerate(p.skills):
                if s:
                    s.idx = idx + 1
        for i in range(self.rounds):
            # print(f"round {i}")
            self.player_team.select_skills()
            self.player_team.act()
            self.player_team.next_turn()
            self.enemy_team.next_turn()
            # print("=" * 60)
        # print("\n\n")
        # print("*" * 60)
        # for p in self.player_team.members:
        #   pass
        # print(f"{p.name}\n 總傷害{p.total_dmg}")


my_ass_cards = [
    Assist("劇場乳神", 643 + 77, 0, 0, 0, 289,
           skill=Skill(debuffs=[Effect(Scope.foes, Damage.foe, 0.15)])
           ),
    Assist("月神", 571 + 72, 0, 0, 0, 284,
           skill=Skill(buffs=[Effect(Scope.my_self, Ability.str, 0.15), Effect(Scope.my_team, Ability.str, 0.10)])
           ),
    Assist("泳裝芙蕾雅", 461, 0, 0, 0, 441,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.ice, 0.10)])
           ),
    Assist("製作人荷米斯1", 459, 0, 0, 0, 459,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.fire, 0.10), Effect(Scope.my_team, Damage.light, 0.10)])
           ),
    Assist("製作人荷米斯2", 459, 0, 0, 0, 459,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.fire, 0.10), Effect(Scope.my_team, Damage.light, 0.10)])
           ),
    Assist("製作人荷米斯3", 459, 0, 0, 0, 459,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.fire, 0.10), Effect(Scope.my_team, Damage.light, 0.10)])
           ),
]
my_one_shot_adv_cards = [
    Adventurer("新裝艾斯1", 2133, 0, 0, 0, 0,
               skills=[
                   Skill(
                       buffs=[Effect(Scope.my_self, Damage.ice, 0.60, 4), Effect(Scope.my_self, Ability.str, 0.60, 4)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Damage.ice, 0.80, 4), Effect(Scope.my_self, Ability.str, 0.80, 4)]
                         ),
               ]),
    Adventurer("新裝艾斯2", 2133, 0, 0, 0, 0,
               skills=[
                   Skill(
                       buffs=[Effect(Scope.my_self, Damage.ice, 0.60, 4), Effect(Scope.my_self, Ability.str, 0.60, 4)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Damage.ice, 0.80, 4), Effect(Scope.my_self, Ability.str, 0.80, 4)]
                         ),
               ]),
]

my_adv_cards = [
    Adventurer("新裝艾斯", 2133, 0, 0, 0, 0,
               skills=[
                   Skill(
                       buffs=[Effect(Scope.my_self, Damage.ice, 0.60, 4), Effect(Scope.my_self, Ability.str, 0.60, 4)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Damage.ice, 0.80, 4), Effect(Scope.my_self, Ability.str, 0.80, 4)]
                         ),
               ]),
    Adventurer("英雄阿爾戈", 2108, 0, 0, 0, 0,
               skills=[Skill(Scope.foes, Power.super, Damage.fire, Attack.phy)]
               ),
    Adventurer("聖誕千草", 2011, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.super, Damage.ice, Attack.phy)]
               ),
    Adventurer("米卡莎", 1928, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎2", 1928, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎3", 1928, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎4", 1928, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
    Adventurer("米卡莎5", 1928, 0, 0, 0, 0,
               skills=[Skill(Scope.foe, Power.high, Damage.dark, Attack.phy)]
               ),
]
cnt = 0
best_team = None
print(f"模擬中...")

boss_1 = Adventurer("九魔姬", 0, 100, 0, 0, 1000,
                    skills=[Skill(Scope.foes, Power.high, Damage.dark, Attack.mag)]
                    )
enemy_team = Team([boss_1])


def check_team_valid(team1, team2):
    for m1 in team1:
        for m2 in team2:
            if m1.name == m2.name:
                return False
    return True


for asses in combinations(my_ass_cards, 6):
    for advs in permutations(my_adv_cards, 4):
        for advs_one_shot in combinations(my_one_shot_adv_cards, 2):
            if check_team_valid(advs, advs_one_shot) is False:
                continue
            cnt += 1
            members = list(advs[0:3])
            members.extend(advs_one_shot)
            members.append(advs[3])

            my_team = Team(members)
            my_team.reset()
            enemy_team.reset()

            for adv, ass in zip(members, asses):
                adv.set_assist(ass)
                adv.skill_policy = SkillPolicy.buff

            battle = BattleStage(9)
            battle.add_player_team(my_team)
            battle.add_enemy_team(enemy_team)
            battle.run()

            if best_team is None:
                best_team = my_team
            else:
                if my_team.total_dmg > best_team.total_dmg:
                    best_team = copy.deepcopy(my_team)

print(f"總共{cnt}總組合.")
print(f"最佳組合是:")
best_team.show_result()
