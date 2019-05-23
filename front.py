from time import sleep
from sys import argv
from util import *
import back

def show_main(player):
    zf = []
    for z in back.ZONES:
        nm = fstr("[%d]%s" % (z.level, z.name), "nb"[player.zone == z], ("red","green")[type(z) == back.Town])
        zf.append(nm)
    print('  ' + ' '.join(zf))
    print('  ' + fstr('"'+player.zone.description+'"', 'i'))
    for i in set(player.items):
        print("  - %s x%d " % (i, player.items.count(i)))
def show_madv(player, events):
    for e in events:
        print("  " + e.name + " appears... ", end='', flush=1)
        sleep(_TWAIT)
        
        prev = len(player.items)
        #print("DEBUG:", prev)
        end = e.clash(player)
        print(fstr(("lose", "win!")[end], font=("red","green")[end]), end='', flush=1)
        if not len(player.items):
            print(fstr(' [die]', 'b', 'red'))
            break

        #print("DEBUG:", len(player.items), prev < len(player.items) - end)
        if end and e.weak:
            print(" [use %s]" % fstr(e.weak, 'b'), end='', flush=1)
        
        print(" " + fstr("reward",'i') + "!" if prev - end < len(player.items) else '', flush=1)
        sleep(_TWAIT)
def show_goal(player):
    for g in back.GOALS:
        per = g.completed(player)
        if g.cond[0][0] == 'W':
            msg = "overcome " + fstr(g.cond[0][1:],'b') + ' "%s"' % g.cond[1]
        if g.cond[0][0] == 'G':
            msg = "collect " + fstr(g.cond[0][1:],'b') + ' "%s"' % g.cond[1]
        if g.cond[0][0] == 'M':
            msg = 'go to "%s" ' % g.cond[1] + fstr(g.cond[0][1:],'b') + ' times'
        
        print("  - %s: %s " % (g.name, msg), end=' ')
        if 0 <= per <= .333: col = "red"
        if .333 < per <= .666: col = "yellow"
        if .666 <= per <= 1: col = "green"
        print(fstr('(' + str(int(100*per)) + '%)', font=col))

# CONST
_TWAIT = 2
_PATH = argv[-1]

if "-m" in argv: Sound.mute = True

# INIT
back.loadData(_PATH)
musicMain = Sound(back._PATH + 'main.wav')
musicTown = Sound(back._PATH + 'town.wav')
musicDung = Sound(back._PATH + 'dung.wav')

musicMain.play()
player = back.logIn(input(fstr("name: ", 'b')))
if type(player.zone) == back.Town: musicTown.play()
if type(player.zone) == back.Dung: musicDung.play()

# MAIN LOOP
while len(player.items):
    cmd = parse_cmd(("mov", "chg", "rol", 'q'), fstr("[%s] > " % player.name, 'b'))

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
        if new: print("  change %s for %s" % (fstr(cmd[1],'b'), fstr(new,'b')))
    
    if cmd[0] == "rol": show_goal(player)

    if cmd[0] == 'q': break

player.save()