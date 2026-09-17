from copy import deepcopy

import pytest
from pulp import LpMinimize, LpProblem, LpStatus, PULP_CBC_CMD, value

from config import *
from model_builder import (
    add_activity_allocation_constraints,
    add_activity_dependency_ratio_constraints,
    add_activity_until_constraints,
    add_activity_within_constraints,
    add_interval_worker_limit,
    add_m2_ratio_constraint,
    add_non_primary_activities_constraint,
    add_rest_interval_constraints,
    add_shift_constraints,
    add_worker_ableno_constraints,
    add_worker_capacity_constraints,
    build_bij_matrix,
    build_ct_matrix,
    build_delta_variables,
    build_model_variables,
    setup_objective_function,
)
from ui_input import compute_able_from_allowed


PROFILES = ["profil1", "profil2", "profil3"]
ACTIVITIES = [
    "activity1",
    "activity2",
    "activity3",
    "activity4",
    "activity5",
    "activity6",
]
M1_SET = list(range(1, len(DEFAULT_N_SET) - DEFAULT_FULL_TIME_SHIFT_LENGTH + 2))
M2_SET = list(range(
    DEFAULT_M2_SHIFT_START,
    DEFAULT_M2_SHIFT_START + len(DEFAULT_N_SET) - DEFAULT_HALF_TIME_SHIFT_LENGTH + 1,
))
M_SET = sorted(set(M1_SET + M2_SET))

BASE_CASE = {
    "demand": DEMAND_EXAMPLE_1,
    "costs_m1": {"profil1": 1.28, "profil2": 1.6, "profil3": 1.4},
    "costs_m2": {"profil1": 0.64, "profil2": 0.8, "profil3": 0.7},
    "allowed": DEFAULT_ALLOWED,
    "primary_able": DEFAULT_PRIMARY_ABLE,
    "p": 0,
    "m2_ratio_limit": DEFAULT_M2_RATIO_LIMIT,
    "non_primary_activities_ratio": DEFAULT_NON_PRIMARY_ACTIVITIES_RATIO,
    "max_m1_shifts": DEFAULT_MAX_M1_SHIFTS,
    "max_m2_shifts": DEFAULT_MAX_M2_SHIFTS,
    "max_workers_per_interval": DEFAULT_MAX_WORKERS_PER_INTERVAL,
}

REGRESSION_CASES = {
    "default": {},
    "lower_profile3_cost": {
        "costs_m1": {"profil1": 1.28, "profil2": 1.6, "profil3": 1.2},
        "costs_m2": {"profil1": 0.64, "profil2": 0.8, "profil3": 0.6},
    },
    "higher_profile1_cost": {
        "costs_m1": {"profil1": 2.0, "profil2": 1.6, "profil3": 1.4},
        "costs_m2": {"profil1": 1.0, "profil2": 0.8, "profil3": 0.7},
    },
    "profile2_allowed_for_activity5": {
        "allowed": {
            **DEFAULT_ALLOWED,
            "activity5": ["profil2", "profil3"],
        },
    },
    "switch_penalty": {"p": 0.1},
}

EXPECTED_RESULTS = {
    "default": ("Optimal", 29.94),
    "lower_profile3_cost": ("Optimal", 27.52),
    "higher_profile1_cost": ("Optimal", 33.70),
    "profile2_allowed_for_activity5": ("Optimal", 29.94),
    "switch_penalty": ("Optimal", 29.94),
}


def solve_case(overrides):
    case = deepcopy(BASE_CASE)
    case.update(deepcopy(overrides))
    allowed = case["allowed"]
    able = compute_able_from_allowed(allowed, PROFILES, ACTIVITIES)
    primary_able = case["primary_able"]
    able_ne = {
        profile_id: [
            activity_id for activity_id in able.get(profile_id, [])
            if activity_id not in primary_able.get(profile_id, [])
        ]
        for profile_id in PROFILES
    }
    demand = case["demand"]
    ind_within = ["activity5", "activity6"]
    ind_until = ["activity1", "activity2", "activity3"]
    within = {"activity5": 1, "activity6": 2, "activity4": 1}
    until = {"activity1": 5, "activity2": 9, "activity3": 12}
    dependency_list = [{"dependent": "activity4", "depends_on": "activity6", "ratio": 0.5}]
    demand = deepcopy(demand)
    demand["activity4"] = [0] + [
        round(0.5 * value) for value in demand["activity6"][1:]
    ]

    model = LpProblem("regression_case", LpMinimize)
    bij = build_bij_matrix(
        M_SET, M1_SET, M2_SET, DEFAULT_N_SET,
        DEFAULT_FULL_TIME_SHIFT_LENGTH, DEFAULT_HALF_TIME_SHIFT_LENGTH,
    )
    ct = build_ct_matrix(
        M_SET, M1_SET, M2_SET, PROFILES,
        case["costs_m1"], case["costs_m2"],
    )
    yjz, yj, ytj, ytija, xaijk = build_model_variables(
        PROFILES, M_SET, M1_SET, M2_SET, DEFAULT_N_SET, ACTIVITIES,
    )
    delta = build_delta_variables(case["p"], PROFILES, M_SET, DEFAULT_N_SET, ACTIVITIES)
    setup_objective_function(
        model, case["p"], PROFILES, M_SET, DEFAULT_N_SET, ytj, delta, ct, ACTIVITIES,
    )

    add_activity_within_constraints(
        model, ind_within, DEFAULT_N_SET, M_SET, PROFILES, ACTIVITIES,
        xaijk, bij, demand, within, able, DEFAULT_FULL_ACTIVITY_NAMES,
    )
    add_activity_until_constraints(
        model, ind_until, DEFAULT_N_SET, M_SET, xaijk, bij,
        demand, until, DEFAULT_FULL_ACTIVITY_NAMES,
    )
    add_activity_dependency_ratio_constraints(
        model, dependency_list, DEFAULT_N_SET, M_SET, xaijk, bij, within, until,
    )
    add_activity_allocation_constraints(
        model, ACTIVITIES, M_SET, DEFAULT_N_SET, xaijk, ytija, bij, allowed,
    )
    add_worker_capacity_constraints(model, PROFILES, DEFAULT_N_SET, M_SET, ytj, ytija, able)
    add_m2_ratio_constraint(
        model, PROFILES, M2_SET, M_SET, ytj, case["m2_ratio_limit"]
    )
    add_interval_worker_limit(
        model, ACTIVITIES, DEFAULT_N_SET, PROFILES, M_SET,
        ytija, case["max_workers_per_interval"],
    )
    add_rest_interval_constraints(
        model, M1_SET, PROFILES, ytj, ytija, ACTIVITIES, able, bij,
        DEFAULT_OJ, 60, 60,
    )
    add_shift_constraints(
        model, M_SET, M1_SET, M2_SET, ytj, PROFILES, yj,
        case["max_m1_shifts"], case["max_m2_shifts"],
    )
    add_non_primary_activities_constraint(
        model, M1_SET, PROFILES, DEFAULT_N_SET, ytija, able,
        able_ne, bij, case["non_primary_activities_ratio"],
    )
    add_worker_ableno_constraints(model, PROFILES, DEFAULT_N_SET, M_SET, ytj, ytija, able, ACTIVITIES)

    model.solve(PULP_CBC_CMD(msg=0, timeLimit=10))
    status = LpStatus[model.status]
    objective = value(model.objective) if model.status == 1 else None
    return status, objective


@pytest.mark.parametrize("case_name", REGRESSION_CASES)
def test_regression_case_matches_baseline(case_name):
    status, objective = solve_case(REGRESSION_CASES[case_name])
    expected_status, expected_objective = EXPECTED_RESULTS[case_name]
    assert status == expected_status
    assert objective == pytest.approx(expected_objective, abs=1e-6)
