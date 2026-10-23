// Calculator.h - hardware-independent calculator logic for a 4x4 keypad.
//
// Keys: '0'-'9', '.', '+', '-', '*', '/', '=', 'C' (clear), '<' (backspace).
// The class only turns key presses into display text, so the same code runs
// on an Arduino and in the desktop unit tests (tests/test_calculator.cpp).
#pragma once

class Calculator {
public:
  static const int kMaxDigits = 12;  // fits a 16x2 LCD line with room for the operator

  Calculator();

  void press(char key);              // feed one key press
  const char* display() const;       // text for the bottom LCD line
  const char* expression() const;    // text for the top LCD line, e.g. "12 +"
  bool hasError() const { return error_; }

private:
  void clear();
  void appendDigit(char key);
  void backspace();
  void chooseOperator(char op);
  void evaluate();
  void showNumber(double value);
  static bool apply(double a, char op, double b, double& out);

  char entry_[kMaxDigits + 2];   // digits being typed (+ sign + terminator)
  int  entryLen_;
  bool entryHasDot_;
  bool startNewEntry_;           // next digit replaces the display instead of appending
  double accumulator_;
  char pendingOp_;               // 0 when no operator is waiting
  bool error_;
  char expr_[kMaxDigits + 4];
};
