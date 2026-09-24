from ui_input import (
    cleanup_removed_mapping_state,
    compute_able_from_allowed,
    get_default_activity_short_code,
    get_default_profile_short_code,
)


def test_compute_able_from_allowed():
    profil_types = ["profil1", "profil2"]
    activities = ["activity1", "activity2", "activity3"]
    allowed = {
        "activity1": ["profil1", "profil2"],
        "activity2": ["profil2"],
        "activity3": [],
    }

    assert compute_able_from_allowed(allowed, profil_types, activities) == {
        "profil1": ["activity1"],
        "profil2": ["activity1", "activity2"],
    }


def test_cleanup_removed_profile_from_mapping_state():
    session_state = {
        "allowed_activity1": ["Komisioner", "Kontrolor"],
        "allowed_activity2": ["Kontrolor"],
        "primary_able_profil1": ["Komisioniranje1"],
        "primary_able_profil2": ["Kontrola"],
        "able_preview_profil1": ["Komisioniranje1"],
    }

    cleanup_removed_mapping_state(
        session_state,
        profile_id="profil1",
        profile_name="Komisioner",
    )

    assert session_state == {
        "allowed_activity1": ["Kontrolor"],
        "allowed_activity2": ["Kontrolor"],
        "primary_able_profil2": ["Kontrola"],
    }


def test_cleanup_removed_activity_from_mapping_state():
    session_state = {
        "allowed_activity1": ["profil1", "profil2"],
        "allowed_activity2": ["profil2"],
        "primary_able_profil1": ["Komisioniranje1", "Komisioniranje2"],
        "primary_able_profil2": ["Komisioniranje2"],
    }

    cleanup_removed_mapping_state(
        session_state,
        activity_id="activity1",
        activity_name="Komisioniranje1",
    )

    assert session_state == {
        "allowed_activity2": ["profil2"],
        "primary_able_profil1": ["Komisioniranje2"],
        "primary_able_profil2": ["Komisioniranje2"],
    }


def test_new_profile_and_activity_short_codes():
    assert get_default_profile_short_code("profil8") == "p8"
    assert get_default_activity_short_code("activity7") == "a7"
    assert get_default_profile_short_code("profil1") == "ks"
    assert get_default_activity_short_code("activity1") == "k1"
