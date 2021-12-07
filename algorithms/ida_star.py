import util
import stopit
import time
from math import sqrt


class NodParcurgere:

    total_instantiations = 0 #retin nr total de noduri calculate
    total_deletions = 0
    is_counting = False

    def __init__(self, info, cost, h=0, parinte=None, directie=None):
        self.info = info
        self.cost = cost
        self.euristica = h
        self.estimare = self.cost + self.euristica
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.directie = directie

        if NodParcurgere.is_counting:
            NodParcurgere.total_instantiations += 1

    def __del__(self):
        if NodParcurgere.is_counting:
            NodParcurgere.total_deletions += 1

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def lungimeDrum(self):
        """
        :return: lungimea drumului
        """
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return len(l)

    def afisDrum(self):
        l = self.obtineDrum()
        path = ""
        for nod in l:
            if nod.directie is not None:
                path += " {} {}".format(nod.directie, nod)
            else:
                path += str(nod)
        path += "\nlungime: {}\ncost: {}\n".format(len(l), self.cost)
        return path

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        return self.info


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        self.start, self.final, self.copii, self.adiacente, self.m, self.ascultati, self.nr_coloane = util.read(
            nume_fisier)
        self.langaProfesor = [0 for i in range(len(self.copii))]

    def testeaza_scop(self, nodCurent):
        return nodCurent.info == self.final

    def obtineDirectie(self, index1, index2):
        """

        :param index1: index-ul din lista de copii al elevului la care se afla biletul
        :param index2: index-ul din lista de copii al elevului la care ar ajunge biletul
        :return: simbolul pentru directie
        """
        directie = None
        row1 = index1 // self.nr_coloane
        column1 = index1 % self.nr_coloane
        row2 = index2 // self.nr_coloane
        column2 = index2 % self.nr_coloane

        if row1 < row2:
            directie = "v"
        elif row1 > row2:
            directie = "^"

        if column1 > column2:
            directie = "<"
            if column2 % 2 != 0:
                directie = "<<"
        elif column1 < column2:
            directie = ">"
            if column2 % 2 == 0:
                directie = ">>"
        return directie

    def euristica_manhattan(self, index):
        """
            Euristica Manhattan putin optimizata

            :param index: din indexul lui in lista de copii obtinem pozitia in clasa
            :return: estimare euristica
        """
        row = index // self.nr_coloane
        column = index % self.nr_coloane

        index_final = self.copii.index(self.final)
        final_row = index_final // self.nr_coloane
        final_column = index_final % self.nr_coloane

        estimare_col = abs(column // 2 - final_column // 2) * 2  # daca se afla pe randuri diferite de banci

        return estimare_col + abs(final_row - row)  # pentru mutarile dintre randuri e cost 1

    def euristica_euclidiana(self, index):
        """
            Euristica euclidiana
            :param index: din indexul lui in lista de copii obtinem pozitia in clasa
            :return: estimare euristica
        """
        row = index // self.nr_coloane
        column = index % self.nr_coloane

        index_final = self.copii.index(self.final)
        final_row = index_final // self.nr_coloane
        final_column = index_final % self.nr_coloane

        return sqrt((final_row - row) ** 2 + (final_column - column) ** 2)

    def calculeaza_h(self, index, tip_euristica="banala"):
        if tip_euristica == "euristica banala":
            if self.copii[index] != self.final:
                return 1
            return 0
        elif tip_euristica == "euristica manhattan":
            return self.euristica_manhattan(index)
        elif tip_euristica == "euristica euclidiana":
            return self.euristica_euclidiana(index)
        else:
            return index

    def genereazaCost(self, index1, index2):
        """
            :param index1: index-ul din lista de copii al elevului la care se afla biletul
            :param index2: index-ul din lista de copii al elevului la care ar ajunge biletul
            :return: costul mutarii
        """
        column = index1 % self.nr_coloane
        row = index1 // self.nr_coloane
        to_column = index2 % self.nr_coloane
        to_row = index2 // self.nr_coloane
        if row != to_row:
            return 1

        if column < to_column:
            if column % 2 == 0:
                return 0
            else:
                return 2
        elif column > to_column:
            if column % 2 == 0:
                return 2
            else:
                return 0
        return 0

    def ascultaElev(self, numeElev):
        """
            :param numeElev: cu ajutorul numelui putem gasi indexul in lista de copii
            :return: lista in care copilul ascultat si cei din jurul sunt marcati cu 1
        """
        indexCurent = self.copii.index(numeElev)
        nrlinii = len(self.copii) // self.nr_coloane
        j = indexCurent % self.nr_coloane
        i = indexCurent // self.nr_coloane

        # tratam separat in functie de pozitia copilului ascultat in clasa
        if j > 0 and j < self.nr_coloane - 1 and i > 0 and i < nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane - 1] = \
                self.langaProfesor[indexCurent + self.nr_coloane + 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane - 1] = \
                self.langaProfesor[indexCurent - self.nr_coloane + 1] = 1

        if j == 0 and i > 0 and i < nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane + 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane + 1] = 1

        if j == 0 and i == 0:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane + 1] = 1

        if j == 0 and i == nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane + 1] = 1

        if j > 0 and j < self.nr_coloane - 1 and i == nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane - 1] = \
            self.langaProfesor[indexCurent - self.nr_coloane + 1] = 1
        if j == self.nr_coloane - 1 and i > 0 and i < nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane - 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane - 1] = 1
        if j == self.nr_coloane - 1 and i == 0:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane - 1] = 1
        if j == self.nr_coloane - 1 and i == nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = 1
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane - 1] = 1
        if i == 0 and j > 0 and j < self.nr_coloane - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] = self.langaProfesor[indexCurent + 1] = 1
            self.langaProfesor[indexCurent + self.nr_coloane] = self.langaProfesor[indexCurent + self.nr_coloane - 1] = \
                self.langaProfesor[indexCurent + self.nr_coloane + 1] = 1

        return self.langaProfesor

    def genereazaSuccesori(self, nodCurent, tip_euristica="banala"):
        listaSuccesori = []
        indexCurent = self.copii.index(nodCurent.info)
        for index in range(len(self.adiacente)):
            if self.adiacente[indexCurent][index] == 1 and not nodCurent.contineInDrum(self.copii[index]):
                    listaSuccesori.append(
                        NodParcurgere(
                            self.copii[index],
                            nodCurent.cost + self.genereazaCost(indexCurent, index),
                            self.calculeaza_h(index, tip_euristica),
                            nodCurent,
                            Graph.obtineDirectie(self, indexCurent, index)
                        )
                    )
        return listaSuccesori

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


max_nodes = 0


def ida_star(gr, nrSolutiiCautate, euristica):
    global max_nodes
    NodParcurgere.is_counting = True
    start_time = time.time()
    results = [] #lista cu solutiile obtinute
    times = [] #lista de timpi pentru fiecare solutie

    start_index = gr.copii.index(gr.start)
    limita = gr.calculeaza_h(start_index, 0)
    nodStart = NodParcurgere(gr.start, 0, limita, None, None)

    while True:
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, euristica, times, start_time,
                                                  results)
        if rez == "gata":
            break
        if rez == float("inf"):
            if results == []:
                results.append("Nu exista drum\n")
                times.append((time.time() - start_time) * 1000)
            break
        limita = rez

    instantiations = NodParcurgere.total_instantiations

    NodParcurgere.total_instantiations = 0
    NodParcurgere.total_deletions = 0
    NodParcurgere.is_counting = False

    _max_nodes = max_nodes
    max_nodes = 0

    return (results, _max_nodes, instantiations, times)


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, euristica, times, start_time, results):
    global max_nodes
    max_nodes = max(NodParcurgere.total_instantiations - NodParcurgere.total_deletions, max_nodes)
    if nodCurent.estimare > limita:
        return nrSolutiiCautate, nodCurent.estimare
    if gr.testeaza_scop(nodCurent) and nodCurent.estimare == limita:

        times.append((time.time() - start_time) * 1000)
        results.append(nodCurent.afisDrum())
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate, "gata"

    # dupa m mutari de bilet este ascultat alt elev
    if nodCurent.lungimeDrum() % (gr.m + 1) == 0:
        i = nodCurent.lungimeDrum() // (gr.m + 1)
        gr.langaProfesor = [0 for j in range(len(gr.copii))]
        if i < len(gr.ascultati):
            gr.langaProfesor = gr.ascultaElev(gr.ascultati[i])

    lSuccesori = gr.genereazaSuccesori(nodCurent, euristica)
    minim = float("inf")
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, euristica, times, start_time,
                                                  results)
        if rez == "gata":
            return nrSolutiiCautate, "gata"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim


@stopit.threading_timeoutable(default='IDA* timed out\n')
def ida_star_timeout(input_path, nsol, euristica):
    graph = Graph(input_path)
    NodParcurgere.graph = graph
    return ida_star(graph, nsol, euristica)

