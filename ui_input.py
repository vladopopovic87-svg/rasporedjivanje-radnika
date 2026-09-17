# UI input handling and parameter collection

import streamlit as st
import pandas as pd
from config import *
from utils import parse_list, generate_profile_types, generate_activities
from translations import get_text


def collect_general_parameters():
    """Collect general model parameters from sidebar."""
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("general_parameters", lang)):
        st.markdown(
            """
            <style>
            [class*="st-key-remove_profile_"] button,
            [class*="st-key-remove_activity_"] button,
            button[aria-label="×"] {
                color: #d32f2f !important;
                background: transparent !important;
                border: 0 !important;
                box-shadow: none !important;
                min-height: 0 !important;
                padding: 0 !important;
                transform: translateY(-0.1rem);
                font-size: 10rem !important;
            }
            [class*="st-key-remove_profile_"] button:hover,
            [class*="st-key-remove_activity_"] button:hover,
            button[aria-label="×"]:hover {
                color: #9f1d1d !important;
                background: transparent !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        num_profiles = st.number_input(
            get_text("num_profiles", lang),
            min_value=1,
            value=DEFAULT_NUM_PROFILES,
            step=1,
            help=get_text("num_profiles_help", lang)
        )
        all_profile_types = generate_profile_types(num_profiles)
        removed_profiles = st.session_state.setdefault("removed_profiles", set())
        profil_types = [
            profile_id for profile_id in all_profile_types
            if profile_id not in removed_profiles
        ]

        num_activities = st.number_input(
            get_text("num_activities", lang),
            min_value=1,
            value=DEFAULT_NUM_ACTIVITIES,
            step=1,
            help=get_text("num_activities_help", lang)
        )
        all_activities = generate_activities(num_activities)
        removed_activities = st.session_state.setdefault("removed_activities", set())
        activities = [
            activity_id for activity_id in all_activities
            if activity_id not in removed_activities
        ]

        # Profile names and codes
        st.subheader(get_text("define_profile_names", lang))
        profile_full_names = {}
        sp = {}
        for generic_profile_id in profil_types:
            profile_number = generic_profile_id.removeprefix("profil")
            st.markdown(f"**Profil {profile_number}**")
            default_full = DEFAULT_FULL_PROFILE_NAMES.get(generic_profile_id, generic_profile_id.capitalize())
            default_short = DEFAULT_SHORT_PROFILES.get(generic_profile_id, generic_profile_id[0:2])
            name_col, code_col, remove_col = st.columns(
                [2, 1, 0.35], vertical_alignment="top"
            )
            with name_col:
                profile_full_names[generic_profile_id] = st.text_input(
                    get_text('full_name_for', lang),
                    value=default_full,
                    key=f"full_name_profile_{generic_profile_id}",
                    help=get_text('profile_full_name_help', lang)
                )
            with code_col:
                sp[generic_profile_id] = st.text_input(
                    get_text('short_code_for', lang),
                    value=default_short,
                    key=f"short_code_profile_{generic_profile_id}",
                    help=get_text('profile_short_code_help', lang)
                )
            with remove_col:
                if st.button(
                    "×",
                    key=f"remove_profile_{generic_profile_id}",
                    disabled=len(profil_types) <= 1,
                    help=get_text("remove_profile_help", lang),
                ):
                    removed_profiles.add(generic_profile_id)
                    st.rerun()

        # Activity names and codes
        st.subheader(get_text("define_activity_names", lang))
        s = {}
        activity_full_names = {}
        for generic_activity_id in activities:
            activity_number = generic_activity_id.removeprefix("activity")
            st.markdown(f"**Aktivnost {activity_number}**")
            default_full = DEFAULT_FULL_ACTIVITY_NAMES.get(generic_activity_id, generic_activity_id.capitalize())
            default_short = DEFAULT_SHORT_ACTIVITIES.get(generic_activity_id, generic_activity_id[0:2])
            name_col, code_col, remove_col = st.columns(
                [2, 1, 0.35], vertical_alignment="top"
            )
            with name_col:
                activity_full_names[generic_activity_id] = st.text_input(
                    get_text('full_name_for', lang),
                    value=default_full,
                    key=f"full_name_activity_{generic_activity_id}",
                    help=get_text("activity_full_name_help", lang)
                )
            with code_col:
                s[generic_activity_id] = st.text_input(
                    get_text('short_code_for', lang),
                    value=default_short,
                    key=f"short_code_activity_{generic_activity_id}",
                    help=get_text("activity_short_code_help", lang)
                )
            with remove_col:
                if st.button(
                    "×",
                    key=f"remove_activity_{generic_activity_id}",
                    disabled=len(activities) <= 1,
                    help=get_text("remove_activity_help", lang),
                ):
                    removed_activities.add(generic_activity_id)
                    st.rerun()

    return profil_types, activities, profile_full_names, sp, activity_full_names, s


def collect_interval_and_shift_parameters():
    """Collect interval and shift set parameters."""
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("interval_shift_sets", lang)):
        display_start_interval = st.number_input(
            get_text("start_working_day", lang),
            min_value=1,
            max_value=100,
            value=8,
            step=1,
            key="display_start_interval",
            help=get_text("display_start_interval_help", lang)
        )

        full_time_shift_length = st.number_input(
            get_text("full_time_shift_length", lang),
            min_value=1,
            max_value=100,
            value=DEFAULT_FULL_TIME_SHIFT_LENGTH,
            step=1,
            key="full_time_shift_length",
            help=get_text("full_time_shift_length_help", lang)
        )

        half_time_shift_length = st.number_input(
            get_text("half_time_shift_length", lang),
            min_value=1,
            max_value=100,
            value=DEFAULT_HALF_TIME_SHIFT_LENGTH,
            step=1,
            key="half_time_shift_length",
            help=get_text("half_time_shift_length_help", lang)
        )

        interval_duration = st.number_input(
            get_text("interval_duration", lang),
            min_value=15,
            max_value=1440,
            value=60,
            step=15,
            key="interval_duration",
            help=get_text("interval_duration_help", lang)
        )
       

        rest_duration = st.number_input(
            get_text("rest_duration", lang),
            min_value=15,
            max_value=1440,
            value=60,
            step=15,
            key="rest_duration",
            help=get_text("rest_duration_help", lang)
        )
       

        num_intervals = st.number_input(
            get_text("num_intervals_label", lang),
            min_value=1,
            max_value=100,
            value=len(DEFAULT_N_SET),
            step=1,
            key="num_intervals",
            help=get_text("num_intervals_help", lang)
        )
        N_set = list(range(1, num_intervals + 1))

        generated_M1_set = list(range(1, max(0, num_intervals - full_time_shift_length + 1) + 1))
        generated_M2_set = list(range(
            DEFAULT_M2_SHIFT_START,
            DEFAULT_M2_SHIFT_START + max(0, num_intervals - half_time_shift_length + 1)
        ))
        generated_M1_set_str = ', '.join(map(str, generated_M1_set))
        generated_M2_set_str = ', '.join(map(str, generated_M2_set))

        user_M1_set_str = st.text_area(
            get_text("m1_set_label", lang),
            generated_M1_set_str,
            help=get_text("m1_set_help", lang)
        )
        M1_set = parse_list(user_M1_set_str, int)
        if not M1_set:
            M1_set = generated_M1_set

        user_M2_set_str = st.text_area(
            get_text("m2_set_label", lang),
            generated_M2_set_str,
            help=get_text("m2_set_help", lang)
        )
        M2_set = parse_list(user_M2_set_str, int)

        M_set = sorted(set(M1_set + M2_set))
        M_set_str = ', '.join(map(str, M_set))

        st.text_area(
            get_text("m_set_label", lang),
            value=M_set_str,
            disabled=True,
            help=get_text("m_set_help", lang)
        )

        st.subheader(get_text("oj_intervals_label", lang))
        Oj = {}
        for j_shift in M1_set:
            default_oj_intervals = DEFAULT_OJ.get(j_shift, [])
            oj_intervals_str = st.text_area(
                f"{get_text('intervals_for_shift', lang)} {j_shift} {get_text('comma_separated_integers', lang)}",
                value=', '.join(map(str, default_oj_intervals)),
                key=f"Oj_{j_shift}",
                help=f"{get_text('oj_help_prefix', lang)} {j_shift}. {get_text('oj_intervals_help', lang)}"
            )
            Oj[j_shift] = parse_list(oj_intervals_str, int)

        min_len = st.number_input(
            get_text("min_len_label", lang),
            min_value=1,
            max_value=100,
            value=3,
            step=1,
            key="min_len",
            help=get_text("min_len_help", lang)
        )

    return display_start_interval, full_time_shift_length, half_time_shift_length, interval_duration, rest_duration, N_set, M_set, M1_set, M2_set, Oj, min_len


def collect_cost_coefficients(profil_types, profile_full_names):
    """Collect cost coefficients for shifts."""
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("cost_coefficients", lang)):
        st.write(get_text("m1_cost_rates", lang))
        ct_m1_inputs = {}
        for p_type in profil_types:
            default_rate = DEFAULT_CT_RATES.get((p_type, 'm1'), 1.0)
            ct_m1_inputs[p_type] = st.number_input(
                f"{profile_full_names.get(p_type, p_type)} (M1)",
                value=default_rate,
                key=f"ct_m1_{p_type}",
                help=f"{get_text('m1_cost_help', lang)} {profile_full_names.get(p_type, p_type)} {get_text('working_full_time', lang)}"
            )

        st.write(get_text("m2_cost_rates", lang))
        ct_m2_inputs = {}
        for p_type in profil_types:
            default_rate = DEFAULT_CT_RATES.get((p_type, 'm2'), 0.5)
            ct_m2_inputs[p_type] = st.number_input(
                f"{profile_full_names.get(p_type, p_type)} (M2)",
                value=default_rate,
                key=f"ct_m2_{p_type}",
                help=f"{get_text('m2_cost_help', lang)} {profile_full_names.get(p_type, p_type)} {get_text('working_part_time', lang)}"
            )

        P = st.number_input(
            get_text("short_duration_penalty", lang),
            min_value=0.00,
            max_value=1.00,
            value=0.00,
            step=0.01,
            help=get_text("p_help_transition_penalty", lang)
        )

    return P, ct_m1_inputs, ct_m2_inputs


def compute_able_from_allowed(allowed, profil_types, activities):
    """Derive profile activity list from the allowed profiles-per-activity mapping."""
    able = {}
    for generic_profile_id in profil_types:
        able[generic_profile_id] = [
            generic_activity_id
            for generic_activity_id in activities
            if generic_profile_id in allowed.get(generic_activity_id, [])
        ]
    return able


def collect_role_activity_mappings(profil_types, activities, profile_full_names, activity_full_names):
    """Collect role-activity mappings from user input."""
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("role_activity_mappings", lang)):
        st.subheader(get_text("allowed_activities_per_role", lang))
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
                f"{get_text('profiles_for', lang)} '{activity_full_names.get(generic_activity_id, generic_activity_id)}'",
                options=[profile_full_names.get(p, p) for p in profil_types],
                default=default_selection_full_names,
                key=f"allowed_{generic_activity_id}",
                help=f"{get_text('select_which_workers', lang)} '{activity_full_names.get(generic_activity_id, generic_activity_id)}'."
            )
            allowed[generic_activity_id] = [
                pid for full_name in selected_full_names
                for pid, pf_name in profile_full_names.items()
                if pf_name == full_name
            ]

        role_activity_validation_errors = [
            get_text("activity_profile_required", lang).format(
                activity=activity_full_names.get(activity_id, activity_id)
            )
            for activity_id in activities
            if not allowed.get(activity_id)
        ]

        able = compute_able_from_allowed(allowed, profil_types, activities)
        with st.expander(get_text("able_activities_per_profile", lang), expanded=False):
            for generic_profile_id in profil_types:
                derived_full_names = [
                    activity_full_names.get(aid, aid) for aid in able.get(generic_profile_id, [])
                ]
                st.write(
                    f"{get_text('activities_for', lang)} '{profile_full_names.get(generic_profile_id, generic_profile_id)}'"
                )
                st.multiselect(
                    "",
                    options=[activity_full_names.get(a, a) for a in activities],
                    default=derived_full_names,
                    disabled=True,
                    label_visibility="collapsed"
                )

        st.subheader(get_text("primary_able_activities", lang))
        primary_able = {}
        for generic_profile_id in profil_types:
            default_selection_generic_ids = [
                aid for aid in DEFAULT_PRIMARY_ABLE.get(generic_profile_id, [])
                if aid in able.get(generic_profile_id, [])
            ]
            default_selection_full_names = [
                activity_full_names.get(aid, aid) for aid in default_selection_generic_ids
            ]

            selected_full_names = st.multiselect(
                f"{get_text('primary_activities_for', lang)} '{profile_full_names.get(generic_profile_id, generic_profile_id)}'",
                options=[activity_full_names.get(a, a) for a in able.get(generic_profile_id, [])],
                default=default_selection_full_names,
                key=f"primary_able_{generic_profile_id}",
                help=f"{get_text('select_which_activities', lang)} {profile_full_names.get(generic_profile_id, generic_profile_id)} {get_text('can_perform_primary', lang)}."
            )
            primary_able[generic_profile_id] = [
                aid for full_name in selected_full_names
                for aid, af_name in activity_full_names.items()
                if af_name == full_name
            ]

        able_ne = {
            generic_profile_id: [
                aid for aid in able.get(generic_profile_id, [])
                if aid not in primary_able.get(generic_profile_id, [])
            ]
            for generic_profile_id in profil_types
        }

    return allowed, able, able_ne, role_activity_validation_errors


def collect_variant_parameters(activities, activity_full_names):
    """Collect variant-dependent parameters."""
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("variant_dependent_parameters", lang), expanded=False):
        # Create reverse mapping: activity name -> ID
        name_to_id = {v: k for k, v in activity_full_names.items()}
        st.subheader(get_text("independent_activities", lang), help="Aktivnosti čiji zahtevi za radnicima se definišu kroz tabelu.")
        
        # ind_within with multiselect
        default_ind_within_generic_ids = [
            aid for aid in DEFAULT_IND_WITHIN
            if aid in activities
        ]
        default_ind_within_full_names = [
            activity_full_names.get(aid, aid) for aid in default_ind_within_generic_ids
        ]
        
        selected_ind_within_names = st.multiselect(
            get_text("ind_within", lang),
            options=[activity_full_names.get(a, a) for a in activities],
            default=default_ind_within_full_names,
            key="ind_within_multiselect",
            help=get_text("ind_within_help", lang)
        )
        # Convert names back to IDs
        ind_within = [name_to_id.get(name, name) for name in selected_ind_within_names]

        # ind_until with multiselect
        default_ind_until_generic_ids = [
            aid for aid in DEFAULT_IND_UNTIL
            if aid in activities
        ]
        default_ind_until_full_names = [
            activity_full_names.get(aid, aid) for aid in default_ind_until_generic_ids
        ]
        
        selected_ind_until_names = st.multiselect(
            get_text("ind_until", lang),
            options=[activity_full_names.get(a, a) for a in activities],
            default=default_ind_until_full_names,
            key="ind_until_multiselect",
            help=get_text("ind_until_help", lang)
        )
        # Convert names back to IDs
        ind_until = [name_to_id.get(name, name) for name in selected_ind_until_names]

        # Validation for overlap
        overlap_activities = set(ind_within).intersection(set(ind_until))
        if overlap_activities:
            overlap_full_names = [activity_full_names.get(a, a) for a in overlap_activities]
            st.error(f"{get_text('error_overlap', lang)} {', '.join(overlap_full_names)}")
        
        within = {}
        if not ind_within:
            st.info(get_text("no_activities_ind_within", lang))
        else:
            st.markdown(
                f"<span style='color: black; font-weight: normal;'>{get_text('within_values', lang)}</span>",
                unsafe_allow_html=True
            )
            for generic_activity_id in ind_within:
                default_val = DEFAULT_WITHIN.get(generic_activity_id)
                within[generic_activity_id] = st.number_input(
                    f"{get_text('within_value', lang)} za {activity_full_names.get(generic_activity_id, generic_activity_id)}",
                    value=default_val,
                    key=f"within_{generic_activity_id}",
                    min_value=0,
                    help=get_text('within_help', lang).format(activity=activity_full_names.get(generic_activity_id, generic_activity_id))
                )

        until = {}
        if not ind_until:
            st.info(get_text("no_activities_ind_until", lang))
        else:
            st.markdown(
                f"<span style='color: black; font-weight: normal;'>{get_text('until_values', lang)}</span>",
                unsafe_allow_html=True
            )
            for generic_activity_id in ind_until:
                default_val = DEFAULT_UNTIL.get(generic_activity_id)
                until[generic_activity_id] = st.number_input(
                    f"{get_text('until_value', lang)} za {activity_full_names.get(generic_activity_id, generic_activity_id)}",
                    value=default_val,
                    key=f"until_{generic_activity_id}",
                    min_value=0,
                    help=get_text('until_help', lang).format(activity=activity_full_names.get(generic_activity_id, generic_activity_id))
                )

        st.subheader(get_text("dependent_activities", lang), help="Aktivnosti čiji zahtevi za radnicima zavise od realizacije drugih aktivnosti")

        # dep_within with multiselect
        default_dep_within_generic_ids = [
            aid for aid in DEFAULT_DEP_WITHIN
            if aid in activities
        ]
        default_dep_within_full_names = [
            activity_full_names.get(aid, aid) for aid in default_dep_within_generic_ids
        ]
        
        selected_dep_within_names = st.multiselect(
            get_text("dep_within", lang),
            options=[activity_full_names.get(a, a) for a in activities],
            default=default_dep_within_full_names,
            key="dep_within_multiselect",
            help=get_text('dependent_within_help', lang)
        )
        # Convert names back to IDs
        dep_within = [name_to_id.get(name, name) for name in selected_dep_within_names]
        
        # dep_until with multiselect
        default_dep_until_generic_ids = [
            aid for aid in DEFAULT_DEP_UNTIL
            if aid in activities
        ]
        default_dep_until_full_names = [
            activity_full_names.get(aid, aid) for aid in default_dep_until_generic_ids
        ]
        
        selected_dep_until_names = st.multiselect(
            get_text("dep_until", lang),
            options=[activity_full_names.get(a, a) for a in activities],
            default=default_dep_until_full_names,
            key="dep_until_multiselect",
            help=get_text('dependent_until_help', lang)
        )
        # Convert names back to IDs
        dep_until = [name_to_id.get(name, name) for name in selected_dep_until_names]

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
                get_text('dep_ratio_prompt', lang).format(dependent=activity_full_names.get(dep_activity_id, dep_activity_id), depends_on=activity_full_names.get(depends_on_id, depends_on_id)),
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                key=f"dep_ratio_{dep_activity_id}"
            )
            dependent_activity_relations[dep_activity_id] = {"depends_on": depends_on_id, "ratio": ratio_val}

        dep_within_values = {}
        if dep_within:
            st.markdown(f"<span style='color: black; font-weight: normal;'>{get_text('dep_within_values_header', lang)}</span>", unsafe_allow_html=True)
            for generic_activity_id in dep_within:
                default_val = DEFAULT_WITHIN.get(generic_activity_id)
                dep_within_values[generic_activity_id] = st.number_input(
                    f"{get_text('dep_within_value_label', lang)} za {activity_full_names.get(generic_activity_id, generic_activity_id)}",
                    value=default_val,
                    key=f"dep_within_{generic_activity_id}",
                    min_value=0,
                    help=get_text('within_help', lang).format(activity=activity_full_names.get(generic_activity_id, generic_activity_id))
                )
        
        dep_until_values = {}
        if dep_until:
            st.markdown(f"<span style='color: black; font-weight: normal;'>{get_text('dep_until_values_header', lang)}</span>", unsafe_allow_html=True)
            for generic_activity_id in dep_until:
                dep_until_values[generic_activity_id] = st.number_input(
                    f"{get_text('dep_until_value_label', lang)} za {activity_full_names.get(generic_activity_id, generic_activity_id)}",
                    key=f"dep_until_{generic_activity_id}",
                    min_value=0,
                    help=get_text('until_help', lang).format(activity=activity_full_names.get(generic_activity_id, generic_activity_id))
                )
        


        if dep_within_values:
            within.update(dep_within_values)
        
        if dep_until_values:
            until.update(dep_until_values)

        activity_validation_errors = []
        activity_types = {
            activity_id: [activity_type for activity_type, selected_ids in (
                ("ind_within", ind_within),
                ("ind_until", ind_until),
                ("dep_within", dep_within),
                ("dep_until", dep_until),
            ) if activity_id in selected_ids]
            for activity_id in activities
        }
        for activity_id, selected_types in activity_types.items():
            activity_name = activity_full_names.get(activity_id, activity_id)
            if not selected_types:
                activity_validation_errors.append(
                    get_text("activity_type_required", lang).format(activity=activity_name)
                )
            elif len(selected_types) > 1:
                activity_validation_errors.append(
                    get_text("activity_type_multiple", lang).format(activity=activity_name)
                )

        value_by_type = {
            "ind_within": within,
            "ind_until": until,
            "dep_within": dep_within_values,
            "dep_until": dep_until_values,
        }
        for activity_id, selected_types in activity_types.items():
            for activity_type in selected_types:
                if value_by_type[activity_type].get(activity_id) is None:
                    activity_validation_errors.append(
                        get_text("activity_value_required", lang).format(
                            activity=activity_full_names.get(activity_id, activity_id),
                            value_type=get_text(activity_type, lang),
                        )
                    )

    # Priprema liste zavisnosti za model
    dependency_list = []
    for dep_id, rel in dependent_activity_relations.items():
        dependency_list.append({
            'dependent': dep_id,
            'depends_on': rel['depends_on'],
            'ratio': rel['ratio']
        })
    return (
        ind_within, ind_until, dep_within, dep_until, within, until,
        overlap_activities, dependency_list, activity_validation_errors,
    )


def collect_demand_data(activities, activity_full_names, N_set):
    """Collect and edit demand data."""
    lang = st.session_state.get("language", "sr")
    st.subheader(get_text("demand_data", lang))
    selected_example = st.selectbox(
        get_text("select_demand_profile", lang),
        [get_text("demand_example_1", lang), get_text("demand_example_2", lang)],
        key="demand_example_selector",
        help=get_text('select_demand_profile_help', lang)
    )

    if selected_example == get_text("demand_example_1", lang):
        default_demand_data = DEMAND_EXAMPLE_1
    else:
        default_demand_data = DEMAND_EXAMPLE_2

    base_demand = {k: list(v) for k, v in default_demand_data.items()}

    # Convert to DataFrame
    initial_df_data = {}
    for generic_activity_id in activities:
        demand_list = base_demand.get(generic_activity_id, [])
        full_activity_name = activity_full_names.get(generic_activity_id, generic_activity_id)
        if demand_list and len(demand_list[1:]) >= len(N_set):
            initial_df_data[full_activity_name] = demand_list[1:len(N_set)+1]
        elif demand_list:
            padded_list = demand_list[1:] + [0] * (len(N_set) - len(demand_list[1:]))
            initial_df_data[full_activity_name] = padded_list
        else:
            initial_df_data[full_activity_name] = [0] * len(N_set)

    if not initial_df_data:
        st.warning(get_text("no_demand_data_dummy", lang))
        if not N_set:
            N_set = [1]
        initial_df_data = {get_text("dummy_activity", lang): [0] * len(N_set)}

    df_demand_editable = pd.DataFrame(initial_df_data, index=N_set)

    st.subheader(get_text("edit_demand_per_interval", lang))
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
    lang = st.session_state.get("language", "sr")
    with st.sidebar.expander(get_text("constraint_parameters", lang)):
        max_workers_per_interval = st.number_input(
            get_text("max_workers_per_interval", lang),
            min_value=1,
            max_value=200,
            value=DEFAULT_MAX_WORKERS_PER_INTERVAL,
            step=1,
            help=get_text('max_workers_per_interval_help', lang)
        )
        
        max_m1_shifts = st.number_input(
            get_text("max_m1_shifts", lang),
            min_value=1,
            max_value=50,
            value=DEFAULT_MAX_M1_SHIFTS,
            step=1,
            help=get_text('max_m1_shifts_help', lang)
        )
        
        max_m2_shifts = st.number_input(
            get_text("max_m2_shifts", lang),
            min_value=1,
            max_value=50,
            value=DEFAULT_MAX_M2_SHIFTS,
            step=1,
            help=get_text('max_m2_shifts_help', lang)
        )
        
        m2_ratio_limit = st.slider(
            get_text("m2_ratio_limit", lang),
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_M2_RATIO_LIMIT,
            step=0.05,
            help=get_text('m2_ratio_limit_help', lang)
        )
        
        istovar_kontrola_ratio = st.slider(
            get_text("istovar_kontrola_ratio", lang),
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_ISTOVAR_KONTROLA_RATIO,
            step=0.05,
            help=get_text('istovar_kontrola_ratio_help', lang)
       )
        non_primary_activities_ratio = st.slider(
            get_text("non_primary_activities_ratio", lang),
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_NON_PRIMARY_ACTIVITIES_RATIO,
            step=0.05,
            help=get_text('non_primary_activities_ratio_help', lang)
        )
        
    
    return max_workers_per_interval, max_m1_shifts, max_m2_shifts, m2_ratio_limit, non_primary_activities_ratio, istovar_kontrola_ratio
