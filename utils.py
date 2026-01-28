# Utility functions for parsing and data manipulation

import streamlit as st
import json


def parse_list(input_str, item_type=str):
    """Parse comma-separated input into a list of specified type."""
    if not input_str.strip():
        return []
    try:
        return [item_type(x.strip()) for x in input_str.split(',') if x.strip()]
    except ValueError:
        st.error(f"Error parsing list: '{input_str}'. Please ensure all items are of type {item_type.__name__}.")
        return []


def parse_json_dict(input_str, default_value=None):
    """Parse JSON string into a dictionary."""
    if default_value is None:
        default_value = {}
    if not input_str.strip():
        return default_value
    try:
        return json.loads(input_str)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {e}. Please ensure the input is valid JSON.")
        return default_value


def generate_profile_types(num_profiles):
    """Generate profile type identifiers."""
    return [f'profil{i+1}' for i in range(num_profiles)]


def generate_activities(num_activities):
    """Generate activity identifiers."""
    return [f'activity{i+1}' for i in range(num_activities)]


def count_consecutive_sequences(series, min_len=3):
    """Count consecutive sequences of same value (excluding 0 and None)."""
    count = 0
    current_val = None
    current_len = 0

    for v in series:
        # Break sequence
        if v == 0 or v == "" or v is None:
            if current_len >= min_len:
                count += 1
            current_val = None
            current_len = 0
            continue

        # Continue same sequence
        if v == current_val:
            current_len += 1
        else:
            if current_len >= min_len:
                count += 1
            current_val = v
            current_len = 1

    # Check at end
    if current_len >= min_len:
        count += 1

    return count
