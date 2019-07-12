import random
import json

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

class Zone2:
    def __init__(self, name, typ, info=0, content=[], description=""):
        self.name = name
        self.type = typ
        self.info = info
        self.content = content
        self.description = description

class Player:
    def __init__(self, name, clas):
        self.name = name
        self.clas = clas
        self.state = 'ok'
        self.time = 0
        self.zone, self.items = world.starts[clas]
        
        #self.winEvent = dict(map(lambda e: (e.name, 0), EVENTS))
        #self.getItem = dict(map(lambda i: (i, 0), ITEMS))
        #self.movZone = dict(map(lambda z: (z.name, 0), ZONES))

        #if not load:
        #    self.hp = CLASS[self.clas][1]
        #    self.zone = META["zone"]
        #    self.items = CLASS[self.clas][2]
        #    self.movZone[self.zone.name] += 1
        #    for i in self.items: self.getItem[i] += 1
    def __nonzero__(self):
        return self.state != 'dead'
    def hit(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp
    def res(self, heal):
        self.hp = min(CLASS[self.clas][1], self.hp + heal)
    def move(self, nameZone):
        z = world.zones[nameZone]
        if z.type == "dung":
            self.zone = z
            self.time += 1
            #self.movZone[z.name] += 1
            return [random.choice(z.events) for i in range(z.level)]
        if type(z) == Town:
            if self.items.count(META["taxes"]) >= z.level:
                [self.items.remove(META["taxes"]) for i in range(z.level)]
                self.zone = z
                self.time += 1
                #self.movZone[z.name] += 1
                self.res(z.level)
        return []
    def save(self):
        try:
            with open(_PATH + 'save') as f:
                old = filter(lambda x: x.split(';')[0] != self.name, f.readlines())
        except:
            old = []
        with open(_PATH + 'save', 'w') as f:
            if self:
                # name, time, clas, state, zone, {item}
                f.write(f"{self.name};{self.time};{self.clas};{self.state};{self.zone};{','.join(self.items)}")
                # win-events, get-items, mov-zones
                #f.write(','.join(["%s|%d" % e for e in self.winEvent.items()]) + ';')
                #f.write(','.join(["%s|%d" % e for e in self.getItem.items()]) + ';')
                #f.write(','.join(["%s|%d" % e for e in self.movZone.items()]) + '\n')
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
    def clash(self, player):
        end = int(not self.weak or (self.weak in player.items))
        if end:
            if self.weak: player.items.remove(self.weak)
            player.winEvent[self.name] += 1
        code = (self.ifLose, self.ifWin)[end]

        # H<N>: GOLPEA AL JUGADOR <N> VECES
        if code[0] == 'H': player.hit(int(code[1:]))
        # I<N>: ENTREGA <N> ITEMS ALEATORIOS
        if code[0] == 'I': player.add(*[random.choice(ITEMS) for i in range(int(code[1:]))])
        # T<Z>: TELEPORTAR A ZONA <Z>
        if code[0] == 'Z':
            player.movZone[player.zone.name] -= 1
            player.zone = zoneByName(code[1:])
        # N: NO PASA NADA
        if code[0] == 'N': pass
        
        return end
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
class World:
    def __init__(self, path):
        
        # sync
        self.path = path
        
        self.zones = dict()
        self.events = dict()
        self.starts = dict()
        
        with open(path + 'data.json') as f:
            data = json.load(f)
            
            # LOAD EVENTS
            for e in data['events']:
                iw = e['ifwin']#.split(' ')
                il = e['iflose']#.split(' ')
                self.events[e['name']] = Event(e['name'], e['weak'], iw, il)
            
            # LOAD ZONES
            for z in data['zones']:
                self.zones[z['name']] = Zone2(z['name'], z['type'], z['info'], z['content'], z['description'])
            
            # LOAD GOALS
            #for g in data['goals']:
            #    c,n,a = g['condition'].split(' ')
            #    Goal(g['name'] ,c[0].upper(), a, int(n))
            
            for s in data['start']:
                self.starts[s['name']] = (s['zone'], s['items'])
            
            self.items = data['items']
            self.taxes = data['taxes']
            self.intro = data['intro']
            self.outro = data['outro']
        
        global world
        world = self

def logIn(namePlayer):
    try:
        f = open(world.path + 'save')
    except:
        return None
    
    p = None
    for l in f:
        if len(l) == 1: continue
        # name, time, clas, state, zone, {item}
        dat = l.strip().split(';')
        if dat[0] == namePlayer:
            p = Player(dat[0], dat[2])
            p.time = int(dat[1])
            p.state = dat[3]
            p.zone = dat[4]
            p.items = dat[5].split(',')
            # WIN-EVENT
            #for e in dat[6].split(','):
            #    name,count = e.split('|')
            #    p.winEvent[name] = int(count)
            # GET-ITEM
            #for e in dat[7].split(','):
            #    name,count = e.split('|')
            #    p.getItem[name] = int(count)
            # MOV-ZONE
            #for e in dat[8].split(','):
            #    name,count = e.split('|')
            #    p.movZone[name] = int(count)
    f.close()
    return p
def get_advice(world):
    typ = random.choice(("zone",))
    if typ == "zone": obj = random.choice(list(world.zones.values()))
    if typ == "event": obj = random.choice(world.events.keys())
    return (typ, obj)

world = None