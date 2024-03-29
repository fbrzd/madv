from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from time import sleep

mixer.init()
class Sound:
    mute = False
    def __init__(self,nf):
        self.nf = nf
    def play(self):
        if not self.mute:
            try:
                mixer.music.load(self.nf)
                mixer.music.play(-1)
            except:
                print(fstr("not music available",'ic','red'))

class Fighter:
    @classmethod
    def load(cls, nf):
        # atk, def, spd, family, anim
        cls.register = dict()
        with open(nf) as f:
            for line in f:
                if line[0] == '#': continue
                if line[:6] == "_weaks":
                    cls.weaks = tuple(line.split(',')[1:])
                    continue
                name,a,d,s,fam,ani = line.strip().split(',')
                cls.register[name] = (int(a), int(d), int(s), fam, ani)
    
    def __init__(self, spec, name=''):
        self.spec = spec
        self.name = spec[:4] if not name else name
        if spec in Fighter.register:
            self.at,self.df,self.sp,self.family,self.anim = Fighter.register[spec]
        else:
            self.at,self.df,self.sp,self.family,self.anim = 0,0,0,'',''
    def show(self, fr=.3):
        for s in self.anim:
            print(s, end='',flush=1)
            sleep(fr)
            print('\033[D',end='')

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
def ftxt(nf,dic=dict()):
    try:
        with open(nf) as f:
            txt = ''.join(f.readlines())
        out = ""
        for i,s in enumerate(txt):
            if i and txt[i-1] == s: out += s
            else:
                fmt = dic[s] if s in dic else ('n','default','default')
                out += fstr(s,fmt[0],fmt[1],fmt[2],False)
        return out+'\033[0m'
    except:
        return fstr("[not img available]",'ci','red')
def dtxt(src, lim, fr, tab=0):
	i = 0
	while len(src) - i - lim > 0:
		j = src.rfind(' ', i, i+lim)
		print(' '*tab + fstr(src[i:j], 'ib'), flush=1)
		i = j+1
		sleep(fr)
	print(' '*tab + fstr(src[i:], 'ib'), flush=1)
	sleep(fr)
def parse_cmd(cmds, promt=fstr("cmd: ", 'b'), unknow=fstr("unknow cmd!", 'n', 'red')):
    while 1:
        cmd = input(promt)
        if cmd == "":
            return None
        cmd = cmd.split(" ")
        if cmd[0] not in cmds:
            print(unknow)
            print(fstr("expected: " + ', '.join(cmds), 'n', 'red'))
        else: return cmd
def qyn(text):
    while 1:
        cmd = input(text)
        if cmd == "y" or cmd == "n": return "ny".index(cmd)
