from sim_common import *

ass_cards = MyCards([
    Assist("劇場乳神", 1207, 213,
           643, 312, 406, 438, 289,
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.dex, 0.2)], debuffs=[Effect(Scope.foes, Endurance.foe, 0.15)],
                       adj_buffs=[], )
           ),
    Assist("奧娜", 1202, 238,
           412, 232, 401, 663, 412,
           skill=Skill(
               buffs=[Effect(Scope.my_self, Ability.counter_rate, 0.3), Effect(Scope.my_self, Ability.guard_rate, 0.3)],
               debuffs=[Effect(Scope.foes, Endurance.phy, 0.15), Effect(Scope.foes, Endurance.mag, 0.15)],
               adj_buffs=[], )
           ),
    Assist("情人埃伊娜", 946, 196,
           299, 180, 304, 434, 315,
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.earth, 0.1), Effect(Scope.my_team, Damage.light, 0.1)],
                       debuffs=[Effect(Scope.foes, Endurance.earth, 0.05), Effect(Scope.foes, Endurance.light, 0.05)],
                       adj_buffs=[], )
           ),
    Assist("新娘乳神", 1015, 158,
           221, 168, 266, 249, 486,
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.mag, 0.15), Effect(Scope.my_team, Ability.crit_rate, 0.08)],
                       debuffs=[], adj_buffs=[], )
           ),
    Assist("溫泉乳神", 942, 278,
           293, 244, 406, 329, 591,
           skill=Skill(buffs=[], debuffs=[Effect(Scope.foes, Ability.str, 0.15)], adj_buffs=[], )
           ),
    Assist("洋裝埃伊娜", 1197, 215,
           265, 227, 391, 393, 652,
           skill=Skill(buffs=[Effect(Scope.my_team, Endurance.foes, 0.1), Effect(Scope.my_team, Endurance.phy, 0.15)],
                       debuffs=[], adj_buffs=[], )
           ),
    Assist("伯爵希兒", 1188, 138,
           323, 268, 297, 206, 389,
           skill=Skill(buffs=[Effect(Scope.my_self, Ability.energy_bar, 0.66)], debuffs=[], adj_buffs=[], )
           ),
])

adv_cards = MyCards([
    Adventurer("折紙", 4045, 414,
               423, 548, 737, 929, 2045,
               skills=[Skill(Scope.foe, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=34, buffs=[],
                             debuffs=[Effect(Scope.foe, Endurance.light, 0.35, 4)], adj_buffs=[], ),
                       Skill(Scope.foe, Power.mid, Damage.light, Attack.mag, mp=30,
                             buffs=[Effect(Scope.my_self, Ability.mag, 0.8, 4)], debuffs=[], adj_buffs=[], ),
                       Skill(Scope.foes, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=29, buffs=[],
                             debuffs=[], adj_buffs=[], ),
                       Skill(Scope.foe, Power.ultra, Damage.light, Attack.mag, temp_boost=True, is_special=True,
                             buffs=[], debuffs=[], adj_buffs=[], )],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, SuccessUp.pene, 0.2),
                                            Effect(Scope.my_self, Endurance.dark, 0.35)])],
               killer=Killer.fairy,
               ),
    Adventurer("情人艾斯", 4017, 421,
               459, 560, 744, 902, 1802,
               skills=[
                   Skill(Scope.foe, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=41, buffs=[], debuffs=[],
                         adj_buffs=[Effect(Scope.foes, AdjBuff.clear_buff, 0, 0, Ability.mag)], ),
                   Skill(Scope.foe, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=44,
                         buffs=[Effect(Scope.my_team, Damage.light, 0.2, 4)], debuffs=[], adj_buffs=[], ),
                   Skill(Scope.foe, Power.low, Damage.light, Attack.mag, mp=27,
                         buffs=[Effect(Scope.my_self, Ability.mag, 0.75, 4)], debuffs=[], adj_buffs=[], ),
                   Skill(Scope.foe, Power.ultra, Damage.light, Attack.mag, temp_boost=True, is_special=True, buffs=[],
                         debuffs=[], adj_buffs=[], )],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, SuccessUp.pene, 0.2),
                                            Effect(Scope.my_self, Endurance.dark, 0.35)])],
               killer=Killer.rock,
               ),

    Adventurer("春姬", 4140, 438,
               1040, 514, 848, 838, 1647,
               skills=[Skill(Scope.foes, Power.mid, Damage.fire, Attack.mag, mp=34, buffs=[],
                             debuffs=[Effect(Scope.foes, Ability.str, 0.4, 3), Effect(Scope.foes, Ability.mag, 0.4, 3)],
                             adj_buffs=[], ),
                       Skill(mp=12, buffs=[Effect(Scope.my_self, Recover.mp_imm, 0.15),
                                           Effect(Scope.my_team, Ability.counter_rate, 0.3, 3),
                                           Effect(Scope.my_team, Ability.pene_rate, 0.3, 3)], debuffs=[],
                             adj_buffs=[], ),
                       Skill(mp=141, buffs=[Effect(Scope.my_team, Recover.hp_imm, 0.3)], debuffs=[],
                             adj_buffs=[Effect(Scope.my_team, AdjBuff.extend_buff, 2, 0),
                                        Effect(Scope.foes, AdjBuff.extend_debuff, 2, 0)], ),
                       Skill(is_special=True, buffs=[Effect(Scope.my_team, Recover.hp_imm, 0.8),
                                                     Effect(Scope.my_team, Recover.hp_turn, 0.4, 3),
                                                     Effect(Scope.my_team, Ability.str, 1.0, 3),
                                                     Effect(Scope.my_team, Ability.mag, 1.0, 3)], debuffs=[],
                             adj_buffs=[], )],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, SuccessUp.guard, 0.3),
                                            Effect(Scope.my_self, Endurance.wind, 0.35),
                                            Effect(Scope.my_self, Ability.mag, 0.25),
                                            Effect(Scope.my_self, Ability.agi, 0.25),
                                            Effect(Scope.my_self, Ability.dex, 0.25),
                                            Effect(Scope.my_self, Recover.hp_turn, 0.04),
                                            Effect(Scope.my_self, Recover.mp_turn, 0.04)])],
               counter_hp=True,

               ),

    Adventurer("偶像莉涅", 2510 + 1084, 312 + 87,
               721 + 201, 212 + 69, 413 + 81, 762 + 284, 727 + 304,
               skills=[
                   Skill(Scope.foes, Power.super, Damage.light, Attack.phy, mp=59,
                         adj_buffs=[Effect(Scope.foes, AdjBuff.clear_buff, 0, 0, Ability.str),
                                    Effect(Scope.foes, AdjBuff.clear_buff, 0, 0, Ability.mag)]),
                   Skill(is_fast=True, p=45, buffs=[Effect(Scope.my_team, Ability.energy_bar, 0.33, 4),
                                                    Effect(Scope.my_team, Ability.counter_rate, 0.20, 4),
                                                    Effect(Scope.my_team, Ability.crit_rate, 0.20, 4),
                                                    Effect(Scope.my_team, Ability.pene_rate, 0.20, 4)]),
                   Skill(Scope.foe, Power.high, Damage.light, Attack.phy, mp=25,
                         boost_by_buff=[Effect(Scope.my_self, Ability.crit_rate, 0.40)]),
               ]),
    Adventurer("無人島春姬", 2103, 313,
               209, 183, 397, 392, 849,
               skills=[Skill(mp=52, buffs=[Effect(Scope.my_self, Ability.mag, 0.6, 4),
                                           Effect(Scope.my_self, Ability.dex, 0.6, 4),
                                           Effect(Scope.my_self, Damage.light, 0.6, 4),
                                           Effect(Scope.my_team, Ability.mag, 0.3, 4),
                                           Effect(Scope.my_team, Ability.dex, 0.3, 4),
                                           Effect(Scope.my_team, Damage.light, 0.3, 4)], debuffs=[], adj_buffs=[], ),
                       Skill(mp=20, buffs=[], debuffs=[Effect(Scope.foe, Endurance.foe, 0.2, 4)],
                             adj_buffs=[Effect(Scope.foe, AdjBuff.clear_buff, 0, 0, Ability.str),
                                        Effect(Scope.foe, AdjBuff.clear_buff, 0, 0, Ability.mag),
                                        Effect(Scope.foe, AdjBuff.clear_buff, 0, 0, Ability.agi)], ),
                       Skill(Scope.foe, Power.super, Damage.light, Attack.mag,
                             boost_by_buff=[Effect(Scope.my_self, Ability.mag, 0.4)], mp=136,
                             buffs=[Effect(Scope.my_team, Recover.hp_turn, 0.2, 1)], debuffs=[], adj_buffs=[], ),
                       Skill(Scope.foe, Power.ultra, Damage.light, Attack.mag,
                             boost_by_buff=[Effect(Scope.my_self, Ability.mag, 0.8)], is_special=True,
                             buffs=[Effect(Scope.my_team, Recover.hp_turn, 0.4, 3),
                                    Effect(Scope.my_team, Damage.light, 0.8, 3)], debuffs=[], adj_buffs=[], )],
               passive_skills=[Skill(
                   buffs=[Effect(Scope.my_self, Recover.hp_turn, 0.08), Effect(Scope.my_self, Recover.mp_turn, 0.08),
                          Effect(Scope.my_self, SuccessUp.counter, 0.5),
                          Effect(Scope.my_self, Endurance.dark, 0.35)])],
               killer=Killer.undead,
               ),
    Adventurer("18", 2506, 224,
               1387, 599, 601, 416, 981,
               skills=[Skill(is_fast=True, mp=47, buffs=[Effect(Scope.my_team, Endurance.foes, 0.35, 3),
                                                         Effect(Scope.my_team, Endurance.foe, 0.35, 3)], debuffs=[],
                             adj_buffs=[], ),
                       Skill(Scope.foe, Power.high, Damage.earth, Attack.phy, temp_boost=True, mp=30, buffs=[],
                             debuffs=[], adj_buffs=[], ),
                       Skill(Scope.foes, Power.super, Damage.earth, Attack.phy, temp_boost=True, mp=69, buffs=[],
                             debuffs=[], adj_buffs=[Effect(Scope.foes, AdjBuff.shorten_buff, 1, 0)], ),
                       Skill(Scope.foes, Power.ultra, Damage.earth, Attack.phy, temp_boost=True, is_special=True,
                             buffs=[], debuffs=[], adj_buffs=[], )],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, SuccessUp.guard, 0.3),
                                            Effect(Scope.my_self, Endurance.thunder, 0.35),
                                            Effect(Scope.my_self, Ability.str, 0.4),
                                            Effect(Scope.my_self, Ability.end, 0.4)])],
               killer=Killer.dragon,
               ),
])
boss_cards = MyCards([
    Adventurer("九魔姬", 100000000, 0,
               0, 100, 0, 0, 1000,
               skills=[Skill(Scope.foes, Power.low, Damage.dark, Attack.mag)],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, Endurance.fire, 0.1)])]
               ),
    Adventurer("紅髮怪人", 100000000, 0,
               100, 100, 0, 0, 0,
               skills=[Skill(Scope.foes, Power.low, Damage.none, Attack.phy),
                       Skill(Scope.foes, Power.high, Damage.none, Attack.phy),
                       Skill(debuffs=[Effect(Scope.my_self, Endurance.mag, 0.7, 15)]),
                       Skill(adj_buffs=[Effect(Scope.my_self, AdjBuff.clear_debuff, 0, 0)]),
                       Skill(buffs=[Effect(Scope.my_self, Ability.str, 0.20, 3)]),
                       ],
               passive_skills=[Skill(debuffs=[Effect(Scope.my_self, Endurance.light, 0.7)])],
               init_skill=Skill(debuffs=[Effect(Scope.my_self, Endurance.mag, 0.7, 15)], idx="init"),
               ),
])
ranker = Ranker()

boss1 = boss_cards.get("紅髮怪人")
enemy_team = Team(1, [boss1.set_steps([
    [1, 1],  # 1
    [1, 1, 1],  # 2
    [1, 1, 1, 5],  # 3
    [1, 1, 2],  # 4
    [1, 1, 4],  # 5
    [1, 1, 1],  # 6
    [1, 1, 1, 5],  # 7
    [1, 1, 2, 3],  # 8
    [1, 1, 4],  # 9
    [1, 1, 1],  # 10
    [1, 1, 1, 5],  # 11
    [1, 1, 2, 3],  # 12
    [1, 1, 1],  # 13
    [1, 1, 1, 1],  # 14
    1,  # 15
])
])

p1 = adv_cards.get("無人島春姬").set_assist(ass_cards.get("溫泉乳神"))
p2 = adv_cards.get("折紙").set_assist(ass_cards.get("奧娜"))
p3 = adv_cards.get("情人艾斯").set_assist(ass_cards.get("洋裝埃伊娜"))
p4 = adv_cards.get("偶像莉涅").set_one_shot().set_assist(ass_cards.get("新娘乳神"))
p5 = adv_cards.get("18").set_one_shot().set_assist(ass_cards.get("情人埃伊娜"))
p6 = adv_cards.get("春姬").set_assist(ass_cards.get("劇場乳神"))

#                                1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
my_team = Team(4, [p1.set_steps([1, 2, 3, 4, 3, 2, 3, 3, 3, 2, 3, 2, 4, 3, 3]),
                   p2.set_steps([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1]),
                   p3.set_steps([3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1]),
                   p4.set_steps([2]),
                   p5.set_steps([x, 1]),
                   p6.set_steps([x, x, 1, 3, 3, 1, 3, 2, 3, 1, 3, 2, 3, 3, 1]),
                   ]
               )

battle = BattleStage(15)
battle.set_player_team(my_team).set_enemy_team(enemy_team)
battle.run()

rank = ranker.add(battle)
ranker.report(rank=rank, detail=True)

# ranker.report(limit=1, detail=False)
# ranker.report(rank=rank, detail=False)

# ranker.report()
