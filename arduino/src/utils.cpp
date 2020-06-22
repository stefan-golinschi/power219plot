#include "utils.hpp"
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

void divide_value(uint32_t value, uint32_t dividend, uint8_t decimal_points,
		char *result) {
	uint32_t quotient;
	uint32_t remainder;

	quotient = value / dividend;
	remainder = value % dividend;

	size_t result_sz = sizeof(result);

	memset(result, 0x0, result_sz);
	itoa(quotient, result, 10);
	strcat(result, ".");

	for (int i = 0; i < decimal_points; i++) {
		value = remainder * 10;
		quotient = value / dividend;
		remainder = value % dividend;

		char quotient_str[1];
		itoa(quotient, quotient_str, 10);
		strcat(result, quotient_str);
	}
}
