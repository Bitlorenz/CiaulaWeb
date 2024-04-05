from cgitb import text
from datetime import timedelta as td, datetime
from re import sub
import io

from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import UserProfileModel
from .forms import *
from .mixins import LookingTourMixin, IsVacanzaUserOwnedMixin
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
            scelta.durata = td(hours=fine.hour - ini.hour, minutes=fine.minute - ini.minute)
            # checkSovrapposizione(request, fine, ini)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:dettagliovacanza", pk=rifvacanza.pk)
    else:
        utente = request.user
        vacanza = Vacanza.objects.filter(utente=request.user, pk=vacanza_id)
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
class AggiungiSpostamento(IsVacanzaUserOwnedMixin, CreateView):
    model = Spostamento
    form_class = SpostamentoForm
    template_name = "HolidayPlanning/spostamento.html"

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        initial['scelta_partenza'] = scelta_partenza
        scelta_arrivo = scelta_partenza.next_scelta()
        initial['scelta_arrivo'] = scelta_arrivo
        return initial

    def form_valid(self, form):
        spostamento = form.save(commit=False)
        # checkOrari(form.cleaned_data['ora_partenza'], form.cleaned_data['ora_arrivo'])
        if form.cleaned_data['durata_spostamento'] in [None, '']:
            arr = form.cleaned_data['ora_arrivo']
            par = form.cleaned_data['ora_partenza']
            spostamento.durata_spostamento = td(hours=(arr.hour - par.hour), minutes=(arr.minute - par.minute))
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        spostamento.scelta_partenza = scelta_partenza
        spostamento.scelta_arrivo = scelta_partenza.next_scelta()
        if spostamento.ora_arrivo > scelta_partenza.next_scelta().oraInizio:
            raise ValidationError("L'orario di arrivo si sovrappone con la successiva.")
        if spostamento.ora_partenza < scelta_partenza.oraFine:
            raise ValidationError("L'orario di partenza anticipa l'orario di fine attrazione")
        spostamento.save()
        rifvacanza = Vacanza.objects.get(pk=self.kwargs['vac'])
        rifvacanza.spostamenti.add(spostamento)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        context['sugg_oraPartenza'] = scelta_partenza.oraFine
        context['sugg_oraArrivo'] = scelta_partenza.next_scelta().oraInizio
        return context

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={"pk": self.kwargs['vac']})


# class per modificare una scelta data la chiave primaria
class ModificaScelta(IsVacanzaUserOwnedMixin, UpdateView):
    model = Scelta
    template_name = "HolidayPlanning/modificascelta.html"
    form_class = ModificaSceltaForm
    slug_url_kwarg = "att_pk"

    def get_object(self, queryset=None):
        attivita_pk = self.kwargs.get(self.slug_url_kwarg)
        attivita = Scelta.objects.get(pk=attivita_pk)
        return attivita

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attivita_pk = self.kwargs['att_pk']
        attivita = Scelta.objects.get(pk=attivita_pk)
        context["attivita"] = attivita
        vacanza_pk = self.kwargs['pk']
        vacanza = Vacanza.objects.get(pk=vacanza_pk)
        context["vacanza"] = vacanza
        context["v_id"] = vacanza_pk
        context["ora inizio attr"] = attivita.attrazione.oraApertura
        context["ora fine attr"] = attivita.attrazione.oraChiusura
        return context

    def form_valid(self, form):
        scelta = form.save(commit=False)
        attr =  scelta.attrazione
        if form.cleaned_data["oraInizio"] < attr.oraApertura or form.cleaned_data["oraInizio"] > attr.oraChiusura:
            return self.form_invalid(form, 1)
        if form.cleaned_data["oraFine"] < attr.oraApertura or form.cleaned_data["oraFine"] > attr.oraChiusura:
            return self.form_invalid(form, 2)
            # TODO controllare che non ci siano sovrapposizioni con altre attrazioni nello stesso giorno
        ini = form.cleaned_data["oraInizio"]
        fine = form.cleaned_data["oraFine"]
        scelta.durata = td(hours=fine.hour - ini.hour, minutes=fine.minute - ini.minute)
        scelta.save()
        return super().form_valid(form)

    def form_invalid(self, form, error_code):
        if error_code == 1:
            form.add_error('oraInizio', "L'ora di inizio non rispetta i limiti d'orario dell'attrazione")
        if error_code == 2:
            form.add_error('oraFine', "L'ora di fine non rispetta i limiti d'orario dell'attrazione")
        return super().form_invalid(form)

    def get_success_url(self):
        vacanza_id = self.kwargs['pk']
        print("Vacanza_id in get_success_url di modificascelta: " + vacanza_id)
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={'pk': vacanza_id})


# class delete view per eliminare una scelta
class CancellaScelta(IsVacanzaUserOwnedMixin, DeleteView):
    model = Scelta
    template_name = "HolidayPlanning/cancellascelta.html"
    slug_url_kwarg = "att_pk"

    def get_object(self, queryset=None):
        attivita_pk = self.kwargs.get(self.slug_url_kwarg)
        attivita = Scelta.objects.get(pk=attivita_pk)
        return attivita

    def delete(self, request, *args, **kwargs):
        return super(CancellaScelta, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacanza_pk = self.kwargs['pk']
        context["v_id"] = vacanza_pk
        return context

    def get_success_url(self):
        vacanza_id = self.kwargs["pk"]
        print("Vacanza_id in get_success_url di cancellascelta: " + vacanza_id)
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={'pk': vacanza_id})


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
# a un altra view
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


# DetailView per vedere il tour organizzato
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
        context['scelte'] = vacanza.sort_scelte()
        context['spostamenti'] = vacanza.spostamenti.all()
        context['totale'] = vacanza.calcolaTotaleAttrazioni()
        return context


# class view per modificare una vacanza
class ModificaVacanza(IsVacanzaUserOwnedMixin, UpdateView):
    model = Vacanza
    template_name = "HolidayPlanning/modificavacanza.html"
    form_class = ModificaVacanzaForm

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
    vacanza = Vacanza.objects.get(pk=pk, utente=request.user)
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
