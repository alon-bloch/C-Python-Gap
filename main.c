#include "sort_bus_lines.h"
#include "test_bus_lines.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define BY_NAME "by_name"
#define BY_FREQ "by_frequency"
#define BY_DISTANCE "by_distance"
#define BY_DURATION "by_duration"
#define MAX_NAME_LEN 21
#define ZERO 0
#define MAX_DUR 100
#define MAX_DIS 1000
#define MAX_FREQ 50
#define ONE 1
#define MIN_DUR 10
#define MAX_LEN 300
#define FOUR 4
#define TWO 2



/**
 * TODO add documentation
 */

int has_uppercase(const char *c)
{
    int j = ZERO;
    while (c[j] != '\0')
    {
        if (!(c[j]>='0' && c[j]<='9') && !(c[j]>='a' && c[j]<='z'))
    {
    return ONE;
    }
    j++;
    }
    return ZERO;
}
void get_lines(BusLine **start_pointer, BusLine **end_pointer,int line_num)
{
    BusLine * arr = (calloc(line_num, sizeof(BusLine)));
    if (arr)
    {
        char buffer[MAX_LEN];

        for (int i = ZERO; i < line_num; i++)
        {
            printf("Enter line info. Then enter\n");
            fgets(buffer, sizeof(buffer), stdin);
            int items = sscanf(buffer,"%20[^,],%d,%d,%d",arr[i].name,&arr[i].distance,&arr[i].duration,&arr[i].frequency);
            if (items != FOUR)
            {
                printf("%s", "USE FORM - <line_name>,<distance>,<duration>,<frequency>. Then enter\n");
                i--;
            }
            else if (has_uppercase(arr[i].name))
            {
                printf("%s", "Error: Bus name cannot contain uppercase letters\n");
                i--;
            }

            else if (strlen(arr[i].name) > MAX_NAME_LEN)
            {
                printf("%s", "Error: Bus name shold contain up to 20 chars\n");
                i--;
            }
            else if ((arr[i].distance < ZERO) || (arr[i].distance > MAX_DIS))
            {
                printf("%s", "Error: distance should be an integer between 0 and 1000 (includes)\n");
                i--;
            }
            else if ((arr[i].duration < MIN_DUR) || (arr[i].duration > MAX_DUR))
            {
                printf("%s", "Error: duration should be an integer between 10 and 100 (includes)\n");
                i--;
            }
            else if ((arr[i].frequency < ONE) || (arr[i].frequency > MAX_FREQ))
            {
                printf("%s", "Error: Bus frequency should be between 1 and 50 \n");
                i--;
            }
        }
        *start_pointer = arr;
        *end_pointer = arr + line_num;
    }
}

void get_input(BusLine **start_pointer, BusLine **end_pointer)
{
    char buffer[MAX_LEN];
    int line_num = ZERO;
    while (line_num<=ZERO)
    {
        printf("%s", "Enter number of lines. Then enter\n");
        fgets(buffer, sizeof(buffer), stdin);
        sscanf(buffer,"%d",&line_num);
        if (line_num<=ZERO)
            printf("Error: Number of lines should be a positive integer\n");
    }
    get_lines(start_pointer, end_pointer,line_num);

}
void my_print(const BusLine *start, const BusLine *end)
{
    if (start)
    {
        for (const BusLine *cur = start; cur < end; cur++)
        {
            printf("%s,%d,%d,%d\n", cur->name, cur->distance, cur->duration, cur->frequency);
        }
    }
}
bool check_input(int argc, char *argv[])
{
    if (argc != TWO)
    {
        printf("%s", "Usage: Enter one argument - for example 'by_name'");
        return false;
    }
    if ((strcmp(argv[ONE], BY_NAME) == ZERO) || (strcmp(argv[ONE], BY_DURATION) == ZERO) || (strcmp(argv[ONE], BY_DISTANCE) == ZERO) || (strcmp(argv[ONE], BY_FREQ) == ZERO) || (strcmp(argv[ONE], BY_FREQ) == ZERO) || (strcmp(argv[ONE], "test") == ZERO))
    {
        return true;
    }
        printf("%s %s", "Usage: 'by_duration', 'by_distance', by_frequency', 'test' - Unknown command ", argv[1]);
        return false;
}
bool my_test(BusLine *start, BusLine *end)
{
    BusLine * arr = (calloc(end-start, sizeof(BusLine)));
    if (!arr)
        return false;
    BusLine *original_start = arr;
    BusLine *original_end = arr+(end-start);
for (int i = ZERO; i<end-start; i++)
{
    original_start[i] = start[i];
}
    bus_quick_sort (start, end,DISTANCE);
    if (is_sorted_by_distance(start,end))
        printf("TEST 1 PASSED: The array is sorted by distance\n");
    else
        printf("TEST 1 FAILED: Not sorted by distance\n");
    if (is_equal (start,end, original_start,original_end))
        printf("TEST 2 PASSED: The array has the same items after sorting\n");
    else
        printf("TEST 2 FAILED: Not equal\n");
    bus_quick_sort (start, end,DURATION);
    if (is_sorted_by_duration(start,end))
        printf("TEST 3 PASSED: The array is sorted by duration\n");
    else
        printf("TEST 3 FAILED: Not sorted by duration\n");
    if (is_equal (start,end, original_start,original_end))
        printf("TEST 4 PASSED: The array has the same items after sorting\n");
    else
        printf("TEST 4 FAILED: Not equal\n");
    bus_quick_sort (start, end,FREQUENCY);
    if (is_sorted_by_frequency(start,end))
        printf("TEST 5 PASSED: The array is sorted by frequency\n");
    else
        printf("TEST 5 FAILED: Not sorted by frequency\n");
    if (is_equal (start,end, original_start,original_end))
        printf("TEST 6 PASSED: The array has the same items after sorting\n");
    else
        printf("TEST 6 FAILED: Not equal\n");
    bus_bubble_sort (start, end);
    if (is_sorted_by_name(start,end))
        printf("TEST 7 PASSED: The array is sorted by name\n");
    else
        printf("TEST 7 FAILED: Not sorted by name\n");
    if (is_equal (start,end, original_start,original_end))
        printf("TEST 8 PASSED: The array has the same items after sorting\n");
    else
        printf("TEST 8 FAILED: Not equal\n");
    free(original_start);
    return true;
}
int main (int argc, char *argv[])
{
    if (!check_input(argc, argv))
    {
        return EXIT_FAILURE;
    }
    BusLine *start = NULL;
    BusLine *end = NULL;
    get_input(&start, &end);
    if (!start)
        return EXIT_FAILURE;
if (strcmp(argv[ONE], "test") == 0)
{
    if (!my_test(start,end))
        return EXIT_FAILURE;
    free(start);
    return EXIT_SUCCESS;
}
    if ((end-start) == ONE)
    {
        my_print(start,end);
        free(start);
        return EXIT_SUCCESS;
    }
    if (strcmp(argv[ONE], BY_NAME) == ZERO)
        bus_bubble_sort (start, end);
    else if ((strcmp(argv[ONE], BY_DURATION) == ZERO))
        bus_quick_sort (start, end,DURATION);
    else if ((strcmp(argv[ONE], BY_DISTANCE) == ZERO))
        bus_quick_sort (start, end,DISTANCE);
    else if ((strcmp(argv[ONE], BY_FREQ) == ZERO))
        bus_quick_sort (start, end,FREQUENCY);
    my_print(start,end);
    free(start);
    return EXIT_SUCCESS;
}


