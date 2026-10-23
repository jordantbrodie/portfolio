"""The calculator must reproduce the hand-calculated values in the design report."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from winch_design import Requirements, design  # noqa: E402

# (key in result.values, value in the report, relative tolerance)
REPORT = [
    ("F_max [N]", 7360, 0.01),
    ("required breaking force [kN]", 40.5, 0.01),
    ("drum diameter D [mm]", 200, 0.001),
    ("drum torque T [N m]", 736, 0.01),
    ("power at drum [W]", 810, 0.01),
    ("min motor power [W]", 950, 0.01),
    ("drum speed [rpm]", 10.5, 0.01),
    ("sprocket torque T_K [N m]", 505, 0.01),
    ("driven sprocket teeth z2", 30, 0.05),   # report rounds 30.4 up to 31
    ("chain speed [m/s]", 0.14, 0.03),
    ("chain load factor K", 2.03, 0.01),
    ("bearing span [mm]", 520, 0.001),
    ("reaction R_A [N]", 11100, 0.03),   # report rounded chain speed to 0.14 m/s
    ("reaction R_B [N]", 2740, 0.01),
    ("bending moment at bearing A [N m]", 488, 0.03),
    ("drum compressive stress [MPa]", 105, 0.01),
]


@pytest.mark.parametrize("key,expected,tol", REPORT)
def test_matches_report(key, expected, tol):
    assert design().values[key] == pytest.approx(expected, rel=tol)


def test_report_design_passes_every_check():
    r = design()
    failed = [c.name for c in r.checks if not c.ok]
    assert failed == []


def test_overload_is_caught():
    # At 1000 kg the selected 1.1 kW motor can no longer deliver the power.
    r = design(Requirements(load_kg=1000))
    assert not r.all_ok
    assert any(c.name.startswith("Motor: power") and not c.ok for c in r.checks)
