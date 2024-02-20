GLOSSARIO:
    TURISTA = UTENTE REGISTRATO E LOGGATO
    
# REQUISITI FONDAMENTALI:
* recensioni
* tour organizzati
* ricerca attrazioni
* piano vacanza scandito per giornate
* calcolare gli spostamenti
* difficoltà prevista della giornata
* recommendation system


## TO-DO:
	BACKEND
    36)la lista delle scelte all'interno della vacanza deve sempre essere ordinata
    32)Aggiungere nome alla vacanza, aggiungere stato chiusa alla vacanza
    25)TEST: Da url non si può cambiare la pk di una vacanza per modificarla, se l'user è diverso non si può fare.   Provare: cambio utente, creo una vacanza, cosa succede se nell'url cambio l'id della vacanza? se vado nella vacanza dell'altro utente è un problema          
    10)aggiungere campo immagine al UserProfileModel, con anche la cartella upload_to
    19)la registrazioe dell admin avviene dalla pagina /admin/signup e il login da /admin/signin

    FRONTEND
    35)nel form di aggiunta scelta bisogna ricordare la vacanza
    34)Il mio itinerario deve ricordare alcuni dettagli della vacanza
    30)sistemare pagina di cancella scelta
    31)In ListaScelte metà pagina mostra la lista delle scelte e l'altra metà mostra i dettaglie del viaggio con il budget che scala
    24)sistemare deatilview vacanza con scelte raggruppate per giorni
    20)sistemare navbar
    9)Creare homepage.html
    26)Riempire sezione "I nostri tour" con delle proposte di tour
    27)Riempire la sezione contatti con alcuni contatti (e magari il form per le mail)
    * Migliorare tutto l'aspetto grafico del sito *

# DOING:
* RECENSIONI ALLE ATTRAZIONI:
  * risolvere bug: quando si clicca sul bottone della recensione bisogna passare la pk che dovrebbe essere quella dell'attrazione non della scelta
  * verifica UI Recensioni: come inserirle, dove, quando, come, chi, dove visualizzarle
  * controllo di possibilità per la scrittura della recensione:si può lasciare una recensione solo se tra tutte le scelte che ha fatto un turista, nelle sue vacanze passate,
 c'è l'attrazione a cui si vuole lasciare una recensione. [andrebbe lasciata dopo che si è fatta l'attrazione, quindi dopo che è passato la data scelta]
*    OPERAZIONI FINE VACANZA: concludere  
      22)Sistemare ScelteList

{!!!HOT!!!} GESTIONE HOLIDAYPLANNING
PROBLEMI
    La vacanza corrente è vista come il carrello e "Gestisci Vacanze" come una sezione "Miei Ordini"
    Le scelte vengono aggiunte sempre all'ultima vacanza: è corretto oppure dobbiamo scegliere a quale vacanza aggiungere una scelta? La vacanza però non dovrebbe essere già passata
    CancellaVacanza view: è utile cancellare una vacanza? al massimo si può svuotare il carrello, ovvero cancellare tutte le scelte dell'attuale vacanza




    DONE:
    OPERAZIONI FINE VACANZA: concludere la vacanza e stampare il piano
37)Immettere interfacce di gestione per cancellare attrazioni
38)Refactoring separando views di gestione dell'attrazione in nuova app attractions (cambiare urls, views, forms, tempalates...)
37)Immettere interfacce di gestione per aggiungere, modificare attrazioni
21)AGGIUNGERE NAVBAR PER OPERAZIONI DI HOLIDAYPLANNING: LISTASCELTE.HTML E MODIFICA SCELTE
    Navbar piccola sotto quella principale che aggiunge qualche link se il turista ha già creato una vacanza oppure
    mostra un messaggio "Inizia a Creare la tua vacanza! Clicca su HolidayPlanning"
29)pulsante di logut quando l'utente è entrato
16)sistemare detailview attrazione con tutti i campi e la foto
23)API per le vacanze: VacanzeList, VacanzaDetail, VacanzaEdit
19)fare detail view della vacanza con tutte le scelte
17)mettere mixin login required nella lista di attrazioni da scegliere e nella pagina della scelta
9)aggiungere campo foto al modello di attrazione
18)aggiungere controllo sui giorni di creazione della vacanza direttamente nel form
3)consistenza scelte
    quando si fa una scelta si controlla che la data sia nel periodo della vacanza
    quando si fa una scelta si controlla che non si sovrapponga ad altre
14)ListView lista attrazioni che mostra le attrazioni in prima pagina (home) e rimanda nella detail view di ogni
 attrazione, a differenza della pagina attrazioni è raggiungibile senza il login
5)unione login e creazione vacanza
        inserimento dei mixin login required per controllare che l'utente sia registrato (creazione vacanza)
6)aggiustare file ciaulaweb\views.py: dare a template_name un valore esistente e in ciaulaweb\urls.py aggiungere il
path('', HomeView.as_view(), name='home') con from ciaulaweb.views import HomeView
!!!RISOLVERE InconsistentMigrationHistory !!!
4)creazione login
        cosa fanno le variabili in settings.py: LOGIN_REDIRECT_URL, LOGIN_URL, AUTH_USER_MODEL
        registrazione di un profilo utente
        recuperare la schermata di admin
        admin.py aggiustamento
7)nell'app profiles fare dei template appositi per login e logout e inserire l'argomento template_name nella funzione
as_view nel path corrispondente in urlpatterns
11)ripopolare db attrazioni

# RECENSIONI
    Le recensioni si visualizzano nella pagina di dettaglio di un attrazione
    sono inseribili tramite form raggiungibile dalla pagina della vacanza: gestisci vacanze -> selziona 1 vacanza -> nella card di una attrazione clicca su bottone recensisci

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