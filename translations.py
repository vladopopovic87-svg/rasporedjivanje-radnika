# Translation strings for the application

TRANSLATIONS = {
    "en": {
        # App titles and headers
        "app_title": "Worker Scheduling Optimization",
        "model_parameters": "Model Parameters",
        "schedule_page": "Schedule",
        "instructions_page": "Instructions",
        "about_page": "About the application",
        "about_content": "Content for this page will be added later.",
        
        # General Parameters
        "general_parameters": "General Parameters",
        "short_duration_penalty": "Activity Switching Cost Coefficient",
        "num_profiles": "Number of Worker Profiles",
        "num_activities": "Number of Activities",
        "remove_profiles": "Remove worker profiles",
        "remove_activities": "Remove activities",
        "remove_profile_help": "Remove this worker profile from the application.",
        "remove_activity_help": "Remove this activity from the application.",
        "choose_activities": "Choose Activities",
        "define_profile_names": "Define Profile Names and Short Codes",
        "define_activity_names": "Define Activity Names and Short Codes",
        "full_name_for": "Full name",
        "short_code_for": "Code",
        
        # Interval and Shift Sets
        "interval_shift_sets": "Interval and Shift Sets",
        "start_working_day": "Start of working day (display intervals from):",
        "full_time_shift_length": "Full-time shift length (in intervals):",
        "half_time_shift_length": "Half-time shift length (in intervals):",
        "interval_duration": "Duration of one interval (in minutes):",
        "rest_duration": "Break duration (in minutes):",
        "m2_shift_start": "Start of M2 shift (interval number):",
        "m1_set_label": "M1_set (Full-time shifts, comma-separated integers)",
        "m2_set_label": "M2_set (Part-time shifts, comma-separated integers)",
        "m1_set_help": "List of full-time shifts (longer working hours). Subset of M_set. M1_set is auto-populated based on full-time shift length and available intervals. M2_set is now auto-populated based on current number of intervals and half-time shift length.",
        "m2_set_help": "List of part-time shifts (shorter working hours). Subset of M_set.",
        "m_set_label": "M_set (Shifts, auto-generated as M1_set + M2_set)",
        "m_set_help": "M_set is auto-generated from M1_set and M2_set.",
        "oj_intervals_label": "Oj (Intervals available for rest shift j, only for M1 shifts):",
        "intervals_for_shift": "Intervals for shift",
        "oj_help_prefix": "Time intervals available for rest during shift",
        "min_len_label": "Minimum length of consecutive activities (min_len):",
        "min_len_help": "Minimum length of consecutive activities (sequences) to analyze. Default is 3.",
        "p_help_transition_penalty": "Multiplied by the number of activity switches. The result is added to the objective function.",
        "num_profiles_help": "Number of different worker profile types (e.g., Komisioner, Kontrolor, Viljuškarista).",
        "num_activities_help": "Number of different activity types that workers can perform.",
        "profile_full_name_help": "Full descriptive name for this worker profile type.",
        "profile_short_code_help": "Short abbreviation or code for this worker profile (used in tables and reports).",
        "activity_full_name_help": "Full descriptive name for this activity type.",
        "activity_short_code_help": "Short abbreviation or code for this activity (used in tables and reports).",
        "display_start_interval_help": "Starting hour for displaying time intervals in the schedule (e.g., 8 means intervals start from 8:00).",
        "full_time_shift_length_help": "Length of full-time shifts in number of intervals.",
        "half_time_shift_length_help": "Length of half-time shifts in number of intervals.",
        "interval_duration_help": "Duration of each time interval in minutes (e.g., 30 for 30 minutes, 60 for 1 hour).",
        "rest_duration_help": "Duration of rest intervals in minutes (e.g., 30 for 30 minutes, 60 for 1 hour).",
        "num_intervals_label": "Number of intervals in 24h:",
        "num_intervals_help": "How many intervals are used in 24h. N_set will be created as list [1..N].",
        "oj_intervals_help": "Workers can take breaks in these intervals during the shift.",
        "ind_within_help": "Activities that have 'within' constraints - workers must complete these activities within a certain number of intervals.",
        "ind_until_help": "Activities that have 'until' constraints - workers must start these activities by a certain interval.",
        "dependent_within_help": "Activities with dependent 'within' constraints - these depend on other activities being completed first.",
        "dependent_until_help": "Activities with dependent 'until' constraints - these depend on other activities being completed first.",
        "no_dependent_within_selected": "No dependent activities selected in dep_within. Add activity IDs above to set dependent within values.",
        "no_dependent_until_selected": "No dependent activities selected in dep_until. Add activity IDs above to set dependent until values.",
        "within_help": "Maximum number of intervals allowed to complete '{activity}' activity.",
        "until_help": "Latest interval by which activity '{activity}' must be completed, excluding that interval.",
        "select_demand_profile_help": "Choose a predefined demand pattern to start with. You can then edit the values in the table below.",
        "dep_within_values_header": "dependent within values (integer per dependent activity):",
        "dep_until_values_header": "dependent until values (integer per dependent activity):",
        "dep_within_value_label": "dep within value",
        "dep_until_value_label": "dep until value",
        "dep_ratio_prompt": "Enter ratio for '{dependent}' from '{depends_on}'",
        "dependency_activity_help": "Choose the independent activity whose completed work determines the required amount of '{activity}'.",
        "dependency_ratio_help": "This coefficient describes the dependency of the required number of workers for '{dependent}' on the number of workers scheduled for '{depends_on}'. For example, with a coefficient of 0.5, if 6 workers are scheduled for '{depends_on}' in an interval, at least 3 workers are required for '{dependent}'.",
        "max_workers_per_interval_help": "Maximum number of workers that can be assigned to work in a single time interval. This constraint prevents overcrowding and ensures safety.",
        "max_m1_shifts_help": "Maximum number of full-time shifts that can be scheduled. Full-time shifts typically have longer working hours.",
        "max_m2_shifts_help": "Maximum number of part-time shifts that can be scheduled. Part-time shifts usually have shorter working hours.",
        "m2_ratio_limit_help": "Maximum ratio of part-time shifts (M2) relative to total shifts (M1 + M2). For example, 0.3 means max 30% of shifts can be part-time.",
        "istovar_kontrola_ratio_help": "Ratio of kontrola workers relative to workers performing istovar.",
        "non_primary_activities_ratio_help": "Maximum ratio of non-primary activities that full-time workers (M1) can perform.",
        "error_parsing_list": "Error parsing list: '{input_str}'. Please ensure all items are of type {item_type}.",
        "error_parsing_json": "Error parsing JSON: {error}. Please ensure the input is valid JSON.",
        "comma_separated_integers": "(comma-separated integers)",
        
        # Cost Coefficients
        "cost_coefficients": "Cost Coefficients",
        "cost_for_m1": "Cost for M1 (full-time) for",
        "cost_for_m2": "Cost for M2 (half-time) for",
        "full_time_label": "full-time",
        "part_time_label": "part-time",
        "m1_cost_rates": "Full-time shift cost rates:",
        "m2_cost_rates": "Part-time shift cost rates:",
        "m1_cost_help": "Cost rate per full shift for",
        "m2_cost_help": "Cost rate per shift for",
        "working_full_time": "working full-time shifts.",
        "working_part_time": "working part-time shifts.",
        
        # Role-Activity Mappings
        "role_activity_mappings": "Role-Activity Mappings",
        "allowed_activities_per_role": "Allowed Activities per Role",
        "profiles_for": "Profiles for",
        "able_activities_per_profile": "Activity Overview: Activities Profiles Can Perform",
        "activities_for": "Activities of profile",
        "primary_able_activities": "Primary Activities per Profile",
        "primary_activities_for": "Primary activities for",
        "select_which_workers": "Select worker profiles that can perform the",
        "select_which_activities": "Select which activities",
        "select_primary_activities_for": "Select primary activities for",
        "workers_are_able": "workers are able to perform",
        "can_perform_primary": "can perform as primary work",
        
        # Variant-Dependent Parameters
        "variant_dependent_parameters": "Variant-Dependent Parameters",
        "ind_within": "ind_within (activity names)",
        "ind_until": "ind_until (activity names)",
        "within_values": "within values (integer per activity)",
        "until_values": "until values (integer per activity)",
        "within_value": "within value",
        "until_value": "until value",
        "independent_activities": "Independent Activities",
        "no_activities_ind_within": "No activities selected in ind_within. Add activity IDs above to set within values.",
        "no_activities_ind_until": "No activities selected in ind_until. Add activity IDs above to set until values.",
        "dependent_activities": "Dependent Activities",
        "dep_within": "dep_within (activity names)",
        "dep_until": "dep_until (activity names)",
        "no_activities_dep_within": "No dependent activities selected in dep_within.",
        "no_activities_dep_until": "No dependent activities selected in dep_until.",
        "error_overlap": "Error: Activities in both 'ind_within' and 'ind_until':",
        "activity_type_required": "Activity '{activity}' must be assigned to exactly one activity type: within, until, dependent within, or dependent until.",
        "activity_type_multiple": "Activity '{activity}' is assigned to multiple activity types. Select only one.",
        "activity_value_required": "Enter a value for '{value_type}' for activity '{activity}'.",
        "activity_profile_required": "Activity '{activity}' must have at least one worker profile that can perform it.",
        "until_value_exceeds_intervals": "The 'until' value {value} for '{activity}' exceeds the maximum allowed value {max_interval}. Because the end interval is excluded, enter a value within the allowed range.",
        "select_activity_depends_on": "Select activity that",
        "depends_on": "depends on",
        
        # Demand Data
        "demand_data": "Demand Data",
        "select_demand_profile": "Select Demand Profile",
        "demand_example_1": "Example 1",
        "demand_example_2": "Example 2",
        "custom_demand": "Custom Demand",
        "demand_for": "Demand for",
        "enter_comma_separated": "Enter comma-separated demand values for each interval",
        
        # Constraint Parameters
        "constraint_parameters": "Constraint Parameters",
        "max_workers_per_interval": "Max Workers Per Interval",
        "max_m1_shifts": "Max M1 Shifts",
        "max_m2_shifts": "Max M2 Shifts",
        "non_primary_activities_ratio": "Non-Primary Activities Ratio",
        "m2_ratio_limit": "M2 Ratio Limit",
        "istovar_kontrola_ratio": "Istovar/Kontrola Ratio",
        "max_number_of": "Maximum number of",
        "instructions": "Instructions",
        "instructions_content": """
    ### Kako unijeti svoj problem

    Aplikacija traži odgovor na tri osnovna pitanja: **ko radi**, **šta treba da se uradi** i **kada treba**. Prije početka unosa potrebno je pripremiti vrijednosti parametara kojima se definiše problem raspoređivanja radnika, a koji su pobrojani i pojašnjeni u nastavku. Potražnja za radnicima unosi se kroz tabelu, dok se ostali parametri unose kroz za to predviđena polja sa lijeve strane.

    Dimenzije tabele potražnje zavise od unesenog **broja aktivnosti** i **broja vremenskih intervala**. Tabela je početno popunjena vrijednostima iz primjera, koje se mogu u potpunosti izmijeniti i prilagoditi konkretnom problemu raspoređivanja. Isto važi i za početno zadate vrijednosti ostalih parametara.

    ### 1. Radnici i aktivnosti

    - **Broj profila radnika**: Unesi koliko različitih vrsta radnika imaš, na primjer komisioner, kontrolor i viljuškarista.
    - **Broj aktivnosti**: Unesi koliko različitih poslova treba raspoređivati.
    - **Puno ime**: Upiši razumljiv naziv profila ili aktivnosti.
    - **Kod**: Upiši kratku oznaku koja će se prikazivati u tabeli rasporeda, na primjer KOM ili VIL.

    ### 2. Intervali i smjene

    Prvo odluči koliko traje jedan interval. Ako interval traje 60 minuta, 8 intervala predstavlja 8 sati.

    - **Početak radnog dana**: Unesi sat od kojeg počinje prikaz, na primjer 8 za 08:00.
    - **Trajanje jednog intervala**: Unesi trajanje intervala u minutama, na primjer 60.
    - **Broj intervala u 24h**: Unesi koliko intervala obuhvata plan, na primjer 12 intervala za period od 08:00 do 20:00.
    - **Dužina pune smjene**: Unesi broj intervala koje radi radnik sa punim radnim vremenom, na primjer 8.
    - **Dužina nepune smjene**: Unesi broj intervala koje radi radnik sa nepunim radnim vremenom, na primjer 4.
    - **Trajanje pauze**: Unesi trajanje pauze u minutama.
    - **Skup smjena sa punim radnim vremenom**: Automatski se popunjava prema dužini pune smjene i broju raspoloživih intervala. Na primjer, ako je dostupno 9 intervala, a smjena traje 8 intervala, postoje dvije smjene. Ako interval traje sat vremena i radni dan počinje u 8, prva počinje u 8, a druga u 9. Smjene se mogu brisati, ali su sve iste dužine.
    - **Skup smjena sa nepunim radnim vremenom**: Automatski se popunjava prema dužini nepune smjene i broju raspoloživih intervala. Smjene počinju od oznake 51 nadalje; broj 5 na početku razlikuje ih od smjena sa punim radnim vremenom. Sve su iste dužine.
    - **Intervali dostupni za odmor**: Za svaku smjenu sa punim radnim vremenom upiši redne brojeve intervala u kojima je dozvoljena pauza.
    - **Minimalna dužina uzastopnih aktivnosti**: Određuje minimalnu dužinu sekvenci koje se prikazuju u dodatnoj analizi rezultata. Ovaj parametar ne utiče na raspored. Na raspored utiče koeficijent troška promjene aktivnosti ako je veći od 0.

    ### 3. Troškovi

    Unose se relativni koeficijenti troška, a ne moraju se unositi stvarni iznosi plata. Koeficijenti se mogu normalizovati prema izabranoj referentnoj vrijednosti. Na primjer, ako su dnevne plate 100, 200 i 300 novčanih jedinica, a 200 se uzme kao referenca, koeficijenti su 0,5, 1 i 1,5. Veći koeficijent znači da će optimizacija više izbjegavati tu opciju.

    - **Koeficijent troška pune smjene**: Relativni trošak smjene sa punim radnim vremenom za profil.
    - **Koeficijent troška nepune smjene**: Relativni trošak smjene sa nepunim radnim vremenom za profil.
    - **Koeficijent troška prebrzog mijenjanja aktivnosti**: Ako je veći od 0, model dodaje kaznu za promjene aktivnosti i time utiče na raspored. Postavi 0 ako ne želiš da se te promjene kažnjavaju.

    ### 4. Mapiranje profila i aktivnosti

    Za svaku aktivnost izaberi profile koji je mogu obavljati. Zatim za svaki profil označi primarne aktivnosti koje taj profil prvenstveno treba da radi. Ne dozvoli aktivnosti koje radnik ne zna ili ne smije obavljati.

    ### 5. Tipovi aktivnosti i zavisnosti

    Nezavisne aktivnosti su aktivnosti čija potražnja za radnicima ne zavisi od neke druge aktivnosti. Njihovu potražnju unesi u početnu tabelu potražnje za svaki interval. Zavisne aktivnosti su aktivnosti čija se potrebna potražnja za radnicima računa na osnovu broja radnika raspoređenih na aktivnost od koje zavise i zadatog odnosa. Na primjer, ako je za utovar raspoređeno 4 radnika, a kontrola zavisi od utovara uz odnos od 50%, potrebno je najmanje 2 radnika za kontrolu.

    Ovaj dio koristi se za dodavanje vremenskih pravila nezavisnim ili zavisnim aktivnostima.

    - **U okviru**: Koristi kada aktivnost tj. zahtjev za radnicima iz nekog intervala mora biti zadovoljen unutar određenog broja intervala.
    - **Do**: Koristi kada aktivnost tj. zahtjev za radnicima iz nekog intervala mora biti zadovoljen najkasnije do određenog intervala.
    - **Zavisna aktivnost**: Koristi kada se potreban broj radnika računa iz druge aktivnosti, na primjer kontrola je 50% istovara.
    - Nemoj istu aktivnost istovremeno označiti kao "u okviru" i "do".

    ### 6. Parametri ograničenja

    Ovi parametri ograničavaju koliko slobode model ima pri izboru rasporeda.

    - **Maksimalni broj radnika po intervalu**: Najveći ukupan broj radnika koji smije istovremeno raditi (u jednom intervalu).
    - **Maksimalan broj smjena sa punim radnim vremenom**: Najveći broj punih smjena koje model smije otvoriti.
    - **Maksimalan broj smjena sa nepunim radnim vremenom**: Najveći broj nepunih smjena koje model smije otvoriti.
    - **Granica odnosa smjena sa nepunim radnim vremenom**: Najveći dozvoljeni udio nepunih smjena među svim smjenama; 0.30 znači najviše 30%.
    - **Odnos sporednih aktivnosti**: Najveći udio vremena radnika sa punim radnim vremenom koji se smije potrošiti na aktivnosti koje nisu primarne.

    Postavi ograničenja dovoljno široko za prvi pokušaj. Ako je rješenje nemoguće, prvo povećaj maksimalan broj radnika ili smjena i provjeri da li su profili pravilno povezani sa aktivnostima.

    ### 7. Pokretanje i provjera rezultata

    Klikni **Pokreni optimizaciju**. U tabeli rasporeda svaka kolona predstavlja jednu smjenu, profil i konkretnog radnika. Tabela aktivnosti po intervalu poredi **Zahtevano** i **Raspoređeno**. Ako se vrijednosti razlikuju, provjeri potražnju, dozvoljene profile, trajanje smjena i ograničenja.

    """,
        
        # Results
        "run_optimization": "Run Optimization",
        "optimization_results": "Optimization Results",
        "no_results": "No results yet. Run the optimization to see results.",
        "status": "Status",
        "optimal_value": "Optimal Value",
        "schedule": "Schedule",
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "success": "Success",
        "optimal_objective_value": "Optimal Objective Value",
        "solver_status_optimal": "Solver Status: Optimal",
        "part_1_cost": "Part 1 (worker cost)",
        "part_2_penalty": "Number of switches from one activity to another",
        "part_2_weighted": "Part 2 weighted (P * part 2)",
        "total_active_shifts": "Total active shifts",
        "full_time": "Full-time",
        "part_time": "Part-time",
        "total_workers": "Total workers",
        "with_full_time": "With full-time work",
        "with_part_time": "With part-time work",
        "total_idle_intervals": "Total idle intervals",
        "employees_per_shift": "Employees per Shift and Profile (ytj)",
        "shift_allocation_timetable": "Shift Allocation Timetable",
        "export_schedule_excel": "Export schedule to Excel",
        "total_activities_per_interval": "Total activities per interval (Demanded vs. Realized)",
        "additional_results_analysis": "Additional Results Analysis",
        "show_activity_sequences": "Show Activity Sequences Analysis",
        "show_nonzero_pulp_variables": "Show all PuLP variables with non-zero values",
        "all_nonzero_variables": "All Non-Zero PuLP Variables",
        "no_shift_assignments": "No shift assignments were generated.",
        "actual": "actual",
        "max": "max",
        "demanded": "Demanded",
        "allocated": "Allocated",
        "interval_hour": "Interval (Hour)",
        "edit_demand_per_interval": "Edit Demand per Interval",
        "no_demand_data_dummy": "No demand data available. Using dummy data.",
        "dummy_activity": "Dummy Activity",
        "running_optimization": "Running optimization with current parameters.",
        "solving_optimization": "Solving optimization problem...",
    },
    "sr": {
        # App titles and headers
        "app_title": "Optimizacija raspoređivanja radnika",
        "model_parameters": "Parametri modela",
        "schedule_page": "Raspored",
        "instructions_page": "Uputstvo",
        "about_page": "O aplikaciji",
        "about_content": r"""
Aplikacija je nastala iz potrebe za rješavanjem problema raspoređivanja radnika u jednom realnom distributivnom skladištu. Zahvaljujući primijenjenom pristupu problemu, aplikacija se može koristiti za rješavanje sličnih problema i u drugim radnim okruženjima. Bazira se na matematičkom modelu predstavljenom u radu Popović i ostali (2021), objavljenom u časopisu *Sustainability*, koji prema podacima sa ResearchGate-a do sada ima 48 citata. Takođe, taj model je korišćen i u doktorskoj disertaciji Vlade Popovića pod nazivom *Optimizacija logističkih procesa u distribuciji proizvoda*.

Primijenjeni pristup problemu raspoređivanja radnika podrazumijeva da se svi poslovi posmatraju kao aktivnosti koje tokom radnog dana zahtijevaju određeni broj radnika. Potreban broj radnika za obavljanje pojedine aktivnosti može biti različit u toku dana. Radni dan se u aplikaciji može podijeliti na duže ili kraće vremenske intervale i za svaki od njih definisati potreban broj radnika po aktivnostima.

Kada je definisana potražnja, zadatak ostaje odrediti potreban broj radnika i njihov raspored tako da budu zadovoljene potrebe svih aktivnosti, uz istovremeno poštovanje definisanih ograničenja i minimiziranje troškova radne snage. Matematički model i definicije njegovih činilaca dati su u nastavku.

## Matematički model

Matematički model je ILP model koji ima sljedeću formu:

$$
\kern-6em
\begin{aligned}
\min\quad
&\sum_{j\in M}\sum_{t\in T} c_t y_{tj}
+ P\sum_{t\in T}\sum_{j\in M}\sum_{a\in A}\sum_{i\in N}\delta_{tija}
&&\text{(1)}
\end{aligned}
$$

$$
\kern-6em
\begin{aligned}
\sum_{j\in M}\sum_{k=i}^{u}x_{aijk}b_{kj} &= d_{ai},
\quad\forall i\in N,\ \forall a\in B\cap A_1,\quad
u=\min(i+v_a,n) &&\text{(2)}\\
\sum_{j\in M}\sum_{k=i}^{r_a}x_{aijk}b_{kj} &= d_{ai},
\quad\forall i\in N,\ \forall a\in B\cap A_2 &&\text{(3)}\\
\sum_{j\in M}\sum_{k=i}^{u}x_{aijk}b_{kj}
&\ge \displaystyle\sum_{a'\in G_a}s_{a'}\sum_{j\in M}\sum_{i\in N}x_{aijk},
\quad\forall k\in N,\ \forall a\in C\cap A_1,\quad
u=\min(k+v_a,n) &&\text{(4)}\\
\sum_{j\in M}\sum_{k=i}^{r_a}x_{aijk}b_{kj}
&\ge \displaystyle\sum_{a'\in G_a}s_{a'}\sum_{j\in M}\sum_{i\in N}x_{aijk},
\quad\forall k\in N,\ \forall a\in C\cap A_2 &&\text{(5)}\\
\sum_{i=1}^{k}x_{aijk}
&=\sum_{t\in T_a}y_{tija},
\quad\forall k\in N,\ \forall j\in M,\ \forall a\in A &&\text{(6)}\\
\sum_{a\in H_t}y_{tija}
&\le y_{tj},
\quad\forall i\in N,\ \forall j\in M,\ \forall t\in T &&\text{(7)}\\
\sum_{t\in T}\sum_{j\in M}\sum_{a\in A}y_{tija}
&\le q,
\quad\forall i\in N &&\text{(8)}\\
\sum_{i\in O_j}\sum_{a\in H_t}y_{tija}b_{ij}
&\le \left(f-\frac{p}{h}\right)y_{tj},
\quad\forall t\in T,\ \forall j\in M_1 &&\text{(9)}\\
\sum_{j\in M_2}y_{tj}
&\le w\sum_{j\in M}y_{tj},
\quad\forall t\in T &&\text{(10)}\\
\sum_{t\in T}y_{tj}
&\le \text{bignumber}\,y_j,
\quad\forall j\in M &&\text{(11)}\\
\sum_{j\in M_1}y_j &\le s_1^{\max} &&&&\text{(12)}\\
\sum_{j\in M_2}y_j &\le s_2^{\max} &&&&\text{(13)}\\
\sum_{i\in N}\sum_{a\in E_t}y_{tija}b_{ij}
&\le e\sum_{i\in N}\sum_{a\in H_t}y_{tija}b_{ij},
\quad\forall t\in T,\ \forall j\in M &&\text{(14)}\\
\sum_{a\in E_t}y_{tija}&=0,
\quad\forall t\in T,\ \forall i\in N,\ \forall j\in M &&\text{(15)}\\
\delta_{tija}&=y_{tija}-y_{t(i+1)ja},
\quad\forall t\in T,\ \forall j\in M,\ \forall a\in A,\ 
\forall i\in N\cap\max(N) &&\text{(16)}\\
&\text{integer:}\quad x_{aijk},\ y_{tija},\ y_{tj},\ y_j,\ \delta_{tija},
\quad\forall i\in N,\ \forall j\in M,\ \forall a\in A,\ \forall t\in T,\ \forall k\in N &&\text{(17)}
\end{aligned}
$$

Funkcija cilja (1) teži da minimizira troškove radne snage. Ograničenja (2, 3, 4, 5) osiguravaju da se zahtjevi za radnicima ispune u predviđenom vremenu. Ograničenje (6) reguliše da ukupan broj radnika koji obavlja neku aktivnost u nekom intervalu bude jednak predviđenom broju radnika tog profila u tom intervalu. Ograničenje (7) reguliše da ukupan broj radnika nekog profila u nekom intervalu angažovanih na svim aktivnostima ne može biti veći od ukupnog broja radnika tog profila u smjeni. Ograničenje (8) reguliše da ukupan broj radnika koji radi u skladištu ne može da bude veći od maksimalnog dozvoljenog broja radnika u bilo kom intervalu radnog dana.

Ograničenje (9) osigurava da svaki radnik ima odmor predviđene dužine u definisanom vremenu. Ograničenje (10) sprječava prevelik broj radnika u smjenama sa skraćenim radnim vremenom i obezbjeđuje da udio radnika određenog profila raspoređenih u takve smjene ne prelazi zadati procenat ukupnog broja radnika tog profila u svim smjenama. Ograničenje (11) obezbjeđuje podatak o broju radnika u smjeni bez obzira na profil. Ograničenjima (12 i 13) definiše se željeni maksimalni broj smjena sa punim i skraćenim radnim vremenom. Ograničenje (14) reguliše vrijeme provedeno u obavljanju aktivnosti koje nisu primarne određenom profilu. Ograničenje (15) obezbjeđuje da radnici određenog profila ne mogu biti dodijeljeni aktivnostima za koje nisu osposobljeni. Ograničenje (16) registruje prelazak sa obavljanja aktivnosti u jednom intervalu na neobavljanje iste aktivnosti u narednom intervalu, odnosno prelazak na drugu aktivnost ili odmor. Ograničenje (17) definiše prirodu promjenljivih.

## Tabela 4.1. Ulazi i izlazi matematičkog modela

### Ulazi

| Oznaka | Opis |
|---|---|
| `N` | Skup intervala radnog dana |
| `M` | Skup svih smjena |
| `M1` | Skup smjena sa punim radnim vremenom |
| `M2` | Skup smjena sa skraćenim radnim vremenom |
| `s1` | Maksimalni broj smjena sa punim radnim vremenom |
| `s2` | Maksimalni broj smjena sa skraćenim radnim vremenom |
| `n` | Redni broj posljednjeg intervala radnog dana |
| `bkj` | Parametar sa vrijednošću 1 ako je interval `k∈N` dio smjene `j∈M`, a 0 u suprotnom |
| `A` | Skup svih aktivnosti |
| `B` | Skup nezavisnih aktivnosti |
| `C` | Skup zavisnih aktivnosti |
| `$G_a$` | Skup aktivnosti od kojih aktivnost `$a\in C$` zavisi |
| `dai` | Potrebe za radnicima aktivnosti `a` u intervalu `i` |
| `$s_{a'}$` | Procenat zavisnosti aktivnosti `$a\in C$` od aktivnosti `$a'\in G_a$` |
| `A1` | Skup aktivnosti sa vremenskim prozorom kao rokom za završetak |
| `va` | Veličina vremenskog prozora za završetak aktivnosti `a∈A1`, u intervalima |
| `A2` | Skup aktivnosti sa rokom predstavljenim rednim brojem intervala do kada se moraju obaviti |
| `ra` | Interval do koga se mora zadovoljiti potreba za radnicima aktivnosti `a∈A2` |
| `T` | Skup svih profila radnika |
| `Ta` | Skup svih profila radnika kojima je dozvoljeno da obavljaju aktivnost `a` |
| `Ht` | Skup svih aktivnosti koje radnik profila `t∈T` može da obavlja |
| `Et` | Skup aktivnosti koje nisu primarne za radnika profila `t∈T` |
| `ct` | Trošak radnika profila `t` |
| `q` | Maksimalni dozvoljeni broj radnika koji može raditi u isto vrijeme |
| `p` | Trajanje pauze, u vremenskim jedinicama |
| `h` | Trajanje intervala, u vremenskim jedinicama |
| `f` | Veličina vremenskog prozora, u intervalima |
| `Oj` | Skup intervala dozvoljenih za pauzu u smjeni `j∈M1` |
| `w` | Maksimalno dozvoljeni procenat radnika sa skraćenim radnim vremenom |
| `e` | Maksimalno dozvoljeni udio vremena provedenog na neprimarnim aktivnostima |
| `P` | Značaj smanjenja promjena aktivnosti |

### Izlazi

| Oznaka | Opis |
|---|---|
| `yj` | Ukupan broj radnika u smjeni `j∈M` |
| `ytj` | Broj radnika profila `t∈T` dodijeljenih smjeni `j∈M` |
| `ytija` | Broj radnika profila `t∈T` dodijeljenih aktivnosti `a∈A` u intervalu `i∈N` smjene `j∈M` |
| `xaijk` | Broj radnika dodijeljenih intervalu `i∈N` smjene `j∈M` da ispuni potrebu aktivnosti `a∈A` iz intervala `k∈N` |
| `δtija` | Nenegativna promjenljiva koja označava prekid obavljanja aktivnosti `a` od strane radnika profila `t` u smjeni `j`, pri prelasku iz intervala `i` u interval `i+1` |
| `bignumber` | Veliki broj |
""",
        
        # General Parameters
        "general_parameters": "Radnici i aktivnosti",
        "short_duration_penalty": "Koeficijent troška prebrzog mijenjanja aktivnosti",
        "num_profiles": "Broj profila radnika",
        "num_activities": "Broj aktivnosti",
        "remove_profiles": "Ukloni tipove profila radnika",
        "remove_activities": "Ukloni tipove aktivnosti",
        "remove_profile_help": "Ukloni ovaj profil radnika iz aplikacije.",
        "remove_activity_help": "Ukloni ovu aktivnost iz aplikacije.",
        "choose_activities": "Odaberi aktivnosti",
        "define_profile_names": "Definiši imena profila i kratke kodove",
        "define_activity_names": "Definiši imena aktivnosti i kratke kodove",
        "full_name_for": "Puno ime",
        "short_code_for": "Kod",
        
        # Interval and Shift Sets
        "interval_shift_sets": "Intervali i smjene",
        "start_working_day": "Početak radnog dana (h):",
        "full_time_shift_length": "Dužina smjene za puno radno vrijeme (u intervalima):",
        "half_time_shift_length": "Dužina smjene za nepuno radno vrijeme (u intervalima):",
        "interval_duration": "Trajanje jednog intervala (u minutama):",
        "rest_duration": "Trajanje pauze (u minutama):",
        "m2_shift_start": "Početak M2 smjene (broj intervala):",
        "m1_set_label": "Skup smijena sa punim radnim vremenom",
        "m2_set_label": "Skup smijena sa nepunim radnim vremenom",
        "m1_set_help": "Skup se automatski popunjava prema dužini pune smjene i broju raspoloživih intervala. Na primjer, ako je dostupno 9 intervala, a puna smjena traje 8 intervala, postoje dvije smjene. Ako interval traje sat vremena i radni dan počinje u 8, prva počinje u 8, a druga u 9. Svaka se može obrisati, a sve su iste dužine.",
        "m2_set_help": "Skup se automatski popunjava prema dužini nepune smjene i broju raspoloživih intervala. Smjene počinju od oznake 51 nadalje; broj 5 na početku služi da se razlikuju od smjena sa punim radnim vremenom. Sve su iste dužine.",
        "m_set_label": "Skup svih smijena ",
        "m_set_help": "Sadrži sve pune i nepune smjene, zbog pregleda",
        "oj_intervals_label": "Intervali dostupni za odmor",
        "intervals_for_shift": "Intervali za smjenu",
        "oj_help_prefix": "Intervali dostupni za odmor u smjeni",
        "min_len_label": "Minimalna dužina uzastopnih aktivnosti (cijeli broj):",
        "min_len_help": "Minimalna dužina sekvence aktivnosti koja se prikazuje u dodatnoj analizi rezultata. Ovaj parametar ne utiče na raspored; na raspored utiče koeficijent troška promjene aktivnosti ako je veći od 0.",
        "p_help_transition_penalty": "Množi se sa brojem prelazaka. Dobijena vrijednost se dodaje funkciji cilja.",
        "num_profiles_help": "Broj različitih profila radnika (npr. komisioner, kontrolor, viljuškarista).",
        "num_activities_help": "Broj različitih tipova aktivnosti koje radnici mogu obavljati.",
        "profile_full_name_help": "Puno opisno ime za ovaj tip profila radnika.",
        "profile_short_code_help": "Skraćenica ili kod za ovaj profil radnika (koristi se u tabelama i izvještajima).",
        "activity_full_name_help": "Puno opisno ime za ovu vrstu aktivnosti.",
        "activity_short_code_help": "Skraćenica ili kod za ovu aktivnost (koristi se u tabelama i izvještajima).",
        "display_start_interval_help": "Početni sat za prikazivanje vremenskih intervala u rasporedu (npr. 8 znači da intervali počinju od 8:00).",
        "full_time_shift_length_help": "Dužina smjene sa punim radnim vremenom izražena u broju intervala.",
        "half_time_shift_length_help": "Dužina smjene sa nepunim radnim vremenom izražena u broju intervala.",
        "interval_duration_help": "Trajanje svakog vremenskog intervala u minutama (npr. 30 za 30 minuta, 60 za 1 sat).",
        "rest_duration_help": "Trajanje odmora u minutama (npr. 30 za 30 minuta, 60 za 1 sat).",
        "num_intervals_label": "Broj intervala u 24h:",
        "num_intervals_help": "Koliko intervala se radi u 24h, tj. koliko traje radno vrijeme u intervalima",
        "oj_intervals_help": "Za svaku smjenu sa punim radnim vremenom unesi redne brojeve intervala u kojima je dozvoljena pauza. Važi samo za smjene sa punim radnim vremenom.",
        "ind_within_help": "Aktivnosti čiji zahtjevi za radnicima se moraju ispuniti u okviru zadatog broja intervala.",
        "ind_until_help": "Aktivnosti čiji zahtjevi za radnicima se moraju ispuniti do zadatog intervala dana.",
        "dependent_within_help": "Aktivnosti čiji zahtjevi za radnicima zavise od realizacije drugih aktivnosti, a potrebno je realizovati ih u okviru datog broja intervala.",
        "dependent_until_help": "Aktivnosti čiji zahtjevi za radnicima zavise od realizacije drugih aktivnosti, a potrebno je realizovati ih do zadatog intervala dana.",
        "no_dependent_within_selected": "Nema odabranih zavisnih aktivnosti u dep_within. Dodaj ID-e aktivnosti iznad da postaviš vrednosti.",
        "no_dependent_until_selected": "Nema odabranih zavisnih aktivnosti u dep_until. Dodaj ID-e aktivnosti iznad da postaviš vrednosti.",
        "within_help": "Maksimalan broj intervala dozvoljen za završetak aktivnosti '{activity}'.",
        "until_help": "Najkasniji interval do kojeg aktivnost '{activity}' mora biti završena, ne uključujući njega.",
        "select_demand_profile_help": "Odaberi unaprijeded definisani obrazac potražnje da počneš. Možeš potom uređivati vrijednosti u tabeli ispod.",
        "dep_within_values_header": "\"U okviru\" vrijednosti",
        "dep_within_value_label": "Vrijednost \"u okviru\"",
        "dep_until_value_label": "Vrijednost \"do\"",
        "dep_ratio_prompt": "Unesi odnos '{dependent}' - '{depends_on}'",
        "dependency_activity_help": "Odaberi nezavisnu aktivnost čija realizacija određuje potreban broj radnika za aktivnost '{activity}'.",
        "dependency_ratio_help": "Koeficijent pokazuje zavisnost potrebnog broja radnika za zavisnu aktivnost '{dependent}' od raspoređenog broja radnika za nezavisnu aktivnost '{depends_on}'. Na primjer, sa koeficijentom 0.5, ako je za '{depends_on}' u nekom intervalu raspoređeno 6 radnika, za '{dependent}' su potrebna najmanje 3 radnika.",
        "dep_until_values_header": "\"Do\" vrijednosti",
        "max_workers_per_interval_help": "Maksimalan broj radnika koji se mogu dodijeliti za rad u jednom vremenskom intervalu. Ovo ograničenje sprečava pretrpanost i garantuje sigurnost.",
        "max_m1_shifts_help": "Maksimalan broj smijena sa punim radnim vremenom koje se mogu izabrati.",
        "max_m2_shifts_help": "Maksimalan broj smijena sa nepunim radnim vremenom koje se mogu izabrati.",
        "m2_ratio_limit_help": "Maksimalni udio smijena sa nepunim radnim vremenom u ukupnom broju aktivnih smijena. Na primjer, 0.3 znaci da maksimalno 30% smjena može biti sa nepunim radnim vremenom.",
        "istovar_kontrola_ratio_help": "Odnos radnika za kontrolu u odnosu na radnike koji obavljaju istovar.",
        "non_primary_activities_ratio_help": "Maksimalni udio sporednih aktivnosti koje radnici pune smjene mogu obavljati. Gleda se odnos broja intervala u kojima radnici obavljaju sporedne aktivnosti i ukupnog broja intervala u kojima radi.",
        "error_parsing_list": "Greška pri parsiranju liste: '{input_str}'. Provjeri da li su svi elementi tipa {item_type}.",
        "error_parsing_json": "Greška pri parsiranju JSON-a: {error}. Provjeri da li je unos validan JSON.",
        "comma_separated_integers": "(brojevi odvojeni zarezima)",
        
        # Cost Coefficients
        "cost_coefficients": "Troškovi",
        "cost_for_m1": "Trošak za M1 (puno radno vreme) za",
        "cost_for_m2": "Trošak za M2 (nepuno radno vrijeme) za",
        "full_time_label": "puna",
        "part_time_label": "nepuna",
        "m1_cost_rates": "Koeficijenti troškova za smjene sa punim radnim vremenom",
        "m2_cost_rates": "Koeficijent troškova za smjene sa nepunim radnim vremenom",
        "m1_cost_help": "Cijena za smjenu sa punim radnim vremenom za",
        "m2_cost_help": "Cijena za smjenu sa nepunim radnim vremenom za",
        "working_full_time": "",
        "working_part_time": "",
        
        # Role-Activity Mappings
        "role_activity_mappings": "Mapiranje uloga i aktivnosti",
        "allowed_activities_per_role": "Dozvoljeni profili po aktivnostima",
        "profiles_for": "Profili za",
        "able_activities_per_profile": "Pregled aktivnosti koje profili mogu da obavljaju",
        "activities_for": "Aktivnosti profila",
        "primary_able_activities": "Primarne aktivnosti po profilu",
        "primary_activities_for": "Primarne aktivnosti za",
        "select_which_workers": "Odaberi profile radnika koji mogu obavljati",
        "select_which_activities": "Odaberi koje aktivnosti",
        "select_primary_activities_for": "Odaberi primarne aktivnosti za",
        "workers_are_able": "Radnici mogu obaviti",
        "can_perform_primary": "Mogu obaviti kao primarni rad",
        
        # Variant-Dependent Parameters
        "variant_dependent_parameters": "Tipovi aktivnosti",
        "ind_within": "Izaberi nezavisne aktivnosti tipa \"u okviru\"",
        "ind_until": "Izaberi nezavisne aktivnosti tipa \"do\"",
        "within_values": "\"U okviru\" vrijednosti",
        "until_values": "\"Do\" vrijednosti",
        "within_value": "Vrijednost \"u okviru\"",
        "until_value": "Vrijednost \"do\"",
        "independent_activities": "Nezavisne aktivnosti:",
        "no_activities_ind_within": "Nema odabranih nezavisnih aktivnosti \"u okviru\". Dodaj aktivnosti iznad da postaviš \"u okviru\" vrijednosti.",
        "no_activities_ind_until": "Nema odabranih nezavisnih aktivnosti \"do\". Dodaj aktivnosti iznad da postaviš \"do\" vrijednosti.",
        "dependent_activities": "Zavisne aktivnosti:",
        "dep_within": "Izaberi zavisne aktivnosti tipa \"u okviru\"",
        "dep_until": "Izaberi zavisne aktivnosti tipa \"do\"",
        "no_activities_dep_within": "Nema odabranih zavisnih aktivnosti u dep_within.",
        "no_activities_dep_until": "Nema odabranih zavisnih aktivnosti u dep_until.",
        "error_overlap": "Greška: Aktivnost je oba tipa i 'u okviru' i 'do:",
        "activity_type_required": "Aktivnosti '{activity}' mora biti određen jedan tip: u okviru, do, zavisna u okviru ili zavisna do.",
        "activity_type_multiple": "Aktivnost '{activity}' pripada više tipova. Odaberi samo jedan tip.",
        "activity_value_required": "Unesi vrijednost za '{value_type}' za aktivnost '{activity}'.",
        "activity_profile_required": "Aktivnosti '{activity}' mora biti dodijeljen bar jedan profil radnika koji može da je obavlja.",
        "until_value_exceeds_intervals": "Vrijednost 'do' {value} za aktivnost '{activity}' veća je od najveće dozvoljene vrijednosti {max_interval}. Pošto se krajnji interval ne uključuje, pomjeri vrijednost u dozvoljeni raspon.",
        "select_activity_depends_on": "Odaberi aktivnost od koje",
        "depends_on": "zavisi",
        
        # Demand Data
        "demand_data": "Potražnja",
        "select_demand_profile": "Odaberi profil potražnje",
        "demand_example_1": "Primjer 1",
        "demand_example_2": "Primjer 2",
        "custom_demand": "Prilagođena potražnja",
        "demand_for": "Potražnja za",
        "enter_comma_separated": "Unesi vrijednosti potražnje odvojene zarezima za svaki interval",
        
        # Constraint Parameters
        "constraint_parameters": "Parametri ograničenja",
        "max_workers_per_interval": "Maksimalni broj radnika po intervalu",
        "max_m1_shifts": "Maksimalni broj smijena sa punim radnim vremenom",
        "max_m2_shifts": "Maksimalni broj smijena sa nepunim radnim vremenom",
        "non_primary_activities_ratio": "Maksimalni udio sporednih aktivnosti radnika",
        "m2_ratio_limit": "Maksimalni udio smijena sa nepunim radnim vremenom",
        "max_number_of": "Maksimalan broj",
        "instructions": "Uputstvo",
        "instructions_content": """
    ### Sidebar sekcije

    **Radnici i aktivnosti** - Definiše profile radnika i aktivnosti koje se koriste u rasporedu.
    - **Broj profila radnika**: Određuje koliko tipova profila radnika postoji.
    - **Broj aktivnosti**: Određuje koliko tipova aktivnosti može biti raspoređeno.
    - **Puno ime**: Definiše opisni naziv profila ili aktivnosti.
    - **Kod**: Definiše kratku oznaku koja se prikazuje u rasporedu i izvještajima.

    **Intervali i smjene** - Definiše vremenski horizont i početke punih i nepunih smjena.
    - **Početak radnog dana**: Određuje početni sat za prikaz vremena intervala.
    - **Dužina pune smjene**: Definiše broj intervala u M1 smjeni.
    - **Dužina nepune smjene**: Definiše broj intervala u M2 smjeni.
    - **Trajanje jednog intervala**: Definiše trajanje planskog intervala u minutama.
    - **Trajanje pauze**: Definiše koliko minuta traje pauza.
    - **Broj intervala u 24h**: Definiše ukupni planski horizont.
    - **Skup smjena sa punim radnim vremenom**: Automatski se popunjava prema dužini pune smjene i broju raspoloživih intervala. Smjene se mogu brisati, a sve su iste dužine.
    - **Skup smjena sa nepunim radnim vremenom**: Automatski se popunjava prema dužini nepune smjene i broju raspoloživih intervala. Počinje od oznake 51, čiji početni broj 5 razlikuje nepune smjene od punih; sve su iste dužine.
    - **M_set**: Prikazuje sve smjene dobijene iz M1_set i M2_set.
    - **Intervali dostupni za odmor**: Za svaku smjenu sa punim radnim vremenom navodi redne brojeve intervala u kojima je dozvoljena pauza.
    - **Minimalna dužina uzastopnih aktivnosti**: Određuje minimalnu dužinu sekvenci u dodatnoj analizi rezultata; ne utiče na raspored.

    **Troškovi** - Definiše relativni trošak dodjele svakog profila punim i nepunim smjenama.
    - **Koeficijent troška M1**: Definiše relativni trošak pune smjene za profil.
    - **Koeficijent troška M2**: Definiše relativni trošak nepune smjene za profil.
    - **Koeficijent troška prebrzog mijenjanja aktivnosti**: Ako je veći od 0, model kažnjava promjene aktivnosti, pa koeficijent utiče na raspored.

    **Mapiranje uloga i aktivnosti** - Definiše koje profile mogu obavljati aktivnosti i koje su aktivnosti primarne.
    - **Profili za aktivnost**: Bira profile kojima je dozvoljeno obavljanje aktivnosti.
    - **Primarne aktivnosti po profilu**: Definiše aktivnosti koje su primarne za profil.

    **Tipovi aktivnosti** - Nezavisne aktivnosti imaju potražnju unesenu u početnu tabelu. Potražnja za zavisne aktivnosti računa se prema broju raspoređenih radnika na povezanoj aktivnosti i zadatom odnosu (npr. 50% kontrole u odnosu na 4 radnika za utovar znači najmanje 2 radnika za kontrolu). Ovdje se definišu i vremenska pravila aktivnosti.
    - **Aktivnosti i vrijednosti "u okviru"**: Zahtijeva da se aktivnost pokrije u zadanom broju intervala.
    - **Aktivnosti i vrijednosti "do"**: Zahtijeva da se aktivnost pokrije do zadanog intervala.
    - **Zavisne aktivnosti**: Definiše aktivnosti čija potražnja zavisi od druge aktivnosti.
    - **Odnos zavisnosti**: Definiše koliko zavisne aktivnosti treba obezbijediti po jedinici izvorne aktivnosti.

    **Potražnja** - Bira primjer i omogućava unos potrebnog broja radnika po aktivnosti i intervalu.
    - **Profil potražnje**: Bira početni obrazac potražnje.
    - **Ulazna tabela potražnje**: Definiše potreban broj radnika, gdje su aktivnosti kolone, a vremenski intervali redovi.

    **Parametri ograničenja** - Ograničava broj radnika, broj smjena, odnos smjena i sporedni rad.
    - **Maks radnika po intervalu**: Ograničava ukupan broj radnika raspoređenih u jednom intervalu.
    - **Maks M1 smjena**: Ograničava broj punih smjena.
    - **Maks M2 smjena**: Ograničava broj nepunih smjena.
    - **Granica M2 odnosa**: Ograničava udio nepunih smjena među svim smjenama.
    - **Odnos sporednih aktivnosti**: Ograničava udio sporednog rada kod M1 radnika.

    ### Tabele

    **Ulazna tabela - Potražnja po intervalu**: U njoj se prije optimizacije unosi potreban broj radnika za svaku aktivnost i vremenski interval.

    **Izlazna tabela - Tabela rasporeda smjena**: Prikazuje generisani raspored, a svaka kolona predstavlja smjenu, profil i konkretnog radnika.

    **Izlazna tabela - Ukupne aktivnosti po intervalu**: Upoređuje traženi i raspoređeni broj radnika za svaku aktivnost i interval.
    """,
        
        # Results
        "run_optimization": "Pokreni optimizaciju",
        "optimization_results": "Rezultati optimizacije",
        "no_results": "Nema rezultata. Pokreni optimizaciju da vidiš rezultate.",
        "status": "Status",
        "optimal_value": "Optimalna vrednost",
        "schedule": "Raspored",
        "error": "Greška",
        "warning": "Upozorenje",
        "info": "Info",
        "success": "Uspješno",
        "optimal_objective_value": "Optimalna vrijednost funkcije",
        "solver_status_optimal": "Status rješavača: Optimalno",
        "part_1_cost": "Dio 1 (trošak radnika)",
        "part_2_penalty": "Broj prelazaka sa aktivnosti na aktivnost",
        "part_2_weighted": "Dio 2 (trošak prelazaka)",
        "total_active_shifts": "Ukupan broj aktivnih smijena",
        "full_time": "Puno radno vrijeme",
        "part_time": "Nepuno radno vrijeme",
        "total_workers": "Ukupan broj radnika",
        "with_full_time": "Sa punim radnim vremenom",
        "with_part_time": "Sa nepunim radnim vremenom",
        "total_idle_intervals": "Ukupan broj neradnih intervala",
        "employees_per_shift": "Izabrane smjene i radnici",
        "shift_allocation_timetable": "Raspored rada",
        "export_schedule_excel": "Izvezi raspored u Excel",
        "total_activities_per_interval": "Ukupne aktivnosti po intervalu (zahtjevano vs. raspoređeno)",
        "additional_results_analysis": "Dodatna analiza rezultata",
        "show_activity_sequences": "Prikaži analizu sekvenci aktivnosti",
        "show_nonzero_pulp_variables": "Prikaži sve PuLP promenljive sa nenula vrijednostima",
        "all_nonzero_variables": "Sve nenula PuLP promjenljive",
        "no_shift_assignments": "Nisu generisani radni raspored.",
        "actual": "Stvarni",
        "max": "Maks",
        "demanded": "Zahtevano",
        "allocated": "Raspoređeno",
        "interval_hour": "Interval (Sat)",
        "edit_demand_per_interval": "Uredi potražnju po intervalu",
        "no_demand_data_dummy": "Nema podataka o potražnji. Koristi se zamjenski skup podataka.",
        "dummy_activity": "Zamjenska aktivnost",
        "running_optimization": "Pokreće se optimizacija sa trenutnim parametrima.",
        "solving_optimization": "Rješava se problem optimizacije...",
    }
}

TRANSLATIONS["sr"]["instructions_content"] = TRANSLATIONS["en"]["instructions_content"]

def get_text(key, language="sr"):
    """Get translated text for a given key and language."""
    if language not in TRANSLATIONS:
        language = "sr"  # Default to Serbian
    return TRANSLATIONS[language].get(key, key)
