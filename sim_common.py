import copy
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
    shorten_buff = "SkillPolicy.shorten_buff"
    shorten_debuff = "SkillPolicy.shorten_debuff"
    # clear_buff not impl
    # clear_debuff not impl


class SpecialPolicy:
    harumime_first = 0
    single_asap = 1
    double_asap = 2
    triple_asap = 3
    max = 4


all_effect_enum = []
for multi_effect_enum in [Ability.get_enums(), Damage.get_enums(), Endurance.get_enums()]:
    for one_effect_enum in multi_effect_enum:
        all_effect_enum.append(one_effect_enum)


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

        self.my_team = None
        self.battle_stage = None
        self.selected_skill = None


    def set_one_shot(self):
        self.is_one_shot = True
        return self

    def set_predefined_steps(self, steps):
        self.predefined_steps = steps
        return self

    def set_assist(self, assist):
        self.assist = assist
        assist.my_adv = self


    def select_skill(self, special_avail):
        if self.predefined_steps is None:
            raise Exception(f"{self.name} 沒有設定預排技能")
        if self.is_one_shot is False:
            if len(self.predefined_steps) < self.battle_stage.max_turns:
                raise Exception("{self.name}  預排技能順序數量不足回合數")
        skill_idx = self.predefined_steps[self.battle_stage.cur_turn - 1]
        if skill_idx == 0:
            raise ValueError
        self.selected_skill = self.skills[skill_idx - 1]
        return

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

    def select_skills(self):
        for m in self.members_on_stage:
            sv = self.max_special_moves()
            if sv > 0:
                has_sv = True
            else:
                has_sv = False
            m.select_skill(has_sv)
            if m.selected_skill.is_special:
                if self.dec_energy_bar() == False:
                    raise Exception(f"{m.name} 必殺技條未滿，無法施放必殺技 @Turn {self.battle_stage.cur_turn}")

    def act(self):
        all_dmg = 0
        for m in self.members_on_stage:
            dmg = m.act()
            # print(f"{m.name}\n => 招{m.selected_skill.idx}: 傷害{dmg}")
            all_dmg += dmg
        # print(f"回合總傷害: {all_dmg}")
        self.total_dmg += all_dmg
        return all_dmg

    def show_berif(self):
        for i, m in enumerate(self.members):
            if m.is_one_shot:
                print(f"  {m.name} + {m.assist.name} (屍體)")
            else:
                print(f"  {m.name} + {m.assist.name} ({m.total_dmg / self.total_dmg * 100:,.0f}%)")
        print(f"剩餘氣條: {self.energy_bar/15:.2f}")

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
            return False
        return True

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

    def set_player_team(self, team):
        self.player_team = team
        return self

    def set_enemy_team(self, team):
        self.enemy_team = team
        return self

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

class Ranker:
    def __init__(self):
        self.all_battles = []
    def add(self, battle):
        self.all_battles.append(copy.deepcopy(battle))
    def report(self):
        battle_result = sorted(self.all_battles, key=lambda team: team.player_team.total_dmg)
        top_dmg = int(battle_result[0].player_team.total_dmg)

        for idx, b in enumerate(battle_result):
            print(f"傷害: {int(b.player_team.total_dmg):,} (rank {idx+1} {b.player_team.total_dmg / top_dmg * 100:,.0f}%)")
            b.player_team.show_berif()
        print("="*60)
