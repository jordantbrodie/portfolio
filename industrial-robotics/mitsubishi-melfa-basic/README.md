# Mitsubishi RV-2AJ: four-station pick-and-place (MELFA BASIC IV)

**Course:** ATR0030 Robotics, Lab 1 (TalTech, September 2026) · **Tools:** CIROS Studio, MELFA BASIC IV

A pick-and-place routine for a 5-axis Mitsubishi RV-2AJ with a gripper. The robot picks a workpiece at station 1 and moves it through stations 2, 3 and 4, setting it down and re-gripping it at each one, then waits for an external signal before ending.

- [`pick_and_place.MB4`](pick_and_place.MB4): the program, with a comment on every line
- [`pick_and_place.POS`](pick_and_place.POS): the taught positions (P11–P26)

## How it is structured

Each station uses the same safe pattern:

1. `MOV` (joint move) to an **approach point** above the station (P2x)
2. `MVS` (straight-line move) **down** to the pick/place point (P1x)
3. `HOPEN` / `HCLOSE` the gripper, with a 1 s `DLY` so it finishes moving
4. `MVS` straight back **up** before travelling on

Joint moves are fast for travel; straight-line moves are used near the workpiece so the gripper comes in vertically and doesn't knock it.

```basic
10 MOV P21      'approach point above station 1
20 HOPEN 1      'open gripper
40 MVS P11      'straight down to the workpiece
50 HCLOSE 1     'grasp
70 MVS P21      'straight back up
...
420 WAIT M_IN(5) = 1   'wait for external input 5 before finishing
```

Full report: [ATR0030_Lab1_Mitsubishi_RV-2AJ.pdf](../../docs/coursework-reports/ATR0030_Lab1_Mitsubishi_RV-2AJ.pdf)
