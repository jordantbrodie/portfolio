// ArduinoCalculator.ino - 4x4 membrane keypad + 16x2 I2C LCD calculator.
//
// Hardware: Arduino Uno, 4x4 keypad on pins 9-2, 16x2 LCD with I2C backpack (address 0x27) on A4/A5.
// Libraries: "Keypad" (Mark Stanley, Alexander Brevig) and "LiquidCrystal I2C" (Frank de Brabander).
//
// Keypad layout (letters remapped to calculator functions):
//   1 2 3 +        A -> +
//   4 5 6 -        B -> -
//   7 8 9 *        C -> *
//   . 0 = /        * -> .   # -> =   D -> /
// Hold '=' for one second to clear (C). Backspace ('<') is supported by the logic but has no key on a 4x4 pad.

#include <Keypad.h>
#include <LiquidCrystal_I2C.h>
#include "Calculator.h"

const byte ROWS = 4, COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', '+'},
  {'4', '5', '6', '-'},
  {'7', '8', '9', '*'},
  {'.', '0', '=', '/'},
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

Keypad keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);
LiquidCrystal_I2C lcd(0x27, 16, 2);
Calculator calc;

const unsigned long kHoldToClearMs = 1000;

void printRightAligned(byte row, const char* text) {
  lcd.setCursor(0, row);
  int pad = 16 - (int)strlen(text);
  for (int i = 0; i < pad; i++) lcd.print(' ');
  lcd.print(text);
}

void refresh() {
  printRightAligned(0, calc.expression());
  printRightAligned(1, calc.display());
}

void setup() {
  lcd.init();
  lcd.backlight();
  keypad.setHoldTime(kHoldToClearMs);
  refresh();
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    calc.press(key);
    refresh();
  }
  // Holding '=' clears everything (the keypad has no spare key for 'C').
  if (keypad.getState() == HOLD && keypad.key[0].kchar == '=') {
    calc.press('C');
    refresh();
    while (keypad.getState() == HOLD) keypad.getKey();   // wait for release
  }
}
