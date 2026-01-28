# Results processing and display functions

import streamlit as st
import pandas as pd
from collections import defaultdict
import random
from pulp import LpStatusOptimal, value
from config import *
from utils import count_consecutive_sequences


def build_bij_matrix(M_set, M1_set, M2_set, N_set):
    """Build the bij matrix for shift interval coverage."""
    bij = {}
    for j in M_set:
        for i in N_set:
            if j in M1_set:
                bij[(i, j)] = 1.00 if j <= i <= j + 8 else 0.00
            elif j in M2_set:
                bij[(i, j)] = 1.00 if j - 5 <= i <= j - 5 + 3 else 0.00
    return bij


def build_ct_matrix(M_set, M1_set, M2_set, profil_types, ct_m1_inputs, ct_m2_inputs):
    """Build cost coefficient matrix from user inputs."""
    ct = {}
    for j in M_set:
        for p_type_id in profil_types:
            if j in M1_set:
                ct[(p_type_id, j)] = ct_m1_inputs[p_type_id]
            elif j in M2_set:
                ct[(p_type_id, j)] = ct_m2_inputs[p_type_id]
    return ct


def generate_schedule_output(model, profil_types, M_set, M1_set, M2_set, N_set, ytj,
                            ytija, activities, s, able):
    """Generate worker schedules from optimized variables."""
    smjena_output = defaultdict(list)

    for j in [M1_set, M2_set]:
        for j_val in j:
            current_i_range_length = 9 if j_val in M1_set else 4

            for p_type_id in profil_types:
                if (p_type_id, j_val) in ytj and ytj[(p_type_id, j_val)].varValue is not None:
                    broj_usmjeni = int(ytj[(p_type_id, j_val)].varValue)
                else:
                    broj_usmjeni = 0

                if broj_usmjeni > 0:
                    for k_idx in range(1, broj_usmjeni + 1):
                        smjena_output[j_val, p_type_id, k_idx] = [0] * current_i_range_length

                    current_i_range_absolute = (
                        list(range(j_val, j_val + 9)) if j_val in M1_set
                        else list(range(j_val - 5, j_val - 5 + 4))
                    )

                    for interval_offset, i in enumerate(current_i_range_absolute):
                        workers_assigned_in_this_interval = set()
                        available_workers = list(range(1, broj_usmjeni + 1))
                        random.shuffle(available_workers)

                        for a_id in activities:
                            if (p_type_id, i, j_val, a_id) in ytija and ytija[(p_type_id, i, j_val, a_id)].varValue is not None:
                                broj_uintervalu = int(ytija[(p_type_id, i, j_val, a_id)].varValue)
                            else:
                                broj_uintervalu = 0

                            if broj_uintervalu > 0:
                                assigned_count = 0
                                for k_idx in list(available_workers):
                                    if k_idx not in workers_assigned_in_this_interval and assigned_count < broj_uintervalu:
                                        if interval_offset < current_i_range_length:
                                            smjena_output[j_val, p_type_id, k_idx][interval_offset] = s[a_id]
                                            workers_assigned_in_this_interval.add(k_idx)
                                            available_workers.remove(k_idx)
                                            assigned_count += 1

    return smjena_output


def balance_schedules(smjena_output, M1_set, profil_types, ytj):
    """Balance worker schedules to distribute work evenly."""
    for j in M1_set:
        for p_type_id in profil_types:
            broj_usmjeni = 0
            if (p_type_id, j) in ytj and ytj[(p_type_id, j)].varValue is not None:
                broj_usmjeni = int(ytj[(p_type_id, j)].varValue)

            if broj_usmjeni == 0:
                continue

            balance_loop_active = True
            while balance_loop_active:
                d = {}
                for k_val in range(1, broj_usmjeni + 1):
                    worker_schedule = smjena_output.get((j, p_type_id, k_val), [])
                    if worker_schedule:
                        d[k_val] = worker_schedule[3:6].count(0)

                if d:
                    max_kljuc, max_v = max(d.items(), key=lambda k_v: k_v[1])
                    min_kljuc, min_v = min(d.items(), key=lambda k_v: k_v[1])

                    balance_loop_active = False
                    if max_v - min_v > 1:
                        balance_loop_active = True
                        schedule_max = smjena_output.get((j, p_type_id, max_kljuc), [])
                        schedule_min = smjena_output.get((j, p_type_id, min_kljuc), [])

                        if schedule_max and schedule_min:
                            for idx in [3, 4, 5]:
                                if idx < len(schedule_max) and schedule_max[idx] == 0:
                                    if idx < len(schedule_min):
                                        schedule_max[idx] = schedule_min[idx]
                                        schedule_min[idx] = 0
                                    break
                else:
                    balance_loop_active = False


def create_shift_allocation_table(smjena_output, M_set, M1_set, M2_set, profil_types,
                                  ytj, sp, display_start_interval=0):
    """Create DataFrame for shift allocation timetable."""
    df = pd.DataFrame(index=range(1, 15), dtype=object)

    for j in M_set:
        for t in profil_types:
            if (t, j) in ytj and ytj[t, j].varValue is not None:
                broj_usmjeni = int(ytj[t, j].varValue)
            else:
                broj_usmjeni = 0

            for k in range(1, broj_usmjeni + 1):
                col_name = f"Smjena_{j}_{sp[t]}_{k}"

                if j in M1_set:
                    for i_offset in range(9):
                        row = j + i_offset
                        if row <= 14 and (j, t, k) in smjena_output:
                            if i_offset < len(smjena_output[j, t, k]):
                                df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                            else:
                                df.loc[row, col_name] = ""
                else:
                    for i_offset in range(4):
                        row = j - 5 + i_offset
                        if row <= 14 and (j, t, k) in smjena_output:
                            if i_offset < len(smjena_output[j, t, k]):
                                df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                            else:
                                df.loc[row, col_name] = ""

    # Adjust display offset
    df_display = df.copy()
    df_display.index = df_display.index + display_start_interval - 1

    return df, df_display


def create_demand_comparison_table(activity_per_interval, N_set, activities, 
                                  activity_full_names, demand):
    """Create DataFrame comparing demand vs realized activities."""
    df_data = []
    for i in sorted(activity_per_interval.keys()):
        row_data = {"Interval": i}
        for a_id in activities:
            full_activity_name = activity_full_names.get(a_id, a_id)
            row_data[f"{full_activity_name}_zahtjevano"] = (
                demand.get(a_id, [0] * (max(N_set) + 1))[i]
                if i < len(demand.get(a_id, [0] * (max(N_set) + 1)))
                else 0
            )
            row_data[f"{full_activity_name}_rasporedjeno"] = activity_per_interval[i][a_id]
        df_data.append(row_data)

    df_activities = pd.DataFrame(df_data).set_index("Interval")

    ordered_columns = []
    for a_id in activities:
        full_activity_name = activity_full_names.get(a_id, a_id)
        ordered_columns.append(f"{full_activity_name}_zahtjevano")
        ordered_columns.append(f"{full_activity_name}_rasporedjeno")

    final_columns = [col for col in ordered_columns if col in df_activities.columns]
    df_activities = df_activities[final_columns]

    return df_activities


def count_idle_intervals(df):
    """Count total intervals where workers have no assignment (value = 0)."""
    broj_nula = 0
    for col in df.columns:
        for v in df[col].iloc[1:]:
            if v == 0:
                broj_nula += 1
    return broj_nula


def analyze_activity_sequences(df, M1_set, M_set):
    """Analyze consecutive sequences of same activity."""
    rezultati = defaultdict(dict)

    for col in df.columns:
        series = df[col].iloc[1:]
        j = int(col.split("_")[1])

        rezultati[col]["maksimalni"] = 2 if j in M1_set else 1
        rezultati[col]["stvarni"] = count_consecutive_sequences(series, min_len=3)

    return rezultati


def display_results(model, obj_part_1, obj_part_2, P, profil_types, M_set, M1_set, M2_set,
                   N_set, ytj, ytija, activities, smjena_output, df, df_display,
                   activity_per_interval, activity_full_names, demand):
    """Display all optimization results."""
    st.header("Optimization Results")
    st.success(f"Optimal Objective Value: {value(model.objective):.2f}")
    st.info(f"Solver Status: Optimal")

    # Cost breakdown
    value_part_1 = value(obj_part_1)
    value_part_2 = 0 if P == 0 else value(obj_part_2)

    st.write(f"Ukupna vrijednost funkcije cilja: {value(model.objective):.2f}")
    st.write(f"  - Dio 1 (trošak radnika): {value_part_1:.2f}")
    st.write(f"  - Dio 2 (penal prelazaka): {value_part_2:.2f}")
    st.write(f"  - Dio 2 ponderisan (P * dio 2): {(P * value_part_2):.2f}")

    # Employee count per shift
    st.subheader("Employees per Shift and Profile (ytj)")
    ytj_data = []
    for j in M_set:
        for p_type_id in profil_types:
            if (p_type_id, j) in ytj and value(ytj[(p_type_id, j)]) > 0:
                ytj_data.append({
                    "Shift": j,
                    "Profile": p_type_id,
                    "Count": value(ytj[(p_type_id, j)])
                })
    if ytj_data:
        st.dataframe(pd.DataFrame(ytj_data))

    # Shift allocation timetable
    st.subheader("Shift Allocation Timetable")
    st.dataframe(df_display.style.hide(axis="columns"))

    # Idle intervals
    broj_nula = count_idle_intervals(df)
    st.markdown(f"### ðﾟﾧﾮ Total intervals without work (value = 0): **{broj_nula}**")

    # Activity sequences
    st.subheader("ðﾟﾓﾊ Activity Sequences Analysis")
    rezultati = analyze_activity_sequences(df, M1_set, M_set)

    ukupno_stvarni = 0
    ukupno_maks = 0
    for col, r in rezultati.items():
        st.write(f"**{col}** → actual: {r['stvarni']} / max: {r['maksimalni']}")
        ukupno_stvarni += r["stvarni"]
        ukupno_maks += r["maksimalni"]

    st.markdown(f"### ✅ TOTAL: {ukupno_stvarni} / {ukupno_maks}")

    # Demand comparison
    st.subheader("Total activities per interval (Demanded vs. Realized)")
    df_activities = create_demand_comparison_table(
        activity_per_interval, N_set, activities, activity_full_names, demand
    )
    st.dataframe(df_activities)

    # Non-zero variables
    if st.checkbox("Show all PuLP variables with non-zero values"):
        st.subheader("All Non-Zero PuLP Variables")
        for v in model.variables():
            if v.varValue is not None and v.varValue > 0:
                st.write(f"{v.name} = {v.varValue}")
