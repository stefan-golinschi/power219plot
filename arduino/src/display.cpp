#include "display.hpp"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT);
boolean blink = 0;

#define CP437_2022 7

void ssd1306_display::draw_statusbar() {
	/* display status bar */
	display.cp437(true);
	display.clearDisplay();
	display.setCursor(0, 0);             // Start at top-left corner
	display.setTextSize(1);             // Draw 2X-scale text

	if (blink)
		display.write(7);
	else
		display.print(" ");
	blink = !blink;

	display.print(" power219plot  v0.1 ");
}

void ssd1306_display::draw_text(String text) {

	/* display text */
	//display.setCursor(cursor_x, cursor_y);
	display.setTextSize(1);
	display.setTextColor(SSD1306_WHITE);
	display.println(text);
}

void ssd1306_display::draw() {
	display.display();
}

bool ssd1306_display::setup() {
	return display.begin(SSD1306_SWITCHCAPVCC, SCREEN_I2C_ADDRESS, false);
}
