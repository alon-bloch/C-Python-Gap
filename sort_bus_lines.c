#include "sort_bus_lines.h"
#define ZERO 0

#define ONE 1
//TODO add implementation here



BusLine *partition (BusLine *start, BusLine *end, SortType sort_type)
{
    int current_val = ZERO;
    int pivot_val = ZERO;
    BusLine *pivot = end-ONE;
    BusLine *small = start;
    for (BusLine *current = start; current < end -1; current++)
    {


        switch (sort_type)
        {
        case DISTANCE:
            ///
            ///
            current_val = current->distance;
            pivot_val = pivot->distance;
            break;

        case DURATION:
            current_val = current->duration;
            pivot_val = pivot->duration;


            break;
        case FREQUENCY:
            current_val = current->frequency;
            pivot_val = pivot->frequency;


            break;

        }
        if (current_val <= pivot_val)
        {
            BusLine temp = *current;
            *current = *small;
            *small = temp;
            small++;

        }
    }
    BusLine temp = *pivot;
    *pivot = *small;
    *small = temp;
    return small;
}

void bus_quick_sort (BusLine *start, BusLine *end, SortType sort_type)
{
    if (start <end)
    {
        BusLine *pivot = partition (start, end, sort_type);
        bus_quick_sort(start, pivot, sort_type);
        bus_quick_sort(pivot +ONE , end, sort_type);
    }
}


void bus_bubble_sort (BusLine *start, BusLine *end)
{
    for (BusLine *current = start; current < end; current++)
    {
        for (BusLine *cur = start; cur+ONE < end; cur++)
        {
            if (strcmp(cur->name, (cur+ONE)->name)>ZERO)
            {
                BusLine temp = *(cur+ONE);
                *(cur+ONE) = *cur;
                *cur = temp;
            }
        }
    }
}
