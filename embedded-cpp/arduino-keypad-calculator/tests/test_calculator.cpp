// Desktop unit tests for the calculator logic.  Build and run with:  make test
#include <cstdio>
#include <cstring>
#include <string>
#include "../ArduinoCalculator/Calculator.h"

static int failures = 0, checks = 0;

static std::string run(const char* keys) {
  Calculator calc;
  for (const char* k = keys; *k; ++k) calc.press(*k);
  return calc.display();
}

static void expect(const char* keys, const char* want) {
  ++checks;
  std::string got = run(keys);
  if (got != want) {
    ++failures;
    printf("FAIL  %-18s expected %-10s got %s\n", keys, want, got.c_str());
  }
}

int main() {
  expect("", "0");
  expect("12+7=", "19");
  expect("9-12=", "-3");
  expect("6*7=", "42");
  expect("7/2=", "3.5");
  expect("1/3=", "0.333333");
  expect("2+3*4=", "20");          // evaluates left to right, like a pocket calculator
  expect("5+-2=", "3");            // second operator replaces the first
  expect("0.1+0.2=", "0.3");
  expect("1..5+1=", "2.5");        // a second decimal point is ignored
  expect("007", "7");              // leading zeros are dropped
  expect("123<", "12");            // backspace
  expect("5<<", "0");
  expect("8/0=", "Error");
  expect("8/0=3+", "Error");       // stays in error until cleared
  expect("8/0=C4+4=", "8");
  expect("10+5=*2=", "30");        // chain from a previous result
  expect("12345678901234", "123456789012");   // display width limit
  expect("99999999999*9=", "Error");          // overflow
  expect("3=", "3");                          // '=' with no operator does nothing
  printf("%d/%d checks passed\n", checks - failures, checks);
  return failures ? 1 : 0;
}
