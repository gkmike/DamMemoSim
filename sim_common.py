import copy

x = 99


class Character:
    def __init__(self, name, hp_val, mp_val, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        self.tags = kwargs.get("tags", [])
        self.name = name
        self.hp = hp_val
        self.mp = mp_val
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
    dex = "Ability.dex"
    agi = "Ability.agi"
    energy_bar = 'Ability.energy_bar'
    crit_rate = "Ability.crit_rate"
    pene_rate = "Ability.pene_rate"
    counter_rate = "Ability.counter_rate"
    guard_rate = "Ability.guard_rate"

    @classmethod
    def get_enums(cls):
        return [cls.str, cls.mag, cls.end, cls.dex, cls.agi, 
                cls.energy_bar, cls.crit_rate, cls.pene_rate, cls.counter_rate, cls.guard_rate]


class Recover:
    hp_imm = "Recover.hp_imm"
    mp_imm = "Recover.mp_imm"
    hp_turn = "Recover.hp_turn"
    mp_turn = "Recover.mp_turn"

    @classmethod
    def get_enums(cls):
        return [cls.hp_turn, cls.mp_turn]


class Attack:
    phy = "Attack.phy"
    mag = "Attack.mag"


class Mission:
    one_shot = "Mission.one_shot"


class SuccessUp:
    crit = "SuccessUp.crit"
    pene = "SuccessUp.pene"
    counter = "SuccessUp.counter"
    guard = "SuccessUp.guard"

    @classmethod
    def get_enums(cls):
        return [cls.crit, cls.pene, cls.counter, cls.guard]


class Damage:
    none = "Damage.none"
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
        return [cls.phy, cls.mag, cls.none,
                cls.fire, cls.earth, cls.wind, cls.ice, cls.thunder, cls.light, cls.dark,
                cls.foe, cls.foes]


class Endurance:
    none = "Endurance.none"
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
        return [cls.phy, cls.mag, cls.none,
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
    simple = "Power.simple"
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


class EndEvent(Exception):
    pass


all_effect_enum = []
for multi_effect_enum in [Ability.get_enums(), Damage.get_enums(), Endurance.get_enums(),
                          Recover.get_enums(), SuccessUp.get_enums()]:
    for one_effect_enum in multi_effect_enum:
        all_effect_enum.append(one_effect_enum)


def clamp(val, min_val, max_val):
    if val < min_val:
        val = min_val
    elif val > max_val:
        val = max_val
    return val


def get_abi_by_eff(chara, eff):
    if eff == Ability.str:
        return chara.str
    elif eff == Ability.mag:
        return chara.mag
    elif eff == Ability.agi:
        return chara.agi
    elif eff == Ability.dex:
        return chara.dex
    elif eff == Ability.end:
        return chara.end
    raise ValueError


def get_coeff(scope, power):
    coeff = 0
    coeff_tmp_boost = 0
    if power is None:
        return coeff, coeff_tmp_boost
    if power == Power.simple:
        return 2, 0
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
        self.is_fast = kwargs.get("is_fast", False)
        self.mp_cost = kwargs.get("mp", 0)
        self.power = power
        self.attack = attack
        self.attr_dmg = attr_dmg
        if attr_dmg:
            self.attr_end_ref = Endurance.get_from_dmg_enum(attr_dmg)
        self.scope = scope
        self.temp_boost = kwargs.get("temp_boost", False)
        self.boost_by_buff = kwargs.get("boost_by_buff", [])
        self.buffs = kwargs.get("buffs", [])
        self.debuffs = kwargs.get("debuffs", [])
        self.adj_buffs = kwargs.get("adj_buffs", [])
        self.extend_buffs = kwargs.get("extend_buffs", None)
        self.extend_debuffs = kwargs.get("extend_debuffs", None)
        self.shorten_buffs = kwargs.get("shorten_buffs", None)
        self.shorten_debuffs = kwargs.get("shorten_debuffs", None)
        self.is_special = kwargs.get("is_special", False)
        self.idx = kwargs.get("idx", None)
        self.coeff = 0
        self.coeff_tmp_boost = 0
        self.coeff, self.coeff_tmp_boost = get_coeff(self.scope, self.power)


class Adventurer(Character):
    def __init__(self, name, hp_val, mp_val, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, hp_val, mp_val, str_val, end_val, dex_val, agi_val, mag_val, **kwargs)
        self.max_hp = 0
        self.max_mp = 0
        self.cur_hp = 0
        self.cur_mp = 0
        self.weapon_crti_rate = 0
        self.weapon_atk = 0
        self.armor_def = 0
        self.init_skill = kwargs.get("init_skill", None)
        self.skills = kwargs.get("skills", None)
        simple_atk_enum = Attack.phy
        if mag_val > str_val:
            simple_atk_enum = Attack.mag
            self.counter_attr = kwargs.get("counter_attr", Damage.light)
        else:
            self.counter_attr = kwargs.get("counter_attr", Damage.none)
        self.counter_skill = Skill(Scope.foe, Power.simple, self.counter_attr, simple_atk_enum)
        self.simple_hit_skill = Skill(Scope.foe, Power.simple, Damage.none, simple_atk_enum)
        # self.skills = [s for s in self.skills if s is not None]
        self.counter_hp = kwargs.get("counter_hp", None)
        self.killer = kwargs.get("killer", None)
        self.weak_killer = kwargs.get("weak_killer", None)
        self.passive_skills = kwargs.get("passive_skills", None)
        self.predefined_steps = None
        self.predefined_targets = None
        self.steps_record = {}
        self.hp_mp_record = {}
        self.turns_dmg_record = {}
        self.turns_got_dmg_record = {}
        self.turns_counter_dmg_record = {}
        self.turns_effect_record = {}
        self.total_skill_dmg = 0
        self.total_counter_dmg = 0
        self.total_dmg = 0
        self.is_one_shot = False
        self.is_dead = False

        self.buff_need_check = set()
        self.debuff_need_check = set()
        self.ass_buff_need_check = set()
        self.ass_debuff_need_check = set()
        self.passive_buff_need_check = set()
        self.passive_debuff_need_check = set()

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

        self.my_team = None
        self.battle_stage = None
        self.selected_skill = None
        self.skill_done = False
        self.selected_enemy = 0

    def set_one_shot(self):
        self.is_one_shot = True
        return self

    def set_steps(self, steps, targets=None):
        self.predefined_steps = steps
        self.predefined_targets = targets
        return self

    def init(self):
        if self.assist:
            self.assist.my_team = self.my_team
            self.max_hp = self.hp + self.assist.hp
            self.max_mp = self.mp + self.assist.mp
        else:
            self.max_hp = self.hp
            self.max_mp = self.mp

        self.cur_hp = self.max_hp
        self.cur_mp = self.max_mp
        if self.init_skill:
            self.selected_skill = self.init_skill
            self.act()


    def set_assist(self, assist):
        self.assist = assist
        assist.my_adv = self
        return self

    def select_skill(self, round=0):
        if self.predefined_steps is None:
            raise Exception(f"{self.name} 沒有設定預排技能")
        cur_turn = self.get_cur_turn()
        turn_idx = cur_turn - 1
        if self.is_one_shot is False:
            if cur_turn > len(self.predefined_steps):
                raise Exception(f"{self.name}  預排技能數量不足回合數 @Turn {cur_turn}")
        if isinstance(self.predefined_steps[turn_idx], list):
            if round >= len(self.predefined_steps[turn_idx]):
                return False
            skill_idx = self.predefined_steps[turn_idx][round]
        else:
            if round > 0:
                return False
            skill_idx = self.predefined_steps[turn_idx]
        if skill_idx == 99:
            raise Exception(f"{self.name} 必須發動技能 @Turn {turn_idx}")
        if skill_idx == 0:
            self.selected_skill = self.simple_hit_skill
        else:
            self.selected_skill = self.skills[skill_idx - 1]
        mp_cost = self.selected_skill.mp_cost
        if mp_cost > self.cur_mp:
            raise Exception(f"{self.name}  MP不足 @Turn {turn_idx}, cost:{mp_cost}, current:{self.cur_mp}")
        if self.predefined_targets:
            self.selected_enemy = self.predefined_targets[turn_idx]
            if self.selected_skill.scope == Scope.foe:
                if self.selected_enemy > len(self.my_team.opponent_team.members_on_stage):
                    raise Exception(f"{self.name}  指定超出敵人數量 @Turn {turn_idx}")
                if self.selected_enemy == 0:
                    raise Exception(f"{self.name}  單體攻擊技能指定對象不可為0 @Turn {turn_idx}")
                self.selected_enemy -= 1
            else:
                if self.selected_enemy != 0:
                    raise Exception(f"{self.name}  非單體攻擊技能指定對象必需為0 @Turn {turn_idx}")
        else:
            self.selected_enemy = 0
        return True

    def get_cur_turn(self):
        return self.my_team.battle_stage.cur_turn

    def got_dmg(self, dmg):
        self.cur_hp -= dmg
        if self.cur_hp <= 0:
            self.is_dead = True
            self.my_team.team_fill()
            if len(self.my_team.members_on_stage) == 0:
                raise EndEvent(self.my_team.tag + ' die')

    def calc_dmg(self, skill, target):
        f = target
        s = skill
        if s.attack == Attack.phy:
            atk = self.calc_total_abi(Ability.str)
            abl_up = self.calc_total_buff(Ability.str)
            enum_atk_end = Endurance.phy
        elif s.attack == Attack.mag:
            atk = self.calc_total_abi(Ability.mag)
            abl_up = self.calc_total_buff(Ability.mag)
            enum_atk_end = Endurance.mag
        else:
            raise ValueError

        atk += self.weapon_atk

        attr_dmg_up = self.calc_total_buff(s.attr_dmg)

        if s.is_special:
            combo_num = self.my_team.combo_num
            if combo_num < 1:
                raise ValueError
            combo_atk_up = (self.my_team.combo_num - 1) * 0.20
        else:
            combo_atk_up = 0

        total_boost_by = 0

        for boost in s.boost_by_buff:
            eff = boost.effect_enum
            num = self.count_buff_num(eff)
            up_rate = boost.value
            total_boost_by += up_rate * num
        killer_up = 0
        if self.killer:
            if f.weak_killer == self.killer:
                killer_up = 0.5
        if s.scope == Scope.foe:
            foe_foes_end = f.calc_total_buff(Endurance.foe)
        elif s.scope == Scope.foes:
            foe_foes_end = f.calc_total_buff(Endurance.foes)
        else:
            raise Exception
        attr_end = f.calc_total_buff(s.attr_end_ref)
        atk_end = f.calc_total_buff(enum_atk_end)
        end_up = f.calc_total_buff(Ability.end)
        crit_dmg = self.count_crit_rate() * 0.5
        pene_def_down = 1 - (self.count_pene_rate() * 0.5)
        guard_atk_down = 1 - (f.count_guard_rate() * 0.5)
        crit_dmg_success_up = 1 + self.calc_total_buff(SuccessUp.crit) * self.count_crit_rate()
        pene_dmg_success_up = 1 + self.calc_total_buff(SuccessUp.pene) * self.count_pene_rate()
        guard_dmg_success_down = 1 - f.calc_total_buff(SuccessUp.guard) * f.count_guard_rate()
        end = f.calc_total_abi(Ability.end) + f.armor_def
        dmg = ((atk * (1 + abl_up) * (1 + killer_up) * (1 + s.coeff_tmp_boost) - end * (1 + end_up) * pene_def_down / 2)
               * s.coeff
               * (1 + total_boost_by)
               * (1 + attr_dmg_up)
               * (1 - attr_end - atk_end)
               * (1 - foe_foes_end)
               * (1 + combo_atk_up)
               * (1 + crit_dmg)
               * guard_atk_down
               * crit_dmg_success_up * pene_dmg_success_up * guard_dmg_success_down
               )
        # print(dmg, self.name)
        # print("   => atk=", atk, "abl_up=", abl_up, "killer_up=", killer_up)
        # print("   => coeff_tmp_boost=", s.coeff_tmp_boost, "coeff=", s.coeff, "attr_dmg_up=", attr_dmg_up)
        # print("   => attr_dmg_up=", attr_dmg_up, "attr_end=", attr_end, "foe_foes_end=", foe_foes_end)
        # print("   => end=", end, "end_up=", end_up, "combo_atk_up=", combo_atk_up)
        # print("   => crit_dmg=", crit_dmg, "guard_atk_down=", guard_atk_down, "pene_def_down=", pene_def_down)
        if dmg < 0:
            dmg = 0
        return dmg

    def calc_counter_dmg(self, f):
        if self.counter_hp:
            recover_hp = self.calc_total_abi(Ability.mag) * self.count_counter_rate() * 2
            members = sorted(self.my_team.members_on_stage, key=lambda m: m.cur_hp)
            member = members[0]
            member.cur_hp = clamp(member.cur_hp + recover_hp, 0, member.max_hp)
            return 0
        else:
            counter_dmg_success_up = 1 + self.calc_total_buff(SuccessUp.counter) * self.count_counter_rate()
            dmg = self.calc_dmg(self.counter_skill, f) * self.count_counter_rate() * counter_dmg_success_up
            # print(self.name, dmg)
            if dmg < 0:
                dmg = 0
            self.total_counter_dmg += dmg
            self.total_dmg += dmg
            self.my_team.team_total_dmg += dmg
            return dmg

    def dmg_proces(self, f):
        cur_turn = self.get_cur_turn()
        s = self.selected_skill
        dmg = self.calc_dmg(s, f)
        f.got_dmg(dmg)
        if cur_turn in f.turns_got_dmg_record:
            all_got_dmg = f.turns_got_dmg_record[cur_turn] + dmg
        else:
            all_got_dmg = dmg
        f.turns_got_dmg_record[cur_turn] = all_got_dmg
        if not f.is_dead:
            counter_dmg = f.calc_counter_dmg(self)
            if cur_turn in self.turns_counter_dmg_record:
                all_counter_dmg = self.turns_counter_dmg_record[cur_turn] + counter_dmg
            else:
                all_counter_dmg = counter_dmg
            self.turns_counter_dmg_record[cur_turn] = all_counter_dmg
            self.got_dmg(counter_dmg)
        return dmg

    def act(self):
        if self.skill_done:
            raise Exception("skill already acted at one turn")
        s = self.selected_skill
        cur_turn = self.get_cur_turn()
        self.cur_mp -= s.mp_cost
        self.hp_mp_record[cur_turn] = [self.cur_hp, self.cur_mp]
        dmg = 0
        foes_on_stage = self.my_team.opponent_team.members_on_stage
        foe_on_stage = foes_on_stage[self.selected_enemy]
        if s.power is not None:
            if s.scope == Scope.foe:
                f = foe_on_stage
                dmg += self.dmg_proces(f)
            else:
                for f in foes_on_stage:
                    dmg += self.dmg_proces(f)
        self.turns_dmg_record[cur_turn] = dmg
        self.total_skill_dmg += dmg
        self.total_dmg += dmg
        self.my_team.team_total_dmg += dmg

        # update after atk
        foes_on_stage = self.my_team.opponent_team.members_on_stage
        foe_on_stage = foes_on_stage[self.selected_enemy]

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
            elif debuff.scope == Scope.my_self:
                self.set_debuff(debuff)
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

        energy_bar_boost = self.calc_buff_value(Ability.energy_bar)
        if not s.is_special:
            self.my_team.inc_energy_bar(1 + energy_bar_boost)

        if isinstance(self.predefined_steps[cur_turn-1], list):
            if cur_turn not in self.steps_record:
                self.steps_record[cur_turn] = []
            self.steps_record[cur_turn].append(s.idx)
            if len(self.steps_record[cur_turn]) > len(self.predefined_steps[cur_turn-1]):
                return True
            else:
                return False
        else:
            self.steps_record[cur_turn] = s.idx
            return True

    def calc_total_abi(self, abi_eff):
        if self.assist:
            ass_val = get_abi_by_eff(self.assist, abi_eff)
        else:
            ass_val = 0
        val = get_abi_by_eff(self, abi_eff)
        return val + ass_val

    def count_rate(self, rate_eff, abi_eff1, abi_eff2):
        v1 = self.calc_total_abi(abi_eff1)
        v2 = self.calc_total_abi(abi_eff2)
        v1 *= (1 + self.sum_eff_value(abi_eff1))
        v2 *= (1 + self.sum_eff_value(abi_eff2))

        rate = (v1 + v2) / 10000
        rate += self.sum_eff_value(rate_eff)
        rate = clamp(rate, 0, 100)
        return rate 

    def count_crit_rate(self):
        rate = self.count_rate(Ability.crit_rate, Ability.dex, Ability.agi)
        rate += self.weapon_crti_rate
        rate = clamp(rate, 0, 1)
        return rate 

    def count_pene_rate(self):
        rate = self.count_rate(Ability.pene_rate, Ability.str, Ability.dex)
        return rate 

    def count_guard_rate(self):
        rate = self.count_rate(Ability.guard_rate, Ability.agi, Ability.end)
        return rate 

    def count_counter_rate(self):
        rate = self.count_rate(Ability.counter_rate, Ability.dex, Ability.agi)
        return rate 

    def sum_eff_value(self, effect):
        val = self.calc_buff_value(effect) - self.calc_debuff_value(effect)
        return val

    def count_buff_num(self, effect):
        cnt = 0
        n1 = self.got_buff[effect][0]
        n2 = self.assist_buff[effect]
        if n1 > 0:
            cnt += 1
        if n2 > 0:
            cnt += 1
        return cnt

    def calc_debuff_num(self, effect):
        cnt = 0
        n1 = self.got_debuff[effect][0]
        n2 = self.assist_debuff[effect]
        if n1 > 0:
            cnt += 1
        if n2 > 0:
            cnt += 1
        return cnt

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
        if effect.effect_enum == Recover.hp_imm:
            rate = effect.value
            self.cur_hp += int(self.max_hp * rate)
            if self.cur_hp > self.max_hp:
                self.cur_hp = self.max_hp
            return
        elif effect.effect_enum == Recover.mp_imm:
            rate = effect.value
            self.cur_mp += int(self.max_mp * rate)
            if self.cur_mp > self.max_mp:
                self.cur_mp = self.max_mp
            return
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

    def set_passive_buff(self, effect):
        self.passive_buff_need_check.add(effect.effect_enum)
        self.set_effect(self.passive_buff, effect)

    def set_passive_debuff(self, effect):
        self.passive_debuff_need_check.add(effect.effect_enum)
        self.set_effect(self.passive_debuff, effect)

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
            if 'Recover' in effect_enum:
                continue
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

    def hp_mp_recover(self, eff, rate):
        if 'hp' in eff:
            self.cur_hp = clamp(self.cur_hp + self.max_hp * rate, 0, self.max_hp)
        if 'mp' in eff:
            self.cur_mp = clamp(self.cur_mp + self.max_mp * rate, 0, self.max_mp)

    def next_turn(self):
        self.skill_done = False
        all_buff = []
        all_debuff = []
        all_ass_buff = []
        all_ass_debuff = []
        all_p_buff = []
        all_p_debuff = []

        for eff in list(self.passive_buff_need_check):
            passive_buff = self.passive_buff[eff]
            if passive_buff > 0:
                all_p_buff.append([eff, passive_buff])
                if 'Recover' in eff:
                    self.hp_mp_recover(eff, passive_buff)

        for eff in list(self.ass_buff_need_check):
            ass_buff = self.assist_buff[eff]
            if ass_buff > 0:
                all_ass_buff.append([eff, ass_buff])
                if 'Recover' in eff:
                    self.hp_mp_recover(eff, ass_buff)

        for eff in list(self.buff_need_check):
            buff = self.got_buff[eff]
            if buff[0] > 0:
                all_buff.append([eff, buff[0]])
            need_check_next_turn = self.effect_next(buff)
            if not need_check_next_turn:
                self.buff_need_check.remove(eff)
                if 'Recover' in eff:
                    self.hp_mp_recover(eff, buff[0])

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

        for eff in list(self.passive_debuff_need_check):
            passive_debuff = self.passive_debuff[eff]
            if passive_debuff > 0:
                all_p_debuff.append([eff, passive_debuff])

        cur_turn = self.get_cur_turn()
        self.turns_effect_record[cur_turn] = [all_buff, all_debuff,
                                              all_ass_buff, all_ass_debuff,
                                              all_p_buff, all_p_debuff]

    def init_passive_skills(self):
        if self.passive_skills:
            for s in self.passive_skills:
                if s.buffs:
                    for eff in s.buffs:
                        if eff.scope == Scope.my_team:
                            raise ValueError
                        elif eff.scope == Scope.my_self:
                            self.set_passive_buff(eff)
                        else:
                            raise ValueError
                if s.debuffs:
                    for eff in s.debuffs:
                        if eff.scope == Scope.my_team:
                            raise ValueError
                        elif eff.scope == Scope.my_self:
                            self.set_passive_debuff(eff)
                        else:
                            raise ValueError


class Assist(Character):
    def __init__(self, name, hp_val, mp_val, str_val, end_val, dex_val, agi_val, mag_val, **kwargs):
        super().__init__(name, hp_val, mp_val, str_val, end_val, dex_val, agi_val, mag_val, **kwargs)
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
    def __init__(self, max_on_stage, members):
        self.battle_stage = None
        self.opponent_team = None
        self.members = copy.deepcopy(members)
        #self.assists = copy.deepcopy(assists)
        self.members_on_stage = self.members[0: max_on_stage]
        self.members_on_reserve = self.members[max_on_stage:]
        self.team_total_dmg = 0
        self.hit_dmg_turns = []
        self.got_dmg_turns = []
        self.energy_bar = 0
        self.energy_bar_record = [0]
        self.combo_num = 0
        self.tag = ""

    def __eq__(self, cmp_team):
        for m1, m2, in zip(self.members, cmp_team.members):
            if m1.name != m2.name:
                return False
            if m1.assist.name != m2.assist.name:
                return False
        return True

    def get_cur_turn(self):
        return self.battle_stage.cur_turn

    def select_skills(self, round = 0):
        ok = False
        for m in self.members_on_stage:
            ok = m.select_skill(round)
            if m.selected_skill.is_special:
                if not self.dec_energy_bar():
                    raise Exception(f"{m.name} 必殺技條未滿({(self.energy_bar+14)/14})，無法施放必殺技 @Turn {self.get_cur_turn()}")
        return ok

    def act(self):
        # special skill first
        for m in self.members_on_stage:
            if m.skill_done:
                continue
            if m.selected_skill.is_special:
                m.skill_done = m.act()

        #  than fast skill
        for m in self.members_on_stage:
            if m.skill_done:
                continue
            if m.selected_skill.is_fast:
                m.skill_done = m.act()

        #  than normal skill
        for m in self.members_on_stage:
            if m.skill_done:
                continue
            m.skill_done = m.act()

            # print(f"{m.name}\n => 招{m.selected_skill.idx}: 傷害{dmg}")
        # print(f"回合總傷害: {all_dmg}")

    def show_brief(self):
        team_total_dmg = self.team_total_dmg
        if team_total_dmg == 0:
            team_total_dmg = 1
        for i, m in enumerate(self.members):
            if m.is_one_shot:
                print(f"  {m.name} + {m.assist.name} (撤退)")
            else:
                dead_text = ""
                if m.is_dead:
                    dead_text = " (死亡) "
                print(f"  {m.name} + {m.assist.name}{dead_text} => "
                      f"{int(m.total_dmg):,} ({m.total_dmg / team_total_dmg * 100:.0f}%) = " +
                      f"技能傷害 {int(m.total_skill_dmg)} ({m.total_skill_dmg / team_total_dmg * 100:.0f}%) + " + 
                      f"反擊傷害 {int(m.total_counter_dmg)} ({m.total_counter_dmg / team_total_dmg * 100:.0f}%)"
                      )
        #print(f"剩餘氣條: {self.energy_bar/14:.2f}")
        print(f"每回合開始氣條:\n  ", end='')
        for i, n in enumerate(self.energy_bar_record):
            print(f"({i+1}) {n}, ", end='')
        print("")

    def show_result(self):
        print("=" * 60)
        for m in self.members:
            print(f"{m.name} 回合詳細")
            for turn in range(1, self.battle_stage.end_turn):
                if turn in m.steps_record:
                    print(f"  Turn {turn}:")
                    if turn not in m.turns_effect_record:
                        if m.is_dead:
                            print(f"    死亡")
                        continue
                    info = m.turns_effect_record[turn]
                    buffs = info[0] 
                    debuffs = info[1]
                    ass_buffs = info[2]
                    ass_debuffs = info[3]
                    passive_buffs = info[4]
                    passive_debuffs = info[5]
                    print(f"    HP:            {m.hp_mp_record[turn][0]}")
                    print(f"    MP:            {m.hp_mp_record[turn][1]}")
                    print(f"    Skill:         [{m.steps_record[turn]}] => Damage {int(m.turns_dmg_record[turn])}")
                    print(f"    GotDmg:        {int(m.turns_got_dmg_record[turn])}")
                    print(f"    Buff:          {buffs}")
                    print(f"    DeBuff:        {debuffs}")
                    print(f"    AssistBuff:    {ass_buffs}")
                    print(f"    AssistDeBuff:  {ass_debuffs}")
                    print(f"    PassiveBuff:   {passive_buffs}")
                    print(f"    PassiveDeBuff: {passive_debuffs}")

            print("*" * 60)

    def team_fill(self):
        advs = []
        for idx, m in enumerate(self.members_on_stage):
            if m.is_dead:
                if len(self.members_on_reserve) > 0:
                    adv = self.members_on_reserve.pop(0)
                    self.members_on_stage[idx] = adv
                    advs.append(adv)
                else:
                    self.members_on_stage[idx] = None
        self.members_on_stage = [m for m in self.members_on_stage if m is not None]
        for adv in advs:
            adv.init_passive_skills()
            adv.assist.act()

    def next_turn(self):
        for m in self.members_on_stage:
            m.next_turn()
            if m.is_one_shot:
                m.is_dead = True
        self.team_fill()
        self.combo_num = 0
        sp_num = self.count_special_num()
        self.energy_bar_record.append(f"{sp_num:.1f}")

    def inc_energy_bar(self, num):
        self.energy_bar += num
        if self.energy_bar > 60:
            self.energy_bar = 60

    def count_special_num(self):
        return self.energy_bar / 14

    def dec_energy_bar(self):
        self.energy_bar -= 14
        if self.energy_bar < 0:
            return False
        self.combo_num += 1
        return True

    def init(self, battle_stage):
        self.battle_stage = battle_stage
        for m in self.members:
            m.battle_stage = battle_stage
            m.my_team = self
            m.init()

        for m in self.members_on_stage:
            m.init_passive_skills()
            if m.assist:
                m.assist.act()


class BattleStage:
    def __init__(self, max_turns):
        self.max_turns = max_turns
        self.end_turn = 1
        self.cur_turn = 1
        self.player_team = None
        self.enemy_team = None
        self.ending = "已達最大回合數"

    def is_last_turn(self):
        if self.cur_turn >= self.max_turns:
            return True
        else:
            return False

    def set_player_team(self, team):
        self.player_team = copy.deepcopy(team)
        self.player_team.tag = "player"
        for m in self.player_team.members:
            m.weapon_atk = 350
            m.weapon_crti_rate = 0.3
            m.armor_def = 350
        return self

    def set_enemy_team(self, team):
        self.enemy_team = copy.deepcopy(team)
        self.enemy_team.tag = "enemy"
        return self

    def run(self):
        try:
            self.try_run()
        except EndEvent as e:
            if str(e) == "enemy die":
                self.ending = "敵人殲滅"
            elif str(e) == "player die":
                self.ending = "玩家陣亡"
            else:
                raise e

    def try_run(self):
        self.player_team.opponent_team = self.enemy_team
        self.enemy_team.opponent_team = self.player_team
        for p in self.player_team.members:
            for idx, s in enumerate(p.skills):
                if s:
                    s.idx = idx + 1
        for p in self.enemy_team.members:
            for idx, s in enumerate(p.skills):
                if s:
                    s.idx = idx + 1
        self.player_team.init(self)
        self.enemy_team.init(self)
        for turn in range(1, self.max_turns+1):
            # print(f"round {i}")
            self.cur_turn = turn
            self.end_turn = turn
            self.player_team.select_skills()
            self.player_team.act()
            round = 0
            while self.enemy_team.select_skills(round):
                self.enemy_team.act()
                round += 1
            self.player_team.next_turn()
            self.enemy_team.next_turn()


class MyCards:
    def __init__(self, cards_list_in=()):
        self.card_list = list(cards_list_in)

    def get(self, name):
        ret = None
        for card in self.card_list:
            if card.name == name:
                if ret is not None:
                    raise ValueError(f"找到重複名稱卡片 {name}")
                ret = card
        if ret is None:
            raise ValueError(f"找不到卡片 {name}")
        return copy.deepcopy(ret)


class Ranker:
    def __init__(self):
        self.all_battles = []

    def add(self, battle_to_add):
        for i, bt in enumerate(self.all_battles):
            if bt.player_team.team_total_dmg == battle_to_add.player_team.team_total_dmg:
                print("分數相同 不列入紀錄")
                return i+1
        self.all_battles.append(copy.deepcopy(battle_to_add))
        self.all_battles = sorted(self.all_battles, key=lambda team: team.player_team.team_total_dmg, reverse=True)
        for i, bt in enumerate(self.all_battles):
            if bt.player_team.team_total_dmg == battle_to_add.player_team.team_total_dmg:
                return i+1
        raise ValueError

    def report(self, **kwargs):
        limit = kwargs.get("limit", 1)
        rank = kwargs.get("rank", None)
        show_detail = kwargs.get("detail", False)
        
        top_dmg = int(self.all_battles[0].player_team.team_total_dmg)
        if top_dmg == 0:
            top_dmg = 1

        for idx, b in enumerate(self.all_battles):
            if rank:
                if idx + 1 != rank:
                    continue
            else:
                if idx >= limit:
                    return 
            print("--")
            print(f"結束回合: {int(b.end_turn)}, 結束事由: {b.ending}")
            print(f"總傷害: {int(b.player_team.team_total_dmg):,} "
                  f"(榮光積分(lv6):{int(b.player_team.team_total_dmg)*17:,}) [rank {idx+1}] "
                  f"({b.player_team.team_total_dmg / top_dmg * 100:,.0f}% of rank1)")
            b.player_team.show_brief()
            if show_detail:
                b.player_team.show_result()
                b.enemy_team.show_result()
        print("="*60)
