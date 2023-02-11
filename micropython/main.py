'''
This is a fairly simple system for taking in sequential frames of data and displaying them on an LED strip
For now, the only frames of data that are coming in are rows from a CSV file
But as this application grows, different data fetcher objects may be able to fetch data frames from different sources and still use the
same mapping and LED handling objects
'''

from machine import ADC, Pin
from utime import sleep_ms

from datafetcher import DataFetcher
from flowstate import map_alarm_count_to_rgb
from ledhandler import LEDHandler


def button_toggler(*args, **kwargs):
    '''
    This function is intended to be used as an interrupt request (IRQ) handler for a simple push-putton
    It's only purpose is to toggle a global Boolean variable that is used to determine whether the main loop is continuing to advance or not

    Parameters
    ----------
    *args : [any]
        list of unnamed arguments; it is assumed that the IRQ handler call only passes one unnamed argument - the input device that triggered
        the IRQ handler, but using *args helps keep the function from crashing if something unexpected is passed in
    **kwargs: dict
        dict of named arguments; it is assumed that the IRQ handler call does not pass any named arguments, but this parameter allows the
        unexpected to happen
    '''
    global is_paused
    is_paused = not is_paused


def adjust_speed(analog_in:ADC):
    '''
    This function is used to set the speed of the main application loop
    Specifically, this function computes the number of miliseconds the system should sleep before moving to the next iteration of the loop

    Parameters
    ----------
    analog_in : machine.ADC
        the input pin on the Raspberry Pi microcontroller that is receiving an analog voltage level between 0 and 3.3 volts
        adjusting the voltage level on this pin is how the speed of the main loop is set

    Returns
    -------
    int
        the number of miliseconds to sleep before iterating through the loop again
    '''

    # Set a default return value and set of options
    return_value = 10
    return_options = [1000, 900, 800, 600, 400, 200, 100, 50, 10, 5]

    # Attempt to read the analog voltage value as a sixteen-bit integer (0 - 65535)
    # If the value was read in, do a linear conversion to an integer to use as the index for which value in return_options to return
    digitized_value = analog_in.read_u16()
    if (type(digitized_value) in [int, float]):
        return_value = return_options[int((digitized_value / 65536) * len(return_options))]

    return return_value


# Declare this variable as a global variable so that it can be toggled in the relevant interrupt request (IRQ) handler
global is_paused
is_paused = True

# Set the relevant variables used by this application
csv_file_name = "count_data.csv"
led_pin_number = 0
pause_pin_number = 14
speed_pin_number = 28
led_count = 60

# Initialize the objects used by this application

# This data fetcher only works with CSV files, but it is all we need right now for this proof-of-concept
fetcher = DataFetcher(csv_file_name)

# This object handles the LED strip
led_strip = LEDHandler(led_pin_number, led_count)

# This button is used to pause/unpause the application's main loop
toggle_button = Pin(pause_pin_number, Pin.IN)
toggle_button.irq(trigger=Pin.IRQ_RISING, handler=button_toggler)

# This analog input is used to control the speed of the application's main loop
speed_controller = ADC(speed_pin_number)


# ********************************************************************************************************************
# Everything is set up, now start the application's main loop by fetching the first data frame from the fetcher object
# ********************************************************************************************************************

row = fetcher.fetch()
while (row != None):
    # A row of data was fetched successfully, think about displaying it on the LED string

    if (not is_paused):
        # The application's main loop is not paused, now really try to display it on the LED string

        # Iterate over the set of elements in the data frame, convert each one to an RGB color set, and send RGB codes to the LED strip
        led_strip.set_gauges([map_alarm_count_to_rgb(alarm_count) for alarm_count in row])

        # Sleep for some number of miliseconds as determined by an analog input pin on the microcontroller
        sleep_ms(adjust_speed(speed_controller))

        # Now attempt to fetch the next data frame from the fetcher object before iterating over this main loop again
        row = fetcher.fetch()
