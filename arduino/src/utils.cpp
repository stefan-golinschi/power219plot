#include "utils.hpp"
#include <stdio.h>
#include <stdint.h>

void divide_value(uint32_t value, uint32_t dividend, uint8_t decimal_points,
		char *result, size_t result_len) {
	if (result == NULL || result_len == 0 || dividend == 0) {
		return;
	}

	uint32_t quotient = value / dividend;
	uint32_t remainder = value % dividend;

	int written = snprintf(result, result_len, "%lu.",
			(unsigned long)quotient);
	if (written < 0 || (size_t)written >= result_len) {
		result[result_len - 1] = '\0';
		return;
	}

	size_t pos = (size_t)written;
	for (uint8_t i = 0; i < decimal_points && pos + 1 < result_len; i++) {
		remainder *= 10;
		uint32_t digit = remainder / dividend;
		remainder %= dividend;
		result[pos++] = (char)('0' + digit);
	}
	result[pos] = '\0';
}
