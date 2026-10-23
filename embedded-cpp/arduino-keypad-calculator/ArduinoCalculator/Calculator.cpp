#include "Calculator.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

Calculator::Calculator() { clear(); }

void Calculator::clear() {
  strcpy(entry_, "0");
  entryLen_ = 1;
  entryHasDot_ = false;
  startNewEntry_ = true;
  accumulator_ = 0.0;
  pendingOp_ = 0;
  error_ = false;
  expr_[0] = '\0';
}

void Calculator::press(char key) {
  if (key == 'C') { clear(); return; }
  if (error_) return;                         // only 'C' gets out of an error
  if ((key >= '0' && key <= '9') || key == '.') appendDigit(key);
  else if (key == '<') backspace();
  else if (key == '+' || key == '-' || key == '*' || key == '/') chooseOperator(key);
  else if (key == '=') evaluate();
}

void Calculator::appendDigit(char key) {
  if (startNewEntry_) {
    strcpy(entry_, "0");
    entryLen_ = 1;
    entryHasDot_ = false;
    startNewEntry_ = false;
  }
  if (key == '.') {
    if (entryHasDot_) return;
    entryHasDot_ = true;
  } else if (entryLen_ == 1 && entry_[0] == '0') {
    entryLen_ = 0;                             // replace the leading zero
  }
  if (entryLen_ >= kMaxDigits) return;         // ignore keys past the display width
  entry_[entryLen_++] = key;
  entry_[entryLen_] = '\0';
}

void Calculator::backspace() {
  if (startNewEntry_) return;
  if (entry_[entryLen_ - 1] == '.') entryHasDot_ = false;
  entry_[--entryLen_] = '\0';
  if (entryLen_ == 0) { strcpy(entry_, "0"); entryLen_ = 1; }
}

void Calculator::chooseOperator(char op) {
  if (pendingOp_ && startNewEntry_) {          // operator pressed twice: just swap it
    pendingOp_ = op;
  } else {
    double value = atof(entry_);
    if (pendingOp_) {
      if (!apply(accumulator_, pendingOp_, value, accumulator_)) { error_ = true; return; }
      showNumber(accumulator_);
    } else {
      accumulator_ = value;
    }
    pendingOp_ = op;
    startNewEntry_ = true;
  }
  snprintf(expr_, sizeof(expr_), "%s %c", entry_, pendingOp_);
}

void Calculator::evaluate() {
  if (!pendingOp_) return;
  double result;
  if (!apply(accumulator_, pendingOp_, atof(entry_), result)) { error_ = true; return; }
  showNumber(result);
  accumulator_ = result;
  pendingOp_ = 0;
  startNewEntry_ = true;
  expr_[0] = '\0';
}

bool Calculator::apply(double a, char op, double b, double& out) {
  switch (op) {
    case '+': out = a + b; break;
    case '-': out = a - b; break;
    case '*': out = a * b; break;
    case '/':
      if (b == 0.0) return false;              // divide by zero -> "Error"
      out = a / b;
      break;
    default: return false;
  }
  return isfinite(out) && fabs(out) < 1e11;    // overflow past the display -> "Error"
}

void Calculator::showNumber(double value) {
  // Up to 6 decimals, then strip trailing zeros: 2.500000 -> 2.5, 4.000000 -> 4
  char buf[32];
#ifdef __AVR__
  dtostrf(value, 1, 6, buf);                   // AVR printf has no %f support
#else
  snprintf(buf, sizeof(buf), "%.6f", value);
#endif
  char* end = buf + strlen(buf) - 1;
  while (*end == '0') *end-- = '\0';
  if (*end == '.') *end = '\0';
  if (strcmp(buf, "-0") == 0) strcpy(buf, "0");
  strncpy(entry_, buf, kMaxDigits + 1);
  entry_[kMaxDigits + 1] = '\0';
  entryLen_ = strlen(entry_);
  entryHasDot_ = strchr(entry_, '.') != nullptr;
}

const char* Calculator::display() const { return error_ ? "Error" : entry_; }
const char* Calculator::expression() const { return expr_; }
