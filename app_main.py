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
    add_istovar_kontrola_constraint,
    add_delta_constraints,
    add_rest_interval_constraints,
    add_m2_ratio_constraint,
    add_non_primary_activities_constraint,
    add_m1_m2_ratio_per_interval_constraint
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
            model, P, profil_types, M_set,N_set, ytj, delta, ct, activities
        )

        # Add delta constraints if P > 0
        # Ograničenje za penalizovanje prelaska na drugu aktivnost nakon samo jednog intervala
        add_delta_constraints(
            model, P, profil_types, M_set, N_set, activities, ytija, delta, able
        )

        # Add constraints
        st.write("--- Model setup complete. Adding constraints. ---")

        # Constraint 2a
        add_activity_within_constraints(
            model, ind_within, N_set, M_set, profil_types, activities, 
            xaijk, bij, demand, within, able, activity_full_names
        )

        # Constraint 2b
        add_activity_until_constraints(
            model, ind_until, N_set, M_set, xaijk, bij, demand, until, activity_full_names
        )

        # Constraint 2d
        add_istovar_kontrola_constraint(
            model, istovar_generic_id, kontrola_generic_id, N_set, M_set, xaijk, bij, ratio=0.5
        )

        # Constraint 3
        add_activity_allocation_constraints(
            model, activities, M_set, N_set, xaijk, ytija, bij, allowed
        )

        # Constraint 4
        add_worker_capacity_constraints(
            model, profil_types, N_set, M_set, ytj, ytija, able
        )

        # Constraint 5
        add_interval_worker_limit(
            model, activities, N_set, profil_types, M_set, ytija, MAX_WORKERS_PER_INTERVAL
        )

        # Ograničenje za ukupan broj radnika i potražnje
        add_demand_constraints(
            model, activities, N_set, M_set, ytija, demand, profil_types
        )

        # Additional constraints from original code
        # Constraint 6
        add_rest_interval_constraints(
            model, M1_set, profil_types, ytj, ytija, activities, able, bij, Oj
        )

        # Constraint 7
        add_m2_ratio_constraint(
            model, profil_types, M2_set, M_set, ytj, M2_RATIO_LIMIT
        )

        # Constraint 11
        add_non_primary_activities_constraint(
            model, M1_set, profil_types, N_set, ytija, able, able_ne, bij, NON_PRIMARY_ACTIVITIES_RATIO
        )

        # Constraint 12
        add_m1_m2_ratio_per_interval_constraint(
            model, N_set, M1_set, M2_set, ytj, bij, profil_types
        )

        # Constraint 8,9,10
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
            smjena_output = balance_schedules(smjena_output, M1_set, profil_types, ytj)

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
