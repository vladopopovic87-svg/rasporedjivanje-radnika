# MODULARNI PREGLED PROJEKTA

## 📁 Struktura Datoteka

```
rasporedjivanje-radnika/
├── app87.py                 # Entry point - pokrenta aplikaciju
├── app_main.py              # Glavna aplikacijska logika
├── config.py                # Sve konfiguracije i default vrednosti
├── utils.py                 # Uslužne/pomoćne funkcije
├── ui_input.py              # Prikupljanje ulaza od korisnika kroz UI
├── model_builder.py         # Izgradnja PuLP optimizacijskog modela
├── results_display.py       # Procesiranje i prikaz rezultata
├── requirements.txt         # Python zavisnosti
└── README.md                # Dokumentacija
```

## 🔧 Opis Svakog Modula

### `app87.py` - Entry Point
- **Uloga**: Glavna datoteka koja se pokreće sa `streamlit run app87.py`
- **Funkcionalnost**: Importuje i pokreće `main()` iz `app_main.py`
- **Sadržaj**: Samo 6 linija koda

```python
from app_main import main
if __name__ == "__main__":
    main()
```

---

### `app_main.py` - Glavna Logika Aplikacije
- **Uloga**: Orkestrira ceo tok aplikacije
- **Ključne Funkcije**:
  - `main()` - Glavna funkcija koja koordinira sve
  
- **Šta radi**:
  1. Konfigurira Streamlit sajt
  2. Poziva sve inputCollection funkcije
  3. Gradi model
  4. Rešava optimizacijski problem
  5. Prikazuje rezultate

- **Veličina**: ~200 linija koda

---

### `config.py` - Konfiguracija i Default Vrednosti
- **Uloga**: Centralizovano mesto za sve default vrednosti i konstante
- **Šta sadrži**:
  - `DEFAULT_NUM_PROFILES`, `DEFAULT_NUM_ACTIVITIES` - Početne vrednosti
  - `DEFAULT_FULL_PROFILE_NAMES` - Imena profila (Komisioner, Kontrolor, itd.)
  - `DEFAULT_FULL_ACTIVITY_NAMES` - Imena aktivnosti (Komisioniranje, Kontrola, itd.)
  - `DEFAULT_SHORT_*` - Kratke kodove za prikaz
  - `DEFAULT_*_SET` - Intervale i smene
  - `DEFAULT_CT_RATES` - Troškovne stope
  - `DEFAULT_ALLOWED` - Osnovno mapiranje profila po aktivnostima
  - `DEMAND_EXAMPLE_1`, `DEMAND_EXAMPLE_2` - Primeri potražnje
  - Konstante za ograničenja

- **Prednosti**:
  - Lako menjivanje default vrednosti
  - Svaka vrednost je na jednom mestu
  - Nije potrebno tražiti kroz kod

- **Veličina**: ~120 linija koda

---

### `utils.py` - Uslužne/Pomoćne Funkcije
- **Uloga**: Pomoćne funkcije koje se koriste u drugim modulima
- **Funkcije**:
  1. `parse_list(input_str, item_type=str)` - Parsira CSV ulaz u listu
  2. `parse_json_dict(input_str, default_value=None)` - Parsira JSON string
  3. `generate_profile_types(num_profiles)` - Generiše IDs profila
  4. `generate_activities(num_activities)` - Generiše IDs aktivnosti
  5. `count_consecutive_sequences(series, min_len=3)` - Broji uzastopne redove istih vrednosti

- **Primer Korišćenja**:
```python
from utils import parse_list
N_set = parse_list("1, 2, 3, 4, 5", int)
```

- **Veličina**: ~65 linija koda

---

### `ui_input.py` - Prikupljanje Ulaza UI-ja
- **Uloga**: Sve Streamlit widgete za prikupljanje korisničkog unosa
- **Funkcije** (6 velikih funkcija):
  1. `collect_general_parameters()` - Osnovni parametri (broj profila, aktivnosti, imena)
  2. `collect_interval_and_shift_parameters()` - Intervale i smene
  3. `collect_cost_coefficients()` - Troškovne stope
  4. `collect_role_activity_mappings()` - Koje aktivnosti mogu obavljati profili
  5. `collect_variant_parameters()` - Zahteve za aktivnosti (within, until)
  6. `collect_demand_data()` - Potražnja po intervalu

- **Karakteristike**:
  - Koristi `st.sidebar.expander()` za organizovanu navigaciju
  - Vraća sve prikupljene vrednosti kao tuple
  - Uključuje validaciju i default vrednosti

- **Primer Korišćenja**:
```python
from ui_input import collect_general_parameters
P, profil_types, activities, ... = collect_general_parameters()
```

- **Veličina**: ~250 linija koda

---

### `model_builder.py` - Izgradnja PuLP Modela
- **Uloga**: Sve što se tiče PuLP linearnog programa
- **Ključne Funkcije**:
  1. `build_model_variables()` - Kreira PuLP promenljive (ytj, ytija, xaijk, itd.)
  2. `build_delta_variables()` - Kreira penalne promenljive
  3. `setup_objective_function()` - Postavlja ciljnu funkciju (minimizacija troškova)
  4. `add_demand_constraints()` - Ograničenja za pokrivanje potražnje
  5. `add_activity_within_constraints()` - Ograničenja za kontinualne aktivnosti
  6. `add_activity_until_constraints()` - Ograničenja za aktivnosti sa rokom
  7. `add_activity_allocation_constraints()` - Linkovanje aktivnosti na radnike
  8. `add_worker_capacity_constraints()` - Kapacitet radnika
  9. `add_interval_worker_limit()` - Max radnika po intervalu
  10. `add_shift_constraints()` - Ograničenja za smene

- **Prednosti Modularnog Pristupa**:
  - Lako se vide sva ograničenja
  - Lako se dodaju nova ograničenja
  - Kod je čitljiviji i održiviji

- **Veličina**: ~200 linija koda

---

### `results_display.py` - Procesiranje i Prikaz Rezultata
- **Uloga**: Sve funkcije za obradu PuLP rešenja i prikaz rezultata
- **Ključne Funkcije**:
  1. `build_bij_matrix()` - Kreira matricu pokrivanja (koji radnici su dostupni u kojem intervalu)
  2. `build_ct_matrix()` - Kreira matricu troškova
  3. `generate_schedule_output()` - Pretvara PuLP rešenje u raspored
  4. `balance_schedules()` - Balanisira rad između radnika
  5. `create_shift_allocation_table()` - Pravi tabelu sa rasporedom
  6. `create_demand_comparison_table()` - Pravi tabelu sa poređenjem potražnje
  7. `count_idle_intervals()` - Broji intervale bez rada
  8. `analyze_activity_sequences()` - Analizira uzastopne aktivnosti
  9. `display_results()` - Prikazuje sve rezultate u Streamlit-u

- **Karakteristike**:
  - Čitljiv prikaz rezultata
  - Analiza kvaliteta rasporeda
  - Validacija da li su zahtevi ispunjeni

- **Veličina**: ~280 linija koda

---

## 🔄 Tok Podataka

```
┌─────────────────────────────────────┐
│   app87.py                          │
│   ↓                                 │
│   Pokreće main() iz app_main.py    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   app_main.py                       │
│   ↓                                 │
│   1. Poziva UI funkcije             │
│      ├─ collect_general_params      │
│      ├─ collect_intervals           │
│      ├─ collect_costs               │
│      ├─ collect_mappings            │
│      ├─ collect_variants            │
│      └─ collect_demand              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   model_builder.py                  │
│   ↓                                 │
│   1. Pravi PuLP model               │
│   2. Dodaje promenljive              │
│   3. Dodaje ograničenja              │
│   4. Postavlja cilj                  │
│   5. Rešava problem                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   results_display.py                │
│   ↓                                 │
│   1. Procesira rešenje               │
│   2. Generiše rasporede              │
│   3. Pravi tabele                    │
│   4. Prikazuje sve                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Streamlit UI                      │
│   Prikazuje rezultate korisniku      │
└─────────────────────────────────────┘
```

## 📊 Integracija Modula

```
         app_main.py
        /    |    \    \
       /     |     \    \
   ui_input  |   model_  results_
             |  builder  display
            config
              |
            utils
```

## 💾 Veličine i Linija Koda

| Datoteka | Linije | Funkcije | Opis |
|----------|--------|----------|------|
| app87.py | 6 | 0 | Entry point |
| app_main.py | 200 | 1 | Glavna logika |
| config.py | 120 | 0 | Konstante |
| utils.py | 65 | 5 | Pomoćne funkcije |
| ui_input.py | 250 | 6 | UI input |
| model_builder.py | 200 | 10 | PuLP model |
| results_display.py | 280 | 9 | Prikaz rezultata |
| **TOTAL** | **~1100** | **31** | **Sve** |

## ✨ Prednosti Modularnog Pristupa

1. **Čitljivost** - Svaki modul ima jasnu uloga
2. **Održivost** - Lako se pronalaze i menjaju dela koda
3. **Proširivost** - Lako se dodaju nove funkcionalnosti
4. **Testljivost** - Svaki modul se može testirati posebno
5. **Ponovno Korišćenje** - Funkcije se mogu koristiti u drugim projektima
6. **Dokumentovano** - Jasne svrhe i interfejsi

## 🚀 Kako Proširiti

### Dodavanje Nove Ograničenja
1. Kreiraj funkciju u `model_builder.py`
2. Pozovi je iz `app_main.py` nakon ostalih ograničenja

### Promena Default Vrednosti
1. Izmeni vrednosti u `config.py`
2. Automatski će se koristiti u svim modulima

### Dodavanje Nove UI Komponente
1. Kreiraj funkciju u `ui_input.py`
2. Pozovi je iz `app_main.py`
3. Korisni parametri će biti dostupni

### Dodavanje Nove Analize Rezultata
1. Kreiraj funkciju u `results_display.py`
2. Pozovi je iz `display_results()`
