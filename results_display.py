# Results processing and display functions

import streamlit as st
import pandas as pd
from collections import defaultdict
import random
import math
from pulp import LpStatusOptimal, value
from config import *
from utils import count_consecutive_sequences

# Matrice za pokrivanje smena i troškove preseljene su u model_builder.py, pošto
# logika izgradnje pripada komponenti modela. Oni su sada umodulirani tamo.

def generate_schedule_output(model, profil_types, M_set, M1_set, M2_set, N_set, ytj,
                            ytija, activities, s, able, full_time_shift_length=8, half_time_shift_length=4):
    """Generate worker schedules from optimized variables."""
    smjena_output = defaultdict(list)

    for j in [M1_set, M2_set]:
        for j_val in j:
            current_i_range_length = full_time_shift_length if j_val in M1_set else half_time_shift_length

            for p_type_id in profil_types:
                if (p_type_id, j_val) in ytj and ytj[(p_type_id, j_val)].varValue is not None:
                    broj_usmjeni = int(ytj[(p_type_id, j_val)].varValue)
                else:
                    broj_usmjeni = 0

                if broj_usmjeni > 0:
                    for k_idx in range(1, broj_usmjeni + 1):
                        smjena_output[j_val, p_type_id, k_idx] = ["0"] * current_i_range_length

                    current_i_range_absolute = (
                        list(range(j_val, j_val + full_time_shift_length)) if j_val in M1_set
                        else list(range(j_val - DEFAULT_M2_SHIFT_START + 1,
                                         j_val - DEFAULT_M2_SHIFT_START + 1 + half_time_shift_length))
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
                        d[k_val] = worker_schedule[3:6].count("0")

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
                                if idx < len(schedule_max) and schedule_max[idx] == "0":
                                    if idx < len(schedule_min):
                                        schedule_max[idx] = schedule_min[idx]
                                        schedule_min[idx] = "0"
                                    break
                else:
                    balance_loop_active = False
    
    return smjena_output


def create_shift_allocation_table(smjena_output, M_set, M1_set, M2_set, profil_types,
                                  ytj, sp, display_start_interval=0, N_set=None, full_time_shift_length=8, half_time_shift_length=4):
    """Create DataFrame for shift allocation timetable."""
    max_interval = max(N_set) if N_set else 0
    df = pd.DataFrame(index=range(1, max_interval + 1), dtype=object)

    for j in M_set:
        for t in profil_types:
            if (t, j) in ytj and ytj[t, j].varValue is not None:
                broj_usmjeni = int(ytj[t, j].varValue)
            else:
                broj_usmjeni = 0

            for k in range(1, broj_usmjeni + 1):
                col_name = f"Smjena_{j}_{sp[t]}_{k}"

                if j in M1_set:
                    for i_offset in range(full_time_shift_length):
                        row = j + i_offset
                        if 1 <= row <= max_interval and (j, t, k) in smjena_output:
                            if i_offset < len(smjena_output[j, t, k]):
                                df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                            else:
                                df.loc[row, col_name] = "0"
                else:
                    for i_offset in range(half_time_shift_length):
                        row = j - DEFAULT_M2_SHIFT_START + i_offset + 1
                        if 1 <= row <= max_interval and (j, t, k) in smjena_output:
                            if i_offset < len(smjena_output[j, t, k]):
                                df.loc[row, col_name] = smjena_output[j, t, k][i_offset]
                            else:
                                df.loc[row, col_name] = "0"

    # Adjust display offset and show interval number with corresponding hour
    df_display = df.copy()
    display_hours = df_display.index + display_start_interval - 1
    df_display.index = [f"{interval}({hour})" for interval, hour in zip(df_display.index, display_hours)]
    df_display.index.name = "Interval (Hour)"

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
            if v == "0":
                broj_nula += 1
    return broj_nula


def analyze_activity_sequences(df, M1_set, M2_set, full_time_shift_length, half_time_shift_length, 
                               rest_duration, interval_duration, min_len=3):
    """Analyze consecutive sequences of same activity.
    
    Maksimalni broj sekvenci se računa kao:
    (shift_length - rest_intervals) // min_len
    """
    rezultati = defaultdict(dict)
    
    # Convert rest_duration (minutes) to number of intervals
    rest_intervals = math.ceil(rest_duration / interval_duration) if interval_duration > 0 else 0

    for col in df.columns:
        series = df[col].iloc[1:].tolist()  # Convert Pandas Series to list
        j = int(col.split("_")[1])

        # Calculate maksimalni based on shift length and min_len
        if j in M1_set:
            available_intervals = max(0, full_time_shift_length - rest_intervals)
            rezultati[col]["maksimalni"] = available_intervals // min_len if min_len > 0 else 0
        elif j in M2_set:
            available_intervals = max(0, half_time_shift_length - rest_intervals)
            rezultati[col]["maksimalni"] = available_intervals // min_len if min_len > 0 else 0
        else:
            rezultati[col]["maksimalni"] = 0
            
        rezultati[col]["stvarni"] = count_consecutive_sequences(series, min_len=min_len)

    return rezultati


def display_results(results):
    """Display all optimization results from stored session results."""
    st.header("Optimization Results")
    st.success(f"Optimal Objective Value: {results['objective']:.2f}")
    st.info("Solver Status: Optimal")

    # Cost breakdown
    st.write(f"Ukupna vrijednost funkcije cilja: {results['objective']:.2f}")
    st.write(f"  - Dio 1 (trošak radnika): {results['value_part_1']:.2f}")
    st.write(f"  - Dio 2 (penal prelazaka): {results['value_part_2']:.2f}")
    st.write(f"  - Dio 2 ponderisan (P * dio 2): {(results['P'] * results['value_part_2']):.2f}")

    # Employee count per shift
    st.subheader("Employees per Shift and Profile (ytj)")
    if results['ytj_data']:
        st.dataframe(pd.DataFrame(results['ytj_data']))

    # Shift allocation timetable
    st.subheader("Shift Allocation Timetable")
    st.dataframe(results['df_display'].style.hide(axis="columns"))

    # Idle intervals
    st.markdown(f"### ðﾟﾧﾮ Total intervals without work (value = 0): **{results['broj_nula']}**")

    # Demand comparison
    st.subheader("Total activities per interval (Demanded vs. Realized)")
    st.dataframe(results['df_activities'])

    # Activity sequences analysis
    st.subheader("Additional Results Analysis")
    if st.checkbox("Show Activity Sequences Analysis", key="show_activity_sequences_analysis"):
        rezultati = analyze_activity_sequences(
            results["df"], results["M1_set"], results["M2_set"],
            results["full_time_shift_length"], results["half_time_shift_length"],
            results["rest_duration"], results["interval_duration"],
            results["min_len"]
        )

        ukupno_stvarni = 0
        ukupno_maks = 0
        for col, r in rezultati.items():
            st.write(f"**{col}** → actual: {r['stvarni']} / max: {r['maksimalni']}")
            ukupno_stvarni += r["stvarni"]
            ukupno_maks += r["maksimalni"]

        st.markdown(f"### ✅ TOTAL: {ukupno_stvarni} / {ukupno_maks}")

    # Non-zero variables
    if st.checkbox("Show all PuLP variables with non-zero values", key="show_nonzero_pulp_vars"):
        st.subheader("All Non-Zero PuLP Variables")
        for var_line in results['non_zero_vars']:
            st.write(var_line)
