#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define SCREEN_I2C_ADDRESS 0x3C

namespace ssd1306_display {
	void draw_text(String text);

	void draw_statusbar();

	void draw();

	bool setup();
}
