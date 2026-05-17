#include "test_bus_lines.h"
#define ZERO 0

#define ONE 1
#include <stdbool.h>
//TODO add implementation here


/**
 * TODO add documentation
 */
int is_sorted_by_distance (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current + ONE< end; ++current)
    {
        if (current->distance > (current+ONE)->distance)
        {
            return ZERO;
        }
    }
    return ONE;
}

/**
 * TODO add documentation
 */
int is_sorted_by_duration (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current +1 < end; ++current)
    {
        if (current->duration > (current+1)->duration)
        {
            return ZERO;
        }
    }
    return ONE;
}

/**
 * TODO add documentation
 */
int is_sorted_by_frequency (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current +1< end; ++current)
    {
        if (current->frequency > (current+1)->frequency)
        {
            return ZERO;
        }
    }
    return ONE;
}

/**
 * TODO add documentation
 */
int is_sorted_by_name (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current + ONE < end; ++current)
    {
        if(strcmp(current->name, (current+ONE)->name) > ZERO)
        {
            return ZERO;
        }
    }
    return ONE;
}


/**
 * TODO add documentation
 */
int is_equal (const BusLine *start_sorted,
              const BusLine *end_sorted,
              const BusLine *start_original,
              const BusLine *end_original)
{
    if ((end_sorted-start_sorted) != (end_original-start_original))
    {
        return ZERO;
    }
    for (const BusLine *i = start_original; i<end_original; i++)
    {
        int origin_sum = ZERO;
        int sort_sum = ZERO;
        for (const BusLine *z = start_sorted; z<end_sorted; z++)
        {
            if (is_identity(i,z))
            {
                sort_sum += ONE;
            }
        }
        for (const BusLine* y = start_original; y<end_original; y++)

        {
            if (is_identity(i,y))
            {
                origin_sum += 1;
            }
        }
        if (origin_sum != sort_sum)
        {
            return 0;
        }
    }

    return 1;
}

int is_identity (const BusLine *first, const BusLine *second)
{
    // if ((first->distance != second->distance))
    // {
    //     return 0;
    // }
    if (strcmp(first->name, second->name))
    {
        return ZERO;
    }
    // if ((first->frequency != second->frequency))
    // {
    //     return 0;
    // }
    // if ((first->duration != second->duration))
    // {
    //     return 0;
    // }
    return ONE;

}
