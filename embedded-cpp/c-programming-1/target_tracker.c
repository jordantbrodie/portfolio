/**
 * Author:          Jordan Brodie
 * Created:         12.12.2024
 * Description:     A program to calculate updated distances from targets
 *                  and count how many objects have hit their targets
 *                  based on distance, speed, and time.
 */

#include <stdio.h>
#include <stdlib.h>

// Constants
#define MAX_SIZE 15

// Function Prototypes
void readInput(int distances[], int speeds[], int *numObjects, int *time);
void displayArray(const int array[], int size, const char *label);
void calculateNewDistances(int distances[], const int speeds[], int size, int time);
int countObjectsAtTarget(const int distances[], int size);

int main(void) {
    int distances[MAX_SIZE];
    int speeds[MAX_SIZE];
    int numObjects, time, hits;

    // Read input
    readInput(distances, speeds, &numObjects, &time);

    // Display initial data
    printf("\nInitial Data:\n");
    displayArray(distances, numObjects, "Distances");
    displayArray(speeds, numObjects, "Speeds");

    // Calculate new distances
    calculateNewDistances(distances, speeds, numObjects, time);

    // Count objects that hit the target
    hits = countObjectsAtTarget(distances, numObjects);

    // Display results
    printf("\nDistances after time:\n");
    displayArray(distances, numObjects, "Distances");
    displayArray(speeds, numObjects, "Speeds");
    printf("\n%d object(s) have hit their target.\n", hits);

    return 0;
}

/**
 * Reads input from the user or a redirected file.
 * Validates the input to ensure all values are within valid ranges.
 * 
 * Parameters:
 *   distances - Array to store distances from the target.
 *   speeds - Array to store speeds of the objects.
 *   numObjects - Pointer to store the number of objects.
 *   time - Pointer to store the time in hours.
 */
void readInput(int distances[], int speeds[], int *numObjects, int *time) {
    printf("Enter the number of objects (between 1 and 15): ");
    if (scanf("%d", numObjects) != 1 || *numObjects < 1 || *numObjects > MAX_SIZE) {
        printf("Error: Number of objects must be between 1 and 15.\n");
        exit(1); // Exit with error
    }

    // Read distances and speeds
    printf("Enter distances and speeds (distance speed) for %d objects:\n", *numObjects);
    for (int i = 0; i < *numObjects; i++) {
        if (scanf("%d %d", &distances[i], &speeds[i]) != 2 || distances[i] < 0 || speeds[i] <= 0) {
            printf("Error: Distances must be non-negative, and speeds must be positive.\n");
            exit(1); // Exit with error
        }
    }

    // Read time
    printf("Enter time (in hours): ");
    if (scanf("%d", time) != 1 || *time < 0) {
        printf("Error: Time must be non-negative.\n");
        exit(1); // Exit with error
    }
}

/**
 * Displays the contents of an array with a label.
 * 
 * Parameters:
 *   array - The array to display.
 *   size - The number of elements in the array.
 *   label - A label to display with the array.
 */
void displayArray(const int array[], int size, const char *label) {
    printf("%s: ", label);
    for (int i = 0; i < size; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

/**
 * Calculates new distances for each object after a given time.
 * If the distance becomes negative, it is replaced with zero.
 * 
 * Parameters:
 *   distances - Array of distances to update.
 *   speeds - Array of speeds.
 *   size - The number of objects.
 *   time - The time in hours.
 */
void calculateNewDistances(int distances[], const int speeds[], int size, int time) {
    for (int i = 0; i < size; i++) {
        distances[i] -= speeds[i] * time;
        if (distances[i] < 0) {
            distances[i] = 0; // Replace negative distances with zero
        }
    }
}

/**
 * Counts how many objects have hit their target (distance = 0).
 * 
 * Parameters:
 *   distances - Array of distances.
 *   size - The number of objects.
 * 
 * Returns:
 *   The number of objects that have hit their target.
 */
int countObjectsAtTarget(const int distances[], int size) {
    int count = 0;
    for (int i = 0; i < size; i++) {
        if (distances[i] == 0) {
            count++;
        }
    }
    return count;
}
