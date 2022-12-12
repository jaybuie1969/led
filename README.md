# led
Generate video configuration files for programmable LED systems

This LED project handler was designed in a Windows environment and intended to be invoked through the let.bat batch file

For example, the command "led quarterwave -l 300" will execute the project located in the .\quarterwave\main.py Python script, passing in the "-l 300"
command-line parameter

Any of the projects that have been built so far will serve as an excellent reference for building any new desired projects

Things will probably grow, but right now a project needs the following:
* One or more signal generator objects
* An LED light string model object that defines how the incoming signal(s) is/are processed and computed for display

The signal generators built so far reside in the ./src/signalenerators.py module
The LED light string models build so far reside in the ./src/ledmodels.py module

The generators and the LED model would be instantiated and used in a project's main.py Python script.  The project handler is built to look for command-line
parameters and use those parameters to set the relevant settings.  For example:

* All projects so far expect an -l parameter to specify the length of the LED string being modeled
* The quarterwave project expects a -w parameter to specify the base sample wavelenghth for the sinusoid generators used by the project
* The morsecode project expects a -s (signal) parameter to specify the text file containing the message to be converted to Morse code

In general, a project will follow the following steps:

1) Load the configuration and read the command-line parameters
2) Intantiate the desired signal generators and model
3) Run the signal (either an entire signal or a select number of samples) through the LED model, saving both:
    * The individual signal output value coming off of the LED string
    * A frame containing the value of every signal element within the LED string at that moment
4) Take the frames and create colorized versions based on the desired matplotlib.colors color map (or colorized manually, as can be seen in the morsecode project)
5) The individual signal outputs retained are saved in a JSON file as a time-series
6) A time-based "waterfall" image of all the colorized frames is saved
7) A video is generated from all the colorized frames

The important output of a project is the video file.  It is used by the LEDEdit software to create the program for the LED light string.

The signal output time series and the waterfall image are technically unnecessary artifacts of the production process, but can be useful.  The time series can be
used again and fed into a "repeater" signal generator.  The waterfall image is a useful analysis tool to show each frame of the video at one time.

