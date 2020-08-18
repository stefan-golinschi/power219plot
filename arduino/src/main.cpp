#include <Wire.h>
#include <Adafruit_INA219.h>

#include "display.hpp"
#include "utils.hpp"
#include "MemoryFree.hpp"

#define MAX_STORED_VALUES 32
#define MAX_VALUE 999000

Adafruit_INA219 ina219;

bool blink_symbol = true;

void setup(void) {
	Serial.begin(115200);
	// while (!Serial)
	// {
	//   // will pause Zero, Leonardo, etc until serial console opens
	//   delay(1);
	// }

	// uint32_t currentFrequency;

	// Initialize the INA219.
	// By default the initialization will use the largest range (32V, 2A).  However
	// you can call a setCalibration function to change this range (see comments).
	if (!ina219.begin()) {
		Serial.println("Failed to find INA219 chip");
		while (1) {
			delay(10);
		}
	}
	// To use a slightly lower 32V, 1A range (higher precision on amps):
	//ina219.setCalibration_32V_1A();
	// Or to use a lower 16V, 400mA range (higher precision on volts and amps):
	//ina219.setCalibration_16V_400mA();

	//Serial.println("Initializing display...");

	if (ssd1306_display::setup() == false) {
		Serial.println(F("SSD1306 allocation failed"));

		/* loop forever */
		while (1) {
			delay(10);
		}
	}
}

uint32_t lowest_current = 9999;
uint32_t highest_current = 0;

char average_current[8];
int average_nvalues = 2;
char current_mA_str[8];

uint32_t stored_values[MAX_STORED_VALUES] = { 0 };
int loop_count = 0;

void loop(void) {
	float shuntvoltage = 0;
	float busvoltage = 0;
	float current_mA = 0;
	uint32_t current_uA = 0;
	float loadvoltage = 0;
	float power_mW = 0;

	shuntvoltage = ina219.getShuntVoltage_mV();
	busvoltage = ina219.getBusVoltage_V();
	current_mA = ina219.getCurrent_mA();
	current_uA = current_mA * 1000;
	power_mW = ina219.getPower_mW();

	loadvoltage = busvoltage + (shuntvoltage / 1000);

	Serial.print(busvoltage); Serial.print(", ");
	Serial.print(shuntvoltage); Serial.print(", ");
	Serial.print(loadvoltage); Serial.print(", ");
	Serial.print(current_mA); Serial.print(", ");
	Serial.print(power_mW); Serial.println("");

	if (current_uA > MAX_VALUE) {
		Serial.print("Overcurrent error: current_uA:");
		Serial.println(current_uA);
		return;
	}

	/* get the peak current value */
	if (current_uA > highest_current)
		highest_current = current_uA;

	/* get the lowest current value */
	if (current_uA < lowest_current)
		lowest_current = current_uA;

	ssd1306_display::draw_statusbar();

//divide_value(current_uA, 1000, 2, current_mA_str);

	if (loop_count == average_nvalues) {

		uint32_t total = 0;

		for (int i = 0; i < average_nvalues; i++) {
			total += stored_values[i];
		}

		divide_value(total, average_nvalues * 1000, 2, average_current);

		average_nvalues += 2;

		if (average_nvalues >= MAX_STORED_VALUES)
			average_nvalues = 2;

	}

	String current_text = String("Current: " + String(current_mA) + " mA");
	String average_text = String("Average: " + String(average_current) + " mA");
	//String loop_count_text = String("#tick: " + String(loop_count + 1) + "/" + String(MAX_STORED_VALUES));
	String vbus_text = String("Bus voltage: " + String(busvoltage) + " V");

	ssd1306_display::draw_text(current_text);
	ssd1306_display::draw_text(average_text);
	//ssd1306_display::draw_text(loop_count_text);
	ssd1306_display::draw_text(vbus_text);
	ssd1306_display::draw();

	stored_values[loop_count] = current_uA;

	loop_count += 1;

	if (loop_count == MAX_STORED_VALUES)
		loop_count = 0;

	delay(1000);
}
