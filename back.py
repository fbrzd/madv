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
    def __init__(self, name, zone, items, load=False):
        self.name = name
        self.zone = zone
        self.items = items

        self.winEvent = dict(map(lambda e: (e.name, 0), EVENTS))
        self.getItem = dict(map(lambda i: (i, 0), ITEMS))
        self.movZone = dict(map(lambda z: (z.name, 0), ZONES))

        if not load:
            self.movZone[zone.name] += 1
            for i in items: self.getItem[i] += 1
    def hit(self, damage):
        random.shuffle(self.items)
        self.items = self.items[min(damage, len(self.items)) : ]
        return len(self.items)
    def move(self, nameZone):
        for z in ZONES:
            if z.name == nameZone:
                if type(z) == Dung:
                    self.zone = z
                    self.movZone[z.name] += 1
                    return [random.choice(z.events) for i in range(z.level)]
                if type(z) == Town:
                    if self.items.count(META["taxes"]) >= z.level:
                        [self.items.remove(META["taxes"]) for i in range(z.level)]
                        self.zone = z
                        self.movZone[z.name] += 1
        return []
    def save(self):
        with open(_PATH + 'save') as f:
            old = filter(lambda x: x.split(';')[0] != self.name, f.readlines())
        with open(_PATH + 'save', 'w') as f:
            f.write("%s;%s;%s;" % (self.name, self.zone.name, ','.join(self.items)))
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
            if len(self.items) == META["bag"]: return n
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
        end = int(self.weak in player.items)
        if end:
            player.items.remove(self.weak)
            player.winEvent[self.name] += 1
        code = (self.ifLose, self.ifWin)[end]

        # H<N>: GOLPEA AL JUGADOR <N> VECES
        if code[0] == 'H': player.hit(int(code[1]))
        # I<N>: ENTREGA <N> ITEMS ALEATORIOS
        if code[0] == 'I': player.add(*[random.choice(ITEMS) for i in range(int(code[1]))])
        # N: NO PASA NADA
        if code[0] == 'N': pass
        
        return end

class Goal:
    def __init__(self, name, cond):
        self.name = name
        self.cond = cond
        GOALS.append(self)
    def completed(self, player):
        if self.cond[0][0] == 'W': per = player.winEvent[self.cond[1]]
        if self.cond[0][0] == 'G': per = player.getItem[self.cond[1]]
        if self.cond[0][0] == 'M': per = player.movZone[self.cond[1]]
        
        return min(round(per / int(self.cond[0][1:]), 2), 1)

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
            if dat[0] == "goal": Goal(dat[1], (dat[2], dat[3]))
            # INIT
            if dat[0] == "meta":
                for z in ZONES:
                    if z.name == dat[1]:
                        META = {
                            "zone":z,
                            "items":dat[2].split(','),
                            "taxes":dat[3],
                            "bag": int(dat[4])
                            }

def logIn(namePlayer):
    with open(_PATH + 'save') as f:
        for l in f:
            if len(l) == 1: continue
            dat = l.strip().split(';')
            if dat[0] == namePlayer:
                for z in ZONES:
                    if z.name == dat[1]:
                        p = Player(dat[0], z, dat[2].split(','), load=True)
                        
                        # WIN-EVENT
                        for e in dat[3].split(','):
                            name,count = e.split('|')
                            p.winEvent[name] = int(count)
                        # GET-ITEM
                        for e in dat[4].split(','):
                            name,count = e.split('|')
                            p.getItem[name] = int(count)
                        # MOV-ZONE
                        for e in dat[5].split(','):
                            name,count = e.split('|')
                            p.movZone[name] = int(count)
                        
                        return p
                        
    return Player(namePlayer, META["zone"], META["items"])

_PATH = "dq1/"

ZONES = list()
EVENTS = list()
ITEMS = list()
GOALS = list()

META = tuple()