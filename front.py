#!/usr/bin/python3

from time import sleep
from sys import argv
from util import *
import back

def show_main(player):
    zf = []
    for z in back.ZONES:
        nm = fstr(f'[{z.level}]{z.name}', "nb"[player.zone == z], ("red","green")[type(z) == back.Town])
        zf.append(nm)
    print('  ' + ' '.join(zf))
    print('  ' + fstr(f'"{player.zone.description}"', 'i'))
    for i in set(player.items):
        print(f'  - {i} x{player.items.count(i)}')
def show_madv(player, events):
    for e in events:
        print(f'  {e.name} appears...', end='', flush=1)
        sleep(_TWAIT)
        
        prev = len(player.items)
        pzon = player.zone
        phps = player.hp
        end = e.clash(player)
        
        # USE ITEM
        if end and e.weak:
            print(f' [use {fstr(e.weak, "b")}]', end='', flush=1)
        
        # GET ITEM
        if prev - (end and bool(e.weak)) < len(player.items):
            print(fstr(" reward!","i", "green"), end='', flush=1)
        
        # MOV ZONE
        if pzon != player.zone:
            print(fstr(' out?', 'i'), flush=1)
            if type(player.zone) == back.Town: musicTown.play()
            if type(player.zone) == back.Dung: musicDung.play()
            break
        
        # HURTS HP
        if phps > player.hp:
            print(fstr(f' hurt {phps-player.hp} hp!', 'i', 'red'), end='')
            if not player.hp:
                print(fstr(' [die]', 'b', 'red'))
                break
        print('')

        # END
        #print(fstr(("lose", "win!")[end], font=("red","green")[end]), end='', flush=1)
        
        sleep(_TWAIT)
def show_goal(player):
    
    ends = True
    for g in back.GOALS:
        per = g.completed(player)
        if g.cond == 'W':
            msg = f'overcome {fstr(g.args[1], "b")} "{g.args[0]}"'
        if g.cond == 'G':
            msg = f'collect {fstr(g.args[1], "b")} "{g.args[0]}"'
        if g.cond == 'M':
            msg = f'go to "{g.args[0]}" {fstr(g.args[1],"b")} times'
        
        print("  - %s: %s " % (g.name, msg), end=' ')
        if 0 <= per <= .333: col = "red"
        if .333 < per <= .666: col = "yellow"
        if .666 < per <= 1: col = "green"
        print(fstr(f'({int(100*per)}%)', font=col))
        if per < 1: ends = False
    
    print(fstr(f"  * turns: {player.time}", 'b'))
    return ends
def show_advc():
    typ,obj = back.get_advice()
    if typ == "zone":
        if type(obj) == back.Dung:
            evs = ','.join(map(lambda e: e.name, obj.events))
            advice = f'{evs} in {obj.name}'
        if type(obj) == back.Town: advice = f'{",".join(obj.shop)} in {obj.name}'
    if typ == "event":
        aux = {"I":"reward items","H":"hurt hp","N":"nothing","Z":"it moves you"}
        win = obj.ifWin.split()[0][0]
        lose = obj.ifLose.split()[0][0]
        win = aux[win]
        lose = aux[lose]
        advice = f'{obj.name} + {obj.weak} = {win}, else {lose}'
    print(fstr(f'* hint: {advice}', 'i', 'cyan'))
def make_promt(player):
    col = ('red','default')[player.hp / back.CLASS[player.clas][1] > .5]
    promt = fstr(f'[{player.name}:{player.hp}] > ', 'b', col)
    return promt

# CONST
_TWAIT = .3 if "-q" in argv else 1.5
_LIMITX = 30
_PATH = argv[-1]

if "-m" in argv: Sound.mute = True

# INIT
back.loadData(_PATH)
musicMain = Sound(_PATH + 'main.wav')
musicTown = Sound(_PATH + 'town.wav')
musicDung = Sound(_PATH + 'dung.wav')
musicEnds = Sound(_PATH + 'ends.wav')
musicMain.play()

# BUILD PLAYER
name = input(fstr("name: ", 'b'))
player = back.logIn(name)
if not player:
    if len(back.CLASS) > 1:
        clas = parse_cmd((tuple(back.CLASS)), fstr("mode: ", 'b'), fstr("invalid mode!", 'n', 'red'))
    else: clas = tuple(back.CLASS)
    if not clas: clas = [None]
    player = back.Player(name, clas[0])

if type(player.zone) == back.Town: musicTown.play()
if type(player.zone) == back.Dung: musicDung.play()
dtxt(f'"{back.META["start"]}"', _LIMITX, _TWAIT, 2)

# MAIN LOOP
while player.hp:
    cmd = parse_cmd(("mov", "chg", "rol", 'q'), make_promt(player))

    #try:
    if not cmd:
        show_main(player)
        continue
    
    if cmd[0] == "mov":
        evs = player.move(cmd[1])
        if type(player.zone) == back.Town: musicTown.play()
        if type(player.zone) == back.Dung: musicDung.play()
        show_madv(player, evs)
    
    if cmd[0] == "chg":
        new = player.change(cmd[1])
        if new: print(f'  change {fstr(cmd[1],"b")} for {fstr(new,"b")}')
    
    if cmd[0] == "rol" and show_goal(player):
        musicEnds.play()
        dtxt(f'"{back.META["final"]}"', _LIMITX, _TWAIT, 2)

    if cmd[0] == 'q': break
    #except:
    #print(fstr('error!', 'red'))
show_advc()
player.save()