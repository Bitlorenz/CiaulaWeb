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

    def processingAttrazioni():
        fileAttrazioni = open("entryAttrazioneDB.txt", "r")
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
            if line == "\n":
                line = fileAttrazioni.readline()
            dataEntryList = line.rsplit(": ", 1)
            #if len(dataEntryList[1]) == 0 :
            #    continue
            # la riga non è una newline, possiamo salvare i campi nel dizionario attrazioni
            tipoCampo = dataEntryList[0]
            valoreCampo = dataEntryList[1]
            # impostare uno switch, aggiungo il valore di ogni campo ad una lista, c'è una lista per ogni campo
            if tipoCampo == "nome":
                if valoreCampo == "":
                    break #se il valore di nome non è stato inserito esco dal ciclo (attrazioni mancanti nel file)
                else:
                        print("Processo l'attrazione: "+valoreCampo)
                listaNome.append(valoreCampo)
            elif tipoCampo == "luogo":
                listaLuogo.append(valoreCampo)
            elif tipoCampo == "via":
                listaVia.append(valoreCampo)
            elif tipoCampo == "citta":
                listaCitta.append(valoreCampo)
            elif tipoCampo == "costo":
                listaCosto.append(valoreCampo)
            elif tipoCampo == "tipo":
                listaTipo.append(valoreCampo)
            elif tipoCampo == "oraApertura":
                listaOraA.append(valoreCampo)
            elif tipoCampo == "oraChiusura":
                listaOraC.append(valoreCampo)
            else: #tipoCampo e' descrizione
                listaDescr.append(valoreCampo)
        #inizializzo il dizionario
        attrazioniDict = dict(nome=listaNome, luogo=listaLuogo, via=listaVia, citta=listaCitta, costo=listaCosto,
                              tipo=listaTipo, oraApertura=listaOraA, oraChiusura=listaOraC, descrizione=listaDescr)
        totEntries = len(listaNome)
        for i in range(totEntries):
            a = Attrazione()
            for k in attrazioniDict:
                if k == "nome":
                        a.nome = attrazioniDict[k][i]
                        print("Salvo attrazione "+a.nome+" nel db")
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
                else: #tipoCampo e' descrizione
                        a.descrizione = attrazioniDict[k][i]
            #print(a)
            a.save()

        print("DUMP DB")
        print(Attrazione.objects.all())
