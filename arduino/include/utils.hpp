#include <stdint.h>

/*
 * Divides a value by a dividend, and stores the result into a char*
 * This function is just a string formatter.
 *
 */
void divide_value(uint32_t value, uint32_t dividend, uint8_t decimal_points,
		char *result);
