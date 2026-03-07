# Model building and constraint definition

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatusOptimal
from config import *


def build_model_variables(profil_types, M_set, M1_set, M2_set, N_set, activities):
    """Build PuLP decision variables."""
    yjz = LpVariable.dicts(
        "u smeni z",
        ((j) for j in M_set),
        lowBound=0,
        cat='Integer'
    )

    yj = LpVariable.dicts(
        "u smeni",
        ((j) for j in M_set),
        lowBound=0,
        upBound=1,
        cat='Integer'
    )

    ytj = LpVariable.dicts(
        "u smeni profila",
        ((t, j) for t in profil_types for j in M_set),
        lowBound=0,
        cat='Integer'
    )

    ytija = LpVariable.dicts(
        "u intervalu",
        ((t, i, j, a) for t in profil_types for i in N_set for j in M_set for a in activities),
        lowBound=0,
        cat='Integer'
    )

    xaijk = LpVariable.dicts(
        "u intervalu",
        ((a, i, j, k) for a in activities for i in N_set for j in M_set for k in N_set),
        lowBound=0,
        cat='Integer'
    )

    return yjz, yj, ytj, ytija, xaijk


def build_delta_variables(P, profil_types, M_set, N_set, activities):
    """Build delta penalty variables if P > 0."""
    if P > 0:
        delta = LpVariable.dicts(
            "delta_switch",
            ((t, j, a, i) for t in profil_types for j in M_set
             for a in activities for i in N_set if i < max(N_set)),
            lowBound=0,
            cat='Continuous'
        )
    else:
        delta = {}
    return delta


def setup_objective_function(model, P, profil_types, M_set,N_set, ytj, delta, ct, activities):
    """Setup the objective function."""
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
            if i<max(N_set)
        )
        model += obj_part_1 + P * obj_part_2, "Total Cost"
    else:
        model += obj_part_1, "Total Cost"

    return obj_part_1, obj_part_2 if P > 0 else None


# Ograničenje za penalizovanje prelaska na drugu aktivnost nakon samo jednog intervala
def add_delta_constraints(model, P, profil_types, M_set, N_set, activities, ytija, delta, able):
    """Add delta penalty constraints if P > 0."""
    if P > 0:
        for t in profil_types:
            for j in M_set:
                for a in activities:
                    if a in able.get(t, []):
                        for i in N_set:
                            if i < max(N_set):
                                if (t, j, a, i) in delta and (t, i, j, a) in ytija and (t, i + 1, j, a) in ytija:
                                    model += delta[t, j, a, i] >= ytija[t, i, j, a] - ytija[t, i + 1, j, a]
                                model += delta[t, j, a, i] >= 0


# Ograničenje za ukupan broj radnika i potražnje
def add_demand_constraints(model, activities, N_set, M_set, ytija, demand, profil_types):
    """Add constraint for total demand satisfaction."""
    for a in activities:
        model += lpSum(
            ytija[t, i, j, a]
            for t in profil_types
            for i in N_set
            for j in M_set
        ) == sum(demand[a]), f"Demand_{a}"


# Constraint 2a
def add_activity_within_constraints(model, ind_within, N_set, M_set, profil_types, 
                                    activities, xaijk, bij, demand, within, able, activity_full_names):
    """Add constraints for activities with 'within' requirement."""
    for a_id in ind_within:
        for i in N_set:
            if a_id in demand and i < len(demand[a_id]):
                model += lpSum(
                    xaijk[(a_id, i, j, k)] * bij.get((k, j), 0)
                    for k in range(i, min(i + within.get(a_id, 11), 12))
                    for j in M_set if (a_id, i, j, k) in xaijk and (k, j) in bij
                ) == demand[a_id][i], f"Constraint_within_{activity_full_names.get(a_id, a_id)}_{i}"

                model += lpSum(
                    xaijk[(a_id, i, j, k)]
                    for k in N_set
                    for j in M_set if (a_id, i, j, k) in xaijk
                ) == demand[a_id][i], f"Constraint_within_sum_{activity_full_names.get(a_id, a_id)}_{i}"


def add_activity_until_constraints(model, ind_until, N_set, M_set, xaijk, bij, 
                                   demand, until, activity_full_names):
    """Add constraints for activities with 'until' requirement."""
    for a_id in ind_until:
        for i in N_set:
            if a_id in demand and i < len(demand[a_id]):
                model += lpSum(
                    xaijk[(a_id, i, j, k)] * bij.get((k, j), 0)
                    for k in range(i, min(until.get(a_id, 11), 12))
                    for j in M_set if (a_id, i, j, k) in xaijk and (k, j) in bij
                ) == demand[a_id][i], f"Constraint_until_{activity_full_names.get(a_id, a_id)}_{i}"


# Constraint 2d
def add_istovar_kontrola_constraint(model, istovar_id, kontrola_id, N_set, M_set, 
                                   xaijk, bij, ratio):
    """
    Add constraint for Istovar/Kontrola relationship (Constraint 2d).
    
    For each interval k, the number of Kontrola activities must be at least 
    'ratio' times the number of Istovar activities in that interval.
    
    Constraint: Kontrola(k) >= ratio * Istovar(k)
    """
    if not istovar_id or not kontrola_id:
        return
    
    for k in N_set:
        # Sum of Istovar activities for all intervals up to k
        istovar_sum = lpSum(
            xaijk[(istovar_id, i, j, k)]
            for i in N_set 
            for j in M_set 
            if (istovar_id, i, j, k) in xaijk
        )
        
        # Sum of Kontrola activities at interval k (weighted by availability)
        kontrola_sum = lpSum(
            xaijk[(kontrola_id, k, j, k)] * bij.get((k, j), 0)
            for j in M_set 
            if (kontrola_id, k, j, k) in xaijk and (k, j) in bij
        )
        
        # Constraint: kontrola >= ratio * istovar
        model += kontrola_sum >= ratio * istovar_sum, \
            f"Constraint_2d_istovar_kontrola_{k}"


# Constraint 3
def add_activity_allocation_constraints(model, activities, M_set, N_set, xaijk, ytija, 
                                       bij, allowed):
    """Add constraints linking activity assignments to worker allocations."""
    for a_id in activities:
        for j in M_set:
            for k in N_set:
                model += lpSum(
                    xaijk[(a_id, i, j, k)]
                    for i in range(1, k + 1) if (a_id, i, j, k) in xaijk
                ) == lpSum(
                    ytija[(t_id, k, j, a_id)]
                    for t_id in allowed.get(a_id, []) if (t_id, k, j, a_id) in ytija
                ), f"Constraint_allocation_{a_id}_{j}_{k}"


# Constraint 4
def add_worker_capacity_constraints(model, profil_types, N_set, M_set, ytj, ytija, 
                                    able):
    """Add constraints for worker capacity limits."""
    for p_type_id in profil_types:
        for i in N_set:
            for j in M_set:
                if (p_type_id, j) in ytj:
                    model += lpSum(
                        ytija[(p_type_id, i, j, a_id)]
                        for a_id in able.get(p_type_id, []) if (p_type_id, i, j, a_id) in ytija
                    ) <= ytj[(p_type_id, j)], f"Constraint_capacity_{p_type_id}_{i}_{j}"


# Constraint 5
def add_interval_worker_limit(model, activities, N_set, profil_types, M_set, ytija, max_workers):
    """Add constraint limiting maximum workers per interval."""
    for i in N_set:
        terms = [
            ytija[(p_type_id, i, j, a_id)]
            for p_type_id in profil_types for j in M_set for a_id in activities
            if (p_type_id, i, j, a_id) in ytija
        ]
        model += lpSum(terms) <= max_workers, f"Constraint_max_workers_{i}"


# Constraint 6
def add_rest_interval_constraints(model, M1_set, profil_types, ytj, ytija, activities, able, bij, Oj):
    """Add rest interval limits for M1 shifts (Constraint 6)."""
    for j in M1_set:
        for p_type_id in profil_types:
            if (p_type_id, j) in ytj:
                rest_sum = 0
                for i in Oj.get(j, []):
                    for a_id in activities:
                        if (p_type_id, i, j, a_id) in ytija and (i, j) in bij:
                            rest_sum += ytija[(p_type_id, i, j, a_id)] * bij[(i, j)]
                model += rest_sum <= 2 * ytj[(p_type_id, j)], f"Constraint_6_{j}_{p_type_id}"


# Constraint 7
def add_m2_ratio_constraint(model, profil_types, M2_set, M_set, ytj, M2_RATIO_LIMIT):
    """Add M2 ratio limit (Constraint 7)."""
    for p_type_id in profil_types:
        if M2_set:
            sum_m2 = sum(ytj[(p_type_id, j)] for j in M2_set if (p_type_id, j) in ytj)
            sum_m_total = sum(ytj[(p_type_id, j)] for j in M_set if (p_type_id, j) in ytj)
            model += sum_m2 <= M2_RATIO_LIMIT * sum_m_total, f"Constraint_7_{p_type_id}"


# Constraint 8,9,10
def add_shift_constraints(model, M_set, M1_set, M2_set, ytj, profil_types, yj,
                         max_m1, max_m2):
    """Add constraints for shift limits."""
    for j in M_set:
        model += lpSum(
            ytj[(p_type_id, j)] for p_type_id in profil_types if (p_type_id, j) in ytj
        ) <= 1000 * yj[j], f"Constraint_shift_{j}"

    model += lpSum(yj[j] for j in M1_set) <= max_m1, "Constraint_M1_limit"
    model += lpSum(yj[j] for j in M2_set) <= max_m2, "Constraint_M2_limit"


# Constraint 11
def add_non_primary_activities_constraint(model, M1_set, profil_types, N_set, ytija, able, able_ne, bij, NON_PRIMARY_ACTIVITIES_RATIO):
    """Add non-primary activities ratio constraint for M1 shifts (Constraint 11)."""
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


# Constraint 12
def add_m1_m2_ratio_per_interval_constraint(model, N_set, M1_set, M2_set, ytj, bij, profil_types):
    """Add M1 vs M2 ratio per interval constraint (Constraint 12)."""
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
