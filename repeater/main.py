'''
This is the script that gets called when this project is called by the application's led.bat batch file
This also serves as an example project for how to set up any other projects
Command line call -- led repeater <<command line parameters>>
'''

import numpy as np

from  matplotlib import pyplot as plt

import led.src.actions as actions

from configuration import Configuration
from led.src.ledmodels import ScrollingWindow
from led.src.signalgenerators import ConstantGenerator, SignalRepeater

default_time_series_file = "repeater_time_series.json"
default_frames_file = "repeater_frames.json"
default_image_file = "repeater_image.png"
default_video_file = "repeater_video.mp4"


def main():
	'''
	This is the meat of this python script
	'''

	configuration = Configuration(default_time_series_file=default_time_series_file, default_frames_file=default_frames_file, default_image_file=default_image_file, default_video_file=default_video_file, default_colormap="seismic")
	if (configuration.configured):
		# All required command-line parameters have been inspected and hav been found to be at least syntactically valid, attempt to run this project

		# Initialize the scrolling window model
		window = ScrollingWindow(configuration.length, configuration.direction, configuration.input_origin)

		# Initialize the Generator that will replay a previous signal
		repeater_source = SignalRepeater(configuration.signal_file, configuration.scaling_factor, configuration.logarithmic)

		# This source will be used to feed no signal into the scrolling window
		zero_source = ConstantGenerator()

		# Initialize pyplot in interactive mode and create an axis for the current flowing through the quarter-wave antenna
		# A pair of pyplot-based obects will be use to generate graphs while model is run
		plt.ion()
		figure = plt.figure()

		# Create an axis to display the current flowing through the antenna and initialize it with the antenna's initial current
		axis = figure.add_subplot(1, 1, 1)
		axis.set_ylim(repeater_source.signal_minimum - 0.1, repeater_source.signal_maximum + 0.1)
		line, = axis.plot(window.frame + 2)

		(time_series, frames) = actions.run_model(window, repeater_source, None, figure, line)
		(time_series, frames) = actions.run_model(window, zero_source, window.length, figure, line, time_series, frames)

		# Create colorized versions of the data frames using the colormap in the configuration
		#(rgb_frames, brg_frames) = actions.colorize_frames(frames, configuration.colormap, window.frame.shape)

		# Instead of using the colorize_frames method above, apply a linear red color filter to the frames
		rgb_frames = np.zeros((frames.shape[0], frames.shape[1], 3), dtype=np.uint8)
		brg_frames = np.zeros((frames.shape[0], frames.shape[1], 3), dtype=np.uint8)
		for i in range(frames.shape[0]):
			rgb_frames[i] = np.c_[(255 * np.ones(frames[i].shape)).astype(np.uint8), (255 - (255 * frames[i] / 100).astype(np.uint8)).astype(np.uint8), (255 - (255 * frames[i] / 100).astype(np.uint8)).astype(np.uint8)]
			brg_frames[i] = np.c_[(255 - (255 * frames[i] / 100).astype(np.uint8)).astype(np.uint8), (255 * np.ones(frames[i].shape)).astype(np.uint8), (255 - (255 * frames[i] / 100).astype(np.uint8)).astype(np.uint8)]

		# Save the time-series version of the model's result to a file
		actions.save_time_series(time_series, configuration.time_series_file)

		# Save the data frames from the model's result to an image file as a "temporal contact sheet"
		image = actions.save_frames_image(rgb_frames, configuration.image_file)
		image.show()

		# Save the data frames from the model's result to a video file, with each frame of data representing a frame of video
		actions.save_frames_video(brg_frames, configuration.video_file, (brg_frames.shape[1], 2))
		'''
		'''


if (__name__ == "__main__"):
	# This Python script was invoked directly, call this script's main() method
	main()
