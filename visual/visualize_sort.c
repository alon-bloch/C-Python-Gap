#include <stdio.h>
#include <string.h>

#define NAME_LEN 21

// ANSI Color Codes for better visualization
#define RED   "\x1B[31m"
#define GRN   "\x1B[32m"
#define YEL   "\x1B[33m"
#define BLU   "\x1B[34m"
#define RESET "\x1B[0m"
#define BOLD  "\x1B[1m"

typedef enum SortType { DISTANCE, DURATION, FREQUENCY } SortType;

typedef struct BusLine
{
    char name[NAME_LEN];
    int distance, duration, frequency;
} BusLine;

void wait_for_user() {
    printf(YEL "  [Press Enter to continue...]" RESET);
    getchar();
}

void print_array(BusLine *start, BusLine *end)
{
    printf(BOLD "\n--- Current Array State ---\n" RESET);
    for (BusLine *p = start; p < end; p++)
    {
        printf("  [" BLU "%p" RESET "] %-10s (Dist: %d)\n", (void*)p, p->name, p->distance);
    }
    printf("---------------------------\n");
}

BusLine *visual_partition(BusLine *start, BusLine *end)
{
    printf(BOLD "\n>>> PARTITION VISUALIZATION (Quick Sort logic) <<<\n" RESET);
    BusLine *pivot = end - 1;
    BusLine *small = start;
    
    printf("Benchmark Pivot: [" BLU "%p" RESET "] (" GRN "%s" RESET ": %d)\n", (void*)pivot, pivot->name, pivot->distance);
    
    for (BusLine *current = start; current < end - 1; current++)
    {
        printf("\nScanner at [" BLU "%p" RESET "] (%s)\n", (void*)current, current->name);
        printf("Comparing " GRN "%d" RESET " vs Pivot " GRN "%d" RESET "\n", current->distance, pivot->distance);
        
        if (current->distance <= pivot->distance)
        {
            printf(RED BOLD "  >> SWAP with small at [%p]\n" RESET, (void*)small);
            BusLine temp = *current;
            *current = *small;
            *small = temp;
            small++;
        } else {
            printf("  >> Larger than pivot, no swap.\n");
        }
        wait_for_user();
    }

    printf(RED BOLD "\nFINAL PIVOT SWAP: [%p] <-> [%p]\n" RESET, (void*)pivot, (void*)small);
    BusLine temp = *pivot;
    *pivot = *small;
    *small = temp;
    wait_for_user();

    return small;
}

void visual_bubble_sort(BusLine *start, BusLine *end)
{
    printf(BOLD "\n>>> BUBBLE SORT VISUALIZATION (By Name) <<<\n" RESET);
    for (BusLine *current = start; current < end; current++)
    {
        printf("\n" BOLD "Pass starting at: " BLU "%p" RESET "\n", (void*)current);
        for (BusLine *cur = start; cur + 1 < end; cur++)
        {
            printf("  Comparing: [" BLU "%p" RESET "] (%s) vs [" BLU "%p" RESET "] (%s)\n", 
                   (void*)cur, cur->name, (void*)(cur+1), (cur+1)->name);
            
            if (strcmp(cur->name, (cur+1)->name) > 0)
            {
                printf(RED BOLD "    [SWAP EXECUTED]\n" RESET);
                BusLine temp = *(cur+1);
                *(cur+1) = *cur;
                *cur = temp;
            }
            wait_for_user();
        }
    }
}

int main()
{
    // Larger array with 6 elements to show more complexity
    BusLine buses[6] = {
        {"Echo", 300, 25, 15},
        {"Charlie", 800, 60, 5},
        {"Fox", 150, 12, 40},
        {"Dan", 500, 40, 10},
        {"Bravo", 900, 70, 2},
        {"Alice", 200, 15, 30}
    };

    int n = 6;
    printf(BOLD "POINTER VISUALIZATION TOOL (Array Size: %d)\n" RESET, n);
    print_array(buses, buses + n);

    printf(YEL "Press Enter to start Partition Visualization (on Distance)..." RESET);
    getchar();

    // Demonstration of Partition
    visual_partition(buses, buses + n);
    
    printf("\nPARTITION COMPLETE. Current order:\n");
    print_array(buses, buses + n);

    printf(YEL "Press Enter to start Bubble Sort (on Name) on the same data..." RESET);
    getchar();

    // Demonstration of Bubble Sort
    visual_bubble_sort(buses, buses + n);

    printf("\nALL VISUALIZATIONS COMPLETE.\n");
    print_array(buses, buses + n);

    return 0;
}
