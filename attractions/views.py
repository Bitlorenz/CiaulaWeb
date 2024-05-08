import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from datetime import datetime
from profiles.models import UserProfileModel
from attractions.forms import CreaAttrazioneForm, CreaRecensioneForm
from attractions.models import Attrazione, Recensione
from HolidayPlanning.models import Vacanza, Scelta


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "attractions/attrazionilista.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listaattrazioni'] = Attrazione.objects.all()
        utente = self.request.user
        context['user'] = utente
        vacanza_id = self.request.GET.get('vacanza_id')
        if vacanza_id:
            context['vacanza_id'] = vacanza_id
        return context


#  View per la visualizzazione dei dati relativi a un'attrazione
#  Possibilità di aggiungere le recensioni se l'attrazione è stata scelta
def DetailAttrazioneEntita(request, nome_attr):
    if Attrazione.objects.filter(nome=nome_attr).exists():
        templ = "attractions/dettaglioattrazione.html"
        attrazione = Attrazione.objects.get(nome=nome_attr)  # Acquisisco attrazione dal nome
        recensioni = Recensione.objects.filter(attrazione=attrazione)

        # Se utente autenticato controllo se ha scelto l'attrazione in una delle sua vacanze
        # Se l'attrazione è stata scelta in una vacanza precedente, allora può scrivere la recensione
        check = False
        if request.user.is_authenticated:
            user = UserProfileModel.objects.get(email__exact=request.user)  # aquisisco user
            if Vacanza.objects.filter(utente=user).exists():
                vacanze = Vacanza.objects.filter(utente=user)  # Prendo le vacanze fatte dall'utente
                for vacanza in vacanze:
                    for v in vacanza.scelte.all():
                        if v.attrazione == attrazione:  # Se utente ha scelto questa attrazione
                            check = True
            # Se utente ha già recensito l'attrazione (non può recensirlo più volte)
            # if Recensione.objects.filter().exists():
            for r in recensioni.all():
                if r.attrazione == attrazione:
                    if r.autore == user:
                        check = False
        ctx = {"attivita": attrazione, "check": check, "recensioni": recensioni, "title": "Dettaglio Attrazione "}
        if request.method == "GET":
            return render(request, template_name=templ, context=ctx)
        else:
            return HttpResponse("ERROR: nome attrazione non valido, RICHIESTA POST")


# CreateView per l'inserimento di un'attrazione da parte dell'admin
class AttrazioneCreateView(UserPassesTestMixin, CreateView):
    model = Attrazione
    template_name = 'attractions/attrazione_form.html'
    success_url = reverse_lazy("attractions:attrazioni")
    login_url = '../../profiles/registration/signin'
    form_class = CreaAttrazioneForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("Non sei un amministratore, non puoi creare attrazioni")

    def form_valid(self, form):
        if not self.request.user.is_staff:
            return reverse("profiles:user-login")
        attrazione = form.save(commit=False)
        attrazione.save()
        return super().form_valid(form)


#  UpdateView per l'aggiornamento di un'attrazione
class AggiornaAttrazione(UserPassesTestMixin, UpdateView):
    model = Attrazione
    template_name = "attractions/aggiorna_attrazione.html"
    form_class = CreaAttrazioneForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("Non sei un amministratore, non puoi modificare attrazioni")

    def form_valid(self, form):
        if not self.request.user.is_staff:
            return reverse("profiles:user-login")
        attrazione = form.save(commit=False)
        attrazione.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Aggiorna attrazione"
        return context

    def get_success_url(self):
        attrazione = Attrazione.objects.get(pk = self.kwargs["pk"])
        return reverse("attractions:dettaglioattr", kwargs={"nome_attr": attrazione.nome})


class CancellaAttrazione(UserPassesTestMixin, DeleteView):
    model = Attrazione
    template_name = "attractions/cancellaattr.html"
    success_url = reverse_lazy("attractions:attrazioni")

    def delete(self, request, *args, **kwargs):
        return super(CancellaAttrazione, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("Non sei un amministratore, non puoi modificare attrazioni")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attr_pk = self.kwargs['pk']
        attr = Attrazione.objects.get(pk=attr_pk)
        context["attr"] = attr
        context["title"] = "Cancella Attrazione"
        return context


# Ricerca sulle attrazioni da parte dei turisti e utenti anonimi
class SearchView(ListView):
    model = Attrazione
    template_name = 'attractions/cerca.html'
    context_object_name = 'listaricerca'

    # Acquisisco i risultati della ricerca
    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Attrazione.objects.filter(
                Q(nome__contains=query) | Q(tipo__contains=query) | Q(citta__contains=query) | Q(luogo__contains=query)
            )
            result = postresult
        else:
            result = None
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Risultati Ricerca"
        return context


class RecensioneCreateView(LoginRequiredMixin, CreateView):
    model = Recensione
    form_class = CreaRecensioneForm
    template_name = 'attractions/crea_recensione.html'
    success_message = 'Recensione Creata correttamente!'
    slug_url_kwarg = "scelta_pk"

    #  controllo validità campi form
    def form_valid(self, form):
        recensione = form.save(commit=False)
        recensione.autore = UserProfileModel.objects.get(nrSocio=self.request.user.pk)
        scelta = Scelta.objects.get(pk=self.kwargs[self.slug_url_kwarg])
        if scelta.giorno > datetime.now().date():
            form.add_error(None, error=ValueError("Recensione inseribile solo dopo aver fatto l'attività"))
            return self.form_invalid(form)
        recensione.attrazione = scelta.attrazione
        recensione.save()
        self.success_url = reverse_lazy("attractions:dettaglioattr",
                                        kwargs={'nome_attr': recensione.attrazione.pk})  # redireziono all'attrazione
        return super().form_valid(form)

    #  Aggiunge l'attrazione alle variabili di contesto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scelta = Scelta.objects.get(pk=self.kwargs['scelta_pk'])
        context['attrazione'] = scelta
        context['title'] = "Recensisci l'attività"
        return context

    #  Restituisce 404 se l'attrazione non è stata trovata
    def dispatch(self, request, *args, **kwargs):
        scelta = get_object_or_404(Scelta, pk=self.kwargs[self.slug_url_kwarg])
        return super().dispatch(request, scelta=scelta, *args, **kwargs)
