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
    def change(self):
        return random.choice(self.shop)

class Dung(Zone):
    def __init__(self, name, description, level, events):
        Zone.__init__(self, name, description, level)
        self.events = events

class Player:
    def __init__(self, name, zone, items):
        self.name = name
        self.zone = zone
        self.items = items
    def hit(self, damage):
        random.shuffle(self.items)
        self.items = self.items[min(damage, len(self.items)) : ]
        return len(self.items)
    def move(self, nameZone):
        for z in ZONES:
            if z.name == nameZone:
                if type(z) == Dung:
                    self.zone = z
                    return [random.choice(z.events) for i in range(z.level)]
                if type(z) == Town:
                    if self.items.count(META["taxes"]) >= z.level:
                        [self.items.remove(META["taxes"]) for i in range(z.level)]
                        self.zone = z
        return []
    def save(self):
        with open(_PATH + 'save') as f:
            old = filter(lambda x: x.split(';')[0] != self.name, f.readlines())
        with open(_PATH + 'save', 'w') as f:
            s = "%s;%s;%s" % (self.name, self.zone.name, ','.join(self.items))
            f.write(s + '\n')
            f.writelines(old)
    
class Event:
    def __init__(self, name, weak, ifWin, ifLose):
        self.name = name
        self.weak = weak
        self.ifWin = ifWin
        self.ifLose = ifLose
        EVENTS.append(self)
    def clash(self, player):
        end = int(self.weak in player.items)
        if end: player.items.remove(self.weak)
        code = (self.ifLose, self.ifWin)[end]

        # H<N>: GOLPEA AL JUGADOR <N> VECES
        if code[0] == 'H': player.hit(int(code[1]))
        # I<N>: ENTREGA <N> ITEMS ALEATORIOS
        if code[0] == 'I':
            rew = [random.choice(ITEMS) for i in range(int(code[1]))]
            player.items += rew[:min(len(rew), META["bag"] - len(player.items))]
        # N: NO PASA NADA
        if code[0] == 'N': pass
        
        return end

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
                    if z.name == dat[1]: return Player(dat[0], z, dat[2].split(','))
        return Player(namePlayer, META["zone"], META["items"])

_PATH = "dq1/"

ZONES = list()
EVENTS = list()
ITEMS = list()
META = tuple()