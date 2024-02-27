from cgitb import text
from datetime import timedelta as td
from re import sub
import io

from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import UserProfileModel
from .forms import *
from .mixins import LookingTourMixin
from .models import Scelta, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


def scegliattrazione(request, pk):
    if request.method == "POST":
        form = ScegliAttrazioneForm(data=request.POST, pk=pk, user=request.user)
        if form.is_valid():
            scelta = form.save(commit=False)
            rifvacanza = Vacanza.objects.filter(utente=request.user).last()
            ini = form.cleaned_data.get("oraInizio")
            fine = form.cleaned_data.get("oraFine")
            scelta.durata = td(hours=fine.hour - ini.hour) + td(minutes=fine.minute - ini.minute)
            # checkSovrapposizione(request, fine, ini)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:scelte")
    else:
        utente = request.user
        att = get_object_or_404(Attrazione, pk=pk)
        form = ScegliAttrazioneForm(pk=pk, user=utente)
        # TODO CONTROLLARE SE ESISTE UNA VACANZA PER L'UTENTE, SE NO CREARNE UNA
        if Vacanza.objects.filter(utente=utente).count() == 0:
            return redirect("HolidayPlanning:creavacanza")
        return render(request, template_name="HolidayPlanning/scegli_attrazione.html",
                      context={"form": form, "att": att, "title": att.nome})
    return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form})


# TODO non ritornare T/F, ma stampare un messaggio avvertendo che c'è sovrapposizione con la specifica scelta
def checkSovrapposizione(request, fine, ini):
    rifvacanza = Vacanza.objects.filter(utente=request.user).last()
    scelteFatte = rifvacanza.scelte
    for i in scelteFatte:
        if i.oraInizio < ini and fine < i.oraFine:  # sovrapposizione totale
            sovrapposta = i
        if i.oraInizio < ini < i.oraFine or i.oraInizio < fine < i.oraFine:  # sovrapposizione parziale
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


# API VACANZA
class VacanzeList(LoginRequiredMixin, ListView):
    model = Vacanza
    template_name = "HolidayPlanning/vacanze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Le tue Vacanze"
        context['utente'] = self.request.user
        context['vacanze'] = Vacanza.objects.filter(utente=self.request.user)
        context['tour'] = False
        return context

def vacanze_by_root(request):
    try:
        user = UserProfileModel.objects.get(nrSocio=1)
        vacanze = Vacanza.objects.filter(utente=user)
        tour = True
        context = {
            'title' : "I Nostri Tour Organizzati",
            'utente': user,
            'vacanze': vacanze,
            'tour' : tour
        }
        return render(request, 'HolidayPlanning/vacanze.html', context)
    except UserProfileModel.DoesNotExist:
        return HttpResponse("User not found", status=404)


# class view per creare una vacanza
class CreaVacanza(LoginRequiredMixin, CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    success_url = reverse_lazy("attractions:attrazioni")

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        vacanza.utente = self.request.user
        vacanza.save()
        return super().form_valid(form)

class AggiungiTourVacanza(LoginRequiredMixin, CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    success_url = reverse_lazy("attractions:attrazioni")

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        vacanza.utente = self.request.user
        vacanza_id = self.kwargs.get('pk')
        if vacanza_id is not None:
            #recupero l'oggetto vacanza
            vacanza_obj = Vacanza.objects.get(pk=vacanza_id)
            vacanza.save()
            for s in vacanza_obj.scelte.all():
                vacanza.scelte.add(s)
            vacanza.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        print("esecuzione metodo get_initial")
        # Controlla se l'oggetto è passato nella richiesta
        vacanza_id = self.kwargs.get('pk')
        if vacanza_id is not None:
            vacanza_obj = Vacanza.objects.get(pk=vacanza_id) # recupero l'oggetto vacanza
            initial['dataArrivo'] = vacanza_obj.dataArrivo
            initial['dataPartenza'] = vacanza_obj.dataPartenza
            initial['budgetDisponibile'] = vacanza_obj.budgetDisponibile
            return initial


# class view per i dettagli di una vacanza
class DettaglioVacanza(LookingTourMixin, DetailView):
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
        context['scelte'] = vacanza.scelte.all().reverse()  # l'ultima aggiunta viene mostrata per prima
        context['totale'] = self.calcolaTotale(vacanza.scelte.all())
        return context


# class view per modificare una vacanza
class ModificaVacanza(LoginRequiredMixin, UpdateView):
    model = Vacanza
    template_name = "HolidayPlanning/modificavacanza.html"
    form_class = ModificaVacanzaForm

    # fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={"pk": self.object.pk})


# view per stampare il pdf della vacanza
def stampaVacanza(request, pk):
    # crea un buffer file-like per ricevere i dati del pdf
    buffer = io.BytesIO()
    # crea un canvas per scrivere il pdf
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    # scrive il testo
    textob = p.beginText()
    textob.setTextOrigin(inch * 0.5, inch * 0.5)
    textob.setFont("Helvetica", 14)

    # recupera l'oggetto vacanza data la chiave primaria
    vacanza = Vacanza.objects.get(pk=pk)
    print(vacanza)
    righeTesto = ["Vacanza di " + vacanza.utente.first_name + " " + vacanza.utente.last_name,
                  "Data di arrivo: " + str(vacanza.dataArrivo), "Data di partenza: " + str(vacanza.dataPartenza),
                  "Numero di persone: " + str(vacanza.nrPersone),
                  "Budget disponibile: " + str(vacanza.budgetDisponibile), "Scelte effettuate: "]
    costoTotale = 0
    for s in vacanza.scelte.all():
        righeTesto.append(
            str(s.giorno) + " - " + str(s.attrazione.nome) + " - " + str(s.oraInizio) + " - " + str(s.oraFine))
        costoTotale = costoTotale + s.attrazione.costo
    righeTesto.append("Costo totale: " + str(costoTotale))
    righeTesto.append("Buona vacanza!")
    righeTesto.append(" ")

    for r in righeTesto:
        textob.textLine(r)

    p.drawText(textob)

    # chiude il canvas
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='vacanza.pdf')


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

        if c.giorno is not None:
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
