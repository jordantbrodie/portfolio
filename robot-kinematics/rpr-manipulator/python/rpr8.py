"""RPR8 manipulator kinematics in Python (NumPy).

A port of my MATLAB coursework for ATR0030 Robotics (TalTech, 2026) - forward
kinematics, collision-free workspace and brute-force inverse kinematics - plus a
closed-form inverse-kinematics solution derived from the same transform chain.

Joint chain (same as the MATLAB model):
    T01  = trans(0, 0, L0)           base offset
    R01  = rot_y(-90 deg)            reorient J1
    r1   = rot_z(A)                  revolute joint A
    T12  = trans(L1, 0, 0)           fixed link
    t2   = trans(0, 0, -L2)          prismatic joint, 0 <= L2 <= L2max
    r3   = rot_z(B)                  revolute joint B
    T3E  = trans(0, L3, 0)           fixed link to the end effector
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np

L0, L1, L2MAX, L3 = 3.0, 5.0, 6.0, 5.0


def trans(x: float, y: float, z: float) -> np.ndarray:
    T = np.eye(4)
    T[:3, 3] = (x, y, z)
    return T


def rot_y(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    T = np.eye(4)
    T[:3, :3] = [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    return T


def rot_z(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    T = np.eye(4)
    T[:3, :3] = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    return T


@dataclass
class Pose:
    J1: np.ndarray
    J2: np.ndarray
    J3: np.ndarray
    EE: np.ndarray

    def points(self) -> np.ndarray:
        """Base, J1, J2, J3 and EE positions as a 5x3 array (for plotting)."""
        return np.vstack([np.zeros(3)] + [T[:3, 3] for T in (self.J1, self.J2, self.J3, self.EE)])


def fk(A: float, B: float, L2: float) -> Pose:
    """Forward kinematics. Angles in radians, lengths in model units."""
    J1 = trans(0, 0, L0) @ rot_y(-math.pi / 2) @ rot_z(A)
    J2 = J1 @ trans(L1, 0, 0)
    J3 = J2 @ trans(0, 0, -L2)
    EE = J3 @ rot_z(B) @ trans(0, L3, 0)
    return Pose(J1, J2, J3, EE)


def ee_position(A: float, B: float, L2: float) -> np.ndarray:
    """Closed-form end-effector position, derived by multiplying out the chain:
    x = L2,  y = L1 sin A + L3 cos(A+B),  z = L0 + L1 cos A - L3 sin(A+B)."""
    return np.array([L2,
                     L1 * math.sin(A) + L3 * math.cos(A + B),
                     L0 + L1 * math.cos(A) - L3 * math.sin(A + B)])


def workspace(n: int = 20, min_z: float = 0.05, a_limit: float = 1.148) -> np.ndarray:
    """Collision-free EE positions, sampled like RPR8_workspace.m.
    Configurations where the EE or J3 would touch the floor (z < min_z) are dropped."""
    pts = []
    for L2, B, A in itertools.product(np.linspace(L2MAX, 0, n),
                                      np.linspace(0, 2 * math.pi, n),
                                      np.linspace(-a_limit, a_limit, n)):
        p = fk(A, B, L2)
        if p.EE[2, 3] >= min_z and p.J3[2, 3] >= min_z:
            pts.append(p.EE[:3, 3])
    return np.array(pts)


def ik_bruteforce(target, n_angle: int = 72, n_len: int = 21, tol: float = 0.05):
    """Generate-and-test IK, as in RPR8_inverse_kinematics.m.
    Returns a list of (A_deg, B_deg, L2) that reach the target within tol on every axis."""
    target = np.asarray(target, float)
    sols = []
    angles = np.arange(n_angle) * 2 * math.pi / n_angle
    for L2 in np.linspace(L2MAX, 0, n_len):
        for B in angles:
            for A in angles:
                if np.all(np.abs(ee_position(A, B, L2) - target) < tol):
                    sols.append((round(math.degrees(A), 6), round(math.degrees(B), 6), round(float(L2), 6)))
    return sols


def ik_analytic(target):
    """Closed-form IK.

    The prismatic joint sets x directly (L2 = x). In the y-z plane the arm is then a
    two-link planar arm with link lengths L1 and L3, first angle A measured from the
    z axis and relative angle q = B + 90 deg, so the usual 2R solution applies:
        cos q = (r^2 - L1^2 - L3^2) / (2 L1 L3),   r^2 = y^2 + (z - L0)^2
        A = atan2(y, z - L0) - atan2(L3 sin q, L1 + L3 cos q)
    Returns 0, 1 or 2 solutions as (A_deg, B_deg, L2), angles wrapped to [0, 360).
    """
    x, y, z = map(float, target)
    if not 0.0 <= x <= L2MAX:
        return []
    zp = z - L0
    r2 = y * y + zp * zp
    c = (r2 - L1 ** 2 - L3 ** 2) / (2 * L1 * L3)
    if c < -1 - 1e-12 or c > 1 + 1e-12:
        return []
    c = max(-1.0, min(1.0, c))
    sols = []
    for q in sorted({math.acos(c), -math.acos(c)}):
        A = math.atan2(y, zp) - math.atan2(L3 * math.sin(q), L1 + L3 * math.cos(q))
        B = q - math.pi / 2
        sols.append((math.degrees(A) % 360, math.degrees(B) % 360, x))
    return sols


if __name__ == "__main__":
    home = fk(0, 0, L2MAX)
    print("Home EE position:", home.EE[:3, 3].round(6))
    target = (6, 5, 8)
    print("Brute-force IK :", ik_bruteforce(target))
    print("Analytic IK    :", [tuple(round(v, 6) for v in s) for s in ik_analytic(target)])
