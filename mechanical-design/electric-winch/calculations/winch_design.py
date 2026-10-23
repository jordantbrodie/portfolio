"""Electric winch design calculator.

Re-implements, as code, the hand calculations from my MES0225 Machine Engineering
project (TalTech, spring 2026): rope and drum, gear motor, chain drive, shaft
strength and fatigue, bearing life, keys and drum shell.

Catalogue choices (rope, motor, chain, bearing, keys) are inputs, exactly as in the
report, and every strength condition is checked and reported as PASS / FAIL. Change
the requirements (load, rope speed) to see which components stop passing.

Usage:
    python winch_design.py                  # the 750 kg design from the report
    python winch_design.py --load 1000      # what breaks if the load goes up?
    python winch_design.py --markdown       # print the results as a Markdown table
"""
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field

G = 9.81  # m/s^2


@dataclass
class Requirements:
    load_kg: float = 750.0           # rated load
    rope_speed: float = 0.11         # m/s


@dataclass
class Selections:
    """Values picked from catalogues or design rules in the report."""
    rope_safety_factor: float = 5.5
    rope_breaking_force: float = 59.7e3   # N, rope TEK 13310
    rope_diameter: float = 0.010          # m
    drum_ratio_e: float = 20              # D = e*d, 20-30 for moderate duty
    drum_length: float = 0.400            # m

    eff_gearmotor: float = 0.94
    eff_chain: float = 0.92
    eff_bearings: float = 0.99
    motor_power_margin: float = 1.2
    chain_ratio: float = 1.6
    motor_power: float = 1.1e3            # W, SEW R77 DT90S4
    motor_speed: float = 17.0             # rpm (gear motor output)

    z1: int = 19                          # driving sprocket teeth
    chain_pitch: float = 0.0254           # m, 16B-2 double strand
    chain_mass: float = 4.21              # kg/m
    chain_breaking_load: float = 106e3    # N
    roller_width: float = 0.01702         # m
    roller_diameter: float = 0.01588      # m
    chain_load_factors: tuple = (1.25, 1.0, 1.0, 1.25, 1.3)  # kd, ka, kn, kr, km
    chain_allowable_pressure: float = 47e6 * 0.85   # Pa, -15 % for double strand
    chain_min_safety: float = 7.3
    centre_distance: float = 0.800        # m
    sag_factor: float = 1.5               # kf at 45 deg

    shaft_allow_shear: float = 30e6       # Pa, for the first torsion sizing
    shaft_d_sprocket: float = 0.050       # m (dv)
    shaft_d_bearing: float = 0.055        # m (dt)
    shaft_d_hub: float = 0.060            # m (dr)
    shaft_yield: float = 370e6            # C45E
    shaft_static_safety: float = 1.5
    sigma_m1: float = 275e6               # fatigue limits, C45E
    tau_m1: float = 165e6
    k_sigma: float = 1.96                 # stress concentration at the 55/50 step, R = 1 mm
    k_tau: float = 1.30
    kd_sigma: float = 0.83
    kd_tau: float = 0.69
    k_f: float = 0.95
    psi_tau: float = 0.1
    fatigue_min_safety: float = 2.5

    sprocket_width: float = 0.070         # m (Ln)
    bearing_width: float = 0.060          # m (SY 55 TF)
    bearing_C: float = 43.6e3             # N, dynamic load rating
    bearing_life_min_h: float = 14_000

    key_b: float = 0.014                  # 14 x 9 key
    key_h: float = 0.009
    key_t1: float = 0.0055
    key_len_hub: float = 0.080
    key_len_sprocket: float = 0.063
    keys_per_joint: int = 2
    key_allow_contact: float = 130e6
    key_allow_shear: float = 70e6

    drum_wall: float = 0.007              # m
    drum_allow: float = 120e6             # S235


@dataclass
class Check:
    name: str
    value: float
    limit: float
    unit: str
    rule: str          # "<=" means value must not exceed limit, ">=" the opposite

    @property
    def ok(self) -> bool:
        return self.value <= self.limit if self.rule == "<=" else self.value >= self.limit


@dataclass
class Result:
    values: dict = field(default_factory=dict)
    checks: list = field(default_factory=list)

    @property
    def all_ok(self) -> bool:
        return all(c.ok for c in self.checks)


def design(req: Requirements = Requirements(), s: Selections = Selections()) -> Result:
    r = Result()
    v = r.values

    # 3. Rope and drum
    F = req.load_kg * G
    v["F_max [N]"] = F
    v["required breaking force [kN]"] = F * s.rope_safety_factor / 1e3
    r.checks.append(Check("Rope: load vs allowable", F, s.rope_breaking_force / s.rope_safety_factor, "N", "<="))
    D = s.drum_ratio_e * s.rope_diameter
    v["drum diameter D [mm]"] = D * 1e3
    v["rope turns per layer"] = s.drum_length / s.rope_diameter

    # 4. Gear motor
    T = F * D / 2
    w = 2 * req.rope_speed / D
    P_drum = T * w
    eta = s.eff_gearmotor * s.eff_chain * s.eff_bearings
    v["drum torque T [N m]"] = T
    v["drum speed [rpm]"] = 30 * w / math.pi
    v["power at drum [W]"] = P_drum
    v["min motor power [W]"] = P_drum / eta
    v["motor power incl. margin [W]"] = s.motor_power_margin * P_drum / eta
    v["required motor output speed [rpm]"] = 30 * w / math.pi * s.chain_ratio
    r.checks.append(Check("Motor: power delivered to drum", s.motor_power * eta, P_drum, "W", ">="))
    n_drum_real = s.motor_speed / s.chain_ratio
    v_real = math.pi * n_drum_real * D / 60
    v["real rope speed [m/s]"] = v_real
    r.checks.append(Check("Motor: rope speed error", abs(v_real - req.rope_speed) / req.rope_speed * 100, 3.0, "%", "<="))

    # 5. Chain drive
    TK = T / (s.chain_ratio * s.eff_chain * s.eff_bearings)
    z2 = round(s.z1 * s.chain_ratio)
    v_chain = s.z1 * s.chain_pitch * s.motor_speed / 60
    Fr = TK * math.pi * s.motor_speed / (30 * v_chain)
    K = math.prod(s.chain_load_factors)
    p = K * Fr / (2 * s.roller_width * s.roller_diameter)
    Ff = G * s.sag_factor * s.chain_mass * s.centre_distance
    Ft = s.chain_mass * v_chain ** 2
    Fv = Fr + 2 * Ff
    v.update({"sprocket torque T_K [N m]": TK, "driven sprocket teeth z2": z2,
              "chain speed [m/s]": v_chain, "chain pull F_R [N]": Fr,
              "chain load factor K": K, "shaft load from chain F_V [N]": Fv})
    r.checks.append(Check("Chain: roller pressure", p / 1e6, s.chain_allowable_pressure / 1e6, "MPa", "<="))
    r.checks.append(Check("Chain: safety factor", s.chain_breaking_load / (Fv + Ft + Ff), s.chain_min_safety, "-", ">="))

    # 6. Shaft
    d_min = (16 * T / (math.pi * s.shaft_allow_shear)) ** (1 / 3)
    v["min shaft diameter (torsion) [mm]"] = d_min * 1e3
    r.checks.append(Check("Shaft: chosen diameter vs torsion minimum", s.shaft_d_sprocket * 1e3, d_min * 1e3 - 0.5, "mm", ">="))
    lr = 1.5 * s.shaft_d_hub
    span = s.drum_length + 2 * s.bearing_width   # 400 + 2*60 = 520 mm
    l1 = s.sprocket_width / 2 + s.bearing_width / 2 + 0.010
    l2 = lr / 2 + s.bearing_width / 2 + 0.015
    l3 = span - 2 * l2
    # Drum load split equally between the two hubs (D and E); chain load overhung at C.
    RB = (F / 2 * l2 + F / 2 * (l2 + l3) - Fv * l1) / span
    RA = Fv + F - RB
    MA = Fv * l1
    v.update({"bearing span [mm]": span * 1e3, "reaction R_A [N]": RA, "reaction R_B [N]": RB,
              "bending moment at bearing A [N m]": MA})
    M_eq = math.sqrt(MA ** 2 + 0.75 * T ** 2)
    sigma_eq = 32 * M_eq / (math.pi * s.shaft_d_bearing ** 3)
    r.checks.append(Check("Shaft: equivalent stress at bearing A", sigma_eq / 1e6,
                          s.shaft_yield / s.shaft_static_safety / 1e6, "MPa", "<="))
    sigma_a = 32 * MA / (math.pi * s.shaft_d_bearing ** 3)
    tau_a = 16 * T / (2 * math.pi * s.shaft_d_bearing ** 3)
    S_sigma = s.sigma_m1 / (s.k_sigma / (s.k_f * s.kd_sigma) * sigma_a)
    S_tau = s.tau_m1 / (s.k_tau / (s.k_f * s.kd_tau) * tau_a + s.psi_tau * tau_a)
    S = S_sigma * S_tau / math.hypot(S_sigma, S_tau)
    v.update({"fatigue S_sigma": S_sigma, "fatigue S_tau": S_tau})
    r.checks.append(Check("Shaft: fatigue safety factor", S, s.fatigue_min_safety, "-", ">="))

    # 7. Bearings
    n_drum = 30 * w / math.pi
    L10 = (s.bearing_C / RA) ** 3 * 1e6 / (60 * n_drum)
    r.checks.append(Check("Bearing A: L10 life", L10, s.bearing_life_min_h, "h", ">="))

    # 8. Keys (two keys per joint share the torque)
    for label, d, length in (("drum hub", s.shaft_d_hub, s.key_len_hub),
                             ("sprocket", s.shaft_d_sprocket, s.key_len_sprocket)):
        lw = length - s.key_b
        n = s.keys_per_joint
        contact = 2 * T / (n * d * (s.key_h - s.key_t1) * lw)
        shear = 2 * T / (n * d * s.key_b * lw)
        r.checks.append(Check(f"Key ({label}): contact stress", contact / 1e6, s.key_allow_contact / 1e6, "MPa", "<="))
        r.checks.append(Check(f"Key ({label}): shear stress", shear / 1e6, s.key_allow_shear / 1e6, "MPa", "<="))

    # 9. Drum shell
    D1 = D - 2 * s.drum_wall
    W = 0.1 * (D ** 4 - D1 ** 4) / D
    M = F / 2 * l3 / 2
    sig_s = F / (s.drum_wall * s.rope_diameter)
    sig_m = M / W
    tau = T / (2 * W)
    sig_eq = math.sqrt((sig_s + sig_m) ** 2 + 4 * tau ** 2)
    v["drum compressive stress [MPa]"] = sig_s / 1e6
    r.checks.append(Check("Drum: equivalent stress", sig_eq / 1e6, s.drum_allow / 1e6, "MPa", "<="))
    return r


def format_result(r: Result, markdown: bool = False) -> str:
    lines = []
    if markdown:
        lines += ["| Check | Value | Limit | Result |", "|---|---:|---:|:---:|"]
        for c in r.checks:
            sign = "≤" if c.rule == "<=" else "≥"
            lines.append(f"| {c.name} | {c.value:,.1f} {c.unit} | {sign} {c.limit:,.1f} {c.unit} | {'✅' if c.ok else '❌'} |")
        return "\n".join(lines)
    lines.append("Key values")
    for k, val in r.values.items():
        lines.append(f"  {k:<40} {val:>12,.2f}")
    lines.append("\nStrength checks")
    for c in r.checks:
        sign = "<=" if c.rule == "<=" else ">="
        lines.append(f"  [{'PASS' if c.ok else 'FAIL'}] {c.name:<44} {c.value:>10,.1f} {sign} {c.limit:,.1f} {c.unit}")
    lines.append(f"\nOverall: {'all checks pass' if r.all_ok else 'redesign needed'}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--load", type=float, default=750.0, help="rated load in kg")
    ap.add_argument("--speed", type=float, default=0.11, help="rope speed in m/s")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    print(format_result(design(Requirements(a.load, a.speed)), markdown=a.markdown))


if __name__ == "__main__":
    main()
