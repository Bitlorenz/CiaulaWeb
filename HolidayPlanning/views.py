from datetime import date, timedelta as td, datetime
import io
from gettext import gettext as _

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import UserProfileModel
from .forms import *
from .mixins import LookingTourMixin, IsVacanzaUserOwnedMixin
from .models import Scelta, Spostamento, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


def checkOrariGiorno(vacanza, scelta, spostamento):
    if spostamento is None:  # caso modifica o aggiungi scelta
        # controllo se il giorno rientra nella vacanza
        if scelta.giorno > vacanza.dataPartenza or scelta.giorno < vacanza.dataArrivo:
            raise ValidationError(_("Giorno non valido: %(valore)s"),
                                  code="invalid", params={"valore": scelta.giorno.strftime("%d-%m-%Y")})
        # controlli ammissibilità orari
        if scelta.oraInizio >= scelta.oraFine:
            raise ValidationError(_("Orario di Inizio precede Orario di fine: %(valore)s"),
                                  code="invalid", params={"valore": scelta.oraInzio.isoformat()})
        if scelta.oraInizio < scelta.attrazione.oraApertura:
            raise ValidationError(_("Orario di Inizio precede Orario di Apertura: %(valore)s"),
                                  code="invalid", params={"valore": scelta.oraInzio.isoformat()})
        if scelta.oraFine > scelta.attrazione.oraChiusura:
            raise ValidationError(_("Orario di Fine successivo a Orario di Chiusura: %(valore)s"),
                                  code="invalid", params={"valore": scelta.oraFine.isoformat()})
        # controllo sovrapposizione con tutte le scelte presenti
        if vacanza.scelte.exists():
            for s in vacanza.scelte.all():
                if s.id != scelta.id:
                    if s.oraInizio <= scelta.oraInizio <= s.oraFine:
                        raise ValidationError(
                        _("Orario di Inizio si sovrappone con la scelta: %(nome)s che inizia alle %(inizio)s"),
                        code="invalid", params={"inizio": scelta.oraInizio.isoformat(), "nome": scelta.attrazione.nome})
                    if s.oraInizio <= scelta.oraFine <= s.oraFine:
                        raise ValidationError(
                        _("Orario di Fine si sovrappone con la scelta: %(nome)s che inizia alle %(inizio)s"),
                        code="invalid", params={"inizio": scelta.oraFine.isoformat(), "nome": scelta.attrazione.nome})
    else:  # caso aggiungi o modifica spostamento
        if spostamento.ora_arrivo < spostamento.ora_partenza:
            raise ValidationError(_("Orario di Arrivo precede Orario di Partenza: %(valore)s"),
                                  code="invalid", params={"valore": spostamento.ora_arrivo.isoformat()})
        if spostamento.ora_arrivo > spostamento.scelta_arrivo.oraInizio:
            raise ValidationError(
                _("Orario di Arrivo %(valore)s posteriore a Orario di inizio attività successiva: %(scelta)s"),
                code="invalid",
                params={"valore": spostamento.ora_arrivo.isoformat(),
                        "scelta": spostamento.scelta_arrivo.oraInizio.isoformat()})
        if spostamento.ora_partenza < spostamento.scelta_partenza.oraFine:
            raise ValidationError(
                _("Orario di Partenza %(valore)s precedente a Orario di fine attività precedente: %(scelta)s"),
                code="invalid",
                params={"valore": spostamento.ora_partenza.isoformat(),
                        "scelta": spostamento.scelta_partenza.oraFine.isoformat()})


# API SPOSTAMENTO

# class create view per aggiungere lo spsotamento tra due scelte
# l' attrazione di partenza e la vacnza sono mandate via url
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
        if form.cleaned_data['durata_spostamento'] in [None, '']:
            arr = form.cleaned_data['ora_arrivo']
            par = form.cleaned_data['ora_partenza']
            spostamento.durata_spostamento = td(hours=(arr.hour - par.hour), minutes=(arr.minute - par.minute))
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        spostamento.scelta_partenza = scelta_partenza
        spostamento.scelta_arrivo = scelta_partenza.next_scelta()
        rifvacanza = Vacanza.objects.get(pk=self.kwargs['pk'])
        checkOrariGiorno(rifvacanza, None, spostamento)
        spostamento.save()
        rifvacanza.spostamenti.add(spostamento)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scelta_partenza = Scelta.objects.get(pk=self.kwargs['par'])
        context['sugg_oraPartenza'] = scelta_partenza.oraFine
        context['sugg_oraArrivo'] = scelta_partenza.next_scelta().oraInizio
        context['title'] = "Aggiungi uno spostamento"
        return context

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={"pk": self.kwargs['pk']})


def getVacanzapkFromSpostamento(user, spostamento):
    vacanzeutente = Vacanza.objects.filter(utente=user)
    for v in vacanzeutente:
        if v.spostamenti.contains(spostamento):
            return v.pk


# class view per modificare gli orari e altri campi di uno spostamento
class ModificaSpostamento(LoginRequiredMixin, UpdateView):
    model = Spostamento
    template_name = "HolidayPlanning/modificaspostamento.html"
    form_class = ModificaSpostamentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spostamento = self.get_object()
        context['spostamento'] = spostamento
        context['v_pk'] = getVacanzapkFromSpostamento(self.request.user, spostamento)
        context['title'] = "Modifica lo Spostamento"
        return context

    def form_valid(self, form):
        spostamento = form.save(commit=False)
        checkOrariGiorno(None, None, spostamento)
        spostamento.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza",
                       kwargs={"pk": getVacanzapkFromSpostamento(self.request.user, self.get_object())})


class CancellaSpostamento(LoginRequiredMixin, DeleteView):
    model = Spostamento
    template_name = 'HolidayPlanning/cancellaspostamento.html'

    def delete(self, request, *args, **kwargs):
        return super(CancellaSpostamento, self).delete(request, *args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['v_pk'] = getVacanzapkFromSpostamento(self.request.user, self.get_object())
        context['title'] = "Cancella Spostamento"
        return context

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza",
                       kwargs={"pk": getVacanzapkFromSpostamento(self.request.user, self.get_object())})


# API SCELTE
# Funzione per creare una scelta data un attrazione
def scegliattrazione(request, pk, vacanza_id):
    if request.method == "POST":
        form = ScegliAttrazioneForm(data=request.POST, pk=pk)
        if form.is_valid():
            scelta = form.save(commit=False)
            rifvacanza = Vacanza.objects.get(utente=request.user, pk=vacanza_id)
            ini = form.cleaned_data.get("oraInizio")
            fine = form.cleaned_data.get("oraFine")
            scelta.durata = td(hours=fine.hour - ini.hour, minutes=fine.minute - ini.minute)
            scelta.attrazione = Attrazione.objects.get(pk=pk)
            checkOrariGiorno(rifvacanza, scelta, None)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:dettagliovacanza", pk=rifvacanza.pk)
    else:
        utente = request.user
        vacanza = Vacanza.objects.get(utente=request.user, pk=vacanza_id)
        att = get_object_or_404(Attrazione, pk=pk)
        form = ScegliAttrazioneForm(pk=pk)
        if Vacanza.objects.filter(utente=utente).count() == 0:
            return redirect("HolidayPlanning:creavacanza")
        return render(request, template_name="HolidayPlanning/scegli_attrazione.html",
                      context={"form": form, "att": att, "title": "Aggiungi questa attrazione alla Vacanza", "vacanza": vacanza})
    return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form})


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
        context['title'] = "Modifica la tua scelta"
        return context

    def form_valid(self, form):
        scelta = form.save(commit=False)
        rifvacanza = get_object_or_404(Vacanza, pk=self.kwargs['pk'])
        ini = form.cleaned_data["oraInizio"]
        fine = form.cleaned_data["oraFine"]
        scelta.durata = td(hours=fine.hour - ini.hour, minutes=fine.minute - ini.minute)
        print("controllo della validità")
        try:
            checkOrariGiorno(rifvacanza, scelta, None)
        except ValidationError as e:
            error_message = e.message % e.params
            messages.error(request=self.request, message=error_message)
            context = self.get_context_data(form=form)
            context['error_message'] = str(e.message)
            return render(self.request, self.template_name, context)
        scelta.oraInizio = ini
        scelta.oraFine = fine
        scelta.giorno = form.cleaned_data["giorno"]
        scelta.save()
        return super().form_valid(form)

    def get_success_url(self):
        vacanza_id = self.kwargs['pk']
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
        context["v_id"] = self.kwargs['pk']
        context["scelta"] = self.get_object()
        context["title"] = "Cancella L' Attrazione Scelta"
        return context

    def get_success_url(self):
        vacanza_id = self.kwargs["pk"]
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={'pk': vacanza_id})


# API VACANZA
# class view per mostrare la lista delle vacanze di un utente
class VacanzeList(LoginRequiredMixin, ListView):
    model = Vacanza
    template_name = "HolidayPlanning/vacanze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Le tue Vacanze"
        context['utente'] = self.request.user
        context['vacanze'] = Vacanza.objects.filter(utente=self.request.user)
        context['tour'] = False
        context['today'] = date.today()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crea la tua Vacanza"
        return context


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
        context['title'] = "La Vacanza nel Dettaglio"
        context['tour'] = False
        context['utente'] = self.request.user
        vacanza = Vacanza.objects.get(pk=kwargs['object'].id)
        context["giorno"] = datetime.now().date()
        context['vacanza'] = vacanza
        context['scelte'] = vacanza.sort_scelte()
        context['spostamenti'] = vacanza.spostamenti.all()
        context['totale'] = vacanza.calcolaTotaleAttrazioni()
        context['difficolta'] = vacanza.difficolta_giornata()
        return context


# class view per modificare una vacanza
class ModificaVacanza(IsVacanzaUserOwnedMixin, UpdateView):
    model = Vacanza
    template_name = "HolidayPlanning/modificavacanza.html"
    form_class = ModificaVacanzaForm

    def dispatch(self, request, *args, **kwargs):
        vacanza = self.get_object()
        if vacanza.dataPartenza < date.today():
            return HttpResponseForbidden("Non puoi modificare una vacanza già conclusa.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        oldVacanza = Vacanza.objects.get(pk=self.kwargs["pk"])
        newDataArrivo = form.cleaned_data["dataArrivo"]
        newDataPartenza = form.cleaned_data["dataPartenza"]
        scelteEliminare = []
        if newDataArrivo.day > oldVacanza.dataArrivo.day:
            scelteEliminare = oldVacanza.scelte.filter(giorno__lt=newDataArrivo)
            for scelta in scelteEliminare:
                vacanza.scelte.remove(scelta)
        if newDataPartenza.day < oldVacanza.dataPartenza.day:
            scelteEliminare = oldVacanza.scelte.filter(giorno__gt=newDataPartenza)
            for scelta in scelteEliminare:
                vacanza.scelte.remove(scelta)
        vacanza.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifica la tua Vacanza"
        context['show_modal'] = True
        return context

    def get_success_url(self):
        return reverse("HolidayPlanning:dettagliovacanza", kwargs={"pk": self.object.pk})


# view per stampare il pdf della vacanza
def stampaVacanza(request, pk):
    # crea un buffer file-like per ricevere i dati del pdf
    buffer = io.BytesIO()
    # crea un canvas per scrivere il pdf
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    #cornice
    larghezza_frame = letter[0] - (2*0.5*cm)
    altezza_frame = letter[1] - (2*0.5*cm)
    p.setStrokeColorRGB(0, 0, 0)
    p.rect(0.5*cm, 0.5*cm, larghezza_frame, altezza_frame)

    # recupera l'oggetto vacanza data la chiave primaria
    vacanza = Vacanza.objects.get(pk=pk, utente=request.user)
    if vacanza.nome is not None:
        titolo = vacanza.nome
        p.setFont("Helvetica", 24)
        p.setFillColorRGB(1, 0, 0) # Rosso
        larghezza_titolo = p.stringWidth(titolo, "Helvetica", 24)
        p.drawCentredString((larghezza_frame - larghezza_titolo) / 2+0.5*cm, 1.5*cm, titolo)

    # scrive il testo
    textob = p.beginText()
    textob.setTextOrigin(cm * 0.7, cm * 2)
    textob.setFont("Helvetica", 14)
    textob.setFillColorRGB(0,0,0)
    righeTesto = ["Vacanza di " + vacanza.utente.first_name + " " + vacanza.utente.last_name,
                  "Data di arrivo: " + str(vacanza.dataArrivo), "Data di partenza: " + str(vacanza.dataPartenza),
                  "Numero di persone: " + str(vacanza.nrPersone),
                  "Budget disponibile: €" + str(vacanza.budgetDisponibile), "Programma Vacanza: "]
    costoTotale = 0
    giornoprec = None
    for index, s in enumerate(vacanza.sort_scelte()):
        giornocorrente = str(s.giorno)
        if giornoprec is None or giornocorrente != giornoprec:
            righeTesto.append("Giornata "+str(index+1)+" - "+giornocorrente)
        righeTesto.append(str(s.attrazione.nome))
        righeTesto.append(" \nOra Inizio: " + str(s.oraInizio) + " - Ora Fine:" + str(s.oraFine))
        spostamenti = vacanza.spostamenti.all()
        spos = vacanza.spostamenti.filter(scelta_arrivo=s)
        spos = spos.first()
        if spos is not None:
            luoghi = "Da " + spos.scelta_partenza.attrazione.citta + " A " + spos.scelta_arrivo.attrazione.citta
            orari = "\nOra Partenza: " + str(spos.ora_partenza) + ", Ora Arrivo: " + str(spos.ora_arrivo) +\
                    ", Durata: " + str(spos.durata_spostamento)
            veicolocosti = "Veicolo: " + spos.veicolo + ", Costo Spostamento: €" + str(spos.costo)
            righeTesto.append("SPOSTAMENTO:" )
            righeTesto.append(luoghi)
            righeTesto.append(orari)
            righeTesto.append(veicolocosti)
        costoTotale = costoTotale + s.attrazione.costo
        giornoprec = giornocorrente
    righeTesto.append("Costo totale: €" + str(costoTotale))
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
