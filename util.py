from functools import reduce

def read(input_file):
    f = open(input_file, "r")
    file_content = f.read()
    info = file_content.split("suparati")
    rows = info[0].strip().split('\n')
    clasa = []
    for row in rows:
        clasa.append(row.split(' '))
    info1 = info[1].split("ascultati:")
    perechi = info1[0].strip().split('\n')
    suparati = []
    for pereche in perechi:
        suparati.append(pereche.split())

    info2 = info1[1].strip().split("mesaj:")
    info3 = info2[0].split(' ')

    m = int(info3[0])
    ascultati = info3[1].strip().split('\n')
    start, final = info2[1].strip().split(' -> ')

    nr_coloane = len(clasa[0])

    def nuSuntSuparati(copil1, copil2):
        return [copil1, copil2] not in suparati and (copil2, copil1) not in suparati

    adiacente = list([0] * (nr_coloane * len(clasa)) for _ in range(nr_coloane * len(clasa)))

    for i in range(len(clasa)):
        for j in range(nr_coloane):

            if j % 2 == 0:  # drumuri orizontale
                if nuSuntSuparati(clasa[i][j], clasa[i][j + 1]) and \
                        clasa[i][j] != "liber" and clasa[i][j + 1] != "liber":
                    adiacente[i * nr_coloane + j][i * nr_coloane + j + 1] = 1
                    adiacente[i * nr_coloane + j + 1][i * nr_coloane + j] = 1

            if i < len(clasa) - 1:  # drumuri verticale
                if clasa[i][j] != "liber" and clasa[i + 1][j] != "liber" and nuSuntSuparati(clasa[i][j], clasa[i + 1][j]):
                    adiacente[i * nr_coloane + j][(i + 1) * nr_coloane + j] = 1
                    adiacente[(i + 1) * nr_coloane + j][i * nr_coloane + j] = 1

            if j % 2 == 1 and j < nr_coloane - 1 and (i >= len(clasa) - 2):  # ultimele 2 randuri de banci
                if nuSuntSuparati(clasa[i][j], clasa[i][j + 1]) and \
                        clasa[i][j] != "liber" and clasa[i][j + 1] != "liber":
                    adiacente[i * nr_coloane + j][i * nr_coloane + j + 1] = 1
                    adiacente[i * nr_coloane + j + 1][i * nr_coloane + j] = 1

    ## Vector de copii
    copii = reduce(lambda x, y: x + y, clasa, [])

    return start, final, copii, adiacente, m, ascultati, nr_coloane
