from ui_input import compute_able_from_allowed


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
