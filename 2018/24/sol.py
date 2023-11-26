from utils import *

players = inp_groups()

class Group:
    def __init__(self, army, line):
        # print(line)
        self.units, self.hp_per_unit, weaks_imms, self.atk, self.ty, self.init = match(r'(\d+) units each with (\d+) hit points(.*) with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
        self.army = army
        self.weaks = match(r'weak to ([^;)]*)', weaks_imms, exact=False, onfail=[""])[0].split(", ")
        self.imms = match(r'immune to ([^;)]*)', weaks_imms, exact=False, onfail=[""])[0].split(", ")
        self.target=None

    def eff_dmg(self):
        return self.units * self.atk
    
    def dmg_to(self, opp):
        mod = 1
        if self.ty in opp.weaks:
            mod *= 2
        if self.ty in opp.imms:
            mod *= 0
        return self.eff_dmg()*mod
    
    def alive(self):
        return self.units > 0

class Army:
    def __init__(self, lines):
        self.name = lines[0] 
        self.groups = [Group(self, x) for x in lines[1:]]

armies=None, 
all_grps=None
def build_armies(boost = 0):
    global armies, all_grps
    armies = mapl(Army, players)
    armies[1].opp, armies[0].opp = armies

    for gr in armies[0].groups:
        gr.atk += boost

    all_grps = armies[0].groups + armies[1].groups

def target_order():
    return sorted(all_grps, key=lambda g:(g.eff_dmg(), g.init), reverse=True)

def select_targets():
    targets = []

    for grp in target_order():
        enemies = grp.army.opp.groups 
        enemies = [e for e in enemies if e not in targets and grp.dmg_to(e) > 0]
        enemies_prio = sorted(enemies, key=(lambda en: (grp.dmg_to(en), en.eff_dmg(), en.init)), reverse=True)
        if enemies_prio:
            en = enemies_prio[0]
            grp.target = en
            targets.append(en)

def attack():
    progress = False
    for grp in sorted(all_grps, key=lambda g: g.init, reverse=True):
        if grp.target and grp.alive():
            opp = grp.target 
            dmg = grp.dmg_to(opp)
            lost_units = dmg // opp.hp_per_unit 
            opp.units -= lost_units 
            grp.target = None
            if lost_units > 0:
                progress = True
    return progress

def fight():
    global all_grps

    select_targets()
    progress = attack()
    for a in armies:
        a.groups = [g for g in a.groups if g.alive()]
    all_grps = armies[0].groups + armies[1].groups
    return progress

def battle(boost):
    print(f"{boost}")
    build_armies(boost)
    progress = True
    while armies[0].groups and armies[1].groups and progress:
    # print(f"Round {round}")
        progress = fight()

    return bool(armies[1].groups)

battle(0)
print("Part 1:", sum(g.units for g in all_grps))

b = bin_search(0, None, battle)
battle(b+1)
print("Part 2:", sum(g.units for g in all_grps))