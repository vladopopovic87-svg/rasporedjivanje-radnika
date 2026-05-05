# BRZI PREGLED MODULA

## 📋 Šta je Svaka Datoteka

### 🎯 `app87.py` (6 linija)
**Uloga**: Glavna datoteka koju pokupuš pokrenuti
**Komanda**: `streamlit run app87.py`
**Radi**: Samo importuje `app_main.py` i pokreće `main()`

---

### 🏢 `app_main.py` (200 linija)
**Uloga**: Mozak aplikacije - koordinira sve
**Radi**:
1. Prikuplja ulaz od korisnika
2. Pravi model
3. Rešava ga
4. Prikazuje rezultate

---

### ⚙️ `config.py` (120 linija)
**Uloga**: Skladište svih konstanti
**Sadrži**: 
- Default imena (profila, aktivnosti)
- Default intervale i smene
- Primere potražnje
- Konstante za ograničenja

---

### 🔨 `utils.py` (65 linija)
**Uloga**: Pomoćne funkcije
**Funkcije**:
- Parsiranje ulaza (CSV, JSON)
- Brojanje uzastopnih redova
- Generisanje IDs-eva

---

### 🎨 `ui_input.py` (250 linija)
**Uloga**: Sve Streamlit widgete za ulaz
**Funkcije**:
- Opšti parametri
- Intervali i smene
- Troškovi
- Mapiranja uloga
- Varijantu-zavisni parametri
- Potražnja

---

### 🧮 `model_builder.py` (200 linija)
**Uloga**: Izgradnja linearnog programa
**Radi**:
- Kreira PuLP promenljive
- Postavlja ciljnu funkciju
- Dodaje sva ograničenja

---

### 📊 `results_display.py` (280 linija)
**Uloga**: Obrada i prikaz rezultata
**Radi**:
- Procesira PuLP rešenje
- Generiše rasporede radnika
- Pravi tabele
- Analizira rezultate

---

## 🔗 Kako Moduli Rade Zajedno

```
┌──────────────────────────────┐
│  app87.py                    │
│  ↓ pokrupa                   │
│  app_main.py                 │
├──────────────────────────────┤
│  1. ui_input.py    ← Prikuplja ulaz
│  2. model_builder.py ← Pravi i rešava model
│  3. results_display.py ← Prikazuje rezultate
├──────────────────────────────┤
│ Svi koriste:                 │
│  - config.py (konstante)     │
│  - utils.py (pomoćne funkcije)
└──────────────────────────────┘
```

---

## 📝 Tok Izvršavanja

1. **Korisnik pokreće**: `streamlit run app87.py`
2. **app87.py** pokreće `main()` iz `app_main.py`
3. **app_main.py**:
   - Pravi Streamlit sajt
   - Poziva sve funkcije iz `ui_input.py` da prikupi ulaze
   - Poziva funkcije iz `model_builder.py` da napravi model
   - Rešava model
   - Poziva funkcije iz `results_display.py` da obradi rezultate
4. **Streamlit** prikazuje rezultate korisniku

---

## 💡 Kada Koristiti Koji Modul

### Trebam Dodati Novi Ulaz
→ Dodaj funkciju u `ui_input.py`

### Trebam Promeniti Default Vrednosti
→ Izmeni vrednosti u `config.py`

### Trebam Novo Ograničenje
→ Dodaj funkciju u `model_builder.py`

### Trebam Novu Analizu Rezultata
→ Dodaj funkciju u `results_display.py`

### Trebam Pomoćnu Funkciju
→ Dodaj je u `utils.py`

---

## 📦 Zavisnosti (iz requirements.txt)

```
streamlit
pulp
pandas
```

---

## 🎯 Ključne Konstante (iz config.py)

```python
DEFAULT_NUM_PROFILES = 3
DEFAULT_NUM_ACTIVITIES = 6
DEFAULT_M2_SHIFT_START = 51  # Početak indeksa za pola vremena smene
MAX_WORKERS_PER_INTERVAL = 40
MAX_M1_SHIFTS = 3
MAX_M2_SHIFTS = 1
```

---

## 🚀 Primer: Dodavanje Nove Ograničenja

### 1. Kreiraj Funkciju u `model_builder.py`
```python
def add_my_constraint(model, profil_types, M_set, ...):
    """Moje novo ograničenje"""
    for p in profil_types:
        model += expression >= value, "My_Constraint"
```

### 2. Pozovi iz `app_main.py`
```python
# U app_main.py nakon ostalih ograničenja
add_my_constraint(model, profil_types, M_set, ...)
```

### 3. Gotovo! Novo ograničenje je dodano

---

## 🐛 Debugging Saveti

### Provera Sintakse
```bash
python -m py_compile modul.py
```

### Test Jednog Modula
```bash
python -c "from modul import funkcija; print(funkcija())"
```

### Pokretanje sa Debug Informacijama
```bash
streamlit run app87.py --logger.level=debug
```

---

## 📈 Veličina Koda

- **Ukupno**: ~1100 linija koda
- **Bez Komentara**: ~900 linija
- **Malo, Modularno & Čitljivo** ✅

---

## ✅ Proveravaj Ove Datoteke Kada...

| Situacija | Datoteka |
|-----------|----------|
| Trebam promeniti default vrednosti | config.py |
| Trebam dodati novi UI unos | ui_input.py |
| Trebam novo ograničenje | model_builder.py |
| Trebam novu analizu | results_display.py |
| Trebam pomoćnu funkciju | utils.py |
| Trebam promeniti tok programa | app_main.py |
| Trebam pokrenuti aplikaciju | app87.py |
