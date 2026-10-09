# Testi delle pagine interne. Presi dal sito attuale (neverbeforeitalia.it/services e /about), parola per parola.
# Dove il sito attuale non ha un testo (i servizi nuovi) resta solo la riga breve della card in home: da completare.

SERVIZI_INTRO = dict(
    big='Efficienza, metodo e trasversalità.',
    text='La capacità di Never Before Italia sta nel conoscere ed interpretare le dinamiche competitive di ogni "industry" per costruire con metodo strategie comunicative efficaci, trasversali e non convenzionali.',
)

# slug, titolo come nella card della home (h3), testo lungo, voci; cats/kw: quali progetti mostrare come esempi
SERVIZI = [
    dict(slug='marketing-strategy', h3='Marketing <em>strategy</em>',
         long='Partendo da accurate analisi di mercato, creiamo ed implementiamo strategie inbound che accompagnano il cliente lungo il viaggio alla scoperta del brand, creando esperienze non convenzionali in grado di fidelizzazione ed assicurare risultati misurabili di lungo termine.',
         subs=['Marketing consulting', 'Business intelligence & market research', 'Marketing coaching', 'Marketing implementation', 'Events', 'Retail design'],
         kw=['Marketing']),
    dict(slug='business-consulting', h3='Business <em>consulting</em>',
         long="A seguito di una fase di business audit e review, supportiamo le aziende partner nel raggiungimento di obiettivi strategici ed operativi, offrendo servizi specialistici che migliorino l'operatività gestionale e soluzioni in grado di assicurare una crescita sostenibile di lungo termine.",
         subs=['Business counselling and mentoring', 'Coaching e formazione'], kw=['Format', 'Progetti Speciali']),
    dict(slug='data-analysis', h3='Data <em>analysis</em>',
         long="La raccolta ed interpretazione di insights è di notevole importanza strategica per costruire un percorso di marketing volto a migliorare la customer experience ed il rendimento aziendale. Crediamo nell’implementazione di azioni di marketing misurabili, che nascono da un'accurata analisi dei dati ed offrono performance quantificabili.",
         subs=['CRM', 'Data analytics']),
    dict(slug='social-media', h3='Social <em>media</em>', cats=['social']),
    dict(slug='campaign-management', h3='Campaign <em>management</em>', cats=['advertising']),
    dict(slug='csr-communication', h3='CSR <em>communication</em>',
         long='La Corporate Social Responsibility - responsabilità delle imprese per il loro impatto sulla società - è descritta nel Libro Verde della Commissione Europea come l’integrazione volontaria delle preoccupazioni sociali e ambientali delle imprese nelle loro operazioni commerciali. La comunicazione sulle attività di responsabilità sociale ha sempre più spazio all’interno delle imprese sia per ragioni di trasparenza sia in quanto opportunità per ottenere lustro sociale.',
         subs=['Brochure', 'Comunicati stampa', 'Eventi', 'Newsletter', 'Report aziendali']),
    dict(slug='digital-innovation', h3='Digital <em>innovation</em>',
         long="Consideriamo la digital innovation un'opportunità per generare new business, migliorare e trasformare l’esperienza di brand. Esplorando l’uso di medium non convenzionali, diamo forma a nuovi modi di comunicare e progettiamo tecnologie al servizio delle persone in grado di sorprendere e creare interazioni nuove e personalizzate.",
         subs=['Web development', 'SEM (Search Engine Marketing)', 'SEO (Search Engine Optimization)', 'Social media marketing', 'Marketing automation', 'Email marketing'],
         kw=['Web/Mobile Design']),
    dict(slug='website-development', h3='Website <em>development</em>', cats=['website']),
    dict(slug='web-app-development', h3='Web app <em>development</em>', cats=['ecommerce']),
    dict(slug='media-relations', h3='Media <em>relations</em>',
         long='Svolgiamo attività di ufficio stampa per ottenere uscite redazionali su riviste e giornali e per aumentare la visibilità del brand online e offline e stimolare la considerazione da parte di tutti gli stakeholder.',
         subs=['Ufficio stampa', 'Rassegna stampa', 'Media planning'], kw=['P.R. Eventi']),
]

CHI_SIAMO = dict(
    kicker="Un'idea può fare miracoli",
    claim='Nuovi modi di comunicare per emozionare e sorprendere.',
    motto='Think different, like Never Before.',
    metodo_big='Tutto quello che è marketing e comunicazione è il nostro lavoro, e ci piace farlo bene.',
    metodo=["Quello che invece ci riesce difficile, è spendere tante parole su noi stessi.",
            'Il modo migliore per parlarvi di noi è invitarvi a visitare la sezione Case Histories, perché quello che ci rappresenta davvero sono le nostre campagne.',
            'Il nostro metodo segue criteri teorici e operativi step by step per assicurare ai nostri clienti risultati concreti, feedback significativi in tempi brevi. Ci piace tutta la comunicazione capace di suscitare grandi effetti con un low budget.',
            'Il team è giovane e appassionato, composto da professionisti del marketing, dell’advertising, della pianificazione, del web e dei social media.'],
    vision='Capitalizzare il cambiamento, definendo nuove strategie comunicative in linea con i mutevoli scenari di mercato.',
    mission='Aiutare i clienti a costruire relazioni di marca che durino nel tempo, che siano parte della vita dei consumatori e che influenzino le loro scelte e la loro fedeltà.',
    qualita=['Abbiamo ottenuto la certificazione di qualità ISO 9001 nel dicembre 2011, a conferma e supporto di un processo di lavoro rigoroso, finalizzato al raggiungimento di output di eccellenza, per la totale soddisfazione del Cliente.',
             'Siamo delegati territoriali per Confindustria Bari e BAT, credendo fermamente che i network professionali e territoriali portano benefici e crescita culturale.'],
    jobs='Vuoi entrare nel team Never Before?',
)
