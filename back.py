import random

class Zone:
    def __init__(self, name, level, description):
        self.name = name
        self.description = description
        self.level = level
        ZONES.append(self)
class Town(Zone):
    def __init__(self, name, description, level, shop):
        Zone.__init__(self, name, description, level)
        self.shop = shop
class Dung(Zone):
    def __init__(self, name, description, level, events):
        Zone.__init__(self, name, description, level)
        self.events = events

class Player:
    def __init__(self, name, clas, load=False):
        self.name = name
        self.clas = clas if clas else random.choice(tuple(CLASS))
        self.time = 0

        self.winEvent = dict(map(lambda e: (e.name, 0), EVENTS))
        self.getItem = dict(map(lambda i: (i, 0), ITEMS))
        self.movZone = dict(map(lambda z: (z.name, 0), ZONES))

        if not load:
            self.hp = CLASS[self.clas][1]
            self.zone = META["zone"]
            self.items = CLASS[self.clas][2]
            self.movZone[self.zone.name] += 1
            for i in self.items: self.getItem[i] += 1
    def hit(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp
    def res(self, heal):
        self.hp = min(CLASS[self.clas][1], self.hp + heal)
    def move(self, nameZone):
        z = zoneByName(nameZone)
        if type(z) == Dung:
            self.zone = z
            self.time += 1
            self.movZone[z.name] += 1
            return [random.choice(z.events) for i in range(z.level)]
        if type(z) == Town:
            if self.items.count(META["taxes"]) >= z.level:
                [self.items.remove(META["taxes"]) for i in range(z.level)]
                self.zone = z
                self.time += 1
                self.movZone[z.name] += 1
                self.res(z.level)
        return []
    def save(self):
        old = []
        try:
            with open(_PATH + 'save') as f:
                old = filter(lambda x: x.split(';')[0] != self.name, f.readlines())
        except:
            pass
        with open(_PATH + 'save', 'w') as f:
            if self.hp:
                # name, time, class, hp, zone, {item}
                f.write("%s;%s;%s;%s;%s;%s;" % (self.name, self.time, self.clas, self.hp, self.zone.name, ','.join(self.items)))
                # win-events, get-items, mov-zones
                f.write(','.join(["%s|%d" % e for e in self.winEvent.items()]) + ';')
                f.write(','.join(["%s|%d" % e for e in self.getItem.items()]) + ';')
                f.write(','.join(["%s|%d" % e for e in self.movZone.items()]) + '\n')
            f.writelines(old)
    def change(self, item):
        if item in self.items and type(self.zone) == Town:
            new = random.choice(self.zone.shop)
            if new != item:
                self.items.remove(item)
                self.add(new)
            return new
        return None
    def add(self, *items):
        for n,i in enumerate(items):
            if len(self.items) == CLASS[self.clas][0]: return n
            self.items.append(i)
            self.getItem[i] += 1
class Event:
    def __init__(self, name, weak, ifWin, ifLose):
        self.name = name
        self.weak = weak
        self.ifWin = ifWin
        self.ifLose = ifLose
        EVENTS.append(self)
    def clash(self, player):
        end = int(not self.weak or (self.weak in player.items))
        if end:
            if self.weak: player.items.remove(self.weak)
            player.winEvent[self.name] += 1
        code = (self.ifLose, self.ifWin)[end]
        if code[0] == 'H': self.hit(player=player, hits=int(code[1]))
        if code[0] == 'I': self.give(player=player, mount=int(code[1]))
        if code[0] == 'M': self.move(player=player, zone=code[1:])
        if code[0] == 'N': pass
        
        return end
    
    def hit(self, **kwargs):
        p = kwargs['player']
        h = kwargs['hits']
        p.hit(h)
    def move(self, **kwargs):
        p = kwargs['player']
        z = kwargs['zone']
        p.movZone[p.zone.name] -= 1
        p.zone = zoneByName(z)
    def give(self, **kwargs):
        p = kwargs['player']
        m = kwargs['mount']
        p.add(*[random.choice(ITEMS) for i in range(m)])

class Goal:
    def __init__(self, name, cond, *args):
        self.name = name
        self.cond = cond
        self.args = args # VALUE, COUNT
        GOALS.append(self)
    def completed(self, player):
        if self.cond == 'W': per = player.winEvent[self.args[0]]
        if self.cond == 'G': per = player.getItem[self.args[0]]
        if self.cond == 'M': per = player.movZone[self.args[0]]
        
        return min(round(per / self.args[1], 2), 1)

def loadData(path):
    global _PATH, META
    _PATH = path
    EVS_AUX = dict()
    
    with open(path + 'data') as f:
        for l in f:
            if len(l) == 1: continue
            dat = l.strip().split(';')
            
            # ZONE
            if dat[0] == "zone":
                dat[3] = int(dat[3])
                dat[5] = dat[5].split(',')
                if dat[1] == "town": Town(*dat[2:])
                if dat[1] == "dung":
                    dat[5] = list(filter(lambda k: k in dat[5], EVS_AUX))
                    dat[5] = list(map(lambda k: EVS_AUX[k], dat[5]))
                    Dung(*dat[2:])
            # EVENT
            if dat[0] == "event": EVS_AUX[dat[1]] = Event(*dat[1:])
            # ITEM
            if dat[0] == "item": ITEMS.append(dat[1])
            # GOAL
            if dat[0] == "goal": Goal(dat[1], dat[2][0], dat[3], int(dat[2][1:]))
            # INIT
            if dat[0] == "meta":
                METAS.append({
                    "zone":zoneByName(dat[1]),
                    "taxes":dat[2],
                    "start":dat[3],
                    "final":dat[4],
                    })
            #CLASS
            if dat[0] == "class": CLASS[dat[1]] = (int(dat[2]), int(dat[3]) ,dat[4].split(','))

        META = METAS[0]
def logIn(namePlayer):
    try:
        f = open(_PATH + 'save')
    except:
        return None
    
    for l in f:
        if len(l) == 1: continue
        dat = l.strip().split(';')
        if dat[0] == namePlayer:
            p = Player(dat[0], dat[2], load=True)
            p.hp = int(dat[3]) # HP
            p.time = int(dat[1]) # TIME
            p.zone = zoneByName(dat[4]) # ZONE
            p.items = dat[5].split(',') # ITEMS
            # WIN-EVENT
            for e in dat[6].split(','):
                name,count = e.split('|')
                p.winEvent[name] = int(count)
            # GET-ITEM
            for e in dat[7].split(','):
                name,count = e.split('|')
                p.getItem[name] = int(count)
            # MOV-ZONE
            for e in dat[8].split(','):
                name,count = e.split('|')
                p.movZone[name] = int(count)
            
            return p
    f.close()
    return None
def zoneByName(name):
    for z in ZONES:
        if z.name == name: return z
    return None
def eventByName(name):
    for e in EVENTS:
        if e.name == name: return e
    return None
def get_advice():
    typ = random.choice(("zone","event"))
    if typ == "zone": obj = random.choice(ZONES)
    if typ == "event": obj = random.choice(EVENTS)
    return (typ, obj)

_PATH = "/"

ZONES = list()
EVENTS = list()
ITEMS = list()
GOALS = list()
CLASS = dict()

METAS = list()
META = None