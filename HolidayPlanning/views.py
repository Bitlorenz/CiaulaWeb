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
from .models import Scelta, Spostamento, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


def scegliattrazione(request, pk, vacanza_id):
    if request.method == "POST":
        form = ScegliAttrazioneForm(data=request.POST, pk=pk, user=request.user)
        if form.is_valid():
            scelta = form.save(commit=False)
            rifvacanza = Vacanza.objects.get(utente=request.user, pk=vacanza_id)
            ini = form.cleaned_data.get("oraInizio")
            fine = form.cleaned_data.get("oraFine")
            scelta.durata = td(hours=fine.hour - ini.hour) + td(minutes=fine.minute - ini.minute)
            # checkSovrapposizione(request, fine, ini)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:dettagliovacanza", pk=rifvacanza.pk)
    else:
        utente = request.user
        vacanza = Vacanza.objects.filter(utente=request.user, pk=vacanza_id)
        print("vacanza in get: "+str(vacanza))
        att = get_object_or_404(Attrazione, pk=pk)
        form = ScegliAttrazioneForm(pk=pk, user=utente)
        # TODO CONTROLLARE SE ESISTE UNA VACANZA PER L'UTENTE, SE NO CREARNE UNA
        if Vacanza.objects.filter(utente=utente).count() == 0:
            return redirect("HolidayPlanning:creavacanza")
        return render(request, template_name="HolidayPlanning/scegli_attrazione.html",
                      context={"form": form, "att": att, "title": att.nome, "vacanza": vacanza})
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


# class create view per aggiungere lo spsotamento tra due scelte
# deve controllare che l'ora di partenza sia successiva alla fine della attrazione A
# e che l'ora di arrivo sia precedente all'inizio dell'attrazione B
# bisogna scrivhere dei metodi per spostare attrazioni e mandare messaggi su infattibilità viaggi
# le attrazioni di partenza e arrivo sono mandate via template con le pk delle scelte
class AggiungiSpostamento(LoginRequiredMixin, CreateView):
    model = Spostamento
    form_class = SpostamentoForm
    template_name = "HolidayPlanning/spostamento.html"

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        initial['scelta_partenza'] = scelta_partenza
        scelta_arrivo = scelta_partenza.next_scelta()
        initial['scelta_arrivo'] = scelta_arrivo

    def form_valid(self, form):
        spostamento = form.save(commit=False)
        # checkOrari(form.cleaned_data['ora_partenza'], form.cleaned_data['ora_arrivo'])
        if form.cleaned_data['durata_spostamento'] in [None, '']:
            spostamento.durata_spostamento = form.cleaned_data['ora_arrivo'] - form.cleaned_data['ora_partenza']
        if form.cleaned_data['costo'] not in [None, '']:
            vacanza = Vacanza.objects.get(pk=self.kwargs['vac'])
            vacanza.costo += form.cleaned_data['costo']
        spostamento.save()
        return super().form_valid(form)


# class per modificare una scelta data la chiave primaria
class ModificaScelta(LoginRequiredMixin, UpdateView):
    model = Scelta
    template_name = "HolidayPlanning/modificascelta.html"
    fields = ['giorno', 'oraInizio', 'oraFine']

    def get_success_url(self):
        vacanza_id = self.kwargs["vacanza_id"]
        print("Vacanza_id in get_success_url di modificascelta: "+vacanza_id)
        return redirect("HolidayPlanning:dettagliovacanza", vacanza_id)


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
        vacanza_id = self.kwargs["vacanza_id"]
        print("Vacanza_id in get_success_url di cancellascelta: "+vacanza_id)
        return reverse("HolidayPlanning:dettagliovacanza", args=[vacanza_id])


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


# view che elenca le vacanze fatte dal root, dato che anche gli utenti anonimi possono vedere i tour vengono rimandati
# ad un altra view
def vacanze_by_root(request):
    try:
        user = UserProfileModel.objects.get(nrSocio=1)
        vacanze = Vacanza.objects.filter(utente=user)
        tour = True
        context = {
            'title': "I Nostri Tour Organizzati",
            'utente': user,
            'vacanze': vacanze,
            'tour': tour
        }
        return render(request, 'HolidayPlanning/vacanze.html', context)
    except UserProfileModel.DoesNotExist:
        return HttpResponse("User not found", status=404)


# DetailView per vedere il toru organizzato
class TourDetail(DetailView):
    model = Vacanza
    template_name = "HolidayPlanning/dettagliovacanza.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tour Organizzato"
        context['tour'] = True
        vacanza = Vacanza.objects.get(pk=kwargs['object'].id)
        context['vacanza'] = vacanza
        context['scelte'] = vacanza.scelte.all().reverse()  # l'ultima aggiunta viene mostrata per prima
        context['totale'] = vacanza.calcolaTotaleAttrazioni()
        return context


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


# classe usata per copiare un tour organizzato e usarlo come vacanza propria
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
            # recupero l'oggetto vacanza
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
            vacanza_obj = Vacanza.objects.get(pk=vacanza_id)  # recupero l'oggetto vacanza
            initial['dataArrivo'] = vacanza_obj.dataArrivo
            initial['dataPartenza'] = vacanza_obj.dataPartenza
            initial['budgetDisponibile'] = vacanza_obj.budgetDisponibile
            return initial


# class view per i dettagli di una vacanza
class DettaglioVacanza(LookingTourMixin, DetailView):
    model = Vacanza
    template_name = "HolidayPlanning/dettagliovacanza.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dettagli Vacanza"
        context['tour'] = False
        context['utente'] = self.request.user
        vacanza = Vacanza.objects.get(pk=kwargs['object'].id)
        context['vacanza'] = vacanza
        context['scelte'] = vacanza.scelte.all().reverse()  # l'ultima aggiunta viene mostrata per prima
        context['totale'] = vacanza.calcolaTotaleAttrazioni()
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