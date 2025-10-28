#### Oppgave 1, Multikriterie, vekt: 10 %

a) A, B, D, H, J, K, M

b) A, H, M

c) A er optimal når w\_1 \in [5/7, 1] og w\_2 \in [0, 2/7] H er optimal når w\_1 \in [3/8, 5/7] og w\_2 \in [2/7, 5/8] M er optimal når w\_1 \in [1, 3/8] og w\_2 \in [5/8, 1] Alltig gitt at w 1 + w 2 = 1 selvsagt

d) Gitt at vi starter på 10 får vi: M, J, H, B

#### Oppgave 2, Simulering, vekt: 10 %

1. Simuleringsklokka

I diskret hendelsessimulering endres tilstanden til systemet som følge av at det skjer en hendelse. Når simuleringsklokka oppdateres med hendelsesbaserte tidsinkrement, flyttes klokka til tidspunktet for neste hendelse, mens om faste tidsinkrement benyttes, inkrementeres klokka med en liten enhet i hvert steg. Hvis man benytter hendelsesbaserte tidsinkrement vil man oppdatere tilstanden ved hvert tidsinkrement basert på hendelsen som skjedde ved inkrementet. Hvis man benytter faste tidsinkrement vil man oppdatere tilstanden basert på alle hendelser som har skjedd siden forrige tidspunkt.

2. Generering av tilfeldige tilfeldige observasjoner fra en sannsynlighetsfordeling:

Beskrivelse av akseptanse-avslag-metoden (kopi fra slides)

Metoden baserer seg kun på en tetthetsfunksjon f (x), som er definert over en endelig intervall [a, b] og er kontinuerlig. Vi definerer L som den største verdien til f (x). L =  $\max\{f(x) \mid a \le x \le b\}$ 

Metoden består av tre steg:

- 1. Generer et uniformt tilfeldig tall X i intervallet [a, b]
- 2. Generer et uniformt tilfeldig tall r i intervallet [0, L]
- 3. Hvis  $r \le f(X)$ , aksepter X, ellers avslå X og gå tilbake til 1
- 3. Simulering for å evaluere løsninger fra en optimeringsmodell

Se slide nr 39 – 43 fra forelesningsnotatene.

### Oppgave 3, Usikkerhet, vekt: 15 %

- a) Dette innebærer at for alle x som tilfredsstiller førstestegsbetingelsene og for alle matriser T(s),  $s \in S$ , så har Q(x,s) minst en tillatt løsning.
- b) I og med relatively complete recourse trenger vi ikke tillathetskutt (feasibility cuts) i L-shaped. Det vi da gjør er å bytte ut problemet i oppgaven med Max  $cx + \theta$  der at  $Ax = b, x \geq 0$ ,  $\theta \leq Q(x)$ . Men siden den nye ulikheten er så komplisert stryker vi den og «håper på det beste». Vi løser resten og får en  $\hat{x}$  og en  $\hat{\theta}$ . Vi regner ut  $Q(\hat{x})$ . I første runden er selvsagt  $\hat{\theta} > Q(\hat{x})$  da det ikke er noen skranker på  $\theta$  og som derfor stikker av til uendelig. Vi må da skjære (kutte) bort denne kombinasjonen av x og  $\theta$ : La  $\pi(x,s)$  være optimal dualløsning til Q(x,s). Vi har da

$$\theta \le Q(x) = \sum_{s \in S} p(s)(b - T(s)x)\pi(x, s) \le \sum_{s \in S} p(s)(b - T(s)x)\pi(\hat{x}, s) = vx + w$$

fordi  $\pi(\hat{x},s)$  er tillatt men ikke nødvendigvis optimal i et minimeringsproblem (som vi akkurat har løst). Vi legger til denne skranken i masterproblemet og løser igjen. Vi stopper når  $\hat{\theta} \leq Q(\hat{x})$ .

c) Her kan alle logiske svar godtas. Det viktigste er at fra én LP til den neste vil bare høyresiden endre seg. Så varm-start er naturlig. Om man bruker primalen eller dualen avhenger av struktur og det vi jo lite om. Om man har veldig mange scenarier kan man også parallellisere, rett og slett ved å fordele LP-ene (med varmstart) på de ulike prosessorene. Her finnes det også mer avanserte svar basert på spørsmålet: Nå har jeg løst en LP, hvilken bør jeg løse nå? Men jeg forventer ikke svar i den retningen.

Kommentar: Også her var det minimering i forelesningene, så igjen vil de som husker men ikke forstår lett snu rundt på ulikheter. Det skal altså ikke diskuteres *feasibility cuts*.

# Oppgave 4, Grenser, vekt: 10 %

Her er den viktigste observasjonen at optimalverdien i et maksimeringsproblem er en konkav funksjon av høyresiden. I forelesningene viste vi at et minimeringsproblem er konvekst i :

- a. Vi ender opp med en øvre skranke Jensens ulikhet
- b. Vi ender opp med en nedre skranke Edmundson og Madansky. Vektene 1/ og ½ kommer fra at fordelingen er symmetrisk.
- c. Dette blir en gjentatt bruk av Edmundson og Madansky-skranken. Vektene blir 1/20 i hvert av de to endepunktene, og 1/10 i hvert av de ni andre.

### Oppgave 5, Sekvensielle beslutninger, vekt: 15 %

The state of the system depends on where the technician is and whether or not each
of the customers has a failure. Denote L<sub>t</sub> ∈ I = {1,...,n} as the location of the
technician and F<sub>it</sub> as a binary (state) variable indicating whether or not customer i
has a failure (in which case we put F<sub>it</sub> = 1) in period t. Then the state of the system
will

$$S_t = (L_t, F_{1t}, \dots, F_{nt})$$

The decision is simply which position to go to i.e.

$$x_t \in \mathcal{I}$$

and the statespace of the exogenous information in a given period  $\Omega_t$  corresponds to the possible realizations of either failure or not failure at each customer i.e. an n-dimensional binary vector:
$$\Omega_t = \mathbb{B}^n$$

2. The direct cost of making a decision x<sub>t</sub> when in state S<sub>t</sub> corresponds to the traveling cost from i = L<sub>t</sub> to j = x<sub>t</sub> (which is a customer). If the customer j has a failure (i.e. when F<sub>jt</sub> = 1) then a payment of r<sub>i</sub> is achieved. Thus the direct cost of

$$C_t(S_t, x_t) = d_{ij} - F_{jt}r_j$$

Note that if customer j has no failure, then the technician will not travel to customer j, as it has a strictly positive cost, and all customers can be reached regardless of where the technician is positioned.

3. The value recursion is given directly in the slides from the lectures as:

$$V_{t}\left(S_{t}\right) = \min_{x_{t} \in \mathcal{X}_{t}} \left(C_{t}\left(S_{t}, x_{t}\right) + \gamma \sum_{\omega \in \Omega_{t+1}} \mathbb{P}\left(W_{t+1} = \omega\right) V_{t+1}\left(S_{t+1} \middle| S_{t}, x_{t}, \omega\right)\right)$$

where you may put in  $X_t = \mathcal{I}$ ,  $S_t = (L_t, F_{1t}, \dots, F_{nt})$ ,  $\Omega_{t+1} = \mathbb{B}^n$ , and  $C_t(S_t, x_t) = d_{L_t j} - F_{jt} r_j$ . We have not directly specified the discount factor and it is fine to let  $\gamma = 1$ . The probability for an outcome  $(\omega_1, \dots, \omega_n)$  where  $\omega_i = 0$  if no failure at customer i and  $\omega_i = 1$  if there is a failure, will then be

$$\mathbb{P}^{p}(W_{t+1} = \omega) = \prod_{i:\omega_{i}=0}(1 - p_{i}) \prod_{i:\omega_{i}=1}p_{i}$$

Note that it is not the intention that the post decision state should be found nor the more notational heavy machinery for the approximate dynamic programming. However, if these are found it is ok.

# Oppgave 6, Airbnb, vekt: 10 %

a) I forhold til den tradisjonelle prosessen med annonsering av rom til leie, gir Airbnb mye lavere annonseringskostnader i.f.t. reelt publikum for utleiere og lavere søkekostnader for potensielle gjester. Dermed blir det attraktivt for mange flere å leie ut eiendom. Slik skapes verdier ved at ledige eiendomsressurser kommer på markedet, og selskapet kan ta en margin på denne meglertjenesten. Tjenesten gir også tilgang til relativt effektive og sikre betalingstjenester, brukervurderinger og id-verifisering. Dette bidrar til å redusere asymmetrisk informasjon som kan gi markedssvikt og hemme omsetning. Forsikring reduserer risiko for utleiere, og meldingstjenesten gir en effektiv kanal for nødvendig kommunikasjon mellom leietaker og utleier. De nevnte mekanismene skaper verdi fordi

ny teknologi utnyttes til å effektivisere et marked. Airbnb høster i tillegg fordeler av at brukere omgår eller bryter etablert lovverk. For eksempel kan det være strengere krav til brannsikkerhet og hygiene i hoteller, pensjonater etc. som utleiere via Airbnb ikke blir omfattet av, og det er nok mange tilfeller av skatteunndragelse som bidrar til at utleiere oppfatter virksomheten som økonomisk attraktiv. Slik drar Airbnb fordel av andres lovbrudd og/eller av imperfeksjoner i offentlig regulering. Nettverkseffekten som oppstår fordi tjenesten er mer attraktiv for potensielle gjester desto flere utleiere som er på den, og fordi den er mer attraktiv for utleiere desto flere brukere som er på den, vil bidra til å gjøre det vanskelig for andre å etablere seg med tilsvarende tjeneste. Det kan igjen gjøre at Airbnb kan ta ganske høye marginer.

b) Tjenestene som tilbys via Airbnb er relativt heterogene. Eierne har mye bedre informasjon om kvalitetene deres eiendom tilbyr enn det Airbnb har. Samtidig vil selskapet ha mye bedre informasjon om hvordan etterspørselen i området varierer. Ved å formidle slik informasjon via anbefalinger, og samtidig la eier ta endelig beslutning, kan det være en tendens til at priser blir satt basert på en samlet vurdering av eiendommens særegenheter og den generelle etterspørselen. Det kan tenkes at det gir en effektiv prising. Samtidig reflekterer nok valget at mange eiere vil ha et sterkt ønske om å få påvirke pris for det de skal leie ut.

## Oppgave 7, Auksjoner, vekt: 15 %

- a) I en mange tilfeller vil en del av de separate objektene som skal selges, være nært perfekte substitutter. For eksempel gjelder det ulike deler av et frekvensbånd i en gitt region. Ved å legge opp til at det bys antall enheter av frekvensbånd i stedet for de spesifikke delbåndene, reduseres kompleksiteten i auksjonen dramatisk. I etterfølgende runder kan det organiseres prosesser slik at gjenværende komplementære egenskaper blir tatt hensyn til. Når det gjelder frekvensbånd kan en slik prosess sikre at hver byder som har vunnet mer enn én enhet frekvensbånd får et sammenhengende delbånd, hvilket er teknisk fordelaktig. Slik kan objekter til en vesentlig grad aggregeres til produkter uten at komplementære sammenhenger blir borte fra budprosessen, og det blir lettere både for selger og bydere å ha oversikt og forståelse for prosessen. Samtidig blir det mye enklere å løse WDP.
- b) Klokkefasen legger opp til en iterativ prosess der det avsløres prisinformasjon. Det bidrar til "price discovery" som igjen kan bidra til høyere pris for selger, jfr. f.eks. "affiliated values model". Samtidig danner prisnivået for klokkene utgangspunktet for etterfølgende kombinatorisk auksjoner. Den kombinatoriske fasen forenkles siden det nå er etablert et prisnivå som avgrenser potensielle bud, en del bydere kan ha falt fra slik at den kombinatoriske auksjonen blir mye mindre komplisert enn dersom det skulle gjennomføres en iterativ kombinatorisk auksjonsprosess uten en klokkefase først.
- c) Hensikten med aktivitetsregelen er å sikre at prisinformasjon avsløres som tenkt. Uten en slik regel kan bydere velge å holde tilbake bud med sikte på å "kuppe" auksjonen helt mot slutten. Det vil ødelegge for "price discovery". Ideelt bør aktivitetsregelen gi insentiver til å avsløre mye verdiinformasjon underveis samtidig som den åpner for at aktørene kan bruke avslørt informasjon til å oppdatere egne verdiestimater

- d) Andreprisprinsippet skal gi insentiver til å by egen verdsetting. Det vil gi den mest åpne avsløringen av prisinformasjon. Slik kan auksjonsprosessen også bidra til at aktørene fokuserer på å utnytte informasjon til å oppdatere verdiestimater heller enn å ha fokus på strategisk adferd.
- e) Kombinasjonen av bud 4 og 5 gir 300. Ingen annen, mulig kombinasjon av bud gir lik eller høyere verdi. Det er altså budene 4 og 5 som blir vinnere. Vickrey-priser finnes ved å ta hvert vinnerbud og så trekke fra forskjellen i verdi for selger når vi starter med vinnerkombinasjonen og så sammenligner med den hypotetiske vinnerkombinasjonen uten det aktuelle vinnerbudet. Her går kombinasjonen av vinnerbud fra 300 til 250 for begge vinnende bydere, og begge skal betale 50 mindre enn budet sitt. Vickrey-prisene er dermed 100 for både A og B, som betales av byder 4 og 5. Figuren under illustrerer Vickrey-prisene. I figuren er også Vickrey-nearest-core illustrert. Core, det vil si kjernen, er avgrenset nedenfra av bud som ikke vinner og ovenfra av vinnende bud. Den delen av kjernen som ikke er påvirket av vinnende bud, og som derfor sikrer insentiver til å by egen verdsetting er den tykke linjen. Vickrey-nearest-core velger ut det punktet som ligger nærmest Vickrey-prisene i euklidsk distanse. I det punktet vil normalen gå gjennom Vickrey-prisene. Her er det enkelt å finne priskombinasjonen ettersom budene er symmetrisk slik at punktet må ligge midt på linjen som illustrerer budet på 230 for kombinasjonen. Prisene er der 115 for både A og B.

## Oppgave 8, Robusthet: 15 %

a) Formuler og løs Karis problem som et robust optimeringsproblem. Bruk tilnærmingen til Soyster (1973) med kolonnevis usikkerhet. Husk å forklare modellen.Soyster (1973) formulerer det f
ølgende robuste optimeringsproblemet

$$\max \mathbf{c^T} \mathbf{x}$$

s.t.

$$\sum_{j=1}^{n} \mathbf{A_j} x_j \le \mathbf{b} \quad j = 1 \dots n, \mathbf{A_j} \in K_j$$

$$\mathbf{x} > 0$$

Dette problemet kan reformuleres som

$$\max c^{T} x$$

s.t.

$$\sum_{j=1}^{n} \bar{A}_{j}x_{j} \le b$$

$$x > 0$$

hvor 
$$\bar{a}_{ij} = \sup_{\mathbf{A}_i \in K_i} (A_{ij}).$$

Med denne reformuleringen kan Karis problem formuleres som
$$\max 7x_1 + 10x_2 + 4$$
,  $5x_3 + 11x_4 + 15x_5 + 6x_6 + 12x_7$ 

s.t.

$$3x_1 + 4x_2 + 2x_3 + 6x_4 + 7x_5 + 3x_6 + 5x_7 \le 15$$
  
 $x_i \in \{0, 1\} \quad i = 1...7$ 

Problemet er en knapsack der vi ønsker å maksimere nytten, mens be-skrankningen utgjør vektbeskraningen for ryggsekken. Beslutningsvariab-lene er binære.Vi finner øvre grense for problemet ved sette  $x_1 = x_2 = x_3 = x_7 = 1, x_6 = \frac{1}{3}$ . Total vekt V = 15, samlet nytte N = 35, 5. Vi forgrener  $x_6$  og får 2 nye lø sninger:

$$x_{6} = 0:$$
  $x_{1} = x_{2} = x_{3} = x_{7} = 1, x_{5} = \frac{1}{7}, V = 15, N = 35,357$   
$$x_{6} = 1:$$
  $x_{1} = x_{2} = x_{6} = x_{7} = 1, V = 15, N = 35$ 

Løsningen for  $x_6 = 1$  er mulig for det opprinnelige problemet og optimal, siden vi ikke kan få en bedre løsning fra forgreningstreet for  $x_6 = 0$ .b) Hvor mye «beskyttelse» mot økning i vekt ligger i den optimale løsningen til det robuste optimeringsproblemet?For intervall-usikkerhet kan Soysters opprinnelige problem også formuleres som
$$\max \mathbf{c^T} \mathbf{x}$$

s.t.
$$\sum_{j} a_{ij} x_j + \sum_{j \in J_i} \hat{a}_{ij} y_j \le b_i \quad i = 1 \dots, m$$

$$-y_j \le x_j \le y_j \quad j = 1 \dots n$$

$$\mathbf{l} \le \mathbf{x} \le \mathbf{u}$$

$$\mathbf{y} \le \mathbf{0}$$

Summen  $\sum_{j \in J_i} \hat{a}_{ij} |x_{ij}^*|$  er beskyttelsen mot uønsket vektøkning i de utvalgte gjenstandene. Den optimale løsningen er beskyttet mot en økning på 4 kg.Kari har hørt at robust optimering leverer svært robuste, men også svært konservative løsninger. Hun ber deg om å bruke stokastisk programmering, siden dette skal gi gode fleksible løsninger.c) Formuler et Karis problem to-stegs stokastisk programmeringsproblem. I første steget skal sekken pakkes slik at forventet vekt ikke overstiger sekkens kapasitet, mens du i andre steget har anledning til å fjerne gjenstander fra sekken, dersom det skulle vise seg at sekken er for tung (det skal ikke være mulig å ta med nye gjenstander). Bruk scenarionotasjon. Husk å føre opp nødvendige antakelser og forklar modellen.

For å kunne formulere problemet som to-stegs stokastisk programemringsproblem må vi ha en fordelingsfunksjon den stokastiske parameteren, dvs. vekt. Vi antar at vekten er uniform fordelt i intervallet angitt i Tabell 1.

Problemet kan da formuleres som

$$\max \sum_{i \in \{1\dots 7\}} c_i x_i - \sum_{s \in \mathcal{S}} \sum_{i \in \{1\dots 7\}} p^s y_i^s$$

s.t.

$$2x_{1} + 3x_{2} + 1.5x_{3} + 4x_{4} + 5.5x_{5} + 2x_{6} + 4x_{7} \le 15$$
 (1)

$$\sum_{i \in \{1...7\}} w_i^s x_i - \sum_{i \in \{1...7\}} w_i^s y_i^s \le 15 \quad s \in \mathcal{S}$$
(2)
$$y_i^s \le x_i \quad i = 1...7, s \in \mathcal{S}$$
(3)

$$y_{i}^{s} \leq x_{i} \quad i = 1...7, s \in S$$

$$(3)$$

 $x_{i} \in \{0, 1\}$   $i = 1...7$  (4)

$$y_{i}^{s} \in \{0, 1\} \quad i = 1...7, s \in S$$
(5)

Beskrankning (1) sikrer at vi i første steg ikke pakker mer enn forventet vekt. Beskrankning (2) sørger for at vi kan fjerne gjenstander, dersom total realisert vekt  $w_i^s$  overstiger tilgjengelig kapasitet. Beskrankning (3) sikrer at vi bare kan fjerne gjenstander som ble pakket i første steg. Beskrankningne (4) og (5) er binærkravene til beslutningsvariablene.