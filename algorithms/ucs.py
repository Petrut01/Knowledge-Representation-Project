import time

import stopit as stopit
import util


class NodParcurgere:

    total_instantiations = 0 #retin nr total de noduri calculate
    total_deletions = 0
    is_counting = False

    def __init__(self, info, cost, parinte, directie=None):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
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

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        path = ""
        for nod in l:
            if nod.directie is not None:
                path += " {} {}".format(nod.directie, nod)
            else:
                path += str(nod)
        path += "\nlungime: {}\ncost: {}\n".format(len(l), self.g)
        return path

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        return str(self.info)


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        self.start, self.final, self.copii, self.adiacente, self.m, self.ascultati, self.nr_coloane = util.read(nume_fisier)
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
        #tratam separat in functie de pozitia copilului ascultat in clasa
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
            self.langaProfesor[indexCurent - self.nr_coloane] = self.langaProfesor[indexCurent - self.nr_coloane - 1] = self.langaProfesor[indexCurent - self.nr_coloane + 1] = 1
        if j == self.nr_coloane - 1 and i > 0 and i < nrlinii - 1:
            self.langaProfesor[indexCurent] = self.langaProfesor[indexCurent - 1] =  1
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

    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        indexCurent = self.copii.index(nodCurent.info)
        for index in range(len(self.adiacente)):
            if self.adiacente[indexCurent][index] == 1 and not nodCurent.contineInDrum(self.copii[index]) and self.langaProfesor[index] == 0:
                nodNou = NodParcurgere(
                    self.copii[index],
                    nodCurent.g + self.genereazaCost(indexCurent, index),
                    nodCurent,
                    Graph.obtineDirectie(self, indexCurent, index)
                )
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir



def uniform_cost(gr, nrSolutiiCautate=1):
    NodParcurgere.is_counting = True
    alg_time = []
    start_time = time.time()  # Inceputul algoritmului
    c = [NodParcurgere(gr.start, 0, None)]

    max_noduri = 0

    results = []
    i = 0
    gr.langaProfesor = gr.ascultaElev(gr.ascultati[i])

    while len(c) > 0:
        max_noduri = max(NodParcurgere.total_instantiations - NodParcurgere.total_deletions, max_noduri)
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            results.append(nodCurent.afisDrum())

            alg_time.append((time.time() - start_time) * 100)

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                instantiations = NodParcurgere.total_instantiations

                NodParcurgere.total_instantiations = 0
                NodParcurgere.total_deletions = 0
                NodParcurgere.is_counting = False

                return (results, max_noduri, instantiations, alg_time)

        #dupa m mutari de bilet este ascultat alt elev
        if nodCurent.lungimeDrum() % (gr.m + 1) == 0:
            i += 1
            gr.langaProfesor = [0 for i in range(len(gr.copii))]
            if i < len(gr.ascultati):
                gr.langaProfesor = gr.ascultaElev(gr.ascultati[i])
        ##

        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i, s)

    instantiations = NodParcurgere.total_instantiations

    NodParcurgere.total_instantiations = 0
    NodParcurgere.total_deletions = 0
    NodParcurgere.is_counting = False
    if results == []:
        return (["Nu exista cale\n"], max_noduri, instantiations, [(time.time() - start_time) * 1000])
    else:
        return (results, max_noduri, instantiations, alg_time)


@stopit.threading_timeoutable(default='UCS timed out\n')
def ucs_timeout(input_path, NSOL):
    gr = Graph(input_path)
    return uniform_cost(gr, nrSolutiiCautate=NSOL)


