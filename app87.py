
import streamlit as st
from pulp import *
import random
import pandas as pd
from collections import defaultdict
import json # Added json import

st.set_page_config(layout="wide")
st.title("Optimization Model with PuLP and Streamlit")

# --- Helper Functions for Parsing ---
def parse_list(input_str, item_type=str):
    if not input_str.strip():
        return []
    try:
        return [item_type(x.strip()) for x in input_str.split(',') if x.strip()]
    except ValueError:
        st.error(f"Error parsing list: '{input_str}'. Please ensure all items are of type {item_type.__name__}.")
        return []

def parse_json_dict(input_str, default_value={}):
    if not input_str.strip():
        return default_value
    try:
        return json.loads(input_str)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {e}. Please ensure the input is valid JSON.")
        return default_value

# --- Default values for editable parameters ---
default_num_profiles = 3 # New default for number of profiles
default_profil_types = [f'profil{i+1}' for i in range(default_num_profiles)] # Generated
default_num_activities = 6 # New default for number of activities
default_activities = [f'activity{i+1}' for i in range(default_num_activities)] # Generated

# Default mappings from generic to descriptive names
default_full_profile_names = {'profil1': 'Komisioner', 'profil2': 'Kontrolor', 'profil3': 'Viljuskarista'}
default_full_activity_names = {
    'activity1': 'Komisioniranje1', 'activity2': 'Komisioniranje2', 'activity3': 'Komisioniranje3',
    'activity4': 'Kontrola', 'activity5': 'Utovar', 'activity6': 'Istovar'
}

# Default mappings for short names (using generic keys)
default_s = {'activity1': "k1", 'activity2': 'k2', 'activity3': 'k3', 'activity5': 'ut', 'activity6': 'is', 'activity4': 'ka'}
default_sp = {'profil1': "ks", 'profil2': "kr", 'profil3': "vi"}

default_Oj = {1: [4, 5, 6], 2: [5, 6, 7], 3: [6, 7, 8]}
default_N_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
default_M_set = [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]
default_M1_set = [1, 2, 3]
default_M2_set = [6, 7, 8, 9, 10, 11, 12, 13]

# Default ct rates keyed by generic profile types
default_ct_rates = {
    ('profil1', 'm1'): 1.28, ('profil2', 'm1'): 1.6, ('profil3', 'm1'): 1.4,
    ('profil1', 'm2'): 0.64, ('profil2', 'm2'): 0.8, ('profil3', 'm2'): 0.7
}

default_allowed = {
    'activity1': ['profil1', 'profil2', 'profil3'],
    'activity2': ['profil1', 'profil2', 'profil3'],
    'activity3': ['profil1', 'profil2', 'profil3'],
    'activity4': ['profil2'],
    'activity5': ['profil3'],
    'activity6': ['profil3']
}
default_able = {
    'profil1': ['activity1', 'activity2', 'activity3'],
    'profil2': ['activity1', 'activity2', 'activity3', 'activity4'],
    'profil3': ['activity1', 'activity2', 'activity3', 'activity5', 'activity6']
}
default_able_ne = {
    'profil1': [],
    'profil2': ['activity1', 'activity2', 'activity3'],
    'profil3': ['activity1', 'activity2', 'activity3']
}

#default_ind_within = ['activity5', 'activity6', 'activity1', 'activity2', 'activity3']
#default_ind_until = []
#default_dep_within = ['activity4']
#default_within = {'activity5': 1, 'activity6': 1, 'activity4': 1,'activity1': 1, 'activity2': 1, 'activity3': 1}
#default_until = {}

default_ind_within = ['activity5', 'activity6']
default_ind_until = ['activity1', 'activity2', 'activity3']
default_dep_within = ['activity4']
default_within = {'activity5': 1, 'activity6': 2, 'activity4': 1
                  }
default_until = {'activity1':5, 'activity2':9, 'activity3':12}

st.sidebar.header("Model Parameters")

with st.sidebar.expander("General Parameters"):
    P = st.number_input("Short-Duration Assignment Penalty", min_value=0.00, max_value=1.00,value=0.00, step=0.01, help="Weight of the transition penalty term in the objective function (P = 0 disables the penalty)."
    "P is multiplied by the number of activity changes occurring before the predefined minimum number of intervals.")

    num_profiles = st.number_input("Number of Worker Profiles", min_value=1, value=default_num_profiles, step=1)
    profil_types = [f'profil{i+1}' for i in range(num_profiles)] # Dynamically generate profil_types

    num_activities = st.number_input("Number of Activities", min_value=1, value=default_num_activities, step=1)
    activities = [f'activity{i+1}' for i in range(num_activities)] # Dynamically generate activities

    st.subheader("Define Profile Names and Short Codes:")
    profile_full_names = {}
    sp = {}
    for generic_profile_id in profil_types:
        default_full = default_full_profile_names.get(generic_profile_id, generic_profile_id.capitalize())
        profile_full_names[generic_profile_id] = st.text_input(f"Full name for '{generic_profile_id}'", value=default_full, key=f"full_name_profile_{generic_profile_id}")
        default_short = default_sp.get(generic_profile_id, generic_profile_id[0:2])
        sp[generic_profile_id] = st.text_input(f"Short code for '{generic_profile_id}'", value=default_short, key=f"short_code_profile_{generic_profile_id}")

    st.subheader("Define Activity Names and Short Codes:")
    s = {}
    activity_full_names = {}
    for generic_activity_id in activities:
        default_full = default_full_activity_names.get(generic_activity_id, generic_activity_id.capitalize())
        activity_full_names[generic_activity_id] = st.text_input(f"Full name for '{generic_activity_id}'", value=default_full, key=f"full_name_activity_{generic_activity_id}")
        default_short = default_s.get(generic_activity_id, generic_activity_id[0:2])
        s[generic_activity_id] = st.text_input(f"Short code for '{generic_activity_id}'", value=default_short, key=f"short_code_activity_{generic_activity_id}")


with st.sidebar.expander("Interval and Shift Sets"):
    # >>> NOVO: unos početka radnog dana (samo za prikaz)
    display_start_interval = st.number_input(
            "Početak radnog dana (prikaz intervala počinje od):",
            min_value=1,
            max_value=100,
            value=8,
            step=1,
            key="display_start_interval"
        )


    user_N_set_str = st.text_area("N_set (Intervals, comma-separated integers)", ', '.join(map(str, default_N_set)))
    N_set = parse_list(user_N_set_str, int)
    if not N_set:
        st.warning("N_set cannot be empty. Defaulting to [1, 2, ..., 11].")
        N_set = default_N_set # Fallback if user clears N_set

    user_M_set_str = st.text_area("M_set (Shifts, comma-separated integers)", ', '.join(map(str, default_M_set)))
    M_set = parse_list(user_M_set_str, int)
    if not M_set:
        st.warning("M_set cannot be empty. Defaulting to [1, 2, ..., 13].")
        M_set = default_M_set # Fallback if user clears M_set

    user_M1_set_str = st.text_area("M1_set (Full-time shifts, comma-separated integers)", ', '.join(map(str, default_M1_set)))
    M1_set = parse_list(user_M1_set_str, int)

    user_M2_set_str = st.text_area("M2_set (Part-time shifts, comma-separated integers)", ', '.join(map(str, default_M2_set)))
    M2_set = parse_list(user_M2_set_str, int)

    st.subheader("Oj (Intervals available for rest shift j, only for M1 shifts):")
    Oj = {}
    for j_shift in M1_set: # Only iterate over M1_set
        default_oj_intervals = default_Oj.get(j_shift, [])
        oj_intervals_str = st.text_area(
            f"Intervals for shift {j_shift} (comma-separated integers)",
            value=', '.join(map(str, default_oj_intervals)),
            key=f"Oj_{j_shift}"
        )
        Oj[j_shift] = parse_list(oj_intervals_str, int)


with st.sidebar.expander("Cost Coefficients (ct)"):
    st.write("Full-time shift (M1) cost rates:")
    ct_m1_inputs = {}
    for p_type in profil_types:
        default_rate = default_ct_rates.get((p_type, 'm1'), 1.0) # Fallback to 1.0 if not found
        ct_m1_inputs[p_type] = st.number_input(f"{profile_full_names.get(p_type, p_type)} (M1)", value=default_rate, key=f"ct_m1_{p_type}")

    st.write("Part-time shift (M2) cost rates:")
    ct_m2_inputs = {}
    for p_type in profil_types:
        default_rate = default_ct_rates.get((p_type, 'm2'), 0.5) # Fallback to 0.5 if not found
        ct_m2_inputs[p_type] = st.number_input(f"{profile_full_names.get(p_type, p_type)} (M2)", value=default_rate, key=f"ct_m2_{p_type}")


with st.sidebar.expander("Role-Activity Mappings"):
    st.subheader("Allowed Activities per Role (activities can be performed by selected profiles):")
    allowed = {}
    for generic_activity_id in activities:
        # Filter default_allowed to only include profil_types that are currently active
        default_selection_generic_ids = [pid for pid in default_allowed.get(generic_activity_id, []) if pid in profil_types]
        default_selection_full_names = [profile_full_names.get(pid, pid) for pid in default_selection_generic_ids]

        selected_full_names = st.multiselect(
            f"Profiles for '{activity_full_names.get(generic_activity_id, generic_activity_id)}'",
            options=[profile_full_names.get(p, p) for p in profil_types], # Display full names
            default=default_selection_full_names, # Default should use full names
            key=f"allowed_{generic_activity_id}"
        )
        # Map selected full names back to generic IDs for internal storage
        allowed[generic_activity_id] = [pid for full_name in selected_full_names for pid, pf_name in profile_full_names.items() if pf_name == full_name]

    st.subheader("Able Activities per Profile (profiles can perform selected activities):")
    able = {}
    for generic_profile_id in profil_types:
        # Filter default_able to only include activities that are currently active
        default_selection_generic_ids = [aid for aid in default_able.get(generic_profile_id, []) if aid in activities]
        default_selection_full_names = [activity_full_names.get(aid, aid) for aid in default_selection_generic_ids]

        selected_full_names = st.multiselect(
            f"Activities for '{profile_full_names.get(generic_profile_id, generic_profile_id)}'",
            options=[activity_full_names.get(a, a) for a in activities], # Display full names
            default=default_selection_full_names, # Default should use full names
            key=f"able_{generic_profile_id}"
        )
        # Map selected full names back to generic IDs for internal storage
        able[generic_profile_id] = [aid for full_name in selected_full_names for aid, af_name in activity_full_names.items() if af_name == full_name]

    st.subheader("Non-Primary Able Activities per Profile:")
    able_ne = {}
    for generic_profile_id in profil_types:
        # Filter default_able_ne to only include activities that are currently active
        default_selection_generic_ids = [aid for aid in default_able_ne.get(generic_profile_id, []) if aid in activities]
        default_selection_full_names = [activity_full_names.get(aid, aid) for aid in default_selection_generic_ids]

        selected_full_names = st.multiselect(
            f"Non-primary activities for '{profile_full_names.get(generic_profile_id, generic_profile_id)}'",
            options=[activity_full_names.get(a, a) for a in activities], # Display full names
            default=default_selection_full_names, # Default should use full names
            key=f"able_ne_{generic_profile_id}"
        )
        # Map selected full names back to generic IDs for internal storage
        able_ne[generic_profile_id] = [aid for full_name in selected_full_names for aid, af_name in activity_full_names.items() if af_name == full_name]

with st.sidebar.expander("Variant-Dependent Parameters"):
    user_ind_within_str = st.text_area("ind_within (comma-separated generic activity IDs)", ', '.join(default_ind_within))
    ind_within = parse_list(user_ind_within_str)

    user_ind_until_str = st.text_area("ind_until (comma-separated generic activity IDs)", ', '.join(default_ind_until))
    ind_until = parse_list(user_ind_until_str)

    # --- Validation for overlap ---
    overlap_activities = set(ind_within).intersection(set(ind_until))
    if overlap_activities:
        overlap_full_names = [activity_full_names.get(a, a) for a in overlap_activities]
        st.error(f"Error: The following activities are in both 'ind_within' and 'ind_until': {', '.join(overlap_full_names)}. An activity cannot be in both sets.")

    user_dep_within_str = st.text_area("dep_within (comma-separated generic activity IDs)", ', '.join(default_dep_within))
    dep_within = parse_list(user_dep_within_str)

    st.subheader("within values (integer per activity):")
    within = {}
    for generic_activity_id in ind_within:
        default_val = default_within.get(generic_activity_id, 1) # Default to 1 if not in default_within
        within[generic_activity_id] = st.number_input(f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' within value", value=default_val, key=f"within_{generic_activity_id}", min_value=0)

    st.subheader("until values (integer per activity):")
    until = {}
    for generic_activity_id in ind_until:
        default_val = default_until.get(generic_activity_id, 1) # Default to 1 if not in default_until
        until[generic_activity_id] = st.number_input(f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' until value", value=default_val, key=f"until_{generic_activity_id}", min_value=0)

# Define initial demand data (using generic activity IDs) staro i novo
demand_example_1 = {
    'activity1': [0, 10, 11, 11, 12, 0, 0, 0, 0, 0, 0, 0],
    'activity2': [0, 0, 0, 0, 0, 12, 13, 10, 14, 0, 0, 0],
    'activity3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 12],
    'activity5': [0, 3, 2, 2, 0, 3, 3, 0, 2, 3, 0, 0],
    'activity6': [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    'activity4': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0] # Default for 'Kontrolaaaa' related to activity4
}
demand_example_2 = {
    'activity1': [0, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0],
    'activity2': [0, 0, 0, 0, 0, 10, 8, 7, 14, 0, 0, 0],
    'activity3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 13, 13],
    'activity5': [0, 3, 2, 2, 0, 2, 3, 0, 2, 2, 0, 0],
    'activity6': [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    'activity4': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0] # Default for 'Kontrola' related to activity4
}

# N_set_display should reflect the current N_set for the demand table index
N_set_display = N_set # Use the user-defined N_set for demand table display

st.subheader("Demand setup")
selected_example = st.selectbox(
    "Odaberi defaultnu postavku potražnje:",
    ["Primjer 1", "Primjer 2"],
    key="demand_example_selector")

if selected_example == "Primjer 1":
    default_demand_data = demand_example_1
else:
    default_demand_data = demand_example_2

# Deep copy da se ne mijenja original
base_demand = {k: list(v) for k, v in default_demand_data.items()}

# Convert demand to a DataFrame for Streamlit's data_editor
initial_df_data = {}
for generic_activity_id, demand_list in base_demand.items():
    if generic_activity_id in activities: # Only include activities that are part of the current 'activities' list
        full_activity_name = activity_full_names.get(generic_activity_id, generic_activity_id)
        if demand_list and len(demand_list[1:]) >= len(N_set_display):
            initial_df_data[full_activity_name] = demand_list[1:len(N_set_display)+1]
        elif demand_list: # Pad if demand_list is shorter than N_set_display
            padded_list = demand_list[1:] + [0] * (len(N_set_display) - len(demand_list[1:]))
            initial_df_data[full_activity_name] = padded_list
        else: # Handle empty demand_list
            initial_df_data[full_activity_name] = [0] * len(N_set_display)

if not initial_df_data:
    st.warning("No demand data available for specified activities. Please ensure activities are defined and match demand keys.")
    if not N_set_display:
        N_set_display = [1]
    initial_df_data = {'Dummy Activity': [0] * len(N_set_display)}

df_demand_editable = pd.DataFrame(initial_df_data, index=N_set_display)

st.subheader("Edit Demand per Interval")
edited_df_demand = st.data_editor(df_demand_editable, num_rows="fixed", use_container_width=True)

# Recalculate 'control' demand based on 'istovar' (using generic IDs internally)
# Find generic ID for 'Istovar'
istovar_generic_id = None
for gen_id, full_name in activity_full_names.items():
    if full_name == activity_full_names.get('activity6', 'Istovar'): # Assuming 'activity6' is default for Istovar
        istovar_generic_id = gen_id
        break

# Find generic ID for 'Kontrola'
kontrola_generic_id = None
for gen_id, full_name in activity_full_names.items():
    if full_name == activity_full_names.get('activity4', 'Kontrola'): # Assuming 'activity4' is default for Kontrola
        kontrola_generic_id = gen_id
        break

if istovar_generic_id and kontrola_generic_id and activity_full_names.get(istovar_generic_id) in edited_df_demand.columns:
    edited_df_demand[activity_full_names.get(kontrola_generic_id)] = (edited_df_demand[activity_full_names.get(istovar_generic_id)] * 0.5).apply(round)
else:
    if istovar_generic_id and activity_full_names.get(istovar_generic_id) not in edited_df_demand.columns:
        st.warning(f"'{activity_full_names.get(istovar_generic_id)}' activity not found in demand, '{activity_full_names.get(kontrola_generic_id, 'Kontrola')}' demand will not be automatically calculated.")


# Convert the edited DataFrame back to the dictionary format for the optimization model
final_demand_for_model = {}
for full_col_name in edited_df_demand.columns:
    generic_col_id = None
    # Map full column name back to generic ID
    for gen_id, full_name in activity_full_names.items():
        if full_name == full_col_name:
            generic_col_id = gen_id
            break
    if generic_col_id:
        final_demand_for_model[generic_col_id] = [0] + edited_df_demand[full_col_name].tolist()


# Streamlit button to run the optimization
run_optimization_disabled = bool(overlap_activities)
if st.button('Run Optimization', disabled=run_optimization_disabled):
    st.write(f"Running optimization with current parameters.")

    demand = final_demand_for_model

    model = LpProblem("Cost minimising problem", LpMinimize)

    N = max(N_set) if N_set else 12

    # Construct ct dictionary from user inputs (using generic profile IDs)
    ct = {}
    for j in M_set:
        for p_type_id in profil_types:
            if j in M1_set:
                ct[(p_type_id, j)] = ct_m1_inputs[p_type_id]
            elif j in M2_set:
                ct[(p_type_id, j)] = ct_m2_inputs[p_type_id]

    bij = {}
    for j in M_set:
        for i in N_set:
            if j in M1_set:
                if i < j or i > j + 8:
                    bij[(i, j)] = 0.00
                else:
                    bij[(i, j)] = 1.00
            elif j in M2_set:
                if i < j - 5 or i > j - 5 + 3:
                    bij[(i, j)] = 0.00
                else:
                    bij[(i, j)] = 1.00

    yjz = LpVariable.dicts("u smeni z",
                                         ((j) for j in M_set),
                                         lowBound=0,
                                         cat='Integer')

    yj = LpVariable.dicts("u smeni",
                                         ((j) for j in M_set),
                                         lowBound=0,
                                         upBound=1,
                                         cat='Integer')

    ytj = LpVariable.dicts("u smeni profila",
                                         ((t, j) for t in profil_types for j in M_set),
                                         lowBound=0,
                                         cat='Integer')

    ytija = LpVariable.dicts("u intervalu",
                                         ((t, i, j, a) for t in profil_types for i in N_set for j in M_set for a in activities),
                                         lowBound=0,
                                         cat='Integer')

    xaijk = LpVariable.dicts("u intervalu",
                                         ((a, i, j, k) for a in activities for i in N_set for j in M_set for k in N_set),
                                         lowBound=0,
                                         cat='Integer')

    if P>0:
      delta = LpVariable.dicts(
      "delta_switch",
      ((t, j, a, i)
      for t in profil_types
      for j in M_set
      for a in activities
      for i in N_set if i < max(N_set)),
      lowBound=0,
      cat='Continuous'  # ili Integer
      )
    else:
      delta={}


    # Objective Function

    obj_part_1 = lpSum(
        ct.get((p_type_id, j), 0) * ytj.get((p_type_id, j), 0)
        for j in M_set
        for p_type_id in profil_types
        if (p_type_id, j) in ct and (p_type_id, j) in ytj
    )

    if P > 0:
      obj_part_2 = lpSum(
          delta[t, j, a, i]
          for t in profil_types
          for j in M_set
          for a in activities
          for i in N_set
          if i < max(N_set)
      )

      model += obj_part_1 + P * obj_part_2, "Total Cost"
    else:
        model += obj_part_1, "Total Cost"

    if P>0:
      K=3; pk={}
      blocks = range(len(N_set)//K)
      for i in N_set:
        if i==K:
          pk[i]=1
          K=K+K
        else:
          pk[i]=0


    #Ograničenje za penalizovanje prelaska na drugu aktivnost nakon samo jednog intervala
    K=3
    if P>0:
      for t in profil_types:
          for j in M_set:
              for a in activities:
                  if a in able[t]:
                      for i in N_set:
                          if i < max(N_set):
                            model += (
                                  delta[t, j, a, i]
                                  >= ytija[t, i, j, a] - ytija[t, i+1, j, a]
                              )

                            model += (
                                  delta[t, j, a, i]
                                  >= 0
                              )


    #Ograničenje za ukupan broj radnika i potražnje
    for a in activities:
        model += lpSum(
            ytija[t, i, j, a]
            for t in profil_types
            for i in N_set
            for j in M_set
        ) == sum(demand[a])

    st.write("--- Model setup complete. Adding constraints. ---")

    # Constraints (as in the original code)
    # 2a
    for a_id in ind_within:
        for i in N_set:
            if a_id in demand and i < len(demand[a_id]):
                model += lpSum([xaijk[(a_id, i, j, k)] * bij.get((k, j), 0)
                                for k in range(i, min(i + within.get(a_id, N), N + 1))
                                for j in M_set if (a_id, i, j, k) in xaijk and (k, j) in bij
                               ]) == demand[a_id][i], f"Constraint_2a_demand_{activity_full_names.get(a_id,a_id)}_{i}"

                model += lpSum([xaijk[(a_id, i, j, k)]
                                for k in N_set
                                for j in M_set if (a_id, i, j, k) in xaijk
                               ]) == demand[a_id][i], f"Constraint_2a_sum_{activity_full_names.get(a_id,a_id)}_{i}"


    # 2b
    for a_id in ind_until:
        for i in N_set:
            if a_id in demand and i < len(demand[a_id]):
                model += lpSum([xaijk[(a_id, i, j, k)] * bij.get((k, j), 0)
                                for k in range(i, min(until.get(a_id, N), N + 1))
                                for j in M_set if (a_id, i, j, k) in xaijk and (k, j) in bij
                               ]) == demand[a_id][i], f"Constraint_2b_{activity_full_names.get(a_id,a_id)}_{i}"

    # 2d sa=0.5
    if kontrola_generic_id and istovar_generic_id:
        for k in N_set:
            if kontrola_generic_id in activities and istovar_generic_id in activities: # Ensure activities exist
                model += lpSum([xaijk[(istovar_generic_id, i, j, k)]
                                for i in N_set for j in M_set if (istovar_generic_id, i, j, k) in xaijk
                               ]) * 0.5 <= lpSum([xaijk[(kontrola_generic_id, k, j, k)] * bij.get((k, j), 0)
                                                  for j in M_set if (kontrola_generic_id, k, j, k) in xaijk and (k, j) in bij
                                                 ]), f"Constraint_2d_{activity_full_names.get(kontrola_generic_id,kontrola_generic_id)}_{k}"

    # 3
    for a_id in activities:
        for j in M_set:
            for k in N_set:
                model += lpSum([xaijk[(a_id, i, j, k)]
                                for i in range(1, k + 1) if (a_id, i, j, k) in xaijk
                               ]) == lpSum([ytija[(t_id, k, j, a_id)]
                                            for t_id in allowed.get(a_id, []) if (t_id, k, j, a_id) in ytija
                                           ]), f"Constraint_3_{activity_full_names.get(a_id,a_id)}_{j}_{k}"


    # 4
    for p_type_id in profil_types:
        for i in N_set:
            for j in M_set:
                if (p_type_id, j) in ytj:
                    model += lpSum([ytija[(p_type_id, i, j, a_id)]
                                    for a_id in able.get(p_type_id, []) if (p_type_id, i, j, a_id) in ytija
                                   ]) <= ytj[(p_type_id, j)], f"Constraint_4_{profile_full_names.get(p_type_id,p_type_id)}_{i}_{j}"


    # 5 q=30
    for i in N_set:
        model += lpSum([ytija[(p_type_id, i, j, a_id)]
                        for p_type_id in profil_types for j in M_set for a_id in activities if (p_type_id, i, j, a_id) in ytija
                       ]) <= 40, f"Constraint_5_{i}"


    # 6
    for j in M1_set:
        for p_type_id in profil_types:
            if (p_type_id, j) in ytj:
                model += lpSum([ytija[(p_type_id, i, j, a_id)] * bij.get((i, j), 0)
                                for i in Oj.get(j, []) for a_id in activities if (p_type_id, i, j, a_id) in ytija and (i, j) in bij
                               ]) <= 2 * ytj[(p_type_id, j)], f"Constraint_6_{j}_{profile_full_names.get(p_type_id,p_type_id)}"


    # 7 f-p=0.3
    for p_type_id in profil_types:
        sum_m2 = lpSum([ytj[(p_type_id, j)] for j in M2_set if (p_type_id, j) in ytj])
        sum_m_total = lpSum([ytj[(p_type_id, j)] for j in M_set if (p_type_id, j) in ytj])
        model += sum_m2 <= 0.3 * sum_m_total, f"Constraint_7_{profile_full_names.get(p_type_id,p_type_id)}"


    # 8,9,10 broj smijena sa punim radnim vremenom ne smije biti veći od 3 da ne bude previse, a ovih sa pola r.v. ne veći od 1.
    for j in M_set:
        model += lpSum([ytj[(p_type_id, j)] for p_type_id in profil_types if (p_type_id, j) in ytj]) <= 1000 * yj[j], f"Constraint_8_10_sum_ytj_{j}"

    model += lpSum([yj[j] for j in M1_set]) <= 3, "Constraint_9_M1_limit"
    model += lpSum([yj[j] for j in M2_set]) <= 1, "Constraint_10_M2_limit"

    # 11 ukupan broj intervala u kojim radnici rade poslove koji im nisu primarni, mora biti manji od pola. važi samo za smjene sa punim radnim vremenom.
    for j in M1_set:
        for p_type_id in profil_types:
            primary_activities_sum = lpSum([ytija[(p_type_id, i, j, a_id)] * bij.get((i, j), 0)
                                            for i in N_set for a_id in able.get(p_type_id, [])
                                            if (p_type_id, i, j, a_id) in ytija and (i, j) in bij])

            non_primary_activities_sum = lpSum([ytija[(p_type_id, i, j, a_id)] * bij.get((i, j), 0)
                                                for i in N_set for a_id in able_ne.get(p_type_id, [])
                                                if (p_type_id, i, j, a_id) in ytija and (i, j) in bij])
            model += non_primary_activities_sum <= 0.5 * primary_activities_sum, f"Constraint_11_{j}_{profile_full_names.get(p_type_id,p_type_id)}"

    # 12
    for i in N_set:
        m1_shifts_sum = lpSum([ytj[(p_type_id, j)] * bij.get((i, j), 0)
                               for j in M1_set for p_type_id in profil_types
                               if (p_type_id, j) in ytj and (i, j) in bij])

        m2_shifts_sum = lpSum([ytj[(p_type_id, j)] * bij.get((i, j), 0)
                               for j in M2_set for p_type_id in profil_types
                               if (p_type_id, j) in ytj and (i, j) in bij])
        model += m1_shifts_sum >= 0.0000001 * m2_shifts_sum, f"Constraint_12_{i}"

    st.write("--- All constraints added. Solving model... ---")

    with st.spinner('Solving optimization problem...'):
        model.solve(PULP_CBC_CMD(msg=0)) # msg=0 to suppress solver output in Streamlit console

    st.write(f"--- Solver Status: {LpStatus[model.status]} ---")
    # Vrijednosti dijelova ciljne funkcije
    value_part_1 = value(obj_part_1)
    value_part_2 = 0 if P==0  else value(obj_part_2)


    st.write(f"Ukupna vrijednost funkcije cilja: {value(model.objective):.2f}")
    st.write(f"  - Dio 1 (trošak radnika): {value_part_1:.2f}")
    st.write(f"  - Dio 2 (penal prelazaka): {value_part_2:.2f}")
    st.write(f"  - Dio 2 ponderisan (P * dio 2): {(P * value_part_2):.2f}")

    Ms = []
    Ms.append(M1_set)
    Ms.append(M2_set)
    smjena_output = defaultdict(list) # Will store lists of activity codes for each worker

    if model.status == LpStatusOptimal:
        st.write("--- Model solved optimally. Processing results for display. ---")
        st.write("--- Starting smjena_output generation (Step 1 of 3) ---")
        for M_grp in Ms:
            for j in M_grp:
                current_i_range_length = 0
                if j in M1_set:
                    current_i_range_length = 9 # Full-time shift covers 9 intervals
                elif j in M2_set:
                    current_i_range_length = 4 # Part-time shift covers 4 intervals

                for p_type_id in profil_types:
                    if (p_type_id, j) in ytj and ytj[(p_type_id,j)].varValue is not None:
                        broj_usmjeni=int(ytj[(p_type_id,j)].varValue)
                    else:
                        broj_usmjeni = 0

                    if broj_usmjeni > 0:
                        # Initialize worker schedules for this shift and profile
                        # Each worker gets a list of size `current_i_range_length`, filled with 0s
                        for k_idx in range(1, broj_usmjeni + 1):
                            smjena_output[j, p_type_id, k_idx] = [0] * current_i_range_length

                        # Now, fill these schedules based on ytija variables
                        current_i_range_absolute = []
                        if j in M1_set:
                            current_i_range_absolute = list(range(j, j + 9))
                        elif j in M2_set:
                            current_i_range_absolute = list(range(j - 5, j - 5 + 4))

                        # Iterate through each absolute interval number
                        for interval_offset, i in enumerate(current_i_range_absolute):
                            # Track which workers have been assigned an activity for this specific interval
                            workers_assigned_in_this_interval = set()
                            available_workers = list(range(1, broj_usmjeni + 1))
                            random.shuffle(available_workers) # Randomize assignment order

                            for a_id in activities:
                                if (p_type_id, i, j, a_id) in ytija and ytija[(p_type_id, i, j, a_id)].varValue is not None:
                                    broj_uintervalu = int(ytija[(p_type_id, i, j, a_id)].varValue)
                                else:
                                    broj_uintervalu = 0

                                if broj_uintervalu > 0:
                                    assigned_count = 0
                                    # Assign activity 'a_id' to 'broj_uintervalu' workers for interval 'i'
                                    for k_idx in list(available_workers): # Iterate over a copy to allow modification
                                        if k_idx not in workers_assigned_in_this_interval and assigned_count < broj_uintervalu:
                                            if interval_offset < current_i_range_length: # Safety check
                                                smjena_output[j, p_type_id, k_idx][interval_offset] = s[a_id]
                                                workers_assigned_in_this_interval.add(k_idx)
                                                available_workers.remove(k_idx)
                                                assigned_count += 1
                                            else:
                                                pass # Should not happen if ranges are consistent


        st.write("--- smjena_output generation complete. Starting BALANCING (Step 2 of 3) ---")
        # BALANSIRANJE (Balancing)
        max_balancing_iterations = 1000  # Added iteration limit to prevent infinite loops
        for j in M1_set:
                for p_type_id in profil_types:
                    broj_usmjeni = 0
                    if (p_type_id, j) in ytj and ytj[(p_type_id,j)].varValue is not None:
                        broj_usmjeni = int(ytj[(p_type_id,j)].varValue)

                    if broj_usmjeni == 0:
                        continue

                    d = {}; balance_loop_active = True
                    current_iteration = 0 # Initialize iteration counter
                    while balance_loop_active:
                        #and current_iteration < max_balancing_iterations: # Check iteration limit
                        #current_iteration += 1 # Increment iteration counter
                        d.clear()
                        for k_val in range(1, broj_usmjeni + 1):
                            worker_schedule = smjena_output.get((j, p_type_id, k_val), [])
                            if worker_schedule:

                                 # For M1, consider intervals 3, 4, 5 (0-indexed slice 3:6)
                                 d[k_val] = worker_schedule[3:6].count(0)

                            else:
                                ValueError(
                                f"Worker schedule too short empty: "
                                f"Shift {j}, Profile {p_type_id}, Worker {k_val}, "
                                f"Length {len(worker_schedule)}")


                        if d: # Check if d is not empty
                            max_kljuc, max_v = max(d.items(), key=lambda k_v: k_v[1])
                            min_kljuc, min_v = min(d.items(), key=lambda k_v: k_v[1])

                            balance_loop_active = False
                            if max_v - min_v > 1:
                                balance_loop_active = True
                                if (j, p_type_id, max_kljuc) in smjena_output and (j, p_type_id, min_kljuc) in smjena_output:
                                    schedule_max = smjena_output[(j, p_type_id, max_kljuc)]
                                    schedule_min = smjena_output[(j, p_type_id, min_kljuc)]

                                    if schedule_max[3] == 0:
                                            schedule_max[3] = schedule_min[3]
                                            schedule_min[3] = 0
                                    elif schedule_max[4] == 0:
                                            schedule_max[4] = schedule_min[4]
                                            schedule_min[4] = 0
                                    elif schedule_max[5] == 0:
                                            schedule_max[5] = schedule_min[5]
                                            schedule_min[5] = 0
                        else:
                            balance_loop_active = False

        st.write("--- BALANCING complete. Starting DataFrame generation (Step 3 of 3) ---")
    # Display Results
    st.header("Optimization Results")
    if model.status == LpStatusOptimal:
        st.success(f"Optimal Objective Value: {value(model.objective):.2f}")
        st.info(f"Solver Status: {LpStatus[model.status]}")

        st.subheader("Employees per Shift and Profile (ytj)")
        ytj_data = []
        for j in M_set:
          for p_type_id in profil_types:
                if (p_type_id, j) in ytj and value(ytj[(p_type_id, j)]) > 0:
                    ytj_data.append({"Shift": j, "Profile": profile_full_names.get(p_type_id,p_type_id),  "Count": value(ytj[(p_type_id, j)])})
        if ytj_data:
            df_ytj = pd.DataFrame(ytj_data)
            st.dataframe(df_ytj)
        else:
            st.write("No ytj variables with non-zero values.")

        # ------------------------------------------
        # TABELA SHIFT ALLOCATION TIMETABLE
        # ------------------------------------------

        st.subheader("Shift Allocation Timetable (smjena)")
        st.write("--- Starting shift allocation timetable processing ---") # Debug message

        max_rows1 = 9
        max_rows2 = 4
        df = pd.DataFrame(index=range(1, 15), dtype=object) # Added dtype=object here
        rbkolone = 0

        for j in M_set:
            for t in profil_types:
                if (t, j) in ytj and ytj[t, j].varValue is not None:
                    broj_usmjeni = int(ytj[t, j].varValue)
                else:
                    broj_usmjeni = 0

                for k in range(1, broj_usmjeni + 1):
                    col_name = f"Smjena_{j}_{sp[t]}_{k}" # Changed 'Shift' to 'Smjena'
                    #df.loc[1, col_name] = sp[t]

                    if j in M1_set:
                        for i_offset in range(max_rows1):
                            row = j + i_offset
                            if row <= 14 and (j, t, k) in smjena_output:
                                if i_offset < len(smjena_output[j, t, k]):
                                    df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                                else:
                                    df.loc[row, col_name] = ""
                    else:
                        for i_offset in range(max_rows2):
                            row = j - 5 + i_offset
                            if row <= 14 and (j, t, k) in smjena_output:
                                if i_offset < len(smjena_output[j, t, k]):
                                    df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                                else:
                                    df.loc[row, col_name] = ""

                rbkolone += broj_usmjeni


        st.write("--- Shift allocation timetable DataFrame generated ---")  # Debug message

        display_offset = int(display_start_interval) - 1

        # >>> PROMJENA: pomjeranje intervala SAMO ZA PRIKAZ
        df_display = df.copy()
        df_display.index = df_display.index + display_offset   # 1→8, 2→9, ...

        # >>> PROMJENA: ako hoćeš da vidiš 8,9,10... NE smiješ sakriti index
        st.dataframe(df_display.style.hide(axis="columns"))

        st.write("--- Shift allocation timetable displayed ---")  # Debug message

        # ------------------------------------------
        # UKUPAN BROJ INTERVALA SA NULOM (samo 0)
        # ------------------------------------------

        broj_nula = 0

        for col in df.columns:
            # preskačemo prvi red (oznaka profila)
            for v in df[col].iloc[1:]:
                if v == 0:
                    broj_nula += 1

        st.markdown(f"### ðﾟﾧﾮ Ukupan broj intervala bez rada (vrijednost = 0): **{broj_nula}**")

        # ------------------------------------------
        # UKUPAN BROJ INTERVALA SA 3 iste aktivnosti
        # ------------------------------------------

        def count_consecutive_sequences(series, min_len=3):
            count = 0
            current_val = None
            current_len = 0

            for v in series:
                # prekid niza
                if v == 0 or v == "" or v is None:
                    if current_len >= min_len:
                        count += 1
                    current_val = None
                    current_len = 0
                    continue

                # nastavak istog niza
                if v == current_val:
                    current_len += 1
                else:
                    if current_len >= min_len:
                        count += 1
                    current_val = v
                    current_len = 1

            # provjera na kraju
            if current_len >= min_len:
                count += 1

            return count


        from collections import defaultdict
        rezultati = defaultdict(dict)

        for col in df.columns:
            series = df[col].iloc[1:]
            j = int(col.split("_")[1])
            if j in M1_set:
              rezultati[col]["maksimalni"] = 2
            else:
              rezultati[col]["maksimalni"] = 1

            stvarni = count_consecutive_sequences(series, min_len=3)

            # procjena da li ima odmor (ti ovdje znaš logiku)
            has_break = True if col in M1_set else False

            rezultati[col]["stvarni"] = stvarni

        st.subheader("ðﾟﾓﾊ Stvarni vs maksimalno mogući nizovi")

        ukupno_stvarni = 0
        ukupno_maks = 0

        for col, r in rezultati.items():
            st.write(
                f"**{col}** → stvarni: {r['stvarni']} / maksimalno: {r['maksimalni']}"
            )
            ukupno_stvarni += r["stvarni"]
            ukupno_maks += r["maksimalni"]

        st.markdown(
            f"### ✅ UKUPNO: {ukupno_stvarni} / {ukupno_maks}")


        # ------------------------------------------
        # TABELA DEMAND vs.REALIZED
        # --

        st.subheader("Total activities per interval (Demanded vs. Realized)")
        st.write("--- Starting total activities per interval processing ---") # Debug message
        activity_per_interval = defaultdict(lambda: defaultdict(float))
        for i in N_set:
                    for a_id in activities:
                        total_activity_for_interval_and_activity = 0
                        for p_type_id in profil_types:
                            for j in M_set:
                                if (p_type_id, i, j, a_id) in ytija and ytija[(p_type_id, i, j, a_id)].varValue is not None:
                                    total_activity_for_interval_and_activity += ytija[(p_type_id, i, j, a_id)].varValue
                        activity_per_interval[i][a_id] = total_activity_for_interval_and_activity

        df_data = []
        for i in sorted(activity_per_interval.keys()):
                    row_data = {"Interval": i}
                    for a_id in activities:
                        full_activity_name = activity_full_names.get(a_id,a_id)
                        row_data[f"{full_activity_name}_zahtjevano"] = demand.get(a_id, [0]*(N+1))[i] if i < len(demand.get(a_id, [0]*(N+1))) else 0
                        row_data[f"{full_activity_name}_rasporedjeno"] = activity_per_interval[i][a_id]

                    df_data.append(row_data)

        df_activities_by_interval = pd.DataFrame(df_data).set_index("Interval")

        ordered_columns = []
        for a_id in activities:
                    full_activity_name = activity_full_names.get(a_id,a_id)
                    ordered_columns.append(f"{full_activity_name}_zahtjevano")
                    ordered_columns.append(f"{full_activity_name}_rasporedjeno")

        final_ordered_columns = [col for col in ordered_columns if col in df_activities_by_interval.columns]
        df_activities_by_interval = df_activities_by_interval[final_ordered_columns]
        st.write("--- Total activities per interval DataFrame generated ---") # Debug message
        st.dataframe(df_activities_by_interval)
        st.write("--- Total activities per interval displayed ---") # Debug message

        if st.checkbox("Show all PuLP variables with non-zero values"):
            st.subheader("All Non-Zero PuLP Variables")
            st.write("--- Starting non-zero PuLP variables display ---") # Debug message
            for v in model.variables():
                if v.varValue is not None and v.varValue > 0:
                    st.write(f"{v.name} = {v.varValue}")
            st.write("--- Non-zero PuLP variables displayed ---") # Debug message


    elif model.status == LpStatusInfeasible:
        st.error(f"Solver Status: {LpStatus[model.status]} (No feasible solution found)")
    else:
        st.warning(f"Solver Status: {LpStatus[model.status]} (Solution might not be optimal or problem not solved)")

