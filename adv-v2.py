from minicom import *
from random import choice,shuffle,randrange
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

_LOOT = 3 # MOUNT OF LOOT
_DAY = 3 # DURATION DAY/NIGHT
_MBAG = 10 # MAX BAG CAPACITY
_SAVES = "saves"

mixer.init()
class Sound:
    def __init__(self,nf):
        self.nf = nf
    def play(self):
        try:
            mixer.music.load(self.nf)
            mixer.music.play(-1)
        except:
            print(fstr("[not music available]",'ic','red'))

class Player:
    def __init__(self, name, zone, time=0):
        self.name = name
        self.zone = zone
        self.time = time
    
    def __nonzero__(self):
        return bool(self.item)
    
    def __str__(self):
        s = "zone: " + str(ZONES[self.zone]) + " | "
        d = int(self.time/(2*_DAY))
        s += "day: " + fstr(d, font="yellow" if self.time%(2*_DAY) < _DAY else "blue")
        s += '\n' + '\n'.join(' - '+i+' x'+str(self.item.count(i)) for i in set(ITEMS))
        return s
    
    def __len__(self):
        return len(self.item)
    
    def hit(self, h=2):
        shuffle(self.item)
        print(fstr("lost "+','.join(self.item[:min(2,len(self))]), 'n', 'red'))
        self.item = self.item[min(2,len(self)):]
    
    def chg(self, obj):
        nobj = choice(ITEMS)
        print(fstr("change "+obj+" for "+nobj, 'n', 'green'))
        self.item.append(nobj)
        self.item.remove(cmd[1])

    def get(self, objs):
        print(fstr("gain "+','.join(objs), 'n', 'green'))
        if _MBAG - len(self) < _LOOT:
            print(fstr("cant charge with all objects!", 'n', 'red'))
        player.item += objs[:min(_LOOT,_MBAG - len(self))]
    
    def save(self):
        with open(_SAVES) as f:
            old = filter(lambda x: x.split(',')[0] != self.name, f.readlines())
        with open(_SAVES, 'w') as f:
            s = "%s,%s,%d:%s " % (self.name,self.zone,self.time,','.join(self.item))
            f.write(s + '\n')
            f.writelines(old)
    
    @classmethod
    def load(cls, name):
        with open(_SAVES) as f:
            for l in f:
                d,i = l.strip().split(':')
                n,z,t = d.split(',')
                if n == name:
                    player = cls(n,z,int(t))
                    player.item = i.split(',')
                    return player
            return None

    @classmethod
    def quest(cls):
        name = input(fstr("name: ", 'b'))
        
        # TRY LOAD BY NAME
        player = cls.load(name)
        if not player:
            cmd = parse_cmd(("hack","wise","merc"),
            fstr("job? (hack,wise,merc): ", 'b'),
            fstr("invalid job", 'n', 'red'))
            
            player = cls(name, "tant")
            if not cmd: cmd = [choice([*JOBS])]
            player.item = JOBS[cmd[0]]
        return player


class Zone:
    def __init__(self, name, typ, lvl, desc="???"):
        self.name = name
        self.typ = typ
        self.lvl = lvl
        self.desc = desc

    def __str__(self):
        return fstr(self.name, 'n', "green" if self.typ == "town" else "red")
    
    def trip(self, player):
        clvl = 0
        while player and 0 <= clvl < self.lvl:
            # SHOW & INPUT
            ev = choice(EVENTS)
            print("road to {0}, lvl {1}: {2}".format(self, clvl, fstr(ev,'b')))
            print(player)
            
            cmd = parse_cmd(("run","q"))
            
            # FORWARD
            if not cmd: winlos = TOWIN[ev] in player.item
            # BACK
            elif cmd[0] == "run":
                clvl -= 2
                continue
            # QUIT (DEBUG)
            elif cmd[0] == 'q': break
            # WIN
            if winlos:
                if ev in ("slime", "ghost"): pass
                if ev in ("chest", "shrine", "dragon"):
                    player.get([choice(ITEMS) for i in range(_LOOT)])
                player.item.remove(TOWIN[ev])
            # LOSE
            else:
                if ev in ("slime", "ghost", "dragon"): player.hit(2)
                if ev in ("chest", "shrine"): pass
            
            player.time += 1
            clvl += 1
        
        # END - DIE
        if not player:
            fstr("you die", "b", "red")
        # END - DONE
        elif clvl == self.lvl:
            print(fstr("zone done!", 'n','green'))
            if self.typ == "dung":
                reward = self.lvl#**2 - randrange(self.lvl)
                player.get(["gold"] * (reward))
        # END - BACK
        else: print(fstr("go back...", 'n', 'red'))
        
        return bool(player) and clvl == self.lvl

# INIT
def load_static(nf):
    cur = "none"
    ZONES,JOBS,EVENTS,ITEMS,TOWIN = dict(),dict(),list(),list(),dict()
    with open(nf) as f:
        for l in f:
            # COMENTS & EMPTY
            if l[0] == '#' or len(l) < 2: continue
            l = l.strip()
            # SECCION
            if l[0] == '*':
                cur = l[1:]
                continue
            if cur == "zones":
                name,typ,lvl,desc = l.split(',')
                ZONES[name] = Zone(name,typ,int(lvl),desc)
            if cur == "class":
                data = l.split(',')
                JOBS[data[0]] = data[1:]
            if cur == "events":
                name,freq,weak = l.split(',')
                EVENTS += [name] * int(freq)
                TOWIN[name] = weak
            if cur == "items":
                name,freq = l.split(',')
                ITEMS += [name] * int(freq)
    return ZONES,JOBS,EVENTS,ITEMS,TOWIN

ZONES,JOBS,EVENTS,ITEMS,TOWIN = load_static("stc-adv")

player = Player.quest()

# MAIN LOOP
while player:
    print(player)
    cmd = parse_cmd(("see", "mov", "chg", "q"))

    if not cmd:
        print(*ZONES.values())
        #print (*map(lambda z: fstr(z, 'n', "town" if ZONES[z].typ == "town" else "green"), [*ZONES]))
        continue

    if cmd[0] == "see": print(fstr(ZONES[player.zone].desc, 'i'))
    
    if cmd[0] == "mov" and ZONES[cmd[1]].trip(player): player.zone = cmd[1]
    
    if cmd[0] == "chg" and ZONES[player.zone].typ == "town":
        if cmd[1] in player.item: player.chg(cmd[1])
        else: print(fstr("not have it!", 'n', 'red'))
    
    if cmd[0] == "q": break
    
    player.time += 1

player.save()