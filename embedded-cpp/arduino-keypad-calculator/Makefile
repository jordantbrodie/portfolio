CXX ?= g++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Werror -O2

test: tests/test_calculator
	./tests/test_calculator

tests/test_calculator: tests/test_calculator.cpp ArduinoCalculator/Calculator.cpp ArduinoCalculator/Calculator.h
	$(CXX) $(CXXFLAGS) -o $@ tests/test_calculator.cpp ArduinoCalculator/Calculator.cpp

clean:
	rm -f tests/test_calculator

.PHONY: test clean
