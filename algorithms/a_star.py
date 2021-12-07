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
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return len(l)

    def afisDrum(self):  # returneaza drumul formatat
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
        :return:
        """
        row = index // self.nr_coloane
        column = index % self.nr_coloane

        index_final = self.copii.index(self.final)
        final_row = index_final // self.nr_coloane
        final_column = index_final % self.nr_coloane

        estimare_col = abs(column // 2 - final_column // 2) * 2 #daca se afla pe randuri diferite de banci

        return estimare_col + abs(final_row - row) # pentru mutarile dintre randuri e cost 1

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
        column1 = index1 % self.nr_coloane
        row1 = index1 // self.nr_coloane
        column2 = index2 % self.nr_coloane
        row2 = index2 // self.nr_coloane
        if row1 != row2:
            return 1

        if column1 < column2:
            if column1 % 2 == 0:
                return 0
            else:
                return 2
        elif column1 > column2:
            if column1 % 2 == 0:
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

    # va genera succesorii sub forma de noduri in arborele de parcurgere
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


def a_star(graph, nrSolutiiCautate, tip_euristica):
    NodParcurgere.is_counting = True
    c = [NodParcurgere(graph.start, 0, graph.calculeaza_h(graph.copii.index(graph.start), tip_euristica), None, None)]
    alg_time = []
    start_time = time.time() # Inceputul algoritmului
    results = []
    max_noduri = 0

    i = 0
    graph.langaProfesor = graph.ascultaElev(graph.ascultati[i])

    while len(c) > 0:
        max_noduri = max(NodParcurgere.total_instantiations - NodParcurgere.total_deletions, max_noduri)
        nodCurent = c.pop(0)

        if graph.testeaza_scop(nodCurent):
            results.append(nodCurent.afisDrum())

            alg_time.append((time.time() - start_time) * 100)

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                instantiations = NodParcurgere.total_instantiations

                NodParcurgere.total_instantiations = 0
                NodParcurgere.total_deletions = 0
                NodParcurgere.is_counting = False

                return (results, max_noduri, instantiations, alg_time)

        # dupa m mutari de bilet este ascultat alt elev
        if nodCurent.lungimeDrum() % (graph.m + 1) == 0:
            i += 1
            graph.langaProfesor = [0 for j in range(len(graph.copii))]
            if i < len(graph.ascultati):
                graph.langaProfesor = graph.ascultaElev(graph.ascultati[i])

        lSuccesori = graph.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].estimare >= s.estimare:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    instantiations = NodParcurgere.total_instantiations

    NodParcurgere.total_instantiations = 0
    NodParcurgere.total_deletions = 0
    NodParcurgere.is_counting = False
    if results == []:
        return (["Nu exista cale\n"], max_noduri, instantiations, [(time.time() - start_time) * 1000])
    else:
        return (results, max_noduri, instantiations, alg_time)

def a_star_opt(graph, tip_euristica):
    NodParcurgere.is_counting = True
    c = [NodParcurgere(graph.start, 0, graph.calculeaza_h(graph.copii.index(graph.start), tip_euristica), None, None)]
    closed = []

    start_time = time.time()

    max_noduri = 0
    i = 0
    graph.langaProfesor = graph.ascultaElev(graph.ascultati[i])

    while len(c) > 0:
        max_noduri = max(NodParcurgere.total_instantiations - NodParcurgere.total_deletions, max_noduri)
        nodCurent = c.pop(0)
        closed.append(nodCurent)

        if graph.testeaza_scop(nodCurent):
            t = time.time() - start_time
            instantiations = NodParcurgere.total_instantiations

            NodParcurgere.total_instantiations = 0
            NodParcurgere.total_deletions = 0
            NodParcurgere.is_counting = False

            return ([nodCurent.afisDrum()], max_noduri, instantiations, [t * 1000])

        # dupa m mutari de bilet este ascultat alt elev
        if nodCurent.lungimeDrum() % (graph.m + 1) == 0:
            i += 1
            graph.langaProfesor = [0 for j in range(len(graph.copii))]
            if i < len(graph.ascultati):
                graph.langaProfesor = graph.ascultaElev(graph.ascultati[i])

        lSuccesori = graph.genereazaSuccesori(nodCurent, tip_euristica)
        lSuccesoriCopy = lSuccesori.copy()
        for s in lSuccesoriCopy:
            gasitOpen = False
            for elem in c:
                if s.info == elem.info:
                    gasitOpen = True
                    if s.estimare < elem.estimare:
                        c.remove(elem)
                    else:
                        lSuccesori.remove(s)
                    break
            if not gasitOpen:
                for elem in closed:
                    if s.info == elem.info:
                        if s.estimare < elem.estimare:
                            closed.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break

        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].estimare >= s.estimare:
                    break
                i += 1
            c.insert(i, s)
    instantiations = NodParcurgere.total_instantiations

    NodParcurgere.total_instantiations = 0
    NodParcurgere.total_deletions = 0
    NodParcurgere.is_counting = False
    return (["Nu exista cale\n"], max_noduri, instantiations, [(time.time() - start_time) * 1000])


@stopit.threading_timeoutable(default='A* timed out\n')
def a_star_timeout(input_path, NSOL, euristica):
    graph = Graph(input_path)
    NodParcurgere.graph = graph
    return a_star(graph, NSOL, euristica)


@stopit.threading_timeoutable(default='A* OPT timed out\n')
def a_star_opt_timeout(input_path, euristica):
    graph = Graph(input_path)
    NodParcurgere.graph = graph
    return a_star_opt(graph, euristica)