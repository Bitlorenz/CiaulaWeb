# comandi iniziali
from HolidayPlanning.models import Attrazione
from django.utils import timezone
from datetime import datetime, timedelta
from threading import Timer


def erase_db():
    print("Cancello il DB")
    Attrazione.objects.all().delete()


def init_db():
    if len(Attrazione.objects.all()) != 0:
        return

    def func_time(off_year=None, off_month=None, off_day=None):
        if off_year == 0 and off_month == 0 and off_day == 0:
            return None
        tz = timezone.now()
        out = datetime(tz.year - off_year, tz.month - off_month,
                       tz.day - off_day, tz.hour, tz.minute, tz.second)
        return out

    def processingAttrazioni():
        fileAttrazioni = open("entryAttrazioneDB.txt", "r")
    # leggere il file con le attrazioni
        while True:
            line = fileAttrazioni.readline()
            if line is "\n":
                line = fileAttrazioni.readline()
            dataEntryList = line.rsplit(": ", 1)
            #if len(dataEntryList[1]) == 0 :
            #    continue
            # la riga non è una newline, possiamo salvare i campi nel dizionario attrazioni
            tipoCampo = dataEntryList[0]
            valoreCampo = dataEntryList[1]
                # impostare uno switch
                # aggiungo il valore di ogni campo ad una lista, c'è una lista per ogni campo
                # creo un dizionario in cui aggiungo come key il tipo del campo e come value la rispettiva lista
