'''
This module includs a handler object for handling the display of a data frame on an industry-standard WS2812 LED string
'''

from machine import Pin

from ws2812 import WS2812


class LEDHandler():
    def __init__(self, pin_number, led_count):
        '''
        Initialization method for LEDHandler-class objects

        Parameters
        ----------
        pin_number : int
            the I/O pin number on the Raspberry Pi microcontroller where data is sent to the LED strip
        led_count : int
            the number of LEDS on the strip that will be used - for longer strips, the rest of the physical strip is ignored
        '''

        # Copy led_count to the object-level attributes, create an attribute for the LED strip, and initialize all the leds being used
        # to white
        self.led_count = led_count
        self.led_strip = WS2812(Pin(pin_number), led_count)
        self.set([[255, 255, 255]] * self.led_count)

    def set(self, led_colors):
        '''
        This method sets the LED string's colors according to the incoming argument

        Parameters
        ----------
        led_colors : list[[int, int, int]]
            list of individual RGB codes for each LED in the strip
        '''

        # Iterate over led_colors to load the LED strip's buffer
        for i, rgb in enumerate(led_colors):
            self.led_strip[i] = rgb

        # Write the newly-loaded buffer to the LEDs
        self.led_strip.write()

    def set_gauges(self, led_colors):
        '''
        This method takes in a set of RGB codes for "gauges" and uses them the set the colors on the LED string
        The set of RGB codes comes from a data frame whose values have been color-mapped

        Parameters
        ----------
        led_colors : [[int, int, int]]
            list of RGB codes that represents a color-mapped data frame
        '''

        # Set the number of LEDs in each gauge, with one blank one on each side to separate each gauge visually
        gauge_size = (self.led_count // len(led_colors)) - 2

        # Iterate through the color-mapped data frame to build out the full set of RGB codes for each individual LED on the string
        # Each color-mapped element produces:
        #	* One black LED to start
        #	* A set of LEDs of length gauge_size, all with that element's same color map
        #	* One more black LED to end
        new_led_colors = []
        for rgb in led_colors:
            new_led_colors.append([0, 0, 0])
            new_led_colors.extend([rgb] * gauge_size)
            new_led_colors.append([0, 0, 0])

        # If the gauges did not evenly fill the LED string, pad the end of new_led_colors with enough black elements to fill the LED strip
        while (len(new_led_colors) < self.led_count):
            new_led_colors.append([0, 0, 0])

        self.set(new_led_colors)
