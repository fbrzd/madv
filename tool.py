import back
from sys import argv
from util import fstr

# BALANCE DE ITEMS AL ENTRAR
# EN UNA ZONA "DUNG" ESPECIFICA
def bal_dung_item(verb=True):
    dungitem = dict()
    for zone in filter(lambda z: type(z) == back.Dung, back.ZONES):
        if verb: print(fstr(zone.name, 'b') + ':')
        
        n_events, count_it, count_hp = len(zone.events), 0, 0
        for e in zone.events:
            bal_hp, bal_it = 0, 0
            w = bool(e.weak)
            if e.ifWin[0] == 'I':  bal_it += .5 * (2 - w) * (int(e.ifWin[1:]) - w)
            if e.ifWin[0] == 'H': bal_hp += .5 * (2 - w) * (-int(e.ifWin[1:]) - w)
            if e.ifWin[0] == 'N': bal_it += .5 * (2 - w) * (- w)
            if e.ifLose[0] == 'I': bal_it += .5 * w * int(e.ifLose[1:])
            if e.ifLose[0] == 'H': bal_hp += .5 * w * -int(e.ifLose[1:])
            if verb: print("  - items & hp in event", fstr(e.name, 'i') + ':', bal_it, bal_hp)
            count_it += bal_it
            count_hp += bal_hp
        
        dungitem[zone.name] = (round(count_it / n_events, 2), round(count_hp / n_events, 2))
        bal_it = fstr(round(count_it / n_events, 2), 'b')
        bal_hp = fstr(round(count_hp / n_events, 2), 'b')
        if verb: print("  * balance:", bal_it, "items,", bal_hp, "hp")
    
    return dungitem

# "TARIFA" PROMEDIO QUE SE
# NECESITA PARA OBTENER UN ITEM
# MEDIANTE CAMBIOS EN "TOWNS"
def val_item(verb=True):
    valitem = dict()
    for item in back.ITEMS:
        if verb: print(fstr(item, 'b') + ':', end=' ')
        prob_z, n_count = 0, 0
        
        for zone in filter(lambda z: type(z) == back.Town, back.ZONES):
            if item in zone.shop:
                prob_z += zone.level # + len(zone.shop)
                n_count += 1
        
        valitem[item] = 0 if not n_count else round(prob_z/n_count, 2)
        if verb: print("only in dung" if not n_count else round(prob_z/n_count, 2))

    return valitem

# FRECUENCIA DE APARICION
# DE UN DETERMINADO EVENTO
# CONSIDERANDO TODAS LAS "DUNG"
def freq_event(verb=True):
    dungs = list(filter(lambda z: type(z) == back.Dung, back.ZONES))
    freqevent = dict()

    for event in back.EVENTS:
        print(fstr(event.name, 'b') + ':')
        prob_e = 0
        
        for zone in dungs:
            val = round((event in zone.events) / len(zone.events), 2)
            if verb: print("  - in", fstr(zone.name, 'i') + ':', val)
            prob_e += val
        
        freqevent[event.name] = round(prob_e/len(dungs), 2)
        if verb: print('  * freq:', fstr(freqevent[event.name],'b'), '%')


if __name__ == "__main__":
    back.loadData(argv[-1])

    if "-a" in argv or len(argv) < 3:
        bal_dung_item()
        val_item()
        freq_event()
    
    if "-d" in argv:
        bal_dung_item() 
    if "-i" in argv:
        val_item()
    if "-e" in argv:
        freq_event()