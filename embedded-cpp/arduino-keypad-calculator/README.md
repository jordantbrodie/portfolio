# Arduino keypad calculator (C++)

A four-function calculator on an **Arduino Uno** with a **4×4 membrane keypad** and a **16×2 LCD** on an I²C backpack. The top LCD line shows the pending operation (`12 +`), the bottom line the current number or result.

## Background

My first C++ project, in my freshman programming course, was a calculator on an Arduino. I no longer have that original code, so **this is a 2026 rewrite of the same idea, written with AI assistance**, with a cleaner design and tests.

## Design

The calculator logic is a small class with no Arduino dependencies:

```
ArduinoCalculator/
├── ArduinoCalculator.ino   ← hardware: reads the keypad, drives the LCD
├── Calculator.h / .cpp     ← logic: turns key presses into display text
tests/
└── test_calculator.cpp     ← 20 checks, compiled and run on a PC
```

Because `Calculator` only takes characters in and gives text out, the same code is compiled for the Arduino and for the desktop tests. That makes it possible to test edge cases without flashing a board every time.

Behaviour covered by the tests:

- Left-to-right evaluation like a pocket calculator (`2 + 3 × 4 = 20`), chaining from a previous result
- Decimals, ignored second decimal point, leading zeros, backspace
- Pressing a second operator replaces the first (`5 + − 2 = 3`)
- **Divide by zero and overflow show `Error`** and lock out input until cleared
- Display width limited to 12 digits; results trimmed (`3.500000` → `3.5`)
- On AVR boards `printf` has no `%f`, so the code uses `dtostrf()` there and `snprintf()` on a PC

## Wiring

| Part | Arduino Uno |
|---|---|
| Keypad rows 1–4 | D9, D8, D7, D6 |
| Keypad columns 1–4 | D5, D4, D3, D2 |
| LCD I²C SDA / SCL | A4 / A5 (address 0x27) |

Keypad layout: digits, `+ − × ÷`, `.` on `*`, `=` on `#`. **Hold `=` for one second to clear.**

Libraries: *Keypad* (Mark Stanley, Alexander Brevig) and *LiquidCrystal I2C* (Frank de Brabander), both from the Arduino Library Manager.

## Run the tests

```bash
make test       # needs g++
# 20/20 checks passed
```
