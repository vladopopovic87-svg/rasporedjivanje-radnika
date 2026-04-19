# UI input handling and parameter collection

import streamlit as st
import pandas as pd
from config import *
from utils import parse_list, generate_profile_types, generate_activities


def collect_general_parameters():
    """Collect general model parameters from sidebar."""
    with st.sidebar.expander("General Parameters"):
        P = st.number_input(
            "Short-Duration Assignment Penalty",
            min_value=0.00,
            max_value=1.00,
            value=0.00,
            step=0.01,
            help="Weight of the transition penalty term in the objective function."
        )

        num_profiles = st.number_input(
            "Number of Worker Profiles",
            min_value=1,
            value=DEFAULT_NUM_PROFILES,
            step=1,
            help="Number of different worker profile types (e.g., Komisioner, Kontrolor, Viljuskarista)."
        )
        profil_types = generate_profile_types(num_profiles)

        num_activities = st.number_input(
            "Number of Activities",
            min_value=1,
            value=DEFAULT_NUM_ACTIVITIES,
            step=1,
            help="Number of different activity types that workers can perform."
        )
        activities = generate_activities(num_activities)

        # Profile names and codes
        st.subheader("Define Profile Names and Short Codes:")
        profile_full_names = {}
        sp = {}
        for generic_profile_id in profil_types:
            default_full = DEFAULT_FULL_PROFILE_NAMES.get(generic_profile_id, generic_profile_id.capitalize())
            profile_full_names[generic_profile_id] = st.text_input(
                f"Full name for '{generic_profile_id}'",
                value=default_full,
                key=f"full_name_profile_{generic_profile_id}",
                help="Full descriptive name for this worker profile type."
            )
            default_short = DEFAULT_SHORT_PROFILES.get(generic_profile_id, generic_profile_id[0:2])
            sp[generic_profile_id] = st.text_input(
                f"Short code for '{generic_profile_id}'",
                value=default_short,
                key=f"short_code_profile_{generic_profile_id}",
                help="Short abbreviation or code for this worker profile (used in tables and reports)."
            )

        # Activity names and codes
        st.subheader("Define Activity Names and Short Codes:")
        s = {}
        activity_full_names = {}
        for generic_activity_id in activities:
            default_full = DEFAULT_FULL_ACTIVITY_NAMES.get(generic_activity_id, generic_activity_id.capitalize())
            activity_full_names[generic_activity_id] = st.text_input(
                f"Full name for '{generic_activity_id}'",
                value=default_full,
                key=f"full_name_activity_{generic_activity_id}",
                help="Full descriptive name for this activity type."
            )
            default_short = DEFAULT_SHORT_ACTIVITIES.get(generic_activity_id, generic_activity_id[0:2])
            s[generic_activity_id] = st.text_input(
                f"Short code for '{generic_activity_id}'",
                value=default_short,
                key=f"short_code_activity_{generic_activity_id}",
                help="Short abbreviation or code for this activity (used in tables and reports)."
            )

    return P, profil_types, activities, profile_full_names, sp, activity_full_names, s


def collect_interval_and_shift_parameters():
    """Collect interval and shift set parameters."""
    with st.sidebar.expander("Interval and Shift Sets"):
        display_start_interval = st.number_input(
            "Početak radnog dana (prikaz intervala počinje od):",
            min_value=1,
            max_value=100,
            value=8,
            step=1,
            key="display_start_interval",
            help="Starting hour for displaying time intervals in the schedule (e.g., 8 means intervals start from 8:00)."
        )

        interval_duration = st.number_input(
            "Trajanje intervala (u minutama):",
            min_value=15,
            max_value=1440,
            value=60,
            step=15,
            key="interval_duration",
            help="Duration of each time interval in minutes (e.g., 30 for 30 minutes, 60 for 1 hour)."
        )
       

        rest_duration = st.number_input(
            "Trajanje odmora (u minutama):",
            min_value=15,
            max_value=1440,
            value=60,
            step=15,
            key="rest_duration",
            help="Duration of rest intervals in minutes (e.g., 30 for 30 minutes, 60 for 1 hour)."
        )
       

        user_N_set_str = st.text_area(
            "N_set (Intervals, comma-separated integers)",
            ', '.join(map(str, DEFAULT_N_SET)),
            help="List of time intervals for the workday. Each number represents a time slot (e.g., 1,2,3,4,5,6,7,8)."
        )
        N_set = parse_list(user_N_set_str, int)
        if not N_set:
            st.warning("N_set cannot be empty. Defaulting to default values.")
            N_set = DEFAULT_N_SET

        user_M_set_str = st.text_area(
            "M_set (Shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M_SET)),
            help="List of all available shifts. Each number represents a different shift type."
        )
        M_set = parse_list(user_M_set_str, int)
        if not M_set:
            st.warning("M_set cannot be empty. Defaulting to default values.")
            M_set = DEFAULT_M_SET

        user_M1_set_str = st.text_area(
            "M1_set (Full-time shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M1_SET)),
            help="List of full-time shifts (longer working hours). Subset of M_set."
        )
        M1_set = parse_list(user_M1_set_str, int)

        user_M2_set_str = st.text_area(
            "M2_set (Part-time shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M2_SET)),
            help="List of part-time shifts (shorter working hours). Subset of M_set."
        )
        M2_set = parse_list(user_M2_set_str, int)

        st.subheader("Oj (Intervals available for rest shift j, only for M1 shifts):")
        Oj = {}
        for j_shift in M1_set:
            default_oj_intervals = DEFAULT_OJ.get(j_shift, [])
            oj_intervals_str = st.text_area(
                f"Intervals for shift {j_shift} (comma-separated integers)",
                value=', '.join(map(str, default_oj_intervals)),
                key=f"Oj_{j_shift}",
                help=f"Time intervals available for rest during shift {j_shift}. Workers can take breaks in these intervals."
            )
            Oj[j_shift] = parse_list(oj_intervals_str, int)

    return display_start_interval, interval_duration, rest_duration, N_set, M_set, M1_set, M2_set, Oj


def collect_cost_coefficients(profil_types, profile_full_names):
    """Collect cost coefficients for shifts."""
    with st.sidebar.expander("Cost Coefficients (ct)"):
        st.write("Full-time shift (M1) cost rates:")
        ct_m1_inputs = {}
        for p_type in profil_types:
            default_rate = DEFAULT_CT_RATES.get((p_type, 'm1'), 1.0)
            ct_m1_inputs[p_type] = st.number_input(
                f"{profile_full_names.get(p_type, p_type)} (M1)",
                value=default_rate,
                key=f"ct_m1_{p_type}",
                help=f"Cost rate per full shift for {profile_full_names.get(p_type, p_type)} working full-time shifts (M1)."
            )

        st.write("Part-time shift (M2) cost rates:")
        ct_m2_inputs = {}
        for p_type in profil_types:
            default_rate = DEFAULT_CT_RATES.get((p_type, 'm2'), 0.5)
            ct_m2_inputs[p_type] = st.number_input(
                f"{profile_full_names.get(p_type, p_type)} (M2)",
                value=default_rate,
                key=f"ct_m2_{p_type}",
                help=f"Cost rate per shift for {profile_full_names.get(p_type, p_type)} working part-time shifts (M2)."
            )

    return ct_m1_inputs, ct_m2_inputs


def collect_role_activity_mappings(profil_types, activities, profile_full_names, activity_full_names):
    """Collect role-activity mappings from user input."""
    with st.sidebar.expander("Role-Activity Mappings"):
        st.subheader("Allowed Activities per Role:")
        allowed = {}
        for generic_activity_id in activities:
            default_selection_generic_ids = [
                pid for pid in DEFAULT_ALLOWED.get(generic_activity_id, [])
                if pid in profil_types
            ]
            default_selection_full_names = [
                profile_full_names.get(pid, pid) for pid in default_selection_generic_ids
            ]

            selected_full_names = st.multiselect(
                f"Profiles for '{activity_full_names.get(generic_activity_id, generic_activity_id)}'",
                options=[profile_full_names.get(p, p) for p in profil_types],
                default=default_selection_full_names,
                key=f"allowed_{generic_activity_id}",
                help=f"Select which worker profiles are allowed to perform the '{activity_full_names.get(generic_activity_id, generic_activity_id)}' activity."
            )
            allowed[generic_activity_id] = [
                pid for full_name in selected_full_names
                for pid, pf_name in profile_full_names.items()
                if pf_name == full_name
            ]

        st.subheader("Able Activities per Profile:")
        able = {}
        for generic_profile_id in profil_types:
            default_selection_generic_ids = [
                aid for aid in DEFAULT_ABLE.get(generic_profile_id, [])
                if aid in activities
            ]
            default_selection_full_names = [
                activity_full_names.get(aid, aid) for aid in default_selection_generic_ids
            ]

            selected_full_names = st.multiselect(
                f"Activities for '{profile_full_names.get(generic_profile_id, generic_profile_id)}'",
                options=[activity_full_names.get(a, a) for a in activities],
                default=default_selection_full_names,
                key=f"able_{generic_profile_id}",
                help=f"Select which activities {profile_full_names.get(generic_profile_id, generic_profile_id)} workers are able to perform."
            )
            able[generic_profile_id] = [
                aid for full_name in selected_full_names
                for aid, af_name in activity_full_names.items()
                if af_name == full_name
            ]

        st.subheader("Non-Primary Able Activities per Profile:")
        able_ne = {}
        for generic_profile_id in profil_types:
            default_selection_generic_ids = [
                aid for aid in DEFAULT_ABLE_NE.get(generic_profile_id, [])
                if aid in activities
            ]
            default_selection_full_names = [
                activity_full_names.get(aid, aid) for aid in default_selection_generic_ids
            ]

            selected_full_names = st.multiselect(
                f"Non-primary activities for '{profile_full_names.get(generic_profile_id, generic_profile_id)}'",
                options=[activity_full_names.get(a, a) for a in activities],
                default=default_selection_full_names,
                key=f"able_ne_{generic_profile_id}",
                help=f"Select which activities {profile_full_names.get(generic_profile_id, generic_profile_id)} can perform as non-primary work (limited by ratio constraints)."
            )
            able_ne[generic_profile_id] = [
                aid for full_name in selected_full_names
                for aid, af_name in activity_full_names.items()
                if af_name == full_name
            ]

    return allowed, able, able_ne


def collect_variant_parameters(activities, activity_full_names):
    """Collect variant-dependent parameters."""
    with st.sidebar.expander("Variant-Dependent Parameters", expanded=True):
        user_ind_within_str = st.text_area(
            "ind_within (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_IND_WITHIN),
            help="Activities that have 'within' constraints - workers must complete these activities within a certain number of intervals."
        )
        ind_within = parse_list(user_ind_within_str)

        user_ind_until_str = st.text_area(
            "ind_until (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_IND_UNTIL),
            help="Activities that have 'until' constraints - workers must start these activities by a certain interval."
        )
        ind_until = parse_list(user_ind_until_str)

        # Validation for overlap
        overlap_activities = set(ind_within).intersection(set(ind_until))
        if overlap_activities:
            overlap_full_names = [activity_full_names.get(a, a) for a in overlap_activities]
            st.error(f"Error: Activities in both 'ind_within' and 'ind_until': {', '.join(overlap_full_names)}")
        
        within = {}
        if not ind_within:
            st.info("No activities selected in ind_within. Add activity IDs above to set within values.")
        else:
            st.subheader("within values (integer per activity):")
            for generic_activity_id in ind_within:
                default_val = DEFAULT_WITHIN.get(generic_activity_id, 1)
                within[generic_activity_id] = st.number_input(
                    f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' within value",
                    value=default_val,
                    key=f"within_{generic_activity_id}",
                    min_value=0,
                    help=f"Maximum number of intervals allowed to complete '{activity_full_names.get(generic_activity_id, generic_activity_id)}' activity."
                )

        until = {}
        if not ind_until:
            st.info("No activities selected in ind_until. Add activity IDs above to set until values.")
        else:
            st.subheader("until values (integer per activity):")
            for generic_activity_id in ind_until:
                default_val = DEFAULT_UNTIL.get(generic_activity_id, 1)
                until[generic_activity_id] = st.number_input(
                    f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' until value",
                    value=default_val,
                    key=f"until_{generic_activity_id}",
                    min_value=0,
                    help=f"Latest interval by which '{activity_full_names.get(generic_activity_id, generic_activity_id)}' activity must be started."
                )

        st.subheader("Dependent aktivnosti:")

        user_dep_within_str = st.text_area(
            "dep_within (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_DEP_WITHIN),
            help="Activities with dependent 'within' constraints - these depend on other activities being completed first."
        )
        dep_within = parse_list(user_dep_within_str)
        
        user_dep_until_str = st.text_area(
            "dep_until (comma-separated generic activity IDs)",    
            help="Activities with dependent 'until' constraints - these depend on other activities being completed first."
        )
        dep_until = parse_list(user_dep_until_str)

        dependent_activity_relations = {}
        for dep_activity_id in dep_within + dep_until:
            available_ids = [aid for aid in activity_full_names.keys() if aid != dep_activity_id]
            available_names = [activity_full_names.get(aid, aid) for aid in available_ids]
            default_dep_on = DEFAULT_DEP_ON.get(dep_activity_id)
            default_dep_idx = available_ids.index(default_dep_on) if default_dep_on in available_ids else 0
            selected_idx = st.selectbox(
                f"Odaberi aktivnost od koje zavisi '{activity_full_names.get(dep_activity_id, dep_activity_id)}'",
                options=range(len(available_ids)),
                index=default_dep_idx,
                format_func=lambda idx: available_names[idx],
                key=f"dep_relation_{dep_activity_id}"
            )
            depends_on_id = available_ids[selected_idx]
            ratio_val = st.slider(
                f"Unesi ratio za '{activity_full_names.get(dep_activity_id, dep_activity_id)}' (od {activity_full_names.get(depends_on_id, depends_on_id)})",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                key=f"dep_ratio_{dep_activity_id}"
            )
            dependent_activity_relations[dep_activity_id] = {"depends_on": depends_on_id, "ratio": ratio_val}

        dep_within_values = {}
        if not dep_within:
            st.info("No dependent activities selected in dep_within. Add activity IDs above to set dep within values.")
        else:
            st.subheader("dependent within values (integer per dependent activity):")
            for generic_activity_id in dep_within:
                default_val = DEFAULT_WITHIN.get(generic_activity_id, 1)
                dep_within_values[generic_activity_id] = st.number_input(
                    f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' dep within value",
                    value=default_val,
                    key=f"dep_within_{generic_activity_id}",
                    min_value=0,
                    help=f"Maximum number of intervals allowed to complete dependent activity '{activity_full_names.get(generic_activity_id, generic_activity_id)}'."
                )
        
        dep_until_values = {}
        if not dep_until:
            st.info("No dependent activities selected in dep_until. Add activity IDs above to set dep until values.")
        else:
            st.subheader("dependent until values (integer per dependent activity):")
            for generic_activity_id in dep_until:
                dep_until_values[generic_activity_id] = st.number_input(
                    f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' dep until value",
                    key=f"dep_until_{generic_activity_id}",
                    min_value=0,
                    help=f"Maximum number of intervals allowed to complete dependent activity '{activity_full_names.get(generic_activity_id, generic_activity_id)}'."
                )
        


        if dep_within_values:
            within.update(dep_within_values)
        
        if dep_until_values:
            until.update(dep_until_values)


    # Priprema liste zavisnosti za model
    dependency_list = []
    for dep_id, rel in dependent_activity_relations.items():
        dependency_list.append({
            'dependent': dep_id,
            'depends_on': rel['depends_on'],
            'ratio': rel['ratio']
        })
    return ind_within, ind_until, dep_within, dep_until, within, until, overlap_activities, dependency_list


def collect_demand_data(activities, activity_full_names, N_set):
    """Collect and edit demand data."""
    st.subheader("Demand setup")
    selected_example = st.selectbox(
        "Odaberi defaultnu postavku potražnje:",
        ["Primjer 1", "Primjer 2"],
        key="demand_example_selector",
        help="Choose a predefined demand pattern to start with. You can then edit the values in the table below."
    )

    if selected_example == "Primjer 1":
        default_demand_data = DEMAND_EXAMPLE_1
    else:
        default_demand_data = DEMAND_EXAMPLE_2

    base_demand = {k: list(v) for k, v in default_demand_data.items()}

    # Convert to DataFrame
    initial_df_data = {}
    for generic_activity_id, demand_list in base_demand.items():
        if generic_activity_id in activities:
            full_activity_name = activity_full_names.get(generic_activity_id, generic_activity_id)
            if demand_list and len(demand_list[1:]) >= len(N_set):
                initial_df_data[full_activity_name] = demand_list[1:len(N_set)+1]
            elif demand_list:
                padded_list = demand_list[1:] + [0] * (len(N_set) - len(demand_list[1:]))
                initial_df_data[full_activity_name] = padded_list
            else:
                initial_df_data[full_activity_name] = [0] * len(N_set)

    if not initial_df_data:
        st.warning("No demand data available. Using dummy data.")
        if not N_set:
            N_set = [1]
        initial_df_data = {'Dummy Activity': [0] * len(N_set)}

    df_demand_editable = pd.DataFrame(initial_df_data, index=N_set)

    st.subheader("Edit Demand per Interval")
    edited_df_demand = st.data_editor(df_demand_editable, num_rows="fixed", use_container_width=True)

    # Find activity IDs for Istovar and Kontrola
    istovar_generic_id = None
    kontrola_generic_id = None
    for gen_id, full_name in activity_full_names.items():
        if full_name == activity_full_names.get('activity6', 'Istovar'):
            istovar_generic_id = gen_id
        if full_name == activity_full_names.get('activity4', 'Kontrola'):
            kontrola_generic_id = gen_id

    if istovar_generic_id and kontrola_generic_id and activity_full_names.get(istovar_generic_id) in edited_df_demand.columns:
        edited_df_demand[activity_full_names.get(kontrola_generic_id)] = (
            edited_df_demand[activity_full_names.get(istovar_generic_id)] * 0.5
        ).apply(round)

    # Convert back to dictionary
    final_demand_for_model = {}
    for full_col_name in edited_df_demand.columns:
        generic_col_id = None
        for gen_id, full_name in activity_full_names.items():
            if full_name == full_col_name:
                generic_col_id = gen_id
                break
        if generic_col_id:
            final_demand_for_model[generic_col_id] = [0] + edited_df_demand[full_col_name].tolist()

    return final_demand_for_model, istovar_generic_id, kontrola_generic_id


def collect_constraint_parameters():
    """Collect constraint parameters from sidebar."""
    with st.sidebar.expander("Constraint Parameters"):
        max_workers_per_interval = st.number_input(
            "Max Workers Per Interval",
            min_value=1,
            max_value=200,
            value=DEFAULT_MAX_WORKERS_PER_INTERVAL,
            step=1,
            help="Maximum number of workers that can be assigned to work in a single time interval. This constraint prevents overcrowding and ensures safety."
        )
        
        max_m1_shifts = st.number_input(
            "Max M1 Shifts (Full-time)",
            min_value=1,
            max_value=50,
            value=DEFAULT_MAX_M1_SHIFTS,
            step=1,
            help="Maximum number of full-time shifts that can be scheduled. Full-time shifts typically have longer working hours."
        )
        
        max_m2_shifts = st.number_input(
            "Max M2 Shifts (Part-time)",
            min_value=1,
            max_value=50,
            value=DEFAULT_MAX_M2_SHIFTS,
            step=1,
            help="Maximum number of part-time shifts that can be scheduled. Part-time shifts usually have shorter working hours."
        )
        
        m2_ratio_limit = st.slider(
            "M2 Ratio Limit",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_M2_RATIO_LIMIT,
            step=0.05,
            help="Maximum ratio of part-time shifts (M2) relative to total shifts (M1 + M2). For example, 0.3 means max 30% of shifts can be part-time."
        )
        
        istovar_kontrola_ratio = st.slider(
            "Istovar-Kontrola Ratio",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_ISTOVAR_KONTROLA_RATIO,
            step=0.05,
            help="Udio radnika za kontrolu u odnosu na broja radnika kojio obavljaju istovar."
       )
        non_primary_activities_ratio = st.slider(
            "Non-Primary Activities Ratio",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_NON_PRIMARY_ACTIVITIES_RATIO,
            step=0.05,
            help="Maximum ratio of non-primary activities that full-time workers (M1) can perform. For example, 0.5 means max 50% of their work can be non-primary activities."
        )
        
    
    return max_workers_per_interval, max_m1_shifts, max_m2_shifts, m2_ratio_limit, non_primary_activities_ratio, istovar_kontrola_ratio
