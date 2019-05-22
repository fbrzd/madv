import back
from sys import argv
from util import fstr

# BALANCE DE ITEMS AL ENTRAR
# EN UNA ZONA "DUNG" ESPECIFICA
def bal_dung_item(verb=True):
    dungitem = dict()
    for zone in filter(lambda z: type(z) == back.Dung, back.ZONES):
        if verb: print(fstr(zone.name, 'b') + ':')
        
        n_events, n_count = len(zone.events), 0
        for e in zone.events:
            prob_e = 0
            if e.ifWin[0] == 'I': prob_e += .5 * (int(e.ifWin[1:]) - 1)
            if e.ifWin[0] == 'H': prob_e += .5 * (-int(e.ifWin[1:]) - 1)
            if e.ifWin[0] == 'N': prob_e += .5 * (- 1)
            if e.ifLose[0] == 'I': prob_e += .5 * int(e.ifLose[1:])
            if e.ifLose[0] == 'H': prob_e += .5 * -int(e.ifLose[1:])
            if e.ifLose[0] == 'N': prob_e += 0
            if verb: print("  - items in event", fstr(e.name, 'i') + ':', prob_e)
            n_count +=  prob_e
        
        dungitem[zone.name] = round(n_count / n_events, 2)
        if verb: print("  * balance:", fstr(round(n_count / len(zone.events), 2), 'b'), "items")
    
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
    back.loadData(argv[1])

    bal_dung_item()
    val_item()
    freq_event()