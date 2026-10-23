#include <stdio.h>
#include <math.h>  
#define MAX_RESULTS 20  // Maximum number of results to display

void calculate(float A, float B, float H, float C);

int main() 
{
    float A, B, H, C;

    // Intro message and user input
    printf("This program will calculate and output the value of x for the function y = (3 + sqrt(1 + sqrt(x^3))) / (4 - x^2) displaying up to 20 results.\n");
    printf("To begin please enter a starting value A for x where you would like to begin our calculations: ");
    scanf("%f", &A);
    printf("Enter stopping value B (B must be greater than A): ");
    scanf("%f", &B);
    printf("Enter step H (H > 0): ");
    scanf("%f", &H);
    printf("Enter coefficient C (C > 0): ");
    scanf("%f", &C);

    // Check inputs
    if (B <= A || H <= 0 || C <= 0) 
    {
        printf("Invalid inputs! Ensure that B > A and both H, C > 0.\n");
        return 1;  // Exit if inputs are not valid
    }

    // Call calculation function
    calculate(A, B, H, C);

    return 0;
}

// Function to calculate x and y values then print them in a table
void calculate(float A, float B, float H, float C) {
    float x, y;
    int i = 0;

    // Top of results table
    printf("\n  X\t\t   Y\n");
    printf("----------------------------\n");

    // Loop to calculate and print values 
    for (x = A; x <= B && i < MAX_RESULTS; i++) 
    {
        // Check denominator is 0 
        if ((4 - x * x) == 0) 
        {
            printf("%8.4f\t   missing\n", x);  // If undefined, print 'missing'
        } 
        // Check if x is negative, complex number
        else if (x < 0) 
        {
            printf("%8.4f\t   complex\n", x);  // Print 'complex' for negative x
        } 
        // calculation of y when x is valid
        else 
        {
            y = (3 + sqrt(1 + sqrt(pow(x, 3)))) / (4 - x * x);  // Compute y
            printf("%8.4f\t   %8.4f\n", x, y);  // Print x and y values
        }

        // Update x value and step with H and C
        x = A + H * (1 + pow(C, i));
    }
}
