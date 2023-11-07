from cgitb import text
from datetime import timedelta as td
from re import sub
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .forms import SearchForm, CreaVacanzaForm, ModificaVacanzaForm, ScegliAttrazioneForm
from .models import Attrazione, Scelta, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/attrazionilista.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listaattrazioni'] = Attrazione.objects.all()
        utente = self.request.user
        context['user'] = utente
        return context


def scegliattrazione(request, pk):
    if request.method == "POST":
        form = ScegliAttrazioneForm(data=request.POST, pk=pk, user=request.user)
        if form.is_valid():
            scelta = form.save(commit=False)
            rifvacanza = Vacanza.objects.filter(utente=request.user).last()
            ini = form.cleaned_data.get("oraInizio")
            fine = form.cleaned_data.get("oraFine")
            scelta.durata = td(hours=fine.hour - ini.hour) + td(minutes=fine.minute - ini.minute)
            #checkSovrapposizione(request, fine, ini)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:scelte")
    else:
        utente = request.user
        att = get_object_or_404(Attrazione, pk=pk)
        form = ScegliAttrazioneForm(pk=pk, user=utente)
        #TODO CONTROLLARE SE ESISTE UNA VACANZA PER L'UTENTE, SE NO CREARNE UNA
        if (Vacanza.objects.filter(utente=utente).count() == 0):
            return redirect("HolidayPlanning:creavacanza")
        return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form, "att": att, "title": att.nome})
    return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form})

#TODO non ritornare T/F, ma stampare un messaggio avvertendo che c'è sovrapposizione con la specifica scelta
def checkSovrapposizione(request, fine, ini):
    rifvacanza = Vacanza.objects.filter(utente=request.user).last()
    scelteFatte = rifvacanza.scelte
    for i in scelteFatte:
        if i.oraInizio < ini and fine < i.oraFine: # sovrapposizione totale
            sovrapposta = i
        if i.oraInizio < ini < i.oraFine or i.oraInizio < fine < i.oraFine: # sovrapposizione parziale
            return True
    return False


class ScelteList(LoginRequiredMixin, ListView):
    model = Scelta
    template_name = "HolidayPlanning/listascelte.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural
    
    def calcolaTotale(self, listaScelte):
        totale = 0
        for s in listaScelte:
            totale = totale + s.attrazione.costo
        return totale

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Itinerario di Viaggio"
        context['utente'] = self.request.user
        vacanzaCorrente = Vacanza.objects.filter(utente=self.request.user).last()
        context['vacanzacorrente'] = vacanzaCorrente
        listaScelte = vacanzaCorrente.scelte.all()
        context['totale'] = self.calcolaTotale(listaScelte)
        context['scelte'] = listaScelte
        return context


# class detail view per un'attrazione
class DetailAttrazioneEntita(DetailView):
    model = Attrazione
    template_name = "HolidayPlanning/dettaglioattrazione.html"


# class per modificare una scelta data la chiave primaria
class ModificaScelta(LoginRequiredMixin, UpdateView):
    model = Scelta
    template_name = "HolidayPlanning/modificascelta.html"
    fields = ['giorno', 'oraInizio', 'oraFine']

    def get_success_url(self):
        return reverse("HolidayPlanning:scelte")


# class delete view per eliminare una scelta
class CancellaScelta(LoginRequiredMixin, DeleteView):
    model = Scelta
    template_name = "HolidayPlanning/cancellascelta.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        entita = "Scelta"
        ctx["entita"] = entita
        return ctx

    def get_success_url(self):
        return reverse("HolidayPlanning:scelte")
    
#API VACANZA
class VacanzeList(LoginRequiredMixin, ListView):
    model = Vacanza
    template_name = "HolidayPlanning/vacanze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Le tue Vacanze"
        context['utente'] = self.request.user
        context['vacanze'] = Vacanza.objects.filter(utente=self.request.user)
        return context
    

# class view per creare una vacanza
class CreaVacanza(LoginRequiredMixin, CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    success_url = reverse_lazy("HolidayPlanning:attrazioni")

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        vacanza.utente = self.request.user
        vacanza.save()
        return super().form_valid(form)
    


# class view per i dettagli di una vacanza
class DettaglioVacanza(LoginRequiredMixin, DetailView):
    model = Vacanza
    template_name = "HolidayPlanning/dettagliovacanza.html"

    def calcolaTotale(self, listaScelte):
        totale = 0
        for s in listaScelte:
            totale = totale + s.attrazione.costo
        return totale
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dettagli Vacanza"
        context['utente'] = self.request.user
        vacanza = Vacanza.objects.get(pk=kwargs['object'].id)
        context['vacanza'] = vacanza
        context['scelte'] = vacanza.scelte.all().reverse()#l'ultima aggiunta viene mostrata per prima
        context['totale'] = self.calcolaTotale(vacanza.scelte.all())
        return context


# class view per modificare una vacanza
class ModificaVacanza(LoginRequiredMixin, UpdateView):
    model = Vacanza
    template_name = "HolidayPlanning/modificavacanza.html"
    form_class = ModificaVacanzaForm
    #fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={"pk": self.object.pk})


#view per confermare l'acquisto effettuato della vacanza, viene inviata una mail e 
#si può stampare il pdf della vacanza
class VacanzaComprata(LoginRequiredMixin, DetailView):
    model = Vacanza
    template_name = "HolidayPlanning/vacanzacomprata.html"
    context_object_name = "vacanza" #nel template si può accedere all'oggetto con questo nome

 # chiamata dopo la conferma dell'acquisto da parte dell'utente tramite una richiesta in post alla pagina
 # alla fine del processo viene visualizzata la pagina di scrittura di una review
    def post(self, request, *args, **kwargs):
        #modifica dello stato della vacanza
        va = Vacanza.objects.get(pk=kwargs['pk'])
        #vacanza.comprata = True
        #vacanza.save()

        #invio della mail
        subject = "[Conferma acquisto vacanza]"

        message = f'Complimenti per la scelta della tua vacanza! \n' \
                    f'Nella tua pagina profilo puoi stampare il piano della vacanza \n' \

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])

        
        #passo il mio oggetto nel contesto della pagina 
        return render(request, self.template_name, context={"vacanza": va})
    

#view per stampare il pdf della vacanza
def stampaVacanza(request, pk):
    #crea un buffer file-like per ricevere i dati del pdf
    buffer = io.BytesIO()

    #crea un canvas per scrivere il pdf
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    #scrive il testo
    textob = p.beginText()
    textob.setTextOrigin(inch*0.5, inch*0.5)
    textob.setFont("Helvetica", 14)

    #recupera l'oggetto vacanza data la chiave primaria
    vacanza = Vacanza.objects.get(pk=pk)
    print(vacanza)
    righeTesto = []
    righeTesto.append("Vacanza di " + vacanza.utente.first_name + " " + vacanza.utente.last_name)
    righeTesto.append("Data di arrivo: " + str(vacanza.dataArrivo))
    righeTesto.append("Data di partenza: " + str(vacanza.dataPartenza))
    righeTesto.append("Numero di persone: " + str(vacanza.nrPersone))
    righeTesto.append("Budget disponibile: " + str(vacanza.budgetDisponibile))
    righeTesto.append("Scelte effettuate: ")
    costoTotale = 0
    for s in vacanza.scelte.all():
        righeTesto.append(str(s.giorno) + " - " + str(s.attrazione.nome) + " - " + str(s.oraInizio) + " - " + str(s.oraFine))
        costoTotale = costoTotale + s.attrazione.costo
    righeTesto.append("Costo totale: " + str(costoTotale))
    righeTesto.append("Buona vacanza!")
    righeTesto.append(" ")

    for r in righeTesto:
        textob.textLine(r)

    p.drawText(textob)

    #chiude il canvas
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='vacanza.pdf')

# ##FORMS###
# raggiunta tramite richiesta GET, al click del pulsante submit, i dati inseriti (nei campi definiti dal SearchForm)
# re-indirizzeranno sul secondo url, i cui parametri sono compilati in funzione di request.POST
def cerca(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            stringa = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")  # indica la table su cui vogliamo fare la query
            return redirect("HolidayPlanning:risultati", stringa, where)
    else:
        form = SearchForm()  # è il form personalizzato, passato poi in context

    return render(request, template_name="HolidayPlanning/cerca.html", context={"form": form})


class RisultatiList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/risultati.html"

    def get_queryset(self):
        stringa = self.request.resolver_match.kwargs["stringa"]
        where = self.request.resolver_match.kwargs["where"]

        if "Scelta" in where:
            sc = Scelta.objects.filter(posizioneInGiornata__exact=int(stringa))
            return sc
        if "Attrazione" in where:
            sa = Attrazione.objects.filter(citta__icontains=stringa)
            return sa


class SceltaFattaView(LoginRequiredMixin, DetailView):
    model = Scelta
    template_name = "HolidayPlanning/sceltafatta.html"
    errore = "NO_ERRORS"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        c = ctx["object"]

        if c.giorno != None:
            if c.utente.pk != self.request.user.pk:
                self.errore = "Non hai scelto attività per questo giorno"
        else:
            self.errore = "Attività ancora non scelta"

        if self.errore == "NO_ERRORS":
            try:
                c.giorno = None
                c.utente = None
                c.save()
            except Exception as e:
                print("Errore! " + str(e))
                self.errore = "Errore nell'operazione di restituzione"

        return ctx
