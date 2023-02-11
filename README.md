# led

Generate video configuration files for programmable LED systems

*NEW - MICROPYTHON - BASED PROJECT*

The ./micropython directory contains my first real Raspberry Pi project
It is a proof-of-concept application that reads through a CSV file and displays the alarm status for four different complex systems in simple GREEN / YELLOW / RED color bars on an LED string


*LED VIDEO CREATION SECTION*

This LED project handler was designed in a Windows environment and intended to be invoked through the led.bat batch file
For example, the command "led quarterwave -l 300" will execute the project defined in the .\quarterwave\main.py Python script, passing in the "-l 300"
command-line parameter

It creates a video file from the project that it executes and this video file is then used to generate an LED controller program

Any of the projects that have been built so far will serve as an excellent reference for building any new desired projects

Things will probably grow, but right now a project needs the following:
* One or more signal generator objects -- or a signal aggregator object
* An LED light string model object that defines how the incoming signal(s) is/are processed and computed for display

The signal generators built so far reside in the ./src/signalenerators.py module
The LED light string models build so far reside in the ./src/ledmodels.py module

The generators and the LED model would be instantiated and used in a project's main.py Python script.  The project handler is built to look for command-line
parameters and use those parameters to set the relevant settings.  For example:

* All projects so far expect an -l parameter to specify the length of the LED string being modeled
* The quarterwave project expects a -w (wavelength) parameter to specify the base sample wavelenghth for the sinusoid generators used by the project
* The morsecode project expects an -s (signal) parameter to specify the text file containing the message to be converted to Morse code
* The repeater project expects an -s (signal) parameter to specify the JSON file containing the data series to be run through the LED model
* The gauges project expects an -s (segnalset) parameter to specify the JSON file containing the definitions of the signals being aggregated and their signals

Various projects also have optional command-line parameters, use the -h parameter on a given model (e.g. "led quarterwave -h") to see its details

Depending on the type of LED model, it can either take a single signal, a sum of signals or a signal aggregator
* For a sum of signals, the outputs of multiple generators are added together into one value that goes into the defined model -- To use one or more signals in this way, the target LED model needs to be designed to use a single input signal instead of an aggregator
* For a signal aggregator, the multiple signals are "ganged" together in time, but otherwise kept separate, they are input into the defined model as a list of discrete values -- To use a signal aggregator, the target LED model needs to be designed to use an aggregator

In general, a project will follow the following steps:

1) Load the configuration and read the command-line parameters
2) Intantiate the desired signal generators and model
3) Run the signal (either an entire signal or a select number of samples) through the LED model, saving both:
    * The individual signal output value coming off of the LED string
    * A frame containing the value of every signal element within the LED string at that moment
4) Take the frames and create colorized versions based on the desired matplotlib.colors color map (or colorized manually, as can be seen in the various projects)
5) The individual signal outputs retained are saved in a JSON file as a time series
6) The full set of frames from the LED model are saved in a JSON file as a multi-dimensional time series
7) A time-based "waterfall" image of all the colorized frames is saved
8) A video is generated from all the colorized frames

The important output of a project is the video file.  It is used by the LEDEdit software to create the program for the LED light string.

The signal output time series and the waterfall image are technically unnecessary artifacts of the production process, but can be useful.  The time series can be
used again and fed into a "repeater" signal generator.  The waterfall image is a useful analysis tool to show each frame of the video at one time.

NOTE:  BY DEFAULT, THE LEDEdit SOFTWARE ENDS UP SWAPPING THE RED AND GREEN CHANNELS FROM THE GENERATED VIDEO, SO A CHANGE WAS MADE TO COLOR-DISTORT THE
VIDEO FILE SO THAT THE GENERATED PROGRAM FOR THE LED LIGHT STRING WILL HAVE THE CORRECT COLORS


I think that this is the end of how far I am going to go with systems that generate static video files.  The next step will be to try and take the models developed so far and use them with a Raspberry Pi controller for more responsive and reactive abilities.
