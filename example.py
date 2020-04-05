from sim_common import *

my_ass_cards = MyCards([
    Assist("劇場乳神", 1207 + 305, 213 + 60, 
           643 + 77, 0, 0, 0, 289 + 77, tags=[Damage.foe],
           skill=Skill(debuffs=[Effect(Scope.foes, Damage.foe, 0.15)], 
                       buffs=[Effect(Scope.my_team, Ability.dex, 0.20)])
           ),
    Assist("月神", 1150+300, 198_60, 
           571 + 72, 0, 0, 0, 284 + 72, tags=[Ability.str],
           skill=Skill(buffs=[Effect(Scope.my_self, Ability.str, 0.15), Effect(Scope.my_team, Ability.str, 0.10)])
           ),
    Assist("泳裝芙蕾雅", 1416+300, 210+50, 
            461 + 72, 0, 0, 0, 441 + 72, tags=[Damage.ice],
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.ice, 0.10)])
           ),
    Assist("製作人荷米斯", 1424+300, 218+60,
            459 + 72, 0, 0, 0, 459 + 72, tags=[Damage.light, Damage.fire],
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.fire, 0.10), Effect(Scope.my_team, Damage.light, 0.10)])
           ),
    Assist("聖爐乳神", 1230+305, 214+60,
            398 + 77, 0, 0, 0, 398 + 77, tags=[Damage.foes],
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.foes, 0.15)], buffs=[Effect(Scope.my_team, Ability.agi, 0.10)])
           ),
    Assist("泳裝埃伊娜", 1420+300, 194+60,
            356 + 56, 0, 0, 0, 372 + 72, tags=[Damage.ice],
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.ice, 0.15)])
           ),
    Assist("奧娜", 1202+300, 238+60,
            412 + 72, 0, 0, 0, 412 + 72, tags=[Damage.phy, Damage.mag],
           skill=Skill(debuffs=[Effect(Scope.foes, Damage.phy, 0.15), Effect(Scope.foes, Damage.mag, 0.15)])
           ),
    Assist("睡衣乳神", 1143+305, 201+60,
            562 + 77, 0, 0, 0, 293 + 77, tags=[Damage.thunder],
           skill=Skill(debuffs=[Effect(Scope.foes, Endurance.thunder, 0.10)])
           ),
    Assist("流氓萬能", 1116+200, 180+38,
            379 + 40, 0, 0, 0, 446 + 41, tags=[Damage.phy, Damage.mag],
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.08), Effect(Scope.my_team, Ability.mag, 0.08),
                              Effect(Scope.my_team, Ability.dex, 0.08), Effect(Scope.my_team, Ability.agi, 0.08)])
           ),
    Assist("新娘希兒", 930+240, 210+60,
            338 + 72, 0, 0, 0, 338 + 72, tags=[Damage.mag],
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.ice, 0.10), Effect(Scope.my_team, Damage.dark, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.ice, 0.05), Effect(Scope.foes, Endurance.dark, 0.05)])
           ),
    Assist("鴨子乳神", 943+305, 204+60,
            390 + 77, 0, 0, 0, 190 + 77, tags=[Ability.str, Damage.wind, Damage.ice],
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.ice, 0.10), Effect(Scope.foes, Endurance.wind, 0.10)])
           ),
    Assist("伯爵希兒", 1188+240, 138+60,
            323 + 72, 0, 0, 0, 389 + 72, tags=[Ability.energy_bar],
           skill=Skill(buffs=[Effect(Scope.my_self, Ability.energy_bar, 0.66)])
           ),
    Assist("情人埃伊娜", 946+300, 196+60,
            299 + 56, 0, 0, 0, 315 + 72, tags=[Damage.light, Damage.earth],
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.light, 0.10), Effect(Scope.my_team, Damage.earth, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.light, 0.05), Effect(Scope.foes, Endurance.earth, 0.05)])
           ),
    Assist("新娘乳神", 1015+305, 158+60,
            221 + 77, 0, 0, 0, 486 + 77, tags=[Ability.mag],
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.mag, 0.15)])
           ),
    Assist("阿波羅", 872+150, 138+40,
            371 + 36, 0, 0, 0, 153+36, tags=[Ability.str, Damage.light, Damage.fire],
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.light, 0.10), Effect(Scope.foes, Endurance.fire, 0.10)])
           ),
    Assist("炸彈娘-蒂", 926+150, 105+30,
            324 + 36, 0, 0, 0, 150 + 36, tags=[Ability.str, Damage.light, Damage.earth],
           skill=Skill(buffs=[Effect(Scope.my_team, Ability.str, 0.10),
                              Effect(Scope.my_team, Damage.fire, 0.08), Effect(Scope.my_team, Damage.earth, 0.08)])
           ),
    Assist("劍之聖女", 684+150, 175+30,
            256+36, 0, 0, 0, 276+36, tags=[Damage.thunder, Damage.dark],
           skill=Skill(buffs=[Effect(Scope.my_team, Damage.thunder, 0.10)],
                       debuffs=[Effect(Scope.foes, Endurance.dark, 0.10)])
           ),
])

my_adv_cards = MyCards([
    Adventurer("新裝艾斯", 3957+1475, 371+ 130,
                2133 + 808, 0, 0, 0, 0, tags=[Damage.phy, Damage.ice, Scope.foe, Scope.foes],
               skills=[
                   Skill(mp=47,
                       buffs=[Effect(Scope.my_self, Damage.ice, 0.60, 4), Effect(Scope.my_self, Ability.str, 0.60, 4)],
                       debuffs=[Effect(Scope.foes, Ability.agi, 0.30, 4)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy, mp=44),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.phy, temp_boost=True, mp=34),
                   Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True,
                         buffs=[Effect(Scope.my_self, Damage.ice, 0.80, 4), Effect(Scope.my_self, Ability.str, 0.80, 4)]
                         ),
               ]),
    Adventurer("英雄阿爾戈", 4017+1475, 356+130,
                2180 + 813, 0, 0, 0, 0, tags=[Damage.phy, Damage.fire, Scope.foe, Scope.foes],
               skills=[
                   Skill(Scope.foes, Power.low, Damage.fire, Attack.phy, mp=37,
                         buffs=[Effect(Scope.my_self, Damage.fire, 0.50, 4),
                                Effect(Scope.my_self, Ability.str, 0.50, 4)]),
                   Skill(Scope.foes, Power.super, Damage.fire, Attack.phy, mp=49),
                   Skill(Scope.foe, Power.high, Damage.fire, Attack.phy, mp=32,
                         adj_buffs=[Effect(Scope.foe, AdjBuff.extend_debuff, 1, 0)]),
                   Skill(Scope.foes, Power.ultra, Damage.fire, Attack.phy, is_special=True, temp_boost=True,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.30, 1)]
                         ),
               ]),
    Adventurer("聖誕千草", 3903+1445, 377+130,
                2011 + 748, 0, 0, 0, 0, tags=[Damage.phy, Damage.ice, Scope.foe, Scope.foes],
               skills=[Skill(mp=35, buffs=[Effect(Scope.my_self, Ability.energy_bar, 1, 5),
                                    Effect(Scope.my_self, Ability.agi, 0.75, 5), 
                                    Effect(Scope.my_self, Ability.dex, 0.75, 5)]),
                       Skill(Scope.foes, Power.super, Damage.ice, Attack.phy, mp=54, temp_boost=True,
                             adj_buffs=[Effect(Scope.my_self, AdjBuff.clear_debuff, 0, 0)]),
                       Skill(Scope.foe, Power.high, Damage.ice, Attack.phy, mp=33,
                             boost_by_buff=[Effect(Scope.my_self, Ability.dex, 0.25)]),
                       Skill(Scope.foes, Power.ultra, Damage.ice, Attack.phy, 
                             boost_by_buff=[Effect(Scope.my_self, Ability.dex, 0.25), 
                                            Effect(Scope.my_self, Ability.agi, 0.25)]),
                       ],
                killer=Killer.worm,
                passive_skill=[Skill(buffs=[Effect(Scope.my_self, Endurance.fire, 0.35)])],
               ),
    Adventurer("米卡莎", 4143+1475, 312+130,
                1928 + 637, 0, 0, 0, 0, tags=[Damage.phy, Damage.dark, Scope.foe],
               skills=[Skill(Scope.foe, Power.low, Damage.dark, Attack.phy, mp=25,
                             buffs=[Effect(Scope.my_self, Ability.str, 0.75, 4)]),
                       Skill(Scope.foe, Power.mid, Damage.dark, Attack.phy, mp=29,
                             buffs=[Effect(Scope.my_self, Damage.dark, 0.60, 4)]),
                       Skill(Scope.foe, Power.high, Damage.dark, Attack.phy, mp=26,
                             adj_buffs=[Effect(Scope.foe, AdjBuff.clear_buff, 0, 0, Ability.mag)]),
                       Skill(Scope.foe, Power.ultra, Damage.dark, Attack.phy, is_special=True, temp_boost=True),
                       ]
               ),
    Adventurer("劇場莉莉", 4059+1435, 323+130,
                1927 + 641, 0, 0, 0, 0, tags=[Damage.phy, Damage.thunder, Scope.foe],
               skills=[Skill(Scope.foe, Power.high, Damage.thunder, Attack.phy, temp_boost=True, mp=27,
                             debuffs=[Effect(Scope.foe, Endurance.foe, 0.15, 4)]),
                       Skill(Scope.foe, Power.high, Damage.thunder, Attack.phy, temp_boost=True, mp=37,
                             buffs=[Effect(Scope.my_team, Damage.thunder, 0.20, 3)]),
                       Skill(Scope.foe, Power.low, Damage.thunder, Attack.phy, mp=25,
                             buffs=[Effect(Scope.my_self, Ability.str, 0.80, 4)]),
                       Skill(Scope.foe, Power.ultra, Damage.thunder, Attack.phy, is_special=True, temp_boost=True),
                       ]
               ),
    Adventurer("歌殺", 3897+1475, 386+130,
                2120 + 806, 0, 0, 0, 0, tags=[Damage.phy, Damage.dark, Mission.one_shot, Scope.foe],
               skills=[
                   Skill(mp=45,
                       debuffs=[Effect(Scope.foes, Endurance.phy, 0.30, 4), Effect(Scope.foes, Endurance.dark, 0.30, 4)]),
                   Skill(Scope.foes, Power.mid, Damage.dark, Attack.phy, mp=32,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.20, 4), Effect(Scope.foe, Endurance.foes, 0.20, 4)]),
                   Skill(Scope.foe, Power.super, Damage.dark, Attack.phy, temp_boost=True, mp=50,
                         buffs=[Effect(Scope.my_self, Ability.str, 0.30, 3),
                                Effect(Scope.my_self, Damage.dark, 0.30, 3)]),
                   Skill(Scope.foe, Power.ultra, Damage.dark, Attack.phy, is_special=True,
                         buffs=[Effect(Scope.my_self, Damage.dark, 0.90, 3),
                                Effect(Scope.my_self, Ability.str, 0.90, 3)]
                         ),
               ]),
    Adventurer("古代黑肉", 2891+675, 249+81,
                1331 + 484, 0, 0, 0, 0, tags=[Mission.one_shot],
               skills=[
                   Skill(Scope.foe, Power.high, Damage.dark, Attack.phy, temp_boost=True, mp=37),
                   Skill(Scope.foes, Power.super, Damage.dark, Attack.phy, temp_boost=True, mp=53),
                   Skill(Scope.foes, Power.high, Damage.dark, Attack.phy, mp=35,
                         debuffs=[Effect(Scope.foes, Endurance.foes, 0.30, 3)]),
                   Skill(Scope.foes, Power.ultra, Damage.dark, Attack.phy, is_special=True),
               ]),
    Adventurer("聖誕樁", 3785+1475, 342+130,
                1751+732, 0, 0, 0, 0, tags=[Damage.phy, Damage.ice, Scope.foe, Scope.foes, Mission.one_shot],
               skills=[
                   Skill(Scope.foes, Power.mid, Damage.ice, Attack.phy, mp=30,
                         debuffs=[Effect(Scope.foes, Endurance.phy, 0.30, 3), Effect(Scope.foes, Endurance.ice, 0.30, 3)]),
                   Skill(Scope.foes, Power.high, Damage.ice, Attack.phy, mp=49),
                   Skill(Scope.foe, Power.high, Damage.ice, Attack.phy, mp=30),
                   Skill(Scope.foe, Power.ultra, Damage.ice, Attack.phy, is_special=True, temp_boost=True),
               ]),
    Adventurer("折紙", 4040+1425, 414+140,
                0, 0, 0, 0, 2045 + 880, tags=[Damage.mag, Damage.light, Scope.foe, Scope.foes],
               skills=[
                   Skill(Scope.foe, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=34,
                         debuffs=[Effect(Scope.foe, Endurance.phy, 0.35, 4)]),
                   Skill(Scope.foe, Power.mid, Damage.light, Attack.mag, mp=30,
                         buffs=[Effect(Scope.my_self, Ability.mag, 0.80, 4)]),
                   Skill(Scope.foes, Power.high, Damage.light, Attack.mag, temp_boost=True, mp=29),
                   Skill(Scope.foe, Power.ultra, Damage.light, Attack.mag, is_special=True, temp_boost=True),
               ]),
    Adventurer("春姬", 3740+1450, 438+160,
                0, 0, 0, 0, 2045 + 880, tags=[Damage.mag, Damage.fire, Scope.foe, Scope.foes],
               skills=[
                   Skill(Scope.foes, Power.mid, Damage.fire, Attack.mag, mp=34,
                         debuffs=[Effect(Scope.foes, Ability.str, 0.40, 3)]),
                   Skill(mp=12, buffs=[Effect(Scope.my_self, Recover.mp, 0.15)]),
                   Skill(mp=141, adj_buffs=[Effect(Scope.foes, AdjBuff.extend_debuff, 2, 0),
                                    Effect(Scope.my_team, AdjBuff.extend_buff, 2, 0)]),
                   Skill(is_special=True, buffs=[Effect(Scope.my_team, Ability.mag, 1.0, 3),
                                Effect(Scope.my_team, Ability.str, 1.0, 3)]),
               ]),
    Adventurer("泳裝媽媽", 2744+864, 334+88,
                0, 0, 0, 0, 1242+489, tags=[Damage.mag, Damage.ice, Scope.foe, Mission.one_shot],
               skills=[
                   Skill(Scope.foe, Power.low, Damage.ice, Attack.mag, mp=30,
                         buffs=[Effect(Scope.my_team, Ability.mag, 0.40, 3),
                                Effect(Scope.my_team, Damage.ice, 0.40, 3)]),
                   Skill(Scope.foe, Power.high, Damage.ice, Attack.mag, mp=32),
                   Skill(Scope.foe, Power.super, Damage.ice, Attack.mag, mp=35,
                         debuffs=[Effect(Scope.foe, Endurance.foe, 0.20, 3)]),
                   Skill(Scope.foe, Power.ultra, Damage.ice, Attack.mag, is_special=True),
               ]),
])

boss_cards = MyCards([
    Adventurer("九魔姬", 100000000, 0,
                0, 100, 0, 0, 1000,
               skills=[Skill(Scope.foes, Power.high, Damage.dark, Attack.mag)],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, Endurance.fire, 0.1)])]
               ),
    Adventurer("骷髏-小", 100000000, 0,
                100, 150, 0, 0, 0,
               skills=[Skill(Scope.foes, Power.high, Damage.dark, Attack.phy)],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, Endurance.fire, 0.1)])]
               ),
    Adventurer("骷髏-大", 100000000, 0,
                100, 150, 0, 0, 0,
               skills=[Skill(Scope.foes, Power.high, Damage.dark, Attack.phy)],
               passive_skills=[Skill(buffs=[Effect(Scope.my_self, Endurance.fire, 0.1)])]
               ),
])

ranker = Ranker()

boss = [boss_cards.get_card_by_name("骷髏-小").set_predefined_steps([1, 1, 1, 1, 1, 1, 1, 1, 1]),
        boss_cards.get_card_by_name("骷髏-小").set_predefined_steps([1, 1, 1, 1, 1, 1, 1, 1, 1]),
        boss_cards.get_card_by_name("骷髏-大").set_predefined_steps([1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ]
enemy_team =  Team(3, boss)

advs = [my_adv_cards.get_card_by_name("新裝艾斯")                   .set_predefined_steps([1, 2, 2, 2, 2, 2, 2, 2, 4]),
        my_adv_cards.get_card_by_name("英雄阿爾戈")                 .set_predefined_steps([1, 2, 2, 2, 2, 2, 2, 2, 2]),
        my_adv_cards.get_card_by_name("聖誕千草")                   .set_predefined_steps([1, 3, 3, 3, 3, 2, 2, 2, 2]),
        my_adv_cards.get_card_by_name("米卡莎").set_one_shot()      .set_predefined_steps([1]),
        my_adv_cards.get_card_by_name("劇場莉莉").set_one_shot()    .set_predefined_steps([0, 1]),
        my_adv_cards.get_card_by_name("春姬")                       .set_predefined_steps([0, 0, 3, 3, 3, 3, 3, 2, 2]),
        ]

asses = [my_ass_cards.get_card_by_name("劇場乳神"),
         my_ass_cards.get_card_by_name("月神"),
         my_ass_cards.get_card_by_name("泳裝芙蕾雅"),
         my_ass_cards.get_card_by_name("製作人荷米斯"),
         my_ass_cards.get_card_by_name("聖爐乳神"),
         my_ass_cards.get_card_by_name("泳裝埃伊娜")
         ]

my_team = Team(4, advs, asses)

battle = BattleStage(9)
battle.set_player_team(my_team).set_enemy_team(enemy_team)
battle.run()


ranker.add(battle)

advs = [my_adv_cards.get_card_by_name("新裝艾斯")                   .set_predefined_steps([1, 2, 2, 2, 2, 2, 2, 2, 4]),
        my_adv_cards.get_card_by_name("英雄阿爾戈")                 .set_predefined_steps([1, 2, 2, 2, 2, 2, 2, 2, 2]),
        my_adv_cards.get_card_by_name("聖誕千草")                   .set_predefined_steps([1, 3, 3, 3, 3, 2, 2, 2, 2]),
        my_adv_cards.get_card_by_name("米卡莎").set_one_shot()      .set_predefined_steps([1]),
        my_adv_cards.get_card_by_name("劇場莉莉").set_one_shot()    .set_predefined_steps([0, 1]),
        my_adv_cards.get_card_by_name("春姬")                       .set_predefined_steps([0, 0, 3, 3, 3, 3, 3, 2, 2]),
        ]

asses = [my_ass_cards.get_card_by_name("月神"),
         my_ass_cards.get_card_by_name("劇場乳神"),
         my_ass_cards.get_card_by_name("泳裝芙蕾雅"),
         my_ass_cards.get_card_by_name("製作人荷米斯"),
         my_ass_cards.get_card_by_name("聖爐乳神"),
         my_ass_cards.get_card_by_name("泳裝埃伊娜")
         ]

my_team = Team(4, advs, asses)

battle = BattleStage(9)
battle.set_player_team(my_team).set_enemy_team(enemy_team)
battle.run()


ranker.add(battle)
# ranker.report(limit=1, detail=False)
ranker.report(limit=1, detail=True)
#ranker.report()