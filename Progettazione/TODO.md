GLOSSARIO:
    TURISTA = UTENTE REGISTRATO E LOGGATO
                    FINIRE TUTTO PER MARTEDÌ 07/05/2024
                    INVIARE PROGETTO IN ZIP VENERDÌ 10/05/2024
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
1) TEST di alcune funzioni e class view
2) url dinamici: se cambio padre non devo cambiare gli url delle view che ereditano
3) controllare cold start recommendation system
4) la registrazione dell admin avviene dalla pagina /admin/signup e il login da /admin/signin, devo farlo io

FRONTEND
1) homepage per admin deve essere tutti i prodotti (quella senza views)
2) inserire bottone creaattrazione e modifica attrazione per l'admin
3) il titolo di attractions/attrazioni deve essere sopra la griglia di attrazioni, oppure eliminare la pagina del tutto
4) inserire metodo difficolta_vacanza, numero giorno e data nel pdf della vacanza
5) il template dettaglivacanza deve avere lo specchietto come modificascelta
6) In ListaScelte metà pagina mostra la lista delle scelte e l'altra metà mostra i dettagli del viaggio con il budget che scala
7) Riempire la sezione contatti con alcuni contatti (e magari il form per le mail)
    

# DOING:
* BACKEND:
  * APP PROFILES REFACTORING: Necessario per capire cosa si è fatto e sistemare i vari utenti
    * Modelli:
      * vedere da dove si è preso il modello fatto
      * provare a cambiarlo, senza distruggere l'admin
      * perche AbstractBaseUSer anzichè AbstractUSer?
      * come usare e cosa fare di user manager?
    * Views
      * specificare il template nelle view non negli url: si fa perchè sono delle view di django, basta specificare quello
      * View per creare un nuovo utente: user create view va bene ma l'admin va creato con create_superuser
      * view per modificare utente: da fare, vedere se c'è qualcosa già pronto
      * View per visualizzare dettagli del proprio profilo: prendere template da watchmarket e provare con stessa view
    * Template
      * fare template per registrazione
      * fare template per modifica
      * fare template per dettagli
  * TEST DI CLASSI E FUNZIONI
      * testare upload foto profilo utente e aggiungerla in un punto visibile
* FRONTEND:
  * L'unica homepage deve essere quella del recommendation system 
  * sistemare header.html ->navbar
  * Sistemare bene il pdf
  * inserire in css
  * class: Top_bar_content
* ampliare vacanze del root
* fare README.md seguendo esempio watchmarket

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
* Test:
  * Turista coccobello: caso "non ho attrazioni popolari scelte dall'utente"

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

# Funzione controlla orari e giorni
  * funzioni comuni: controlla che l'ora di fine sia posteriore a quella di inizio 
  * per aggiungispostamento: 
    * l'ora di arrivo dello spostamento sia antecedente all'inizio della seguente scelta
    * l'ora di partenza dello spostamento sia posteriore all'ora di fine della scelta precedente
  *  per scegliattrazione: modifica attrazione
    * gli orari devono essere ammissibili 
    * controlla che la scelta non si sovrapponga ad altre scelte, nello stesso giorno

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

    
# DONE:
1) ModificaVacanza: se restringo i giorni in una vacanza con delle scelte, le scelte di quel giorno vanno rimosse
2) modificare template modifica vacanza con specchietto uguale a modifica scelta
3) inserire dettagli scelta o migliorare scheda della scelta in dettaglio vacanza
4) Miglioramento pagina dettagli della vacanza, bisogna aggiustare grandezza card e immagine
5) sistemare pagina di cancella scelta
    * ingrandire bottoni
    * mostrare dettagli della scelta
6) migliorati template modifica scelta e aggiungiscelta
7) nel template di aggiunta scelta bisogna ricordare la vacanza
    * aggiungere l'attrazione (nome o field form che si vuole aggiungere)
    * aggiungere anche dettagli sull'attrazione da aggiungere, costo, orari apertura ecc...
8) inclusione nei templates di HolidayPlanning e profiles del blocco head e del titolo
9) fare view cancella attrazione solo per admin
10) una recensione all'attività lasciata dopo che si è fatta l'attrazione, quindi dopo che è passata la data scelta
11) fare form e template modifica attrazione accessibile solo all'admin
12) l'url è sbagliato quando si clicca sul titolo immagine dei risultati
13) sistemare pannello scelta, deve funzionare anche per root
14) home page principale: definita dal recommendation system, cliccando su logo o home tutte le attrazioni
15) TEST: Da url si può cambiare la pk di una vacanza/scelta e accedere alla vacanza/scelta di un altro utente.
16) aggiungere campo immagine al UserProfileModel, con anche la cartella upload_to
17) Aggiungere nome alla vacanza
18) Aggiustare CancellaScelta perchè non ritorna nessun parametro, andrebbe ritornata la pk della vacanza
19) Aggiustare ModificaScelta, prendere spunto da ProductUpdateView in progetto fillo
20) aggiustare itinerario di viaggio perchè nel mixin quando viene chiamato con pk==0 non viene trovata attrazione
21) difficoltà prevista della giornata
22) la lista delle scelte all'interno della vacanza deve sempre essere ordinata in dettagliovacanza: metodo all'interno della classe model Vacanza 
23) OPERAZIONI FINE VACANZA: concludere la vacanza e stampare il piano
24) Immettere interfacce di gestione per cancellare attrazioni
25) Refactoring separando views di gestione dell'attrazione in nuova app attractions (cambiare urls, views, forms, tempalates...)
26) Immettere interfacce di gestione per aggiungere, modificare attrazioni
27) AGGIUNGERE NAVBAR PER OPERAZIONI DI HOLIDAYPLANNING: LISTASCELTE.HTML E MODIFICA SCELTE
    Navbar piccola sotto quella principale che aggiunge qualche link se il turista ha già creato una vacanza oppure
    mostra un messaggio "Inizia a Creare la tua vacanza! Clicca su HolidayPlanning"
28) pulsante di logut quando l'utente è entrato
29) sistemare detailview attrazione con tutti i campi e la foto
30) API per le vacanze: VacanzeList, VacanzaDetail, VacanzaEdit
31) fare detail view della vacanza con tutte le scelte
32) mettere mixin login required nella lista di attrazioni da scegliere e nella pagina della scelta
33) aggiungere campo foto al modello di attrazione
34) aggiungere controllo sui giorni di creazione della vacanza direttamente nel form
35) consistenza scelte
     quando si fa una scelta si controlla che la data sia nel periodo della vacanza
     quando si fa una scelta si controlla che non si sovrapponga ad altre
36) ListView lista attrazioni che mostra le attrazioni in prima pagina (home) e rimanda nella detail view di ogni
 attrazione, a differenza della pagina attrazioni è raggiungibile senza il login
37) unione login e creazione vacanza
         inserimento dei mixin login required per controllare che l'utente sia registrato (creazione vacanza)
38) aggiustare file ciaulaweb\views.py: dare a template_name un valore esistente e in ciaulaweb\urls.py aggiungere il
path('', HomeView.as_view(), name='home') con from ciaulaweb.views import HomeView
!!!RISOLVERE InconsistentMigrationHistory !!!
39) creazione login
         cosa fanno le variabili in settings.py: LOGIN_REDIRECT_URL, LOGIN_URL, AUTH_USER_MODEL
         registrazione di un profilo utente
         recuperare la schermata di admin
         admin.py aggiustamento
40) nell'app profiles fare dei template appositi per login e logout e inserire l'argomento template_name nella funzione
as_view nel path corrispondente in urlpatterns
41) ripopolare db attrazioni


* testing delle view di HolidayPlanning (soprattutto quelle protette dal mixin)
  * aggiungi spostamento: 
    * funzionante per Admin e Turista
    * migliorare i messaggi di errore ad esempio quello della sovrapposizione
  * ModificaVacanza: funzionante per Admin e Turista
  * ModificaScelta: funzionante per Turista e Admin
  * CancellaScelta: funzionante per Admin e Turista
  * CreaVacanza: funzionante per Admin e Turista
  * AggiungiTourVacanza: funzionante per turista
  * ModificaVacanza: funzionante per turista e admin
  * stampavacanza: funzionante per turista e admin
  * AggiornaAttrazione per admin: controlli se esiste un attrazione uguale, se gli orari sono corretti, fare template
  * Creaattrazione: funzionante per admin
  * CancellaAttrazione: funzionante per admin, una vacanza con un attrazione, poi cancellare l'attrazione, la vacanza rimane senza scelte
  * SearchView funziona per Turista e admin

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
