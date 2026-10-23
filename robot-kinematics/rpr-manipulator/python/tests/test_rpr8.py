import math
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rpr8 import L2MAX, ee_position, fk, ik_analytic, ik_bruteforce, workspace  # noqa: E402


def test_home_position_matches_matlab():
    # The MATLAB FK report gives PE = [6 5 8] at A = B = 0, L2 = 6.
    assert np.allclose(fk(0, 0, L2MAX).EE[:3, 3], [6, 5, 8])


def test_closed_form_position_equals_matrix_chain():
    rng = random.Random(1)
    for _ in range(200):
        A, B, L2 = rng.uniform(-math.pi, math.pi), rng.uniform(-math.pi, math.pi), rng.uniform(0, L2MAX)
        assert np.allclose(fk(A, B, L2).EE[:3, 3], ee_position(A, B, L2))


def test_bruteforce_reproduces_matlab_ik_result():
    # MATLAB (configs.csv) found exactly two configurations: (0, 0, 6) and (90, 180, 6).
    assert sorted(ik_bruteforce((6, 5, 8))) == [(0.0, 0.0, 6.0), (90.0, 180.0, 6.0)]


def test_analytic_ik_agrees_with_bruteforce():
    got = sorted((round(a, 6) % 360, round(b, 6) % 360, l2) for a, b, l2 in ik_analytic((6, 5, 8)))
    assert got == [(0.0, 0.0, 6.0), (90.0, 180.0, 6.0)]


@pytest.mark.parametrize("seed", range(50))
def test_analytic_ik_round_trip(seed):
    rng = random.Random(seed)
    A, B, L2 = rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi), rng.uniform(0, L2MAX)
    target = ee_position(A, B, L2)
    sols = ik_analytic(target)
    assert sols, "a reachable target must have a solution"
    for a, b, l2 in sols:
        assert np.allclose(ee_position(math.radians(a), math.radians(b), l2), target, atol=1e-9)


def test_unreachable_targets():
    assert ik_analytic((7, 0, 3)) == []      # x beyond the prismatic stroke
    assert ik_analytic((3, 20, 3)) == []     # outside the 10-unit reach in y-z


def test_workspace_is_above_floor():
    pts = workspace(n=10)
    assert len(pts) > 0 and pts[:, 2].min() >= 0.05
