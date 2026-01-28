# Worker Scheduling Optimization System

## Pregled Projekta

Ovo je Streamlit aplikacija za optimizaciju raspoređivanja radnika korišćenjem linearnog programiranja (PuLP). Aplikacija omogućava korisnicima da definišu profil radnika, aktivnosti, intervale, i druge parametre, a zatim automatski generiše optimalno raspoređivanje radnika sa minimalnom potrošnjom troškova.

## Struktura Projekta

Projekat je refaktorisan u modularnu strukturu sa sledećim komponentama:

### Glavne Datoteke

- **`app87.py`** - Glavna Streamlit aplikacija (entry point)
- **`app_main.py`** - Glavna logika aplikacije

### Moduli

#### 1. **`config.py`** - Konfiguracija i Default Vrednosti
Sadrži sve default vrednosti za:
- Profil radnika i aktivnosti
- Intervale i smene
- Troškovne koeficijente (ct)
- Mapiranja uloga i aktivnosti
- Zahteve za aktivnosti (within, until)
- Primere potražnje

#### 2. **`utils.py`** - Uslužne Funkcije
Pomoćne funkcije:
- `parse_list()` - Parsiranje CSV ulaza
- `parse_json_dict()` - Parsiranje JSON ulaza
- `generate_profile_types()` - Generisanje identifikatora profila
- `generate_activities()` - Generisanje identifikatora aktivnosti
- `count_consecutive_sequences()` - Brojanje uzastopnih nizova istih vrednosti

#### 3. **`ui_input.py`** - Prikupljanje Ulaza UI-ja
Funkcije za prikupljanje korisničkog unosa:
- `collect_general_parameters()` - Opšti parametri
- `collect_interval_and_shift_parameters()` - Intervali i smene
- `collect_cost_coefficients()` - Troškovni koeficijenti
- `collect_role_activity_mappings()` - Mapiranja uloga
- `collect_variant_parameters()` - Varijantu-zavisni parametri
- `collect_demand_data()` - Podatke o potražnji

#### 4. **`model_builder.py`** - Izgradnja PuLP Modela
Funkcije za izgradnju optimizacijskog modela:
- `build_model_variables()` - Izgradnja beslanova
- `build_delta_variables()` - Izgradnja delta promenljivih za penale
- `setup_objective_function()` - Postavljanje ciljne funkcije
- `add_*_constraints()` - Dodavanje raznih ograničenja

#### 5. **`results_display.py`** - Prikaz Rezultata
Funkcije za procesiranje i prikaz rezultata:
- `build_bij_matrix()` - Izgradnja matrice pokrivanja intervala
- `build_ct_matrix()` - Izgradnja matrice troškova
- `generate_schedule_output()` - Generisanje rasporeda iz PuLP rešenja
- `balance_schedules()` - Balansiranje rasporeda između radnika
- `create_shift_allocation_table()` - Kreiranje tabele sa rasporedom smena
- `create_demand_comparison_table()` - Kreiranje tabele sa poređenjem potražnje
- `display_results()` - Prikazivanje svih rezultata

## Kako Pokrenuti Aplikaciju

### Instalacija Zavisnosti

```bash
pip install -r requirements.txt
```

### Pokretanje Streamlit Aplikacije

```bash
streamlit run app87.py
```

Aplikacija će se otvoriti na `http://localhost:8501`

## Kako Koristiti

### 1. Opšti Parametri
- Unesite broj profila radnika i aktivnosti
- Definirajte imena profila i aktivnosti na lokalnom jeziku
- Definirajte kratke kodove za brži prikaz

### 2. Intervali i Smene
- Postavite intervale (N_set) - vremenske periode
- Postavite smene (M_set) - raspored smena
- Podelite smene na pune (M1) i pola radnog vremena (M2)
- Definirajte dostupne intervale za odmor (Oj)

### 3. Troškovni Koeficijenti
- Postavite trošak po radniku za pune i pola smene

### 4. Mapiranja Uloga i Aktivnosti
- Izaberite koje aktivnosti može obavljati svaki profil
- Definirajte primarnih i sekundarne aktivnosti

### 5. Varijantu-zavisni Parametri
- Odredite aktivnosti sa zahtevom za kontinuiranost (within)
- Odredite aktivnosti sa zahtevom za završetak do određenog vremena (until)

### 6. Potražnja
- Izaberite primer potražnje ili kreirajte svoju
- Uredite potražnju za svaku aktivnost po intervalu

### 7. Pokrenite Optimizaciju
- Kliknite na "Run Optimization" dugme
- Čekajte da se model reši
- Pregledajte rezultate

## Arhitektura Modela

### Promenljive Odluke
- `ytj` - Broj radnika po smeni i profilu
- `ytija` - Broj radnika po smeni, intervalu, smeni i aktivnosti
- `xaijk` - Broj radnika dodeljenoj aktivnosti u intervalu
- `delta` - Penali za prelazak između aktivnosti (opciono)

### Ograničenja
1. **Ograničenja Potražnje** - Svaka aktivnost mora biti pokrivena zahtevima
2. **Ograničenja Kapaciteta** - Radnici ne mogu obavljati više od svog kapaciteta
3. **Ograničenja Smena** - Broj smena je ograničen
4. **Ograničenja Intervala** - Maksimalan broj radnika po intervalu
5. **Ograničenja Uloga** - Samo određeni profili mogu obavljati određene aktivnosti

### Ciljna Funkcija
- Minimizacija: `Trošak = Σ(broj_radnika × trošak_po_radniku) + P × Penali_prelazaka`

## Rezultati

Aplikacija prikazuje:
1. **Optimalna vrijednost** - Minimalni troškovi
2. **Rasporedi smena** - Tabela sa rasporedom radnika po smeni
3. **Analiza aktivnosti** - Broj uzastopnih aktivnosti
4. **Poređenje potražnje** - Zahtevana vs. dodeljena potražnja
5. **Detaljne promenljive** - Sve PuLP promenljive sa ne-nula vrednostima

## Konfiguracija

Sve default vrednosti se mogu promeniti u `config.py`:
- Promjena default imena profila i aktivnosti
- Promjena default intervala i smena
- Promjena default troškova
- Promjena primena potražnje

## Zavisnosti

- `streamlit` - Framework za web aplikaciju
- `pulp` - Biblioteka za linearno programiranje
- `pandas` - Rad sa podacima
- `python-3.9+` - Verzija Python-a

## Napomene

- Model koristi CBC solver iz PuLP biblioteke
- Za velike probleme može trajati duže vreme rešavanja
- Preporuka je da se počne sa manjim brojem intervala i profila za testiranje

## Autori i Licenca

Projekat je razvijen kao sistem za optimizaciju raspoređivanja radnika.
