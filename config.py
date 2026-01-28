# Configuration and default values for the optimization model

# Default number of profiles and activities
DEFAULT_NUM_PROFILES = 3
DEFAULT_NUM_ACTIVITIES = 6

# Default profile and activity names
DEFAULT_FULL_PROFILE_NAMES = {
    'profil1': 'Komisioner',
    'profil2': 'Kontrolor',
    'profil3': 'Viljuskarista'
}

DEFAULT_FULL_ACTIVITY_NAMES = {
    'activity1': 'Komisioniranje1',
    'activity2': 'Komisioniranje2',
    'activity3': 'Komisioniranje3',
    'activity4': 'Kontrola',
    'activity5': 'Utovar',
    'activity6': 'Istovar'
}

# Short codes
DEFAULT_SHORT_ACTIVITIES = {
    'activity1': "k1",
    'activity2': 'k2',
    'activity3': 'k3',
    'activity5': 'ut',
    'activity6': 'is',
    'activity4': 'ka'
}

DEFAULT_SHORT_PROFILES = {
    'profil1': "ks",
    'profil2': "kr",
    'profil3': "vi"
}

# Interval and shift sets
DEFAULT_OJ = {1: [4, 5, 6], 2: [5, 6, 7], 3: [6, 7, 8]}
DEFAULT_N_SET = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
DEFAULT_M_SET = [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]
DEFAULT_M1_SET = [1, 2, 3]
DEFAULT_M2_SET = [6, 7, 8, 9, 10, 11, 12, 13]

# Cost rates
DEFAULT_CT_RATES = {
    ('profil1', 'm1'): 1.28, ('profil2', 'm1'): 1.6, ('profil3', 'm1'): 1.4,
    ('profil1', 'm2'): 0.64, ('profil2', 'm2'): 0.8, ('profil3', 'm2'): 0.7
}

# Role-activity mappings
DEFAULT_ALLOWED = {
    'activity1': ['profil1', 'profil2', 'profil3'],
    'activity2': ['profil1', 'profil2', 'profil3'],
    'activity3': ['profil1', 'profil2', 'profil3'],
    'activity4': ['profil2'],
    'activity5': ['profil3'],
    'activity6': ['profil3']
}

DEFAULT_ABLE = {
    'profil1': ['activity1', 'activity2', 'activity3'],
    'profil2': ['activity1', 'activity2', 'activity3', 'activity4'],
    'profil3': ['activity1', 'activity2', 'activity3', 'activity5', 'activity6']
}

DEFAULT_ABLE_NE = {
    'profil1': [],
    'profil2': ['activity1', 'activity2', 'activity3'],
    'profil3': ['activity1', 'activity2', 'activity3']
}

# Variant-dependent parameters
DEFAULT_IND_WITHIN = ['activity5', 'activity6']
DEFAULT_IND_UNTIL = ['activity1', 'activity2', 'activity3']
DEFAULT_DEP_WITHIN = ['activity4']
DEFAULT_WITHIN = {'activity5': 1, 'activity6': 2, 'activity4': 1}
DEFAULT_UNTIL = {'activity1': 5, 'activity2': 9, 'activity3': 12}

# Demand examples
DEMAND_EXAMPLE_1 = {
    'activity1': [0, 10, 11, 11, 12, 0, 0, 0, 0, 0, 0, 0],
    'activity2': [0, 0, 0, 0, 0, 12, 13, 10, 14, 0, 0, 0],
    'activity3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 12],
    'activity5': [0, 3, 2, 2, 0, 3, 3, 0, 2, 3, 0, 0],
    'activity6': [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    'activity4': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
}

DEMAND_EXAMPLE_2 = {
    'activity1': [0, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0],
    'activity2': [0, 0, 0, 0, 0, 10, 8, 7, 14, 0, 0, 0],
    'activity3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 13, 13],
    'activity5': [0, 3, 2, 2, 0, 2, 3, 0, 2, 2, 0, 0],
    'activity6': [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    'activity4': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
}

# Model constraints
MAX_WORKERS_PER_INTERVAL = 40
MAX_M1_SHIFTS = 3
MAX_M2_SHIFTS = 1
M2_RATIO_LIMIT = 0.3
NON_PRIMARY_ACTIVITIES_RATIO = 0.5
BALANCING_MAX_ITERATIONS = 1000
