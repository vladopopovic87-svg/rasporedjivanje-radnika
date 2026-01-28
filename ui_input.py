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
            step=1
        )
        profil_types = generate_profile_types(num_profiles)

        num_activities = st.number_input(
            "Number of Activities",
            min_value=1,
            value=DEFAULT_NUM_ACTIVITIES,
            step=1
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
                key=f"full_name_profile_{generic_profile_id}"
            )
            default_short = DEFAULT_SHORT_PROFILES.get(generic_profile_id, generic_profile_id[0:2])
            sp[generic_profile_id] = st.text_input(
                f"Short code for '{generic_profile_id}'",
                value=default_short,
                key=f"short_code_profile_{generic_profile_id}"
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
                key=f"full_name_activity_{generic_activity_id}"
            )
            default_short = DEFAULT_SHORT_ACTIVITIES.get(generic_activity_id, generic_activity_id[0:2])
            s[generic_activity_id] = st.text_input(
                f"Short code for '{generic_activity_id}'",
                value=default_short,
                key=f"short_code_activity_{generic_activity_id}"
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
            key="display_start_interval"
        )

        user_N_set_str = st.text_area(
            "N_set (Intervals, comma-separated integers)",
            ', '.join(map(str, DEFAULT_N_SET))
        )
        N_set = parse_list(user_N_set_str, int)
        if not N_set:
            st.warning("N_set cannot be empty. Defaulting to default values.")
            N_set = DEFAULT_N_SET

        user_M_set_str = st.text_area(
            "M_set (Shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M_SET))
        )
        M_set = parse_list(user_M_set_str, int)
        if not M_set:
            st.warning("M_set cannot be empty. Defaulting to default values.")
            M_set = DEFAULT_M_SET

        user_M1_set_str = st.text_area(
            "M1_set (Full-time shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M1_SET))
        )
        M1_set = parse_list(user_M1_set_str, int)

        user_M2_set_str = st.text_area(
            "M2_set (Part-time shifts, comma-separated integers)",
            ', '.join(map(str, DEFAULT_M2_SET))
        )
        M2_set = parse_list(user_M2_set_str, int)

        st.subheader("Oj (Intervals available for rest shift j, only for M1 shifts):")
        Oj = {}
        for j_shift in M1_set:
            default_oj_intervals = DEFAULT_OJ.get(j_shift, [])
            oj_intervals_str = st.text_area(
                f"Intervals for shift {j_shift} (comma-separated integers)",
                value=', '.join(map(str, default_oj_intervals)),
                key=f"Oj_{j_shift}"
            )
            Oj[j_shift] = parse_list(oj_intervals_str, int)

    return display_start_interval, N_set, M_set, M1_set, M2_set, Oj


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
                key=f"ct_m1_{p_type}"
            )

        st.write("Part-time shift (M2) cost rates:")
        ct_m2_inputs = {}
        for p_type in profil_types:
            default_rate = DEFAULT_CT_RATES.get((p_type, 'm2'), 0.5)
            ct_m2_inputs[p_type] = st.number_input(
                f"{profile_full_names.get(p_type, p_type)} (M2)",
                value=default_rate,
                key=f"ct_m2_{p_type}"
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
                key=f"allowed_{generic_activity_id}"
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
                key=f"able_{generic_profile_id}"
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
                key=f"able_ne_{generic_profile_id}"
            )
            able_ne[generic_profile_id] = [
                aid for full_name in selected_full_names
                for aid, af_name in activity_full_names.items()
                if af_name == full_name
            ]

    return allowed, able, able_ne


def collect_variant_parameters(activities, activity_full_names):
    """Collect variant-dependent parameters."""
    with st.sidebar.expander("Variant-Dependent Parameters"):
        user_ind_within_str = st.text_area(
            "ind_within (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_IND_WITHIN)
        )
        ind_within = parse_list(user_ind_within_str)

        user_ind_until_str = st.text_area(
            "ind_until (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_IND_UNTIL)
        )
        ind_until = parse_list(user_ind_until_str)

        # Validation for overlap
        overlap_activities = set(ind_within).intersection(set(ind_until))
        if overlap_activities:
            overlap_full_names = [activity_full_names.get(a, a) for a in overlap_activities]
            st.error(f"Error: Activities in both 'ind_within' and 'ind_until': {', '.join(overlap_full_names)}")

        user_dep_within_str = st.text_area(
            "dep_within (comma-separated generic activity IDs)",
            ', '.join(DEFAULT_DEP_WITHIN)
        )
        dep_within = parse_list(user_dep_within_str)

        st.subheader("within values (integer per activity):")
        within = {}
        for generic_activity_id in ind_within:
            default_val = DEFAULT_WITHIN.get(generic_activity_id, 1)
            within[generic_activity_id] = st.number_input(
                f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' within value",
                value=default_val,
                key=f"within_{generic_activity_id}",
                min_value=0
            )

        st.subheader("until values (integer per activity):")
        until = {}
        for generic_activity_id in ind_until:
            default_val = DEFAULT_UNTIL.get(generic_activity_id, 1)
            until[generic_activity_id] = st.number_input(
                f"'{activity_full_names.get(generic_activity_id, generic_activity_id)}' until value",
                value=default_val,
                key=f"until_{generic_activity_id}",
                min_value=0
            )

    return ind_within, ind_until, dep_within, within, until, overlap_activities


def collect_demand_data(activities, activity_full_names, N_set):
    """Collect and edit demand data."""
    st.subheader("Demand setup")
    selected_example = st.selectbox(
        "Odaberi defaultnu postavku potražnje:",
        ["Primjer 1", "Primjer 2"],
        key="demand_example_selector"
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

    return final_demand_for_model
