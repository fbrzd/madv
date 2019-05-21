from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from time import sleep
import back

mixer.init()
class Sound:
    def __init__(self,nf):
        self.nf = nf
    def play(self):
        try:
            mixer.music.load(self.nf)
            mixer.music.play(-1)
        except:
            print(fstr("not music available",'ic','red'))

def fstr(src,att='n',font='default',back='default',end=True):
	F = {'n':'0','b':'1','s':'2','i':'3','u':'4','r':'7','h':'8','c':'9'}
	C = {'black':30,'red':31,'green':32,'yellow':33,'blue':34,'magenta':35,
		 'cyan':36,'white':37,'default':39}
	try:
	    pre = "\033[" + ';'.join(map(lambda f: F[f], att))
	    pre += ';' + str(C[font]) + ';' + str(C[back]+10) + 'm'
	except:
	    pre = ''
	return pre + str(src) + '\033[0m'*end
def parse_cmd(cmds, promt=fstr("cmd: ", 'b'), unknow=fstr("unknow cmd!", 'n', 'red')):
    while 1:
        cmd = input(promt)
        if cmd == "":
            return None
        cmd = cmd.split(" ")
        if cmd[0] not in cmds: print(unknow)
        else: return cmd
def qyn(text):
    while 1:
        cmd = input(text)
        if cmd == "y" or cmd == "n": return "ny".index(cmd)

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
        print(fstr(("lose", "win!")[end], font=("red","green")[end]), end='')
        if not len(player.items): break

        #print("DEBUG:", len(player.items), prev < len(player.items) - end)
        if end:
            print(" [use %s]" % fstr(e.weak, 'b'), end='')
        
        print(" " + fstr("reward",'i') + "!" if prev - end < len(player.items) else '')

# INIT
_TWAIT = 2
player = back.logIn(input(fstr("name: ", 'b')))

# MAIN LOOP
while len(player.items):
    cmd = parse_cmd(("mov", "run", "chg", 'q'), fstr("[%s] > " % player.name, 'b'))

    if not cmd:
        show_main(player)
        continue
    
    if cmd[0] == "mov":
        show_madv(player, player.move(cmd[1]))
    
    if cmd[0] == "chg" and cmd[1] in player.items and type(player.zone) == back.Town:
        player.items.remove(cmd[1])
        new = player.zone.change()
        player.items.append(new)
        print(fstr("change %s for %s" % (cmd[1], new)))
    
    if cmd[0] == 'q': break

player.save()