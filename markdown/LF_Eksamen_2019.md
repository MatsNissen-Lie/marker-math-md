# Løsningsforslag til eksamen i TIØ4505 AØO fordypningsemne, 2019

## Oppgave 1

- a) Dette problemet har dimensjon *N* i «decision variable space» fordi det har *N* variabler. Problemet har dimensjon 2 i «objective function space» fordi det har to objektiver (minimere produksjonskostnader og maksimere servicegrad).
- b) I  $\varepsilon$ -contraint-metoden beholder man én objektivfunksjon i målfunksjonen, mens de andre flyttes ned i restriksjonene, men begrenses av en  $\varepsilon$ -verdi. Det betyr at vi sitter igjen med et Single Objective Problem (SOP).
  - I vårt eksempel vi for eksempel minimere produksjonskostnadene, samtidig som en sikrer med en restriksjon at servicegraden er over en gitt  $\varepsilon$ -verdi. Ved å løse dette for flere  $\varepsilon$ -verdier, kan en få opp (deler av) Paretofronten.
  - En begrensning med vektet-sum-metoden i forhold til  $\varepsilon$ -contraint-metoden, er at den ikke vil finne løsninger i den konkave delen av Paretofronten ved minimering (og den konvekse delen ved maksimering).
- c) I den leksikografiske metoden er de ulike objektivene rangert etter viktighet. Da vil en først optimere mhp. den viktigste objektivfunksjonen. I neste iterasjon, vil en optimere mhp. den neste viktigste, men samtidig legge til en restriksjon som sier at den første objektfunksjonen skal ikke ha en dårligere verdi enn man fant i forrige iterasjon, osv. (Se også side 9 i Jaimes et al., 2009 for enda mer detaljer på gjennomføringen av dette).
- d) Her var oppgaven noe uheldig formulert som et «lengste vei-problem», som indikerer at en ønsker å maksimere  $z_1$ . Det fremgår likevel av informasjonen i oppgaven ellers at en her ønsker å minimere  $z_1$ .
  - Den foreslåtte metoden er uheldig å bruke av to grunner: 1) Her er det en kombinasjon av objektiv som skal minimeres  $(z_1)$  og maksimeres  $(z_2)$ . Skal en bruke vektet-sum-metoden som angitt, må en i så fall omdefinere f.eks.  $z_2'=1-z_2$ , slik at en ønsker å minimerer også denne, slik at  $z=\alpha z_1+(1-\alpha)z_2'$ . Men selv om en gjør dette, vil imidlertid fortsatt den foreslåtte metoden være uheldig av følgende grunn: 2) De to objektivene har så store forskjeller i verdier at dette uansett vil være en veldig dårlig metode. F.eks. dersom en velger  $\alpha=0.25$ , som angir en større vekt på objektiv 2 enn objektiv 1, vil likevel objektiv 1 fullstendig dominere over objektiv 2 pga. de mye høyere verdiene. En kan imidlertid vekte de to objektivene slik at de blir i størrelsesorden like, og da kan en gjerne bruke den foreslåtte vektet-sum-metoden (selvsagt med den begrensning diskutert i oppgave 1 b)).

## Oppgave 2 (20 %)

a) Bruker  $x_i$ , i=1,2, som beslutningsvariabel for innkjøp av råolje i. Men de gitte opplysningene blir optimeringsmodellen

|            | $min 10x_1 + 15x_2$    | råvarekostnad          |
|------------|------------------------|------------------------|
| subject to |                        |                        |
|            | $x_1 + x_2 \le 15$     | prosesseringskapasitet |
|            | $6x_1 + 3x_2 \ge 48$   | etterspørsel produkt A |
|            | $1.6x_1 + 4x_2 \ge 32$ | etterspørsel produkt B |
|            | $x_1, x_2 \ge 0$       | ikke-negativitet       |

![](./LF_Eksamen_2019_assets/LF_Eksamen_2019_001__page_1_Figure_0.jpeg)

Vi kan løse problemet grafisk. Løsningsrommet det gråe arealet i figuren over, målfunksjonen er den stiplete linjen. Vi ser også den optimale løsningen er i skjæringspunktet av de to etterspørselsbeskrankningene, slik at vi kan finne den optimale løsningen analytisk. Uansett metode, den optimale løsningen er gitt som  $x_1=5, x_2=6$ . Ettersom markeder er imperfekte med vesentlig friksjon, vil komplementære egenskaper mellom objekter ikke bli effektivt priset via ordinære auksjoner og selger går altså glipp av en del av verdien. Ekte kombinatoriske auksjoner legger til rette for at selger skal kunne nyte godt også av verdien som ligger i de komplementære egenskapene. Dersom selger er det offentlige, vil det også kunne være et poeng at prising av komplementære egenskaper vil føre til allokering som i større grad reflekterer kjøpernes evne til å utnytte ressursene effektiv.

b) Innfører *Cap* som usikker prosesseringskapasitet og omformulerer modellen med én probabilistisk beskranking:

$$\min 10x_1 + 15x_2$$
subject to

$$Pr(x_1 + x_2 \leq Cap) \geq 0.9$$

$$6x_1 + 3x_2 \geq 48$$

$$1,6x_1 + 4x_2 \geq 32$$

$$x_1,x_2 \geq 0$$
råvarekostnad

individuell prob. beskrankning

etterspørsel produkt A

etterspørsel produkt B

ikke-negativitet

Siden usikkerheten er kun på høyresiden av beskrankningen, kan vi erstatte den probabilistiske beskrankningen med en ekvivalent deterministisk beskrankning der vi erstatter *Cap* med tilsvarende persentil.

| $min 10x_1 + 15x_2$    | råvarekostnad          |
|------------------------|------------------------|
| subject to             |                        |
| $x_1 + x_2 \le 12.4$   | prosesseringskapasitet |
| $6x_1 + 3x_2 \ge 48$   | etterspørsel produkt A |
| $1,6x_1 + 4x_2 \ge 32$ | etterspørsel produkt B |

$$x_1, x_2 \ge 0$$

ikke-negativitet

Beskrankningen for prosesseringskapasitet er ikke-bindende i den optimale løsningen (se svar på oppgave a). I tillegg er slakket større enn endringen i høyresiden (vi bruker 11 fat råolje). Den optimale løsningen forblir derfor uendret.

c) Bruker  $D_i$ , i = A, B, for å beskrive usikker etterspørsel. Problemet med felles probabilistisk beskrankning kan så formuleres:

$$\min 10x_1 + 15x_2 \qquad \qquad \text{råvarekostnad}$$
subject to
$$x_1 + x_2 \leq 15 \qquad \qquad \text{prosesseringskapasitet}$$
$$\Pr\begin{pmatrix}6x_1 + 3x_2 \geq D_A \\ 1.6x_1 + 4x_2 \geq D_B\end{pmatrix} \geq 0.9 \qquad \qquad \text{felles prob. beskrankning}$$
$$x_1, x_2 \geq 0 \qquad \qquad \text{ikke-negativitet}$$

Den optimale løsningen må tilfredsstille scenarioene 1 og 3 for å sikre at etterspørselen kan tilfredsstilles med sannsynlighet på minst 90 %. Vi kan derfor erstatte problemet med felles probabilistisk beskrankning med følgende deterministiske formulering

$$\min 10x_1 + 15x_2 \qquad \qquad \text{råvarekostnad}$$
 subject to 
$$x_1 + x_2 \leq 15 \qquad \qquad \text{prosesseringskapasitet} \\ 6x_1 + 3x_2 \geq 51 \qquad \qquad \text{etterspørsel produkt A} \\ 1.6x_1 + 4x_2 \geq 32 \qquad \qquad \text{etterspørsel produkt B} \\ x_1, x_2 \geq 0 \qquad \qquad \text{ikke-negativitet}$$

Optimal løsning for dette problemet kan bestemmes grafisk eller ved å beregne skjæringspunktet for de 2 etterspørselsbeskrankningene. Optimal løsning er gitt som  $x_1 = 5.625$  og  $x_2 = 5.75$ .

Legg merke til at vi også har en mulig løsning der alle 3 scenarier tilfredsstilles, men denne løsningen vil være dårligere enn løsningen som kun tilfredsstiller scenarioene 1 og 3.

d) Vi kan bruke binære indikatorvariabler i kombinasjon med stor M for å finne ut av om en beskrankning brytes i et gitt scenario eller ikke. Totalt må  $\lceil (1-\alpha) \cdot |S| \rceil$  beskrankninger være oppfylte for at den probabilistiske beskrankningen skal holde.

La  $z^s$  være den binære indikatorvariabelen som er 1 dersom knapsack-beskrankningen holder i scenario s og 0 ellers. I tillegg må vi har en beskrankning, som sikrer at tilstrekkelig mange knapsack-beskrankningene er oppfylte:

$$\sum_{i} w_i^s x_i \leq C + (1-z^s) \cdot M, \quad s \in S$$
knapsack-beskrankning
$$\sum_{s} z^s \geq (1-\alpha) \cdot |S|$$
sikre sannsynlighet  $1-\alpha$ 

## Oppgave 3

- a) The answer is no. The reason is that what-if use of the model would (as always) disregard possible decisions containing options (flexibility) to face the uncertainty in markup.
- b) In this case, the what-if use is OK as we are asking what we would be doing if the markup was different, but still known, when the model is used.

## Oppgave 4

For sampling: Very easy to use. If the resulting problem is easy to solve with the number of samples you need for high enough quality of solutions (so we talk about stability analysis) this is smart as it is quick and simple. Also positive that the approach converges in the limit (as the number of scenarios goes to infinity)

Against sampling: You may not have something to sample from. Sampling in very high dimensions is actually very hard, except in the independent case. But the main point is: For large problems (whatever way they are large), it is important to have few scenarios for a given requirement on quality OR as much quality as possible for a given number of scenarios. And with few scenarios sampling has few good properties, whereas other approaches might be fit to the problem – and research shows that this is indeed the case.

Point: Many answers can be accepted here, but they must understand the weakness of small sample sized relative to the weakness of the resulting model to solve.

## Oppgave 5

Sentrale førstemannsfordeler er nettverkseffekter og akkumulering av vurderingsinformasjon. Merkevarelojalitet og byttekostnader bidrar også, men er mer generelle effekter og typisk ikke like viktige. Punktene under forklarer de to mest sentrale mekanismene.

- Nettverkseffekter, eller nettverkseksternaliteter, fører til at verdien av et gode avhenger av hvor mange andre som konsumerer samme gode. I delingsøkonomien er det positive nettverkseffekter som går mellom kjøper- og tilbyderside. For de som tilbyr goder via f.eks. mobilapper er det en fordel med mange potensielle kjøpere. For de som ønsker å låne eller leie goder er det en fordel med mange potensielle tilbydere. Når en aktør først er etablert innenfor en nisje, og har opparbeidet seg en vesentlig masse på tilbuds- og kjøpersiden, blir det vanskelig for nye aktører å bygge seg opp siden de må konkurrere med den etablerte aktøren som allerede har attraktive kjøper- og tilbydersider.
- Vurderingsinformasjonen som bygges opp ved at brukere på etterspørsels- og tilbudssiden legger inn vurderinger bidrar til å redusere graden av asymmetrisk informasjon. I mange tilfeller vil brukere være bekymret for at motparten i en eventuell transaksjon er uhederlig eller ikke innstilt på å levere god kvalitet. I teorien kan markeder for erfaringsgoder bli dominert av dårlig kvalitet ettersom betalingsvilligheten ikke blir høy nok til å gi leverandører betalt for god kvalitet. Vurderingene motvirker denne effekten, skaper høyere tillit til tjenesten og gir dermed flere brukere og flere transaksjoner. Men verdien av vurderingene er klart størst når det er så mange at det blir meningsfylt å aggregere til gjennomsnitt som fanger opp tendenser over tid. Derfor vil

akkumulering av vurderingsinformasjon bidra til konkurransefortrinn for aktøren som kommer først i gang.

Bekymringen i det samfunnsøkonomiske perspektivet er relatert til det potensielle dødvektstapet som vil oppstå i markeder der én eller noen svært få aktører blir dominerende.

Førstemannsfordelene kan gi noe i nærheten av monopolsituasjoner i enkelte nisjer. Det gir grunnlag for at plattformene kan ta svært høye marginer på tjenester med lave variable kostnader og prisene blir betydelig over marginalkostnadene. Dermed blir ikke samfunnsøkonomisk overskudd maksimert. Denne effekten vil naturligvis bli moderert ved at det typisk finnes alternative kanaler for potensielle kjøpere av de aktuelle godene.

## Oppgave 6

a) Resultatet om «revenue equivalence» i Klemperer (1999) som også er tatt inn i forelesningsnotatet gjelder for vilkårlige mekanismer og uavhengig av om bydere har gitt, privat verdsetting eller et verdisignal gitt risikonøytralitet. I «private value model» har hver deltaker en verdi som deltakeren kjenner, men som er ukjent for andre. Mekanismene må ha samme startpunkt, for eksempel ved at forventet verdi for deltaker med laveste mulige verdi, er null, og må gi objektet til deltaker med høyeste verdi i likevekt. I førsteprisauksjoner vil det da være optimalt å by basert på forventningen av nest høyeste verdi betinget av at egen verdi er høyest. Forventet nest høyeste verdi blir lik forventningen til nest høyeste verdi for deltaker med høyest verdi slik at forventet pris i andreprisauksjoner blir den samme. I «common value» vil oppfatningen av verdi være relatert til eget verdisignal, men slik at den avhenger i prinsippet av verdisignalene til de andre. Så lenge verdisignalene er uavhengige vil imidlertid avsløring av verdisignaler forventningsmessig bidra like mye opp som ned. Og tilsvarende bevis som for «private value» leder til uavhengighet av mekanisme.

I «affiliated value» er verdisignaler korrelert i svært streng forstand slik at korrelasjonen gjenspeiles i tettheten i alle punkter i (den simultane) fordelingen. Avsløring av verdisignaler innebærer da at bydere oppdaterer sin oppfatning av verdi for objektet. Deltaker med nest høyeste signal vil i utgangspunktet betinge som om eget signal er høyest og vil altså opptre som om verdisignal for andre ikke er høyere enn eget. Det igjen gir en betinging for deltaker med faktisk nest høyeste signal der forventet verdisignal for nest høyeste signal, og lavere signaler, gitt at eget signal er høyest, tenderer til å bli underestimert. Ved avsløring av verdisignaler for deltakere med lavere signaler, vil altså deltaker med nest høyeste signal tendere til å oppjustere egen oppfatning av verdi. Det igjen gir høyere forventet verdi for selger gitt en auksjonsform der verdisignaler avsløres underveis, slik at for eksempel engelsk auksjon blir mer attraktiv for selger enn hollandsk eller lukkede første- eller andreprisauksjoner.

- b) Crampton (1998), som er i pensum argumenterer for flere fordeler med åpne, iterative auksjoner:
  - Tryggere estimater på verdi gjennom at andre vurderinger avsløres gir mindre sannsynlighet for winner's curse og dermed mer aggressiv budgivning.
  - Prosessen kan bidra til å relaksere budsjettbegrensninger. For eksempel kan et styre ha satt en grense basert på en vurdering av at ledelsen vil ha tendens til å overdrive verdi. Når andre selskapers verdsetting avsløres, kan styret endre syn.

- Den åpne prosessen som gjør at bydere vet hva de vil måtte betale gitt at de vinner, legger til rette for at de kan utnytte budsjetter fullt ut.
- Visse former for juks kan unngås: Falske bud i lukket andrepris; budgiver får informasjon om høyeste bud i lukket førstepris og legger inn et bud rett over.

(Det kan også være ulemper relatert til muligheten for bydere å danne koalisjoner.)

- c) I fasen med prisklokker er det en simultan avsløring av verdiinformasjon for de ulike objektene samtidig om kompleksiteten i en ekte kombinatorisk auksjon unngås. Den ekte kombinatoriske auksjonen i etterkant vil fange opp komplementære verdier, men vil være mye enklere ettersom mange bydere er ute, og en svært stor andel av de budene som var mulige i utgangspunktet for gjenværende bydere er blitt utelukket i den første fasen.
- d) Hensikten er å legge til rette for avsløring av verdiinformasjon. Andreprisprinsippet legger til retter for at det er optimalt å by opp til egen verdsetting og slik avsløre troverdig verdiinformasjon via bud. Aktivitetsregelen er laget med sikte på å unngå strategisk adferd der bydere bevisst holder igjen bud tidlig i auksjonen med sikte på å ikke avsløre verdiinformasjon for så å prøve å «kuppe» mot slutten. Varianten kalt «Vickrey-nearest-core» eliminerer en svakhet med det andreprisprinsippet som ligger i Vickrey-Clarke-Groves, VCG. I VCG skal vinner betale alternativkostnaden for egen seier. Men når hver vinner betaler basert på verdi for selger uten vinnerens deltakelse, vil summen av verdier for objekter kunne havne under bud fra andre på kombinasjoner. «Vickrey-nearest-core» er priskombinasjonen som ligger nærmest VCG-priser i euklidsk distanse, men samtidig innenfor mengden avgrenset av vinnende bud ovenfra og tapende bud nedenfra.