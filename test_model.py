from pulp import LpProblem, LpMinimize, PULP_CBC_CMD, LpStatus
from config import *
from utils import parse_list
from ui_input import collect_variant_parameters
from model_builder import *
from results_display import *

# Set defaults
num_profiles = 3
num_activities = 6
profil_types = ['profil1', 'profil2', 'profil3']
activities = ['activity1', 'activity2', 'activity3', 'activity4', 'activity5', 'activity6']
activity_full_names = DEFAULT_FULL_ACTIVITY_NAMES
N_set = DEFAULT_N_SET
M_set = DEFAULT_M_SET
M1_set = DEFAULT_M1_SET
M2_set = DEFAULT_M2_SET
ct_m1_inputs = {'profil1': 1.28, 'profil2': 1.6, 'profil3': 1.4}
ct_m2_inputs = {'profil1': 0.64, 'profil2': 0.8, 'profil3': 0.7}
allowed = DEFAULT_ALLOWED
able = DEFAULT_ABLE
able_ne = DEFAULT_ABLE_NE
demand = DEMAND_EXAMPLE_1
max_workers = 20
max_m1 = 10
max_m2 = 10
P = 0
M2_RATIO_LIMIT = 0.5
NON_PRIMARY_ACTIVITIES_RATIO = 0.3
Oj = DEFAULT_OJ

# Get variant parameters - hardcoded for testing
ind_within = ['activity5', 'activity6']
ind_until = ['activity1', 'activity2', 'activity3']
dep_within = ['activity4']
within = {'activity5': 1, 'activity6': 2, 'activity4': 1}
until = {'activity1': 5, 'activity2': 9, 'activity3': 12}
overlap_activities = []
dependency_list = [{'dependent': 'activity4', 'depends_on': 'activity6', 'ratio': 0.5}]  # Back to activity6

# Build model
model = LpProblem("Worker_Scheduling", LpMinimize)
bij = build_bij_matrix(M_set, M1_set, M2_set, N_set)
ct = build_ct_matrix(M_set, M1_set, M2_set, profil_types, ct_m1_inputs, ct_m2_inputs)
yjz, yj, ytj, ytija, xaijk = build_model_variables(profil_types, M_set, M1_set, M2_set, N_set, activities)
delta = build_delta_variables(P, profil_types, M_set, N_set, activities)

# Objective
setup_objective_function(model, P, profil_types, M_set, N_set, ytj, delta, ct, activities)

# Constraints
add_demand_constraints(model, activities, N_set, M_set, ytija, demand, profil_types)
add_activity_within_constraints(model, ind_within, N_set, M_set, profil_types, activities, xaijk, bij, demand, within, able, activity_full_names)
add_activity_until_constraints(model, ind_until, N_set, M_set, xaijk, bij, demand, until, activity_full_names)
add_activity_dependency_ratio_constraints(model, dependency_list, N_set, M_set, xaijk, bij, within)
add_activity_allocation_constraints(model, activities, M_set, N_set, xaijk, ytija, bij, allowed)
add_worker_capacity_constraints(model, profil_types, N_set, M_set, ytj, ytija, able)
add_interval_worker_limit(model, activities, N_set, profil_types, M_set, ytija, max_workers)
add_rest_interval_constraints(model, M1_set, profil_types, ytj, ytija, activities, able, bij, Oj)
add_m2_ratio_constraint(model, profil_types, M2_set, M_set, ytj, M2_RATIO_LIMIT)
add_shift_constraints(model, M_set, M1_set, M2_set, ytj, profil_types, yj, max_m1, max_m2)
add_non_primary_activities_constraint(model, M1_set, profil_types, N_set, ytija, able, able_ne, bij, NON_PRIMARY_ACTIVITIES_RATIO)
add_m1_m2_ratio_per_interval_constraint(model, N_set, M1_set, M2_set, ytj, bij, profil_types)
add_delta_constraints(model, P, profil_types, M_set, N_set, activities, ytija, delta, able)

# Solve
model.solve(PULP_CBC_CMD(msg=1))

print(f"Solver Status: {LpStatus[model.status]}")
if model.status == 1:
    print("Optimal solution found")
    print(f"Objective value: {model.objective.value()}")
else:
    print("No feasible solution")