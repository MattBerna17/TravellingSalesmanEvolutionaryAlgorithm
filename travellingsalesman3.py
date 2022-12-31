# IDEA: un venditore deve visitare x città, e vuole trovare il modo di visitarle tutte in modo da impiegare il minor tempo (camminare di meno), partendo da un punto iniziale p e ritornando al solito, senza passare 2 volte dalla solita città.
# Fitness: funzione che ci permette di calcolare il minor percorso, sarà una fitness minimal.
# Ogni individuo è un percorso, e ogni percorso eredita da Fitness per poter valutare l'efficacia del path.
# Ogni percorso ha una distanza, calcolata come sqrt((xi - xf)^2 + (yi - yf)^2).
# Inoltre dobbiamo inizializzare le strutture di individuo e popolazione (insieme di individui).
# Funzione valutazione: somma delle distanze tra una città e le altre. Il miglior percorso è quello più breve.
# Registriamo le funzioni per l'accoppiamento, le mutazioni e la selezione tramite tornei.
# Scriviamo il main.


import math
import random
from deap import creator, base, tools

class Citta:
    def __init__(self, nome, coordinate: dict) -> None:
        self.nome = nome
        self.coordinate = coordinate

listaCitta = []
NUMERO_CITTA = 5

listaCitta.append(Citta("Lucca", {'x': 100.0, 'y': 300.0}))
listaCitta.append(Citta("Pisa", {'x': 250.0, 'y': 200.0}))
listaCitta.append(Citta("Livorno", {'x': 600.0, 'y': 350.0}))
listaCitta.append(Citta("Firenze", {'x': 125.0, 'y': 200.0}))
listaCitta.append(Citta("Siena", {'x': 400.0, 'y': 150.0}))

partenza = listaCitta[0]    # ipotizzo di partire da Lucca.
# il percorso migliore sarebbe Lucca - Firenze - Pisa - Siena - Livorno - Lucca (CREDO)

# Funzione per il calcolo della distanza tra due città
def calcolaDistanza(listaCitta: list, partenza: Citta):
    distanze = []
    for arrivo in listaCitta:
        distanze.append(calcolaDistanzaTraCitta(partenza, arrivo))
    return distanze

def calcolaDistanzaTraCitta(partenza: Citta, arrivo: Citta):
    return math.sqrt((arrivo.coordinate['x'] - partenza.coordinate['x'])**2 + (arrivo.coordinate['y'] - partenza.coordinate['y'])**2)


matriceDistanze = []
for citta in listaCitta:
    matriceDistanze.append(calcolaDistanza(listaCitta, citta))


def totalCalcolaDistanzaTraCitta(listaCitta: list):
    totalDistanze = []
    for citta in listaCitta:
        totalDistanze.append(calcolaDistanza(listaCitta, citta))
    
    return totalDistanze

print(totalCalcolaDistanzaTraCitta(listaCitta))

#[{'Lucca;Pisa': 180.27756377319946},       {'Lucca;Livorno': 502.4937810560445},   {'Lucca;Firenze': 103.07764064044152},      {'Lucca;Siena': 335.4101966249685}]
#[{'Pisa;Lucca': 180.27756377319946},       {'Pisa;Livorno': 380.7886552931954},    {'Pisa;Firenze': 125.0},                    {'Pisa;Siena': 158.11388300841898}]
#[{'Livorno;Lucca': 502.4937810560445},     {'Livorno;Pisa': 380.7886552931954},    {'Livorno;Firenze': 498.1214711292819},     {'Livorno;Siena': 282.842712474619}]
#[{'Firenze;Lucca': 103.07764064044152},    {'Firenze;Pisa': 125.0},                {'Firenze;Livorno': 498.1214711292819},     {'Firenze;Siena': 279.5084971874737}]
#[{'Siena;Lucca': 335.4101966249685},       {'Siena;Pisa': 158.11388300841898},     {'Siena;Livorno': 282.842712474619},        {'Siena;Firenze': 279.5084971874737}]

distanze = totalCalcolaDistanzaTraCitta(listaCitta)
# [
#   [0.0, 180.27756377319946, 502.4937810560445, 103.07764064044152, 335.4101966249685],
#   [180.27756377319946, 0.0, 380.7886552931954, 125.0, 158.11388300841898],
#   [502.4937810560445, 380.7886552931954, 0.0, 498.1214711292819, 282.842712474619],
#   [103.07764064044152, 125.0, 498.1214711292819, 0.0, 279.5084971874737],
#   [335.4101966249685, 158.11388300841898, 282.842712474619, 279.5084971874737, 0.0]
# ]


# FitnessMin perché cerco il path più breve
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))     # moltiplica i valori dell'individuo.fitness.values per -1, così otteniamo lo score negativo che ci serve per determinare il peso minore (percorso migliore)
# Un individuo è semplicemente un percorso, quindi una lista di distanze in cui si parte da Lucca e si torna a Lucca passando da sole e tutte le città
creator.create("Individuo", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
# Gli attributi sono le distanze tra città
toolbox.register("indici", random.sample, listaCitta, k=NUMERO_CITTA) # prende delle città randomiche
# Ogni individuo corrisponde a un percorso... magari con random?
toolbox.register("individuo", tools.initIterate, creator.Individuo, toolbox.indici)
toolbox.register("popolazione", tools.initRepeat, list, toolbox.individuo, n=20)

def valutazione(individuo):
    somma = 0
    inizio = 0
    for i in range(1, len(individuo)):
        fine = i
        somma += distanze[inizio][fine]
        inizio = fine
    return somma,

toolbox.register("valuta", valutazione)

def acc(individuo1, individuo2):
    for element1 in individuo1:
        print("Ind1: " + element1.nome)
    for element2 in individuo2:
        print("Ind2: " + element2.nome)

    print("\n")

toolbox.register("accoppia", acc)
toolbox.register("muta", tools.mutShuffleIndexes, indpb=1)
toolbox.register("seleziona", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
    popolazione = toolbox.popolazione() # 20 possibili cammini
    CXPB, MUTPB = 0.7, 0.5

    print("Inizia l'evoluzione")
    fitnesses = list(map(valutazione, popolazione))
    for ind, fit in zip(popolazione, fitnesses):
        ind.fitness.values = fit
    
    fits = [ind.fitness.values[0] for ind in popolazione]

    print(fits)

    generazione = 0
    while generazione < 150:
        generazione += 1
        prole = toolbox.seleziona(popolazione, len(popolazione))
        prole = list(map(toolbox.clone, prole))
        print("PROLE: ")
        for element1 in prole:
            for element2 in element1:
                print(element2.nome, end="; ")
            print()
        for figlio1, figlio2 in zip(prole[::2], prole[1::2]):
            if random.random() < CXPB:
                toolbox.accoppia(figlio1, figlio2)

                del figlio1.fitness.values
                del figlio2.fitness.values
        
        for mutante in prole:
            if random.random() < MUTPB:
                toolbox.muta(mutante)
                del mutante.fitness.values
        
        invalidi = [ind for ind in prole if not ind.fitness.valid]
        fitnesses = map(toolbox.valuta, invalidi)
        for ind, fit in zip(invalidi, fitnesses):
            ind.fitness.values = fit
        
        popolazione[:] = prole
        fits = [ind.fitness.values[0] for ind in popolazione]

    
    print("-------- FINE EVOLUZIONE -------")

    migliori = tools.selBest(popolazione, 5, fit_attr="fitness")

    print("Migliori percorsi:\n")

    for path in migliori:
        for element in path:
            print(element.nome + " " + str(element.coordinate))

        print()


if __name__ == "__main__":
    main()
