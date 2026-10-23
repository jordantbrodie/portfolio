# Systems engineering case study: 750 kg electric winch

*One-page view of my [electric winch project](../mechanical-design/electric-winch/), laid out the way a systems engineer tracks a design: every requirement traced to a design decision, a verification method and a result.*

## Need

Lift and position heavy components in an assembly workshop, where handling them by hand is unsafe. The winch must be compact and light.

## Requirements → design → verification

Verification methods: **A** = analysis (calculation), **I** = inspection (drawing / catalogue), **T** = test (planned for a physical build).

| ID | Requirement | Design decision | Verif. | Result |
|---|---|---|:---:|---|
| R1 | Lift a **750 kg** rated load | Rope TEK 13310 Ø10 mm (breaking force 59.7 kN) with safety factor 5.5 | A | 7.36 kN ≤ 10.85 kN allowable ✅ |
| R2 | Rope speed **0.11 m/s** | Drum Ø200 mm; SEW R77 DT90S4 gear motor at 17 rpm; chain ratio 1.6 | A | 0.111 m/s, error 1.1 % (limit 3 %) ✅ |
| R3 | Drive the drum by **chain** from a gear motor | 16B-2 double-strand chain, sprockets 19 / 31 teeth | A | Roller pressure 24.7 ≤ 40 MPa; chain safety factor 15.8 ≥ 7.3 ✅ |
| R4 | **Minimise size and mass** | Double-strand 16B chain instead of a bulky single-strand 20B; 19-tooth driving sprocket instead of the recommended 26 | A, I | Smaller sprockets and centre distance while all checks pass ✅ |
| R5 | Motor sized for losses | Efficiency chain 0.94 × 0.92 × 0.99, plus a 20 % margin | A | 942 W delivered ≥ 809 W needed at the drum ✅ |
| R6 | Shaft survives static and **fatigue** loads | C45E shaft Ø50 / 55 / 60 mm; fillet at the bearing step | A | Equivalent stress 49.6 ≤ 247 MPa; fatigue safety factor 3.2 ≥ 2.5 ✅ |
| R7 | Bearings last in industrial duty | SKF SY 55 TF self-aligning units | A, I | L10 ≈ 91 000 h ≥ 14 000 h ✅ |
| R8 | Torque transmitted reliably to drum and sprocket | 14 × 9 mm keys, **two per joint** | A | Single key failed (172 > 130 MPa), so I changed to two keys: 85.8 ≤ 130 MPa ✅ |
| R9 | Drum wall strong enough | S235 drum, 7 mm wall | A | Equivalent stress 108 ≤ 120 MPa (90 % utilised) ✅ |
| R10 | Safe operation (Machinery Directive 2006/42/EC) | Fail-safe load-holding brake; overload cut-off at 110–120 %; annual rope test; proof load 1.5× rated | I, T | Specified in design; test planned for a physical build |
| R11 | Environment −10 °C … +40 °C, IP55 | Sealed motor housing; galvanised or powder-coated drum and frame | I | Specified ✅ |

All analysis results above come from [`winch_design.py`](../mechanical-design/electric-winch/calculations/winch_design.py), which re-runs every check. Its tests confirm it matches my hand calculations.

## Change impact: what if the requirement changes?

Raising **R1 from 750 kg to 1000 kg** and re-running the checks shows which parts of the design break:

| Check | 750 kg | 1000 kg |
|---|---|---|
| Motor power delivered | ✅ | ❌ 942 W < 1079 W needed |
| Shaft diameter (torsion) | ✅ | ❌ needs 54.5 mm |
| Shaft fatigue safety factor | ✅ 3.2 | ❌ 2.4 < 2.5 |
| Drum equivalent stress | ✅ 108 MPa | ❌ 144 MPa > 120 MPa |

So a heavier load means a new motor, a thicker shaft and a thicker drum wall; the rope, chain, bearings and keys still pass.

## Configuration control

Checking the drawing against the calculations found **three mismatches**:
- the drawing's bill of materials listed an older motor (R77 DV100M4), 20B sprockets and an 18 × 11 key;
- the analysis used the R77 DT90S4 motor, 16B-2 sprockets and a 14 × 9 key;
- one table in the report gave the bearing span as L_tr + L_b + 30 (490 mm), while the calculations used 520 mm.

I corrected the documents so the drawing, report and calculations describe the same design. Keeping documents consistent like this is what configuration management means.
