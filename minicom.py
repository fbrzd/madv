#X,Y = 20,

def fstr(src,att='n',font='default',back='default',end=True):#formato para strings
	F = {'n':'0','b':'1','s':'2','i':'3','u':'4','r':'7','h':'8','c':'9'}
	C = {'black':30,'red':31,'green':32,'yellow':33,'blue':34,'magenta':35,
		 'cyan':36,'white':37,'default':39}
	try:
	    pre = "\033[" + ';'.join(map(lambda f: F[f], att))
	    pre += ';' + str(C[font]) + ';' + str(C[back]+10) + 'm'
	except:
	    pre = ''
	return pre + str(src) + '\033[0m'*end

def fprint(src, att='n', font='default', back='default', x=0, y=0):
    nx = max(0, x - len(src))
    ny = size_y
    print(fstr(src, att, font, back), end='')
    print(" "*nx + "\033[" + nx + "C", end= ("\033[" + y) if y else '\n')

# X Y
# 0 0 -> print normal
# N 0 -> limpiar x (input)
# N N -> limpiar x, nueva linea, subir + 1
# 0 N -> nueva linea, subir + 1

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
