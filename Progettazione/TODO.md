GLOSSARIO:
    TURISTA = UTENTE REGISTRATO E LOGGATO
    
# REQUISITI FONDAMENTALI:
* recensioni --> FATTO
* tour organizzati --> FATTO
* ricerca attrazioni --> FATTO
* piano vacanza scandito per giornate --> frontend
* calcolare gli spostamenti --> FATTO
* difficoltà prevista della giornata --> FATTO
  * metodo calcola difficoltà nel modello vacanza, se in una giornata ci sono più di 4 attrazioni allora è difficile
  * se ce ne sono 2-3 è media, 1 è facile
* recommendation system --> FATTO, va testato e documentato bene


## TO-DO:
BACKEND
2) aggiungere stato chiusa alla vacanza (NECESSARIO)?
3) la registrazione dell admin avviene dalla pagina /admin/signup e il login da /admin/signin
4) una recensione all'attività andrebbe lasciata dopo che si è fatta l'attrazione, quindi dopo che è passata la data scelta

FRONTEND
1) inserire la foto dell'utente nella navbar o in altro posto
2) inserire nome_vacanza nel dettaglio di una vacanza e nella lista di vacanze
3) inserire metodo difficolta_vacanza nel dettaglio di una vacanza e nel template
4) inserire dettagli scelta o migliorare scheda della scelta in dettaglio vacanza
5) piano vacanza scandito per giornate: è solo una cosa di frontend? Controlli su orari e giorni: se la giornata è finita non si possono aggiungere più attrazioni
per ogni attrazione stampata nella lista o nel piano pdf, se quella successiva è di una giornata seguente si stampa il giorno e il numero della giornata
6) Migliorare frontend per barra di ricerca e per i risultati della ricerca
7) nel form di aggiunta scelta bisogna ricordare la vacanza
8) Il mio itinerario deve ricordare alcuni dettagli della vacanza
9) sistemare pagina di cancella scelta
10) In ListaScelte metà pagina mostra la lista delle scelte e l'altra metà mostra i dettagli del viaggio con il budget che scala
11) sistemare navbar
12) Creare homepage.html
13) Riempire la sezione contatti con alcuni contatti (e magari il form per le mail)
    * Migliorare tutto l'aspetto grafico del sito *

# DOING:
* 
* ampliare vacanze del root

# RECOMMENDATION SYSTEM
* raccomandazioni basate sulla tipologia e durata e costo
* differenze tra turista e utente anonimo
  * se utente anonimo gli posso raccomandare i più popolari che sono le attrazioni più presenti nelle varie vacanze
  * se utente è turista
    * che ha fatto già vacanze con altre scelte: 
      * posso raccomandare delle scelte che sono presenti in vacanze di altri utenti che hanno fatto almeno una scelta uguale
    * non ha ancora fatto vacanze o scelte:
      * prendo le vacanze degli altri utenti e restituisco le attrazioni scelte di più
  * se non esistono attività di altri turisti si presentano tutte le attrazioni oppure non si consiglia niente 

# Difficoltà prevista della giornata
  * metodo calcola difficoltà nel modello vacanza, se in una giornata ci sono più di 4 attrazioni allora è difficile
  * se ce ne sono 2-3 è media, 1 è facile

# SPOSTAMENTI: DA INSERIRE A MANO (può essere esteso venendo calcolato dal sistema)
  * la durata e la tipologia degli spostamenti sono parte di una scelta, definiscono il trasferimento verso un'attrazione
  * fanno ricalcolare il tempo di una giornata e per la prossima attività
  * calcolare gli spostamenti:
  * Modello:
    * provare a inserire nuova model class -> fatto
    * inserire metodi per controllare i vari campi
      * durata da calcolare e correggere --> fatto
      * lo spostamento deve essere compreso tra un attrazione e l'altra altrimenti non si può salvare --> fatto by design
      * se lo spostamento si sovrappone totalmente o parzialmente ad un'altra attività allora non va bene --> fatto
    * inserire alcune entità di spostamento nel db --> fatto
  * Template:
    * sezione nel dettaglio di una vacanza in cui mettere gli spostamenti: bottone tra una attrazione e la successiva --> fatto
    * card in cui appaiono i dettagli dello spostamento --> fatto
    * bisogna mettere dei suggerimenti nel form per gli orari e il giorno --> fatto migliorabile
  * View:
    * riceve il riferimento alla vacanza --> fattp
    * view AggiungiSpostamento che prende in ingresso due primary key di una scelta e vacanza --> fatto
  * Form:
    * form che inserisce i campi degli orari e del tipo, costo --> fatto
    * le due scelte non devono essere modificabili --> fatto

# TOUR organizzati: 
  * vacanze del root sono visualizzabili nella sezione dedicata da tutti
  * uno può aggiungere direttamente quegli itinerari alla sua lista vacanze, e si possono modificare

# RECENSIONI
  * Le recensioni si visualizzano nella pagina di dettaglio di un attrazione
  * Le può inserire soltanto un utente registrato che ha compilato una vacanza con quella attivita
  *  NON SI PUÒ RECENSIRE LA STESSA ATTIVITÀ PIÙ VOLTE
  *  sono inseribili tramite form raggiungibile dalla pagina della vacanza:
  *  1° modo)gestisci vacanze -> selziona 1 vacanza -> nella card di una attrazione clicca su bottone recensisci
  *  2° modo)home-> dettaglio dell'attrazione-> sotto la finestra delle recensioni Bottone recensisci
  *  in crea recensione ci deve essere scritto il riferimento "Recensisci attivita fatta il durante la vacanza..."
  *  --> bisogna recensire l'attrazione in quanto tale oppure come scelta e attività svolta con data, costi ecc...

    DONE:
1) home page principale: definita dal recommendation system, cliccando su logo o home tutte le attrazioni
2) TEST: Da url si può cambiare la pk di una vacanza/scelta e accedere alla vacanza/scelta di un altro utente.
3) aggiungere campo immagine al UserProfileModel, con anche la cartella upload_to
4) Aggiungere nome alla vacanza
5) Aggiustare CancellaScelta perchè non ritorna nessun parametro, andrebbe ritornata la pk della vacanza
6) Aggiustare ModificaScelta, prendere spunto da ProductUpdateView in progetto fillo
7) aggiustare itinerario di viaggio perchè nel mixin quando viene chiamato con pk==0 non viene trovata attrazione
8) difficoltà prevista della giornata
9) la lista delle scelte all'interno della vacanza deve sempre essere ordinata in dettagliovacanza: metodo all'interno della classe model Vacanza 
10) OPERAZIONI FINE VACANZA: concludere la vacanza e stampare il piano
11) Immettere interfacce di gestione per cancellare attrazioni
12) Refactoring separando views di gestione dell'attrazione in nuova app attractions (cambiare urls, views, forms, tempalates...)
13) Immettere interfacce di gestione per aggiungere, modificare attrazioni
14) AGGIUNGERE NAVBAR PER OPERAZIONI DI HOLIDAYPLANNING: LISTASCELTE.HTML E MODIFICA SCELTE
    Navbar piccola sotto quella principale che aggiunge qualche link se il turista ha già creato una vacanza oppure
    mostra un messaggio "Inizia a Creare la tua vacanza! Clicca su HolidayPlanning"
15) pulsante di logut quando l'utente è entrato
16) sistemare detailview attrazione con tutti i campi e la foto
17) API per le vacanze: VacanzeList, VacanzaDetail, VacanzaEdit
18) fare detail view della vacanza con tutte le scelte
19) mettere mixin login required nella lista di attrazioni da scegliere e nella pagina della scelta
20) aggiungere campo foto al modello di attrazione
21) aggiungere controllo sui giorni di creazione della vacanza direttamente nel form
22) consistenza scelte
     quando si fa una scelta si controlla che la data sia nel periodo della vacanza
     quando si fa una scelta si controlla che non si sovrapponga ad altre
23) ListView lista attrazioni che mostra le attrazioni in prima pagina (home) e rimanda nella detail view di ogni
 attrazione, a differenza della pagina attrazioni è raggiungibile senza il login
24) unione login e creazione vacanza
         inserimento dei mixin login required per controllare che l'utente sia registrato (creazione vacanza)
25) aggiustare file ciaulaweb\views.py: dare a template_name un valore esistente e in ciaulaweb\urls.py aggiungere il
path('', HomeView.as_view(), name='home') con from ciaulaweb.views import HomeView
!!!RISOLVERE InconsistentMigrationHistory !!!
26) creazione login
         cosa fanno le variabili in settings.py: LOGIN_REDIRECT_URL, LOGIN_URL, AUTH_USER_MODEL
         registrazione di un profilo utente
         recuperare la schermata di admin
         admin.py aggiustamento
27) nell'app profiles fare dei template appositi per login e logout e inserire l'argomento template_name nella funzione
as_view nel path corrispondente in urlpatterns
28) ripopolare db attrazioni



contatore (globale?) per aggiungere la scelta in fondo alle altre scelte
controllo degli orari e giorno per la scelta
mettere posizione nella giornata
cambiare nome modello Scelta --> AttivitaModel
NON fare lista infinita attrazioni, Fare griglia come amazon

App Profiles per gestire i profili:
-in views.py: UserCreationView, UserUpdateView, UserDetailView
-in urls.py: urlpatterns deve contenere gli indirizzi delle views derivate da auth_views:LoginView,LogoutView,PasswordChangeView,
più anche le views contenute in views.py
-in admin.py: si può lasciare com'è oppure aggiungere una classe UserProfileModelAdmin con dei campi che filtrano gli
attributi
-in forms.py: classe form (eredita da UserCreationForm) per il form di creazione utente e UserUpdateForm per l'aggiornamento
-in mixins.py: una classe IsMyselfMixin per controllare che l'utente che fa la richiesta sia lo stesso che deve essere
modificato, con all'interno solo un metodo dispatch
-in model aggiungere un campo bool per contrassegnare se un utente è un tour manager
-aggiungere la classe ProfilesTest con tutte le funzioni di test connesse


DA Mockup_Holidayplanning2_HOME
La colonna dell' info profilo presenta la possibilità di registrarsi o accedere al profilo ciaulaweb
---> 	se si accede al profilo allora viene ricaricata la home, identica tranne per alcuni dettagli del profilo al 
	posto del bottone (vacanze fatte, nome, cognome, vacanze organizzate?, riprendi ad organizzare la vacaza?)

La parte centrale presenta tutte le attrazioni in ordine sparso presenti nel database, può essere presenta il form
di filtraggio e ricerca presente nella sezione di creazione vacanza. Non sono presenti azioni possibili sulle attr.
E' possibile scorrere solamente l'elenco delle attrazioni? ci devono essere più pagine per mostrarle?

Modalità crea vacanza
Campo arrivo, partenza, nr persone, budget disponibile x persona, questi campi sono settabili (inserire anche trasporto?)
tramite calendari e text->int e text->float
--->	premuto il bottone inizia: se l'UTENTE è REGISTRATO vengono presi i valori dei campi e si crea un oggetto/
	entità vacanza salvata nel db per l'utente e si passa alla schermata di holiday making, inoltre vengono settati
	i tot giorni e notti, vengono creati tanti oggetti giorni tanti quanti sono i tot_giorni
				   se l'UTENTE NON è REGISTRATO, viene presentata una scritta rossa che avverte di registrarsi


DA Mockup_Holidayplanning2_MAKE
Header e footer rimangono sempre gli stessi
la colonna di sinistra mostra sempre alcune info sul profilo come foto nome e cognome, ma in questa schermata
può mostrare anche alcune info sulla vacanza che si sta organizzando come il nome della vacanza, il budget iniziale
e il budget disponibile che è calcolato dal budget iniziale meno quello disponibile.
Nella parte centrale ci sono sempre le attrazioni, ma con alcuni dettagli in meno rispetto alla home (fondamentali:
tipo, citta, luogo, costo e immagine). Ma per ogni attrazione devono essere presenti bottoni per compiere azioni
sulle attrazioni legate alla vacanza, come l'aggiunta alla vacanza (in un giorno particolare o in quello correntemente
usato e in che posizione). Nella parte centrale rimane il filtro di ricerca delle attrazioni.
La parte di sinistra contiene le scelte fatte, per ognuna di queste vengono inserite il nome, orari inizio fine e prezzo
insieme ai tasti modifica(?) e cancella, per cambiare l'ordine delle scelte inserire i tastini su e giù nella destra
di ogni scelta, se si preme giù si abbassa la posizione della scelta di uno (il contrario se si preme sù).
Viene presentata soltanto la lista delle scelte di una giornata, in cima alla parte sx si può scegliere la giornata
su cui lavorare (tramite un text field che cliccando mostra le giornate).

Possibilità di creare la propria attrazione?


"todo-tree.highlights.defaultHighlight": {
    "icon": "alert",
    "type": "text",
    "foreground": "red",
    "background": "white",
    "opacity": 50,
    "iconColour": "blue"
},
