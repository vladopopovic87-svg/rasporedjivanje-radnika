# Main Streamlit application - Worker Scheduling Optimization

import streamlit as st
from pulp import LpProblem, LpMinimize, PULP_CBC_CMD, LpStatus, LpStatusOptimal, value
from collections import defaultdict

# Import modules
from config import *
from utils import parse_list
from ui_input import (
    collect_general_parameters,
    collect_interval_and_shift_parameters,
    collect_cost_coefficients,
    collect_role_activity_mappings,
    collect_variant_parameters,
    collect_demand_data
)
from model_builder import (
    build_model_variables,
    build_delta_variables,
    setup_objective_function,
    add_demand_constraints,
    add_activity_within_constraints,
    add_activity_until_constraints,
    add_activity_allocation_constraints,
    add_worker_capacity_constraints,
    add_interval_worker_limit,
    add_shift_constraints,
    add_istovar_kontrola_constraint
)
from results_display import (
    build_bij_matrix,
    build_ct_matrix,
    generate_schedule_output,
    balance_schedules,
    create_shift_allocation_table,
    create_demand_comparison_table,
    count_idle_intervals,
    analyze_activity_sequences,
    display_results
)


def main():
    """Main application logic."""
    st.set_page_config(layout="wide")
    st.title("Optimization Model with PuLP and Streamlit")
    st.sidebar.header("Model Parameters")

    # Collect all input parameters
    (P, profil_types, activities, profile_full_names, sp, 
     activity_full_names, s) = collect_general_parameters()

    (display_start_interval, N_set, M_set, M1_set, M2_set, 
     Oj) = collect_interval_and_shift_parameters()

    ct_m1_inputs, ct_m2_inputs = collect_cost_coefficients(profil_types, profile_full_names)

    allowed, able, able_ne = collect_role_activity_mappings(
        profil_types, activities, profile_full_names, activity_full_names
    )

    (ind_within, ind_until, dep_within, within, until, 
     overlap_activities) = collect_variant_parameters(activities, activity_full_names)

    demand, istovar_generic_id, kontrola_generic_id = collect_demand_data(activities, activity_full_names, N_set)

    # Run optimization button
    run_optimization_disabled = bool(overlap_activities)
    if st.button('Run Optimization', disabled=run_optimization_disabled):
        st.write("Running optimization with current parameters.")

        # Build PuLP model
        model = LpProblem("Cost minimising problem", LpMinimize)

        # Build matrices
        bij = build_bij_matrix(M_set, M1_set, M2_set, N_set)
        ct = build_ct_matrix(M_set, M1_set, M2_set, profil_types, ct_m1_inputs, ct_m2_inputs)

        # Build variables
        yjz, yj, ytj, ytija, xaijk = build_model_variables(
            profil_types, M_set, M1_set, M2_set, N_set, activities
        )
        delta = build_delta_variables(P, profil_types, M_set, N_set, activities)

        # Setup objective function
        obj_part_1, obj_part_2 = setup_objective_function(
            model, P, profil_types, M_set, ytj, delta, ct, activities
        )

        # Add delta constraints if P > 0
        if P > 0:
            for t in profil_types:
                for j in M_set:
                    for a in activities:
                        if a in able.get(t, []):
                            for i in N_set:
                                if i < max(N_set):
                                    if (t, j, a, i) in delta and (t, i, j, a) in ytija and (t, i + 1, j, a) in ytija:
                                        model += (
                                            delta[t, j, a, i] >= ytija[t, i, j, a] - ytija[t, i + 1, j, a]
                                        )
                                        model += delta[t, j, a, i] >= 0

        # Add constraints
        st.write("--- Model setup complete. Adding constraints. ---")

        add_activity_within_constraints(
            model, ind_within, N_set, M_set, profil_types, activities, 
            xaijk, bij, demand, within, able, activity_full_names
        )

        add_activity_until_constraints(
            model, ind_until, N_set, M_set, xaijk, bij, demand, until, activity_full_names
        )

        add_istovar_kontrola_constraint(
            model, istovar_generic_id, kontrola_generic_id, N_set, M_set, xaijk, bij, ratio=0.5
        )

        add_activity_allocation_constraints(
            model, activities, M_set, N_set, xaijk, ytija, bij, allowed
        )

        add_worker_capacity_constraints(
            model, profil_types, N_set, M_set, ytj, ytija, able
        )

        add_interval_worker_limit(
            model, N_set, profil_types, M_set, ytija, MAX_WORKERS_PER_INTERVAL
        )

        # Additional constraints from original code
        # Constraint 6: Rest interval limits for M1 shifts
        for j in M1_set:
            for p_type_id in profil_types:
                if (p_type_id, j) in ytj:
                    rest_sum = 0
                    for i in Oj.get(j, []):
                        for a_id in activities:
                            if (p_type_id, i, j, a_id) in ytija and (i, j) in bij:
                                rest_sum += ytija[(p_type_id, i, j, a_id)] * bij[(i, j)]
                    model += rest_sum <= 2 * ytj[(p_type_id, j)], f"Constraint_6_{j}_{p_type_id}"

        # Constraint 7: M2 ratio limit
        for p_type_id in profil_types:
            if M2_set:
                sum_m2 = sum(ytj[(p_type_id, j)] for j in M2_set if (p_type_id, j) in ytj)
                sum_m_total = sum(ytj[(p_type_id, j)] for j in M_set if (p_type_id, j) in ytj)
                model += sum_m2 <= M2_RATIO_LIMIT * sum_m_total, f"Constraint_7_{p_type_id}"

        # Constraint 11: Non-primary activities ratio (M1 only)
        for j in M1_set:
            for p_type_id in profil_types:
                primary_sum = sum(
                    ytija[(p_type_id, i, j, a_id)] * bij.get((i, j), 0)
                    for i in N_set for a_id in able.get(p_type_id, [])
                    if (p_type_id, i, j, a_id) in ytija and (i, j) in bij
                )
                non_primary_sum = sum(
                    ytija[(p_type_id, i, j, a_id)] * bij.get((i, j), 0)
                    for i in N_set for a_id in able_ne.get(p_type_id, [])
                    if (p_type_id, i, j, a_id) in ytija and (i, j) in bij
                )
                model += non_primary_sum <= NON_PRIMARY_ACTIVITIES_RATIO * primary_sum, \
                    f"Constraint_11_{j}_{p_type_id}"

        # Constraint 12: M1 vs M2 ratio per interval
        for i in N_set:
            m1_shifts_sum = sum(
                ytj[(p_type_id, j)] * bij.get((i, j), 0)
                for j in M1_set for p_type_id in profil_types
                if (p_type_id, j) in ytj and (i, j) in bij
            )
            m2_shifts_sum = sum(
                ytj[(p_type_id, j)] * bij.get((i, j), 0)
                for j in M2_set for p_type_id in profil_types
                if (p_type_id, j) in ytj and (i, j) in bij
            )
            model += m1_shifts_sum >= 0.0000001 * m2_shifts_sum, f"Constraint_12_{i}"

        add_shift_constraints(
            model, M_set, M1_set, M2_set, ytj, profil_types,
            yj, MAX_M1_SHIFTS, MAX_M2_SHIFTS
        )

        st.write("--- All constraints added. Solving model... ---")

        # Solve
        with st.spinner('Solving optimization problem...'):
            model.solve(PULP_CBC_CMD(msg=0))

        st.write(f"--- Solver Status: {LpStatus[model.status]} ---")

        # Process results
        if model.status == LpStatusOptimal:
            st.write("--- Model solved optimally. Processing results for display. ---")

            # Generate output
            smjena_output = generate_schedule_output(
                model, profil_types, M_set, M1_set, M2_set, N_set, ytj,
                ytija, activities, s, able
            )

            # Balance schedules
            st.write("--- Starting BALANCING ---")
            balance_schedules(smjena_output, M1_set, profil_types, ytj)

            # Create tables
            st.write("--- Starting DataFrame generation ---")
            df, df_display = create_shift_allocation_table(
                smjena_output, M_set, M1_set, M2_set, profil_types,
                ytj, sp, display_start_interval
            )

            # Calculate activity per interval
            activity_per_interval = defaultdict(lambda: defaultdict(float))
            for i in N_set:
                for a_id in activities:
                    total_activity = sum(
                        ytija[(p_type_id, i, j, a_id)].varValue or 0
                        for p_type_id in profil_types
                        for j in M_set
                        if (p_type_id, i, j, a_id) in ytija
                    )
                    activity_per_interval[i][a_id] = total_activity

            # Display results
            display_results(
                model, obj_part_1, obj_part_2, P, profil_types, M_set, M1_set, M2_set,
                N_set, ytj, ytija, activities, smjena_output, df, df_display,
                activity_per_interval, activity_full_names, demand
            )

        elif model.status == 0:  # LpStatusInfeasible
            st.error("Solver Status: Infeasible (No feasible solution found)")
        else:
            st.warning(f"Solver Status: {LpStatus[model.status]}")


if __name__ == "__main__":
    main()
