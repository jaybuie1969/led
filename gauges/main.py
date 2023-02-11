'''
This is the script that gets called when this project is called by the application's led.bat batch file
This also serves as an example project for how to set up any other projects
Command line call -- led repeater <<command line parameters>>
'''

import numpy as np

from math import pi
from  matplotlib import pyplot as plt

import led.src.actions as actions

from configuration import Configuration
from led.src.ledmodels import Gauges
from led.src.signalaggregators import SimpleAggregator
from led.src.signalgenerators import ConstantGenerator, SineWaveGenerator

default_time_series_file = "gauge_time_series.json"
default_frames_file = "gauge_frames.json"
default_image_file = "gauge_image.png"
default_video_file = "gauge_video.mp4"


def main():
	'''
	This is the meat of this python script
	'''

	configuration = Configuration(default_time_series_file=default_time_series_file, default_frames_file=default_frames_file, default_image_file=default_image_file, default_video_file=default_video_file, default_colormap="seismic")
	if (configuration.configured):
		# All required command-line parameters have been inspected and hav been found to be at least syntactically valid, attempt to run this project

		# Initialize a simple signal aggregator that will be used to produce the signals that will be displayed by the gauges
		aggregator = SimpleAggregator(configuration.signal_file, configuration.project_folder)

		# Initialize the gauges window model
		gauges = Gauges(configuration.length, len(aggregator.generators))

		# Initialize pyplot in interactive mode and create an axis for the current flowing through the quarter-wave antenna
		# A pair of pyplot-based obects will be use to generate graphs while model is run
		plt.ion()
		figure = plt.figure()

		# Create an axis to display the current flowing through the antenna and initialize it with the antenna's initial current
		axis = figure.add_subplot(1, 1, 1)
		axis.set_ylim(-2.1, 105.0)
		line, = axis.plot(gauges.frame + 2)

		(time_series, frames) = actions.run_model(gauges, aggregator, None, figure, line)

		# Create colorized versions of the data frames using the colormap in the configuration
		#(rgb_frames, brg_frames) = actions.colorize_frames(frames, configuration.colormap, window.frame.shape)

		# Instead of using the colorize_frames method above, apply a specialized color filter to each frame

		# First, initialize the color-related frames to be all zeros before iterating through the frames of data
		rgb_frames = np.zeros((frames.shape[0], frames.shape[1], 3), dtype=np.uint8)
		brg_frames = np.zeros((frames.shape[0], frames.shape[1], 3), dtype=np.uint8)

		for i in range(frames.shape[0]):
			for location in gauges.gauge_locations:
				if (frames[i][location[0]] == None):
					# This gauge is not returing any data, color this section black
					rgb_frames[i][location[0] : location[1] + 1] = [0, 0, 0]
					brg_frames[i][location[0] : location[1] + 1] = [0, 0, 0]
				elif (frames[i][location[0]] <= 2):
					# This gauge is very low (2 or lower), color this section green
					rgb_frames[i][location[0] : location[1] + 1] = [0, 255, 0]
					brg_frames[i][location[0] : location[1] + 1] = [0, 0, 255]
				elif (frames[i][location[0]] <= 50):
					# This gauge is high enough to be worth paying attention to (between 2 and 50), color this section a progressively brighter yellow based on its value
					color_code = int(205 + (((frames[i][location[0]] - 2) / 48) * 50)) % 256
					rgb_frames[i][location[0] : location[1] + 1] = [color_code, color_code , 0]
					brg_frames[i][location[0] : location[1] + 1] = [0, color_code, color_code]
				elif (frames[i][location[0]] <= 90):
					# This gauge is high enough to pay closer attention to (between 50 and 90), color this section a progressively brighter orange based on its value
					red_code = int(205 + (((frames[i][location[0]] - 50) / 40) * 50)) % 256
					green_code = int(120 + (((frames[i][location[0]] - 50) / 40) * 45)) % 256
					rgb_frames[i][location[0] : location[1] + 1] = [red_code, green_code, 0]
					brg_frames[i][location[0] : location[1] + 1] = [0, red_code, green_code]
				else:
					# This gauge needs to be giving a warning (greater than 90), color this section a progressively brighter red based on its value
					red_code = int(205 + (((min(frames[i][location[0]], 100) - 90) / 10) * 50)) % 256
					rgb_frames[i][location[0] : location[1] + 1] = [red_code, 0, 0]
					brg_frames[i][location[0] : location[1] + 1] = [0, red_code, 0]

		# Save the time-series version of the model's result to a file
		actions.save_time_series(time_series, configuration.time_series_file)

		# Save the frames version of the model's result to a file
		actions.save_frames(frames, configuration.frames_file)

		# Save the data frames from the model's result to an image file as a "temporal contact sheet"
		image = actions.save_frames_image(rgb_frames, configuration.image_file)
		image.show()

		# Save the data frames from the model's result to a video file, with each frame of data representing a frame of video
		actions.save_frames_video(brg_frames, configuration.video_file, (brg_frames.shape[1], 2))


if (__name__ == "__main__"):
	# This Python script was invoked directly, call this script's main() method
	main()
