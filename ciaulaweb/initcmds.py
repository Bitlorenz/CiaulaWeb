#comandi iniziali
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
          if off_year == 0 and off_month==0 and off_day==0:
              return None
          tz = timezone.now()
          out = datetime(tz.year-off_year,tz.month-off_month,
                       tz.day-off_day,tz.hour,tz.minute, tz.second)
          return out

    #leggere il file con le attrazioni
    #aprire il file
    #leggere prima riga: leggere fino ai due punti e salvare la stringa in un parametro
    #impostare uno switch