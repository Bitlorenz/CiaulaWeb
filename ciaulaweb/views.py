import operator

from django.db.models import Q
from django.shortcuts import render
from attractions.models import Attrazione
from HolidayPlanning.models import Vacanza
from profiles.models import UserProfileModel


# Metodo per ottenere la quantità di scelte fatte per ogni attrazione in ordine di quantità
def mostpopular(popular, request):
    if request.user.is_authenticated:
        vacanze = Vacanza.objects.filter()  # Acquisisco tutte le vacanze
        vacanze_utente = Vacanza.objects.filter(utente=request.user)
        # Acquisisco scelte fatte dall'utente
        scelte_utente = []
        for vu in vacanze_utente:
            for sc in vu.scelte.all():
                scelte_utente.append(sc.attrazione)
        scelte_utente = list(set(scelte_utente))  # Rimozione duplicati

        # metto in un dizionario la coppia scelta-quantità acquistata
        for vacanza in vacanze:
            for s in vacanza.scelte.all():
                if s.attrazione in popular:
                    popular[s.attrazione] += 1
                else:
                    popular[s.attrazione] = 1
        popular_ord = dict(sorted(popular.items(), key=operator.itemgetter(1),
                                  reverse=True))  # Ordino elementi sulla base di quante volte sono stati scelti

        # rimuovo dal dizionario scelte già fatte dall'utente
        for scelte in scelte_utente:
            del popular_ord[scelte]

        popular_ord = dict(list(popular_ord.items())[:9])  # Massimo 9 elementi
        return popular_ord
    else:
        vacanze = Vacanza.objects.filter()  # prendo tutte le vacanze di tutti gli utenti
        # Metto in un dizionario la coppia prodotto-quantità acquistata
        for vacanza in vacanze:
            for s in vacanza.scelte.all():
                if s.attrazione in popular:
                    popular[s.attrazione] += 1
                else:
                    popular[s.attrazione] = 1
        # Ordino elementi sulla base della quantità acquistata
        popular_ord = dict(sorted(popular.items(), key=operator.itemgetter(1), reverse=True))
        popular_ord = dict(list(popular_ord.items())[:9])  # Massimo 9 elementi
        return popular_ord


def recommend(user):
    vacanze_utente = Vacanza.objects.filter(utente=user)  # Acquisisco vacanze fatte dal turista

    scelte_utente = []  # lista con scelte fatte dall'utente
    for vac in vacanze_utente:
        for s in vac.scelte.all():
            scelte_utente.append(s.attrazione)  # Acquisisco scelte fatte dall'utente

    # rimuovo duplicati dalla lista
    scelte_utente_nd = list(set(scelte_utente))  # nuova lista contenente le scelte delle vacanze senza duplicati

    vacanze = Vacanza.objects.exclude(utente=user)  # Acquisisco tutte le vacanze degli altri turisti
    recommend = []
    for vacanza in vacanze:
        if vacanza.scelte.count() > 1:  # Se vacanza con più di una scelta
            for s in vacanza.scelte.all():
                # Se la vacanza di un altro turista contiene scelta aggiunta dall'utente
                if s.attrazione in scelte_utente_nd:
                    recommend.append(vacanza)  # Salvo la vacanza

    # Rimuovo dalla lista le scelte che ho fatto (non raccomandarmi ciò che ho già acquistato)
    recommend_new = []
    for r in recommend:
        for s in r.scelte.all():
            if s.attrazione not in scelte_utente_nd:
                recommend_new.append(s.attrazione)

    recommend_new = list(set(recommend_new))  # Rimuovo duplicati dalla lista
    return recommend_new


def all_attrazioni():
    attrazioni = Attrazione.objects.filter()  # Acquisisco tutte le attrazioni
    return attrazioni


# View per la homepage
def home(request):
    ctx = {}

    # caso Turista (utente loggato)
    if request.user.is_authenticated:
        if not request.user.is_staff:  # superfluo?
            # Se il Turista ha creato vacanze
            if Vacanza.objects.filter(utente=request.user).exists():
                recommended = recommend(request.user)  # Acquisisco attrazioni consigliate per l'utente
                if len(recommended) > 0:  # Se ho almeno un' attrazione consigliata
                    ctx = {"listaattrazioni": recommended,
                           "title": "Attrazioni consigliate in base alle tue scelte"}  # listaattrazioni contiene le attrazioni consigliate
                else:  # Se non ho attrazioni da consigliare
                    admin = UserProfileModel.objects.get(is_admin=True)
                    if Vacanza.objects.exclude(Q(utente=request.user) | Q(
                            utente=admin)).exists():  # Se esistono vacanza fatte da altri utenti
                        popular = {}
                        popular_ord = mostpopular(popular,
                                                  request)  # Acquisisco attrazioni più popolari in ordine di quantità acquistata
                        # Se ho attrazioni popolari non scelte dall'utente
                        if len(popular_ord) > 0:
                            ctx = {"listaattrazioni": popular_ord,
                                   "title": "Attrazioni popolari"}  # listaattrazioni contiene le attrazioni più popolari
                        # Se non ho attrazioni popolari non scelte dall'utente
                        else:
                            attrazioni = all_attrazioni()  # Acquisisco tutte le vacanze
                            ctx = {"listaattrazioni": attrazioni, "title": "Tutte le Attrazioni Belle"}
                    else:  # Se non esistono vacanze fatte da altri turisti
                        attrazioni = all_attrazioni()  # Acquisisco tutte le vacanze
                        ctx = {"listaattrazioni": attrazioni, "title": "Tutte le Attrazioni"}
            # Se il Turista non ha creato vacanze
            else:
                # Se esistono vacanze di altri turisti
                if Vacanza.objects.filter().exists():
                    popular = {}
                    popular_ord = mostpopular(popular,
                                              request)  # Acquisisco attrazioni più popolari in ordine di quantità acquistata
                    ctx = {"listaattrazioni": popular_ord,
                           "title": "Attrazioni popolari"}  # listaattrazioni contiene le attrazioni più popolari
                # Se non esistono vacanze di altri utenti
                else:
                    attrazioni = all_attrazioni()
                    ctx = {"listaattrazioni": attrazioni, "title": "Tutte le Attrazioni"}
        else:
            attrazioni = all_attrazioni()
            ctx = {"listaattrazioni": attrazioni, "title": "Tutte le Attrazioni"}
    # se utente non è loggato
    else:
        # Se esistono vacanze degli utenti
        if Vacanza.objects.filter().exists():
            popular = {}
            popular_ord = mostpopular(popular,
                                      request)  # Acquisisco attrazioni più popolari in ordine di quantità acquistata
            ctx = {"listaattrazioni": popular_ord,
                   "title": "Attrazioni popolari"}  # listaattrazioni contiene le attrazioni più popolari
            # Se non esistono vacanze di altri utenti
        else:
            attrazioni = all_attrazioni()
            ctx = {"listaattrazioni": attrazioni, "title": "Tutte le Attrazioni"}

    return render(request, template_name="homepage.html", context=ctx)  # restituisco il template
