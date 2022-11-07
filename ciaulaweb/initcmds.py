# comandi iniziali
from HolidayPlanning.models import Attrazione

def erase_db():
    print("Cancello il DB")
    Attrazione.objects.all().delete()

def init_db():
    print("Controllo che non ci siano elementi...")
    if len(Attrazione.objects.all()) != 0:
        return
    else:
        print("Non ci sono elementi!")
    fileAttrazioni = open('/home/lorenzo/tecnologieWeb/CiaulaWeb/listaattrazionidb.txt')
    listaNome = []
    listaLuogo = []
    listaCitta = []
    listaVia = []
    listaCosto = []
    listaTipo = []
    listaOraA = []
    listaOraC = []
    listaDescr = []
    # leggere il file con le attrazioni
    while True:
        line = fileAttrazioni.readline()
        print("riga letta "+line)
        if line == "\n":
            line = fileAttrazioni.readline()
        dataEntryList = line.rsplit("% ", 2)
        # if len(dataEntryList[1]) == 0 :
        #    continue
        # la riga non è una newline, possiamo salvare i campi nel dizionario attrazioni
        tipoCampo = dataEntryList[0]
        print("tipo campo: "+tipoCampo)
        valoreCampo = dataEntryList[1]
        print("valore campo: "+valoreCampo)
        # impostare uno switch, aggiungo il valore di ogni campo ad una lista, c'è una lista per ogni campo
        if tipoCampo == "nome":
            print("Processo l'attrazione: " + valoreCampo)
            listaNome.append(valoreCampo)
            print("lista nome:"+str(listaNome))
        if tipoCampo == "luogo":
            listaLuogo.append(valoreCampo)
            print("lista luogo: "+str(listaLuogo))
        if tipoCampo == "via":
            listaVia.append(valoreCampo)
            print("lista via: "+str(listaVia))
        if tipoCampo == "citta":
            listaCitta.append(valoreCampo)
            print(listaCitta)
        if tipoCampo == "costo":
            listaCosto.append(valoreCampo)
            print(listaCosto)
        if tipoCampo == "tipo":
            listaTipo.append(valoreCampo)
            print(listaTipo)
        if tipoCampo == "oraApertura":
            listaOraA.append(valoreCampo)
            print(listaOraA)
        if tipoCampo == "oraChiusura":
            listaOraC.append(valoreCampo)
            print(listaOraC)
        if tipoCampo == "descrizione":
            listaDescr.append(valoreCampo)
            print(listaDescr)
        # inizializzo il dizionario
        attrazioniDict = dict(nome=listaNome, luogo=listaLuogo, via=listaVia, citta=listaCitta, costo=listaCosto,
                              tipo=listaTipo, oraApertura=listaOraA, oraChiusura=listaOraC, descrizione=listaDescr)
        totEntries = 4
    for i in range(totEntries):
        a = Attrazione()
        for k in attrazioniDict:
            if k == "nome":
                a.nome = attrazioniDict[k][i]
                print("Salvo attrazione " + a.nome + " nel db")
            if k == "luogo":
                a.luogo = attrazioniDict[k][i]
            if k == "via":
                a.via = attrazioniDict[k][i]
            if k == "citta":
                a.citta = attrazioniDict[k][i]
            if k == "costo":
                a.costo = attrazioniDict[k][i]
            if k == "tipo":
                a.tipo = attrazioniDict[k][i]
            if k == "oraApertura":
                a.oraApertura = attrazioniDict[k][i]
            if k == "oraChiusura":
                a.oraChiusura = attrazioniDict[k][i]
            else:  # tipoCampo e' descrizione
                a.descrizione = attrazioniDict[k][i]
            # print(a)
        a.save()
        print("attrazione " + a.nome + " salvata nel db")