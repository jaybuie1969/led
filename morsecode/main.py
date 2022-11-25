'''
This is the script that gets called when this project is called by the application's led.bat batch file
This also serves as an example project for how to set up any other projects
Command line call -- led morsecode <<command line parameters>>
'''

from  matplotlib import pyplot as plt

import led.src.actions as actions

from configuration import Configuration
from led.src.ledmodels import ScrollingWindow
from led.src.signalgenerators import ConstantGenerator, MorseCodeGenerator

default_time_series_file = "morsecode_time_series.json"
default_image_file = "morsecode_image.png"
default_video_file = "morsecode_video.mp4"


def main():
	'''
	This is the meat of this python script
	'''

	configuration = Configuration(default_time_series_file=default_time_series_file, default_image_file=default_image_file, default_video_file=default_video_file, default_colormap="hot")
	if (configuration.configured):
		# All required command-line parameters have been inspected and hav been found to be at least syntactically valid, attempt to run this project

		# Initialize the scrolling window model
		window = ScrollingWindow(configuration.length, configuration.direction, configuration.input_origin)

		# Initialize the Generator that will convert the text message to Morse code
		morse_source = MorseCodeGenerator(configuration.signal_file)
		print(morse_source.stream_length)

		# This source will be used to feed no signal into the scrolling window
		zero_source = ConstantGenerator()

		# Initialize pyplot in interactive mode and create an axis for the current flowing through the quarter-wave antenna
		# A pair of pyplot-based obects will be use to generate graphs while model is run
		plt.ion()
		figure = plt.figure()

		# Create an axis to display the current flowing through the antenna and initialize it with the antenna's initial current
		axis = figure.add_subplot(1, 1, 1)
		axis.set_ylim(-0.1, 1.1)
		line, = axis.plot(window.frame + 2)

		(time_series, frames) = actions.run_model(window, morse_source, None, figure, line)
		(time_series, frames) = actions.run_model(window, zero_source, window.length, figure, line, time_series, frames)

		# Create colorized versions of the data frames using the colormap in the configuration
		(rgb_frames, bgr_frames) = actions.colorize_frames(frames, configuration.colormap, window.frame.shape)

		# Save the time-series version of the model's result to a file
		actions.save_time_series(time_series, configuration.time_series_file)

		# Save the data frames from the model's result to an image file as a "temporal contact sheet"
		image = actions.save_frames_image(rgb_frames, configuration.image_file)
		#image.show()

		# Save the data frames from the model's result to a video file, with each frame of data representing a frame of video
		actions.save_frames_video(bgr_frames, configuration.video_file, (bgr_frames.shape[1], 2))


if (__name__ == "__main__"):
	# This Python script was invoked directly, call this script's main() method
	main()
