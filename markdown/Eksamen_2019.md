![](./Eksamen_2019_assets/fig1.jpeg)

Institutt for industriell økonomi og teknologiledelse

# Eksamensoppgave i TIØ4505 Anvendt økonomi og

| Faglig kontakt under eksamen:           | Kjetil Fagerholt                                                   |
|-----------------------------------------|--------------------------------------------------------------------|
| Tlf.:                                   | 97 56 84 97                                                        |
| Eksamensdato:                           | 02.12.2019                                                         |
| Eksamenstid (fra-til):                  | 09.00 – 13.00                                                      |
| Hjelpemiddelkode/Tillatte hjelpemidler: | C / godkjent kalkulator og K. Rottmann: «Matematisk formelsamling» |
| Annen informasjon:                      |                                                                    |
| Målform/språk:                          | Bokmål (engelsk)                                                   |
| Antall sider (uten forside):            | 4                                                                  |
| Antall sider vedlegg:                   | 0                                                                  |

Informasjon om trykking av eksamensoppgave

| Originalen er:         |   |
|------------------------|---|
| 1-sidig                | □ |
| 2-sidig                | ☒ |
| sort/hvit              | □ |
| farger                 | □ |
| skal ha flervalgskjema | □ |

Kontrollert av:*Irene Entsen*
  
*21/11-19*![](./Eksamen_2019_assets/fig2.jpeg)

## Oppgave 1 (20 %)

En bedrift har et planleggingsproblem hvor de ønsker å minimere produksjonskostnader samtidig som de vil maksimere servicegrad til dine kunder. Problemet skal tilfredsstille følgende sett av restriksjoner:

$$\sum_{i=1}^{N} A_{ij} x_i = B_j, \quad j = 1, 2, ..., M$$

Anta videre at du ønsker å løse dette problemet som et multi-objektiv optimeringsproblem (MOP).

- a) Hvor mange dimensjoner har dette problemet i henholdsvis «decision variable space» og «objective function space»?
- b) Forklar hvordan du kunne brukt  $\varepsilon$ -contraint-metoden å få frem (deler av) Paretofronten for problemet over. Nevn en vesentlig fordel med denne metoden sammenlignet med vektet-summetoden?
- c) Forklar kort hvordan den leksikografiske metoden for et generelt MOP fungerer.
- d) Du løser et lengste vei-problem mellom to punkter i et nettverk og finner en optimal løsning med objektfunksjonsverdi  $z_1 = 14267$ . Det er imidlertid en sannsynlighet koblet til hver bue i nettverket som angir sannsynligheten for at buen blir brutt (dvs. ikke kan benyttes). Når du løser dette problemet med å maksimere sannsynligheten for at den valgte stien ikke har en brutt bue får du objektfunksjonsverdien  $z_2 = 0.894$  (men denne har dessverre en veldig høy kostnad/lengde med  $z_1 = 20924$ ). En venn av deg foreslår derfor å løse dette som et bi-objektiv optimeringsproblem hvor du optimerer mhp.  $z = \alpha z_1 + (1 \alpha)z_2$ , og deretter løser dette for  $\alpha = 0, 0.25, 0.5, 0.75, 1$ . Diskutere hvorvidt dette er en god løsningsstrategi eller ikke (ikke samme grunner som evt. i oppgave b), og foreslå eventuelt en bedre måte å løse problemet på.

## Oppgave 2 (25 %)

Et raffineri planlegger sitt innkjøp av råolje for å kunne dekke etterspørselen etter anleggets 2 produkter. Begge av raffineriets produkter produseres simultant, dvs. et fat råolje prosesseres i flere produkter samtidig. Ett fat av råolje 1 kan prosesseres i 6 fat av produkt A og 1.6 fat av produkt B. Råolje 2 gir 3 fat av produkt A og 4 fat av produkt B.

Raffineriet må dekke en etterspørsel etter 48 fat av produkt A og 32 fat av produkt B. Den totale prosesseringskapasiteten er på 15 fat råolje. Ett fat råolje 1 koster 10, mens ett fat av råolje 2 koster 15. Raffineriet ønsker å minimere de totale råvarekostnadene.

- a) Formuler det deterministiske optimeringsproblemet. Hva er den optimale løsningen?
- b) Anta nå at prosesseringskapasiteten er usikker. Kapasiteten er uniform fordelt mellom 12 fat og 16 fat. Raffineriet ønsker at de innkjøpte råvarene med en sannsynlighet på 90% er innenfor den tilgjengelige kapasiteten.
  - Formuler optimeringsproblemet med én probabilistisk beskrankning (chance constraint). Angi

også en ekvivalent formulering uten probabilistisk beskrankning. Hvordan ser den den optimale løsningen nå ut?

c) Anta nå at det er etterspørselen som er usikker. Etterspørselen,  $D_i$ , etter produkt i er gitt ved den følgende diskrete fordelingen:

$$\Pr\begin{pmatrix} D_A = 48 \\ D_B = 32 \end{pmatrix} = 0.78,$$

$$\Pr\binom{D_A = 45}{D_B = 36} = 0.05,$$

$$\Pr\binom{D_A = 51}{D_B = 28} = 0.17.$$

Etterspørselen skal tilfredsstilles med en sannsynlighet på 90%. Formuler optimeringsproblemet med én felles probabilistisk beskrankning (joint chance constraint). Hva er den optimale løsningen?

d) Ta nå utgangspunkt i følgende optimeringsproblem med én individuell probabilistisk beskrankning:

$$\max ux$$

subject to

$$\Pr\left(\sum_{i} w_{i}(\xi) \cdot x_{i} \leq C\right) \geq 1 - \alpha,$$

$$x_{i} \in \{0,1\}.$$

Denne formuleringen kan tolkes som knapsack-problem, der gjenstandenes vekt,  $w_i(\xi)$ , er usikker og knapsackens kapasitet, C, ikke skal overskrides med sannsynlighet  $\alpha$ .

Diskuter bruken av teknikker fra (blandet) heltallsprogrammering for å omformulere den probabilistiske beskrankningen slik at problemet kan løses vha. Xpress. Skisser hvordan de nødvendige beskrankningene vil se ut. Anta at gjenstandenes vekt er gitt i form av *S* scenarier.

#### Oppgave 3 (15 %)

Assume you are a somewhat low-level manager responsible for producing some commodity for your firm. For decision-support, you have an optimization model where the company markup on your product is a deterministic parameter. By markup we mean that the product will be sold for your marginal production cost times the markup. In other words, the markup is a number like 1.45, implying a sales price 45% over marginal production costs. You are fully aware that sales depend on the price. Your planning process is as follows: By January 1, you make plans for February, March and April. By April 1, you make plans for May, June and July, and similarly for the next two quarters of the year. Therefore, plans are always ready one month before the quarter starts. This is needed, as some materials with long lead-times must be ordered.

- a) Today is December 2, and you are working on the plan for February, March and April, which needs to be finished by January 1. You have been told that the top management might change the markup from March 15, and that worries you, as it will invalidate the optimality of your production plan for the next quarter. Is it appropriate to use your decision-support model in what-if mode to investigate what plan you should make for the next period in light of this uncertainty? You have a fairly good idea of what are the possible changes in markup (including no change at all). Explain your answer. (It is the explanation, not the yes/no that is evaluated.)
- b) Now, disregard the issues in question a). As part of the top management activities of a potential change in markup, you are asked for information about how your production plans would change if the markup was changed. You are given five possible new values (including a non-change option). Is it appropriate to use your decision-support model in what-if mode to answer the top management? Explain your answer. (It is the explanation, not the yes/no that is evaluated.)

## Oppgave 4 (vekt 10 %)

The most common way to generate scenarios for stochastic programs is to sample. Argue for and against this approach relative to other more structured methods, such as property matching. The point here is to argue for and against sampling, not to make technical comparisons among alternative methods. Think about such as: When would you advise people to use sampling? Why? When should sampling not be used? Why not?

#### Oppgave 5 (10 %)

Flere av selskapene i delingsøkonomien kan potensielt nyte godt av såkalte førstemannsfordeler. De samme førstemannsfordelene kan gi grunn til bekymring i et samfunnsøkonomisk perspektiv. Forklar hvilke mekanismer som typisk skaper førstemannsfordeler i delingsøkonomien og hva som eventuelt er problemet samfunnsøkonomisk!

## Oppgave 6 (20 %)

- a) Forklar hvorfor «revenue equivalence» gitt risikonøytralitet holder innenfor «private value model» og «common value model», men ikke i «affiliated value model»!
- b) Utover det som er direkte knyttet til «affiliated value», hvilke mekanismer kan bidra til at åpne, iterative auksjonsformer gir høyere verdi for selger?
- c) I en bestemt type kombinatorisk auksjon omtalt som Combinatorial Clock Auction, CCA, er det først en fase med prisklokker og så en ekte kombinatorisk auksjon. Forklar hensikten med å ha den første fasen!
- d) I en bestemt type kombinatorisk auksjon omtalt som Combinatorial Clock Auction, CCA, brukes en andreprisregel kalt «Vickrey-nearest-core pricing» sammen med en aktivitetsregel. Forklar hva som er hensikten med disse to reglene!