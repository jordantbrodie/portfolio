# C programming: first-year coursework (IAX0583 Programming I, TalTech, autumn 2024)

Two programs from my first programming course, kept as they were submitted. They compile cleanly with `-Wall -Wextra`.

| Program | What it does | Shows |
|---|---|---|
| [`function_table.c`](function_table.c) | Tabulates y = (3 + √(1 + √x³)) / (4 − x²) over a user-given range with a step that grows each row (up to 20 rows). Flags points where the function is undefined (x = ±2) or complex (x < 0). | Input validation, edge cases, `math.h` |
| [`target_tracker.c`](target_tracker.c) | Reads up to 15 objects with distance and speed, advances them by a time step and counts how many reached their target. | Arrays, pointers, functions, documented code |

The first program comes with a full written report: [function_table_report.pdf](function_table_report.pdf) (task analysis, flowchart, algorithm and special cases).

```bash
make
printf '3\n100 20\n50 30\n10 5\n2\n' | ./target_tracker
# Distances after time: 60 0 0  ->  2 object(s) have hit their target.
```
