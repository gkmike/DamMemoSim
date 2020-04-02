# import enum
from itertools import permutations, combinations
import copy
import time


class Character:
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        self.tags = kwargs.get("tags", [])
        self.name = name
        self.str = str_val
        self.end = end_val
        self.dex = dex_val
        self.agi = agi_val
        self.mag = mag_val


class Scope:
    foe = "Scope.foe"
    foes = "Scope.foes"
    my_self = "Scope.my_self"
    my_team = "Scope.my_team"


class Ability:
    str = "Ability.str"
    mag = "Ability.mag"
    end = "Ability.end"
    energy_bar = 'Ability.energy_bar'

    @classmethod
    def get_enums(cls):
        return [cls.str, cls.mag, cls.end, cls.energy_bar]


class Attack:
    phy = "Attack.phy"
    mag = "Attack.mag"


class Mission:
    one_shot = "Mission.one_shot"


class Damage:
    phy = "Damage.phy"
    mag = "Damage.mag"
    fire = "Damage.fire"
    earth = "Damage.earth"
    wind = "Damage.wind"
    ice = "Damage.ice"
    thunder = "Damage.thunder"
    light = "Damage.light"
    dark = "Damage.dark"
    foe = "Damage.foe"
    foes = "Damage.foes"

    @classmethod
    def get_enums(cls):
        return [cls.phy, cls.mag,
                cls.fire, cls.earth, cls.wind, cls.ice, cls.thunder, cls.light, cls.dark,
                cls.foe, cls.foes]


class Endurance:
    phy = "Endurance.phy"
    mag = "Endurance.mag"
    fire = "Endurance.fire"
    earth = "Endurance.earth"
    wind = "Endurance.wind"
    ice = "Endurance.ice"
    thunder = "Endurance.thunder"
    light = "Endurance.light"
    dark = "Endurance.dark"
    foe = "Endurance.foe"
    foes = "Endurance.foes"

    @classmethod
    def get_enums(cls):
        return [cls.phy, cls.mag,
                cls.fire, cls.earth, cls.wind, cls.ice, cls.thunder, cls.light, cls.dark,
                cls.foe, cls.foes]

    @classmethod
    def get_from_dmg_enum(cls, dmg_enum):
        d_str = dmg_enum.split(".")[1]
        all_enum = cls.get_enums()
        for e in all_enum:
            e_str = e.split(".")[1]
            if d_str == e_str:
                return e
        raise ValueError



class Power:
    low = "Power.low"
    mid = "Power.mid"
    high = "Power.high"
    super = "Power.super"
    ultra = "Power.ultra"


class AdjBuff:
    extend_buff = "AdjBuff.extend_buff"
    extend_debuff = "AdjBuff.extend_debuff"
    shorten_buff = "AdjBuff.shorten_buff"
    shorten_debuff = "AdjBuff.shorten_debuff"
    clear_buff = "AdjBuff.clear_buff"
    clear_debuff = "AdjBuff.clear_debuff"


class Killer:
    bull = "Killer.bull"
    giant = "Killer.giant"
    beast = "Killer.beast"
    fairy = "Killer.fairy"
    plant = "Killer.plant"
    bug = "Killer.bug"
    rock = "Killer.rock"
    worm = "Killer.worm"
    dragon = "Killer.dragon"
    aquatic = "Killer.aquatic"
    orge = "Killer.orge"
    undead = "Killer.undead"


class SkillPolicy:
    buff = "SkillPolicy.buff"
    debuff = "SkillPolicy.debuff"
    extend_buff = "SkillPolicy.extend_buff"
    extend_debuff = "SkillPolicy.extend_debuff"


class SpecialPolicy:
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
    def __init__(self, scope, effect_enum, value, turns=None, limit_enum=None):
        self.scope = scope
        self.effect_enum = effect_enum
        self.value = value
        self.turns = turns
        self.limit_enum = limit_enum


class Skill:
    def __init__(self, scope=None, power=None, attr_dmg=None, attack=None, **kwargs):
        self.power = power
        self.attack = attack
        self.attr_dmg = attr_dmg
        if attr_dmg:
            self.attr_end_ref = Endurance.get_from_dmg_enum(attr_dmg)
        self.scope = scope
        self.temp_boost = kwargs.get("temp_boost", False)
        self.buffs = kwargs.get("buffs", [])
        self.debuffs = kwargs.get("debuffs", [])
        self.adj_buffs = kwargs.get("adj_buffs", [])
        self.extend_buffs = kwargs.get("extend_buffs", None)
        self.extend_debuffs = kwargs.get("extend_debuffs", None)
        self.shorten_buffs = kwargs.get("shorten_buffs", None)
        self.shorten_debuffs = kwargs.get("shorten_debuffs", None)
        self.is_special = kwargs.get("is_special", False)
        self.idx = None
        self.coeff = 0
        self.coeff_tmp_boost = 0
        self.coeff, self.coeff_tmp_boost = get_coeff(self.scope, self.power)


all_effect_enum = []
for multi_effect_enum in [Ability.get_enums(), Damage.get_enums(), Endurance.get_enums()]:
    for one_effect_enum in multi_effect_enum:
        all_effect_enum.append(one_effect_enum)


class Adventurer(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs)
        self.killer = None  # TODO
        self.skills = kwargs.get("skills", None)
        # self.skills = [s for s in self.skills if s is not None]
        self.passive_skill = None  # TODO
        self.predefined_steps = None
        self.steps_record = []
        self.stages_dmg_record = []
        self.stages_effect_record = []
        self.total_dmg = 0
        self.is_one_shot = False
        self.is_dead = False

        self.buff_need_check = set()
        self.debuff_need_check = set()
        self.ass_buff_need_check = set()
        self.ass_debuff_need_check = set()

        self.got_buff = dict()
        self.got_debuff = dict()
        self.passive_buff = dict()
        self.passive_debuff = dict()
        self.assist_buff = dict()
        self.assist_debuff = dict()
        for eff in all_effect_enum:
            self.got_buff[eff] = [0, 0]
            self.got_debuff[eff] = [0, 0]
            self.passive_buff[eff] = 0
            self.passive_debuff[eff] = 0
            self.assist_buff[eff] = 0
            self.assist_debuff[eff] = 0

        self.assist = None

        self.skill_policy = None  # TODO
        self.my_team = None
        self.battle_stage = None
        self.selected_skill = None
        self.skill_policy_lambdas = []

    def set_skill_policy_order(self, policies):
        for p in policies:
            if p == SkillPolicy.buff:
                self.skill_policy_lambdas.append(self.set_buff_skill)
            elif p == SkillPolicy.debuff:
                self.skill_policy_lambdas.append(self.set_debuff_skill)
            else:
                raise Exception


    def reset(self):
        self.steps_record = []
        self.stages_dmg_record = []
        self.stages_effect_record = []
        self.total_dmg = 0
        self.skill_policy_lambdas = []
        for eff in all_effect_enum:
            self.got_buff[eff] = [0, 0]
            self.got_debuff[eff] = [0, 0]
            self.passive_buff[eff] = 0
            self.passive_debuff[eff] = 0
            self.assist_buff[eff] = 0
            self.assist_debuff[eff] = 0
        self.assist = None
        self.skill_policy = None
        self.selected_skill = None
        self.is_one_shot = False
        self.predefined_steps = None
        self.is_dead = False

    def set_one_shot(self):
        self.is_one_shot = True
        return self

    def set_predefined_steps(self, steps):
        self.predefined_steps = steps
        return self

    def set_assist(self, assist):
        self.assist = assist
        assist.my_adv = self

    def need_buff(self, effect):
        return self.need_skill_effect(self.got_buff, effect)

    def need_debuff(self, effect):
        return self.need_skill_effect(self.got_debuff, effect)

    @staticmethod
    def need_skill_effect(look_up, effect):
        kind = effect.effect_enum
        value = effect.value
        cur_value = look_up[kind][0]
        if value > cur_value:
            return True
        else:
            return False

    def set_buff_skill(self, special_avail):
        for s in self.skills:
            if special_avail is False and s.is_special:
                continue
            for effect in s.buffs:
                if effect.scope == Scope.my_team:
                    if self.my_team.need_buff(effect):
                        self.selected_skill = s
                        return True
                elif effect.scope == Scope.my_self:
                    if self.need_buff(effect):
                        self.selected_skill = s
                        return True
                else:
                    raise Exception
        return False

    def set_debuff_skill(self, special_avail):
        for s in self.skills:
            if special_avail is False and s.is_special:
                continue
            for effect in s.debuffs:
                if effect.scope == Scope.foes:
                    if self.my_team.opponent_team.need_debuff(effect):
                        self.selected_skill = s
                        return True
                elif effect.scope == Scope.foe:
                    if self.my_team.opponent_team.need_debuff(effect):
                        self.selected_skill = s
                        return True
                else:
                    raise Exception
        return False

    def select_skill(self, special_avail):
        if self.predefined_steps is not None:
            if len(self.predefined_steps) < self.battle_stage.max_turns:
                raise Exception("預排技能順序定回合數不足")
            skill_idx = self.predefined_steps[self.battle_stage.cur_turn - 1]
            self.selected_skill = self.skills[skill_idx - 1]
            return
        self.selected_skill = None

        for policy_set in self.skill_policy_lambdas:
            if policy_set(special_avail):
                return True

        enemy_num = len(self.my_team.opponent_team.members_on_stage)
        cur_coeff = -1
        for s in self.skills:
            if s.is_special:
                if not special_avail:
                    continue
            if s.scope == Scope.foes:
                hit_enemy_num = enemy_num
            else:
                hit_enemy_num = 1
            s_coeff = (s.coeff + s.coeff_tmp_boost) * hit_enemy_num
            if s_coeff > cur_coeff:
                cur_coeff = s_coeff
                self.selected_skill = s

        if self.selected_skill is None:
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
                abl_up = self.calc_total_buff(Ability.str)
                enum_atk_end = Damage.phy
            elif s.attack == Attack.mag:
                atk = self.mag + self.assist.mag
                abl_up = self.calc_total_buff(Ability.mag)
                enum_atk_end = Damage.mag
            else:
                raise ValueError

            attr_dmg_up = self.calc_total_buff(s.attr_dmg)

            if s.scope == Scope.foe:
                f = foe_on_stage
                foe_end = f.calc_total_buff(Endurance.foe)
                attr_end = f.calc_total_buff(s.attr_end_ref)
                atk_end = f.calc_total_buff(enum_atk_end)
                end_up = f.calc_total_buff(Ability.end)
                end = f.end
                dmg = ((atk * (1 + abl_up) * (1 + s.coeff_tmp_boost) - end * (1 + end_up))
                       * s.coeff
                       * (1 + attr_dmg_up)
                       * (1 - attr_end - atk_end)
                       * (1 - foe_end)
                       )
            else:
                for f in foes_on_stage:
                    foes_end = f.calc_total_buff(Endurance.foes)
                    attr_end = f.calc_total_buff(s.attr_end_ref)
                    atk_end = f.calc_total_buff(enum_atk_end)
                    end_up = f.calc_total_buff(Ability.end)
                    end = f.end
                    dmg = ((atk * (1 + abl_up) * (1 + s.coeff_tmp_boost) - end * (1 + end_up))
                           * s.coeff
                           * (1 + attr_dmg_up)
                           * (1 - attr_end - atk_end)
                           * (1 - foes_end)
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

        for adj in s.adj_buffs:
            if adj.scope == Scope.foes:
                for f in foes_on_stage:
                    f.adj_buff(adj)
            elif adj.scope == Scope.foe:
                foe_on_stage.adj_buff(adj)
            elif adj.scope == Scope.my_self:
                self.adj_buff(adj)
            elif adj.scope == Scope.my_team:
                for m in self.my_team.members_on_stage:
                    m.adj_buff(adj)
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

    def calc_total_buff(self, effect):
        return self.calc_buff_value(effect) - self.calc_debuff_value(effect)

    @staticmethod
    def set_effect(item, effect):
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
        self.buff_need_check.add(effect.effect_enum)
        self.set_effect(self.got_buff, effect)

    def set_assit_buff(self, effect):
        self.ass_buff_need_check.add(effect.effect_enum)
        self.set_effect(self.assist_buff, effect)

    def set_debuff(self, effect):
        self.debuff_need_check.add(effect.effect_enum)
        self.set_effect(self.got_debuff, effect)

    def set_assist_debuff(self, effect):
        self.ass_debuff_need_check.add(effect.effect_enum)
        self.set_effect(self.assist_debuff, effect)

    def adj_buff(self, adj):
        kind = adj.effect_enum
        val = adj.value
        limit_enum = adj.limit_enum
        if kind == AdjBuff.extend_buff:
            buff_for_adj = self.got_buff
            num_to_cal = val
        elif kind == AdjBuff.extend_debuff:
            buff_for_adj = self.got_debuff
            num_to_cal = val
        elif kind == AdjBuff.shorten_buff:
            buff_for_adj = self.got_buff
            num_to_cal = -val
        elif kind == AdjBuff.shorten_debuff:
            buff_for_adj = self.got_debuff
            num_to_cal = -val
        elif kind == AdjBuff.clear_buff:
            buff_for_adj = self.got_buff
            num_to_cal = -99
        elif kind == AdjBuff.clear_debuff:
            buff_for_adj = self.got_debuff
            num_to_cal = -99
        else:
            raise ValueError

        for effect_enum in all_effect_enum:
            if limit_enum:
                if effect_enum != limit_enum:
                    continue
            if buff_for_adj[effect_enum][0] > 0:
                buff_for_adj[effect_enum][1] += num_to_cal
                if buff_for_adj[effect_enum][1] < 0:
                    buff_for_adj[effect_enum][1] = 0

    @staticmethod
    def effect_next(item):
        item_val = item[0]
        item_turn = item[1]
        if item_turn <= 1:
            item[0] = 0
            item[1] = 0
            return False
        else:
            item[0] = item_val
            item[1] = item_turn - 1
            return True

    def next_turn(self):
        # TODO: speed-up
        all_buff = []
        all_debuff = []
        all_ass_buff = []
        all_ass_debuff = []

        for eff in list(self.ass_buff_need_check):
            ass_buff = self.assist_buff[eff]
            if ass_buff > 0:
                all_ass_buff.append([eff, ass_buff])

        for eff in list(self.buff_need_check):
            buff = self.got_buff[eff]
            if buff[0] > 0:
                all_buff.append([eff, buff[0]])
            need_check_next_turn = self.effect_next(buff)
            if not need_check_next_turn:
                self.buff_need_check.remove(eff)

        for eff in list(self.debuff_need_check):
            debuff = self.got_debuff[eff]
            if debuff[0] > 0:
                all_debuff.append([eff, debuff[0]])
            need_check_next_turn = self.effect_next(debuff)
            if not need_check_next_turn:
                self.debuff_need_check.remove(eff)

        for eff in list(self.ass_debuff_need_check):
            ass_debuff = self.assist_debuff[eff]
            if ass_debuff > 0:
                all_ass_debuff.append([eff, ass_debuff])

        self.stages_effect_record.append([all_buff, all_debuff, all_ass_buff, all_ass_debuff])


class Assist(Character):
    def __init__(self, name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, str_val, end_val, dex_val, agi_val, mag_val, **kwargs)
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
    def __init__(self, max_on_stage, members, assists=None):
        self.battle_stage = None
        self.opponent_team = None
        self.members = members
        self.assists = assists
        self.members_on_stage = self.members[0: max_on_stage]
        self.members_on_reserve = self.members[max_on_stage:]
        self.hit_dmg_turns = []
        self.got_dmg_turns = []
        self.total_dmg = 0
        self.energy_bar = 0

    def set_skill_policy_order(self, policies):
        for m in self.members:
            m.set_skill_policy_order(policies)

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

    def need_debuff(self, debuff):
        for m in self.members_on_stage:
            if m.need_debuff(debuff):
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
        for i, m in enumerate(self.members):
            print(f"{i + 1}:")
            ass_name = ""
            if m.assist:
                ass_name = f"+ {m.assist.name}"
            if self.total_dmg == 0:
                self.total_dmg = 1
            print(f"    {m.name} {ass_name} : {int(m.total_dmg):,} ({m.total_dmg / self.total_dmg * 100:,.0f}%)")
            print(f"    招式順序: {m.steps_record}")
        print(f"\n總傷害:{int(self.total_dmg):,}")
        print("=" * 60)
        for m in self.members:
            print(f"{m.name} 回合詳細")
            for n_stage, info in enumerate(m.stages_effect_record):
                print(f"  Turn {n_stage + 1}:")
                buffs = info[0]
                debuffs = info[1]
                ass_buffs = info[2]
                ass_debuffs = info[3]
                print(f"    Buff:         {buffs}")
                print(f"    DeBuff:       {debuffs}")
                print(f"    AssistBuff:   {ass_buffs}")
                print(f"    AssistDeBuff: {ass_debuffs}")

            print("*" * 60)

    def team_fill(self):
        adv = None
        for idx, m in enumerate(self.members_on_stage):
            if m.is_one_shot or m.is_dead:
                if len(self.members_on_reserve) > 0:
                    adv = self.members_on_reserve.pop(0)
                self.members_on_stage[idx] = adv
        self.members_on_stage = [m for m in self.members_on_stage if m is not None]
        if adv:
            adv.assist.act()

    def next_turn(self):
        self.team_fill()
        for m in self.members_on_stage:
            m.next_turn()

    def inc_energy_bar(self, num):
        self.energy_bar += num
        if self.energy_bar > 60:
            self.energy_bar = 60

    def max_special_moves(self):
        return int(self.energy_bar / 15)

    def dec_energy_bar(self):
        self.energy_bar -= 15
        if self.energy_bar < 0:
            raise Exception("必殺技條未滿，無法施放必殺技")

    def init(self, battle_stage):
        self.battle_stage = battle_stage
        for m in self.members:
            m.battle_stage = battle_stage
            m.my_team = self
        if self.assists:
            for adv, ass in zip(self.members, self.assists):
                adv.set_assist(ass)
                ass.my_team = self
        for m in self.members_on_stage:
            if m.assist:
                m.assist.act()

    def reset(self):
        self.hit_dmg_turns = []
        self.got_dmg_turns = []
        self.total_dmg = 0
        self.energy_bar = 0
        for m in self.members:
            m.reset()


class BattleStage:
    def __init__(self, max_turns):
        self.max_turns = max_turns
        self.cur_turn = 1
        self.player_team = None
        self.enemy_team = None

    def is_last_turn(self):
        if self.cur_turn >= self.max_turns:
            return True
        else:
            return False

    def add_player_team(self, team):
        self.player_team = team

    def add_enemy_team(self, team):
        self.enemy_team = team

    def run(self):
        self.player_team.opponent_team = self.enemy_team
        self.enemy_team.opponent_team = self.player_team
        self.player_team.init(self)
        self.enemy_team.init(self)
        for p in self.player_team.members:
            for idx, s in enumerate(p.skills):
                if s:
                    s.idx = idx + 1
        for i in range(self.max_turns):
            # print(f"round {i}")
            self.cur_turn = i+1
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

    def end(self):
        self.enemy_team.reset()
        self.player_team.reset()


class MyCards:
    def __init__(self, cards_list_in=()):
        self.card_list = list(cards_list_in)

    def get_card_by_name(self, name, **kwargs):
        is_one_shot = kwargs.get("is_one_shot", False)
        ret = None
        for card in self.card_list:
            if card.name == name:
                if ret is not None:
                    raise ValueError
                card.is_one_shot = is_one_shot
                ret = card
        if ret is None:
            raise ValueError
        return ret

    def select_tag(self, tag, reverse=False):
        if reverse:
            list_out = [card for card in self.card_list if tag not in card.tags]
        else:
            list_out = [card for card in self.card_list if tag in card.tags]
        return MyCards(list_out)

    def get_card_list(self):
        if len(self.card_list) == 0:
            raise ValueError
        return self.card_list


my_ass_cards = MyCards([
    Assist("劇場乳神", 643 + 77, 0, 0, 0, 289 + 77,
           skill=Skill(debuffs=[Effect(Scope.foes, Damage.foe, 0.15)])
           ),
    Assist("月神", 571 + 72, 0, 0, 0, 284 + 72,
           skill=Skill(buffs=[Effect(Scope.my_self, Ability.str, 0.15), Effect(Scope.my_team, Ability.str, 0.10)])
           ),
    Assist("泳裝芙蕾雅", 461 + 72, 0, 0, 0, 441 + 72,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.ice, 0.10)])
           ),
    Assist("製作人荷米斯", 459 + 72, 0, 0, 0, 459 + 72,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.fire, 0.10), Effect(Scope.my_team, Damage.light, 0.10)])
           ),
    Assist("聖爐乳神", 398 + 77, 0, 0, 0, 398 + 77,
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.foes, 0.15)])
           ),
    Assist("泳裝埃伊娜", 356 + 56, 0, 0, 0, 372 + 72,
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.ice, 0.15)])
           ),
    Assist("奧娜", 412 + 72, 0, 0, 0, 412 + 72,
           skill=Skill(debuffs=[Effect(Scope.foes, Damage.phy, 0.15), Effect(Scope.foes, Damage.mag, 0.15)])
           ),
    Assist("睡衣乳神", 562 + 77, 0, 0, 0, 293 + 77,
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.thunder, 0.10)])
           ),
    Assist("流氓萬能", 379 + 40, 0, 0, 0, 446 + 41,
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.08), Effect(Scope.my_team, Ability.mag, 0.08)])
           ),
    Assist("新娘希兒", 338 + 72, 0, 0, 0, 338 + 72,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.ice, 0.10), Effect(Scope.my_team, Damage.dark, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.ice, 0.05), Effect(Scope.foes, Endurance.dark, 0.05)])
           ),
    Assist("鴨子乳神", 390 + 77, 0, 0, 0, 190 + 77,
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.ice, 0.10), Effect(Scope.foes, Endurance.wind, 0.10)])
           ),
])

my_adv_cards = MyCards([
    Adventurer("新裝艾斯", 2133 + 808, 0, 0, 0, 0, tags=[Damage.phy, Damage.ice],
               skills=[
                   Skill(
                       buffs=[Effect(Scope.my_self, Damage.ice, 0.60, 4), Effect(Scope.my_self, Ability.str, 0.60, 4)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Damage.ice, 0.80, 4), Effect(Scope.my_self, Ability.str, 0.80, 4)]
                         ),
               ]),
    Adventurer("英雄阿爾戈", 2180 + 813, 0, 0, 0, 0, tags=[Damage.phy, Damage.fire],
               skills=[
                   Skill(Scope.foes, Power.low, Damage.fire, Attack.phy,
                         buffs=[Effect(Scope.my_self, Damage.fire, 0.50, 4),
                                Effect(Scope.my_self, Ability.str, 0.50, 4)]),
                   Skill(Scope.foes, Power.super, Damage.fire, Attack.phy),
                   Skill(Scope.foe, Power.high, Damage.fire, Attack.phy,
                         adj_buffs=[Effect(Scope.foe, AdjBuff.extend_debuff, 1, 0)]),
                   Skill(Scope.foes, Power.ultra, Damage.fire, Attack.phy, is_special=True, temp_boost=True,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.30, 1)]
                         ),
               ]),
    Adventurer("聖誕千草", 2011 + 748, 0, 0, 0, 0, tags=[Damage.phy, Damage.ice],
               skills=[Skill(buffs=[Effect(Scope.my_self, Ability.energy_bar, 1, 5)]),
                       Skill(Scope.foes, Power.super, Damage.ice, Attack.phy, temp_boost=True,
                             adj_buffs=[Effect(Scope.my_self, AdjBuff.clear_debuff, 0, 0)]),
                       Skill(Scope.foe, Power.high, Damage.ice, Attack.phy),
                       ]
               ),
    Adventurer("米卡莎", 1928 + 637, 0, 0, 0, 0, tags=[Damage.phy, Damage.dark, Damage.foe],
               skills=[Skill(Scope.foe, Power.low, Damage.dark, Attack.phy,
                             buffs=[Effect(Scope.my_self, Ability.str, 0.75, 4)]),
                       Skill(Scope.foe, Power.mid, Damage.dark, Attack.phy,
                             buffs=[Effect(Scope.my_self, Damage.dark, 0.60, 4)]),
                       Skill(Scope.foe, Power.high, Damage.dark, Attack.phy,
                             adj_buffs=[Effect(Scope.foe, AdjBuff.clear_buff, 0, 0, Ability.mag)]),
                       Skill(Scope.foe, Power.ultra, Damage.dark, Attack.phy, is_special=True, temp_boost=True),
                       ]
               ),
    Adventurer("劇場莉莉", 1927 + 641, 0, 0, 0, 0, tags=[Damage.phy, Damage.thunder, Damage.foe],
               skills=[Skill(Scope.foe, Power.high, Damage.thunder, Attack.phy, temp_boost=True,
                             debuffs=[Effect(Scope.foe, Endurance.foe, 0.15, 4)]),
                       Skill(Scope.foe, Power.high, Damage.thunder, Attack.phy, temp_boost=True,
                             buffs=[Effect(Scope.my_team, Damage.thunder, 0.20, 3)]),
                       Skill(Scope.foe, Power.low, Damage.thunder, Attack.phy,
                             buffs=[Effect(Scope.my_self, Ability.str, 0.80, 4)]),
                       Skill(Scope.foe, Power.ultra, Damage.thunder, Attack.phy, is_special=True, temp_boost=True),
                       ]
               ),
    Adventurer("歌殺", 2120 + 806, 0, 0, 0, 0, tags=[Damage.phy, Damage.dark, Mission.one_shot],
               skills=[
                   Skill(
                       debuffs=[Effect(Scope.foes, Endurance.phy, 0.30, 4), Effect(Scope.foes, Endurance.dark, 0.30, 4)]),
                   Skill(Scope.foes, Power.mid, Damage.dark, Attack.phy,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.20, 4), Effect(Scope.foe, Endurance.foes, 0.20, 4)]),
                   Skill(Scope.foe, Power.super, Damage.dark, Attack.phy, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Ability.str, 0.30, 3),
                                Effect(Scope.my_self, Damage.dark, 0.30, 3)]),
                   Skill(Scope.foe, Power.ultra, Damage.dark, Attack.phy, is_special=True,
                         buffs=[Effect(Scope.my_self, Damage.dark, 0.90, 3),
                                Effect(Scope.my_self, Ability.str, 0.90, 3)]
                         ),
               ]),
    Adventurer("古代黑肉", 1331 + 484, 0, 0, 0, 0, tags=[Damage.phy, Damage.dark, Mission.one_shot],
               skills=[
                   Skill(Scope.foe, Power.high, Damage.dark, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.super, Damage.dark, Attack.phy, temp_boost=True),
                   Skill(Scope.foes, Power.high, Damage.dark, Attack.phy,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.30, 3)]),
                   Skill(Scope.foes, Power.ultra, Damage.dark, Attack.phy, is_special=True),
               ]),
])

boss_cards = MyCards([
    Adventurer("九魔姬", 0, 100, 0, 0, 1000,
               skills=[Skill(Scope.foes, Power.high, Damage.dark, Attack.mag)]
               )
])


def check_team_valid(team1, team2):
    for m1 in team1:
        for m2 in team2:
            if m1.name == m2.name:
                return False
    return True


def get_enemy_team():
    boss_1 = boss_cards.get_card_by_name("九魔姬")
    boss_ass = Assist("buff", 0, 0, 0, 0, 0,
                      skill=Skill(buffs=[Effect(Scope.my_self, Endurance.ice, 0.1)]))
    # return Team(4, [boss_1, boss_1, boss_1], [boss_ass])
    return Team(4, [boss_1], [boss_ass])


def my_plan():
    enemy_team = get_enemy_team()

    advs = [my_adv_cards.get_card_by_name("新裝艾斯"), # .set_predefined_steps([1, 2, 2, 2, 4, 2, 2, 2, 4]),
            my_adv_cards.get_card_by_name("英雄阿爾戈"),
            my_adv_cards.get_card_by_name("聖誕千草"),
            my_adv_cards.get_card_by_name("米卡莎").set_one_shot(),
            my_adv_cards.get_card_by_name("劇場莉莉").set_one_shot(),
            my_adv_cards.get_card_by_name("歌殺")]

    asses = [my_ass_cards.get_card_by_name("劇場乳神"),
             my_ass_cards.get_card_by_name("月神"),
             my_ass_cards.get_card_by_name("泳裝芙蕾雅"),
             my_ass_cards.get_card_by_name("製作人荷米斯"),
             my_ass_cards.get_card_by_name("聖爐乳神"),
             my_ass_cards.get_card_by_name("泳裝埃伊娜")]

    team1 = Team(4, advs, asses)
    team1.set_skill_policy_order([SkillPolicy.debuff, SkillPolicy.buff])

    battle = BattleStage(16)
    battle.add_player_team(team1)
    battle.add_enemy_team(enemy_team)
    battle.run()

    team1.show_result()
    enemy_team.show_result()


def sim_all():
    cnt = 0
    best_team = None
    print(f"模擬中...")

    enemy_team = get_enemy_team()

    ass_cards = my_ass_cards.get_card_list()[0:9]
    adv_cards = my_adv_cards.get_card_list()[0:8]
    adv_one_shot_cards = my_adv_cards.select_tag(Mission.one_shot).get_card_list()

    total_comb = (len(list(combinations(ass_cards, 6))) *
                  len(list(permutations(adv_cards, 4))) *
                  len(list(combinations(adv_one_shot_cards, 2)))
                  )

    for asses in combinations(ass_cards, 6):
        for advs in permutations(adv_cards, 4):
            for advs_one_shot in combinations(adv_one_shot_cards, 2):
                cnt += 1
                if check_team_valid(advs, advs_one_shot) is False:
                    continue
                print(f"\r{cnt}/{total_comb}", end='')
                for m in advs_one_shot:
                    m.set_one_shot()

                members = list(advs[0:3])
                members.extend(advs_one_shot)
                members.append(advs[3])

                my_team = Team(4, members, asses)

                battle = BattleStage(9)
                battle.add_player_team(my_team)
                battle.add_enemy_team(enemy_team)
                battle.run()

                if best_team is None:
                    best_team = my_team
                else:
                    if my_team.total_dmg > best_team.total_dmg:
                        best_team = copy.deepcopy(my_team)

                battle.end()

    # print(f"總共{cnt}組合.")
    print(f"\r{cnt}/{total_comb}", end='')
    print(f"最佳組合是:")
    best_team.show_result()
    enemy_team.show_result()


tStart = time.time()
# sim_all()
my_plan()
tEnd = time.time()
print(f"cost {tEnd - tStart} sec")
