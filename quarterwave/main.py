from sys import argv, path

# Before doing anything else, add this directory's parent directory to the path options for importing modules
path.append("..")

import cv2
import json
import numpy as np

from  matplotlib import colormaps, pyplot as plt
from PIL import Image
from time import sleep

from configuration import Configuration
from led_models import QuarterWave
from signal_generators import SineWaveGenerator


default_time_series_file = "quarterwave_time_series.json"
default_image_file = "quarterwave_image.png"
default_video_file = "quarterwave_video.mp4"


def main():
	'''
	This is the meat of this python script
	'''

	configuration = Configuration(default_time_series_file=default_time_series_file, default_image_file=default_image_file, default_video_file=default_video_file)
	if (configuration.configured):
		print("YES!  Configured!")

	exit(0)

	display_values = []
	frames = None

	argv_count = len(argv)
	if (argv_count < 2):
		print("Usage python main.py <antenna length>")
	else:
		# The expected argument is present, instantiate a quarter-wave antenna model
		antenna = QuarterWave(argv[1])

		# Instantiate a set of sine wave generators that will feed into this antenna
		sine_sources = [
			SineWaveGenerator(*argv[2 : ]),
			SineWaveGenerator((float(argv[2]) / 2) if (argv_count > 2) else None, (float(argv[3]) * 1.5) if (argv_count > 3) else None, *argv[4 : ]),
			SineWaveGenerator((float(argv[2]) / 4) if (argv_count > 2) else None, (float(argv[3]) * 2) if (argv_count > 3) else None, *argv[4 : ]),
			SineWaveGenerator((float(argv[2]) / 8) if (argv_count > 2) else None, (float(argv[3]) * 2.5) if (argv_count > 3) else None, *argv[4 : ]),
		]

		'''
			SineWaveGenerator(*argv[2 : ]),
			SineWaveGenerator((float(argv[2]) / 2) if (argv_count > 2) else None, (float(argv[3]) * 1.5) if (argv_count > 3) else None, *argv[4 : ]),
			SineWaveGenerator((float(argv[2]) / 4) if (argv_count > 2) else None, (float(argv[3]) * 2) if (argv_count > 3) else None, *argv[4 : ]),
			SineWaveGenerator((float(argv[2]) / 8) if (argv_count > 2) else None, (float(argv[3]) * 2.5) if (argv_count > 3) else None, *argv[4 : ]),
		'''

		# Set frames to be an empty numpy array with shape (0, <antenna length>)
		frames = np.empty((0, antenna.length))

		# Calculate the theoretical maximum amplitude for the current that can be running throuh the antenna
		current_amplitude = sum([sine_source.amplitude for sine_source in sine_sources])

		for sine_source in sine_sources:
			print(f"{sine_source.wavelength} | {sine_source.amplitude} | {sine_source.phase}")

		# Initialize pyplot in interactive mode and create an axis for the current flowing through the quarter-wave antenna
		plt.ion()
		figure = plt.figure()

		# Create an axis to display the current flowing through the antenna and initialize it with the antenna's initial current
		axis_current = figure.add_subplot(1, 1, 1)
		axis_current.set_ylim(-2.1 * current_amplitude, 2.1 * current_amplitude)
		line_current, = axis_current.plot(antenna.current)

		# Ierate over a set of sampling intervals, feed the next values from the sine wave generators into the antenna and retrieve the antenna's current into the plot line
		samples_to_run = int (8 * sine_sources[0].wavelength)
		#samples_to_run = 15
		for i in range(samples_to_run):
			antenna.input(sum([sine_source.next for sine_source in sine_sources]))

			line_current.set_ydata(antenna.current)

			display_values.append(float(antenna.current[0]))
			frames = np.append(frames, [antenna.current], axis=0)

			figure.canvas.draw()
			figure.canvas.flush_events()

		# Iterate over another set of sampling intervals equal to double the length of the antenna
		# Feed no current into the antenna and retrieve the antenna's current into the plot line
		# This number of samples was chosen because it gives all current in the antenna to travel down to the end and get reflected back to the beginning
		no_signal_samples = 2 * antenna.length
		#no_signal_samples = 15
		for i in range(no_signal_samples):
			antenna.input(None)
			line_current.set_ydata(antenna.current)

			display_values.append(float(antenna.current[0]))
			frames = np.append(frames, [antenna.current], axis=0)

			figure.canvas.draw()
			figure.canvas.flush_events()

	#print(display_values)
	if (len(display_values) > 0):
		# At least one display value was generated, save the display values out to a file so that they can be re-used as an input sequence
		with open("quarterwave_sequence.json", "w") as file_out:
			json.dump(display_values, file_out)

		'''
		All of the code below is involved in converting the timeline of values refrieved from the antenna's current values into a desired colormap
		It is being kept because it can make cool bar charts, but it isn't how we build our images or video
		# Shift display_values up so that no values in it are negative, and then normalize the list (i.e. scale it between zero and one)
		min_display_value = min(display_values)
		display_values = [display_value - min_display_value for display_value in display_values]

		max_display_value = max(display_values)
		if (max_display_value != 0):
			display_values = [display_value / max_display_value for display_value in display_values]

		x_labels = list(range(len(display_values)))
		axis_current.set_ylim((min(display_values) - 0.5), (max(display_values) + 0.5))
		axis_current.bar(x_labels, display_values, color=colormaps["plasma"](display_values))
		plt.show(block=True)

		# Convert display_values from numbers to colors according to a colormap
		display_values = [[int(256 * color_value) for color_value in colormaps["plasma"](display_value)[ : 3]] for display_value in display_values]
		'''

	#print(frames)
	if ((type(frames) == np.ndarray) and (len(frames.shape) >= 2) and (frames.shape[0] > 0) and (frames.shape[1] > 0)):
		# At least one frame of data was generated by this run, save the frames generated out to both images and a final video

		# Add a DC-bias to frames so that no value will be below zero
		frames = frames - np.amin(frames)

		# Assuming that the maximum values in frames is not zero, normalize the values in frames so that they are all between zero and one
		frames_max = np.amax(frames)
		if (frames_max > 0):
			frames = frames / frames_max

		# Initialize the color-mapped version of the data frames by applying a color map to the first frame, removing its alpha value (the A in RGBA)
		# and converting the remaining RGB values from floats between 0 and 1 to integers between 0 and 255
		# Then iterate over the rest of frames, perform the same color mapping and conversion on each one and append the result to mapped_frames
		mapped_frames = np.empty((0, antenna.length, 4))
		for i in range(0, frames.shape[0]):
			mapped_frames = np.append(mapped_frames, [colormaps["plasma"](frames[i])], axis=0)

		mapped_rgb_frames = np.array(255 * np.delete(mapped_frames, 3, 2)).astype(np.uint8)

		# The image serves as a two-dimensional "still" or "temporal contact sheet" of final video product, each line corresponds to a frame in the video
		img = Image.fromarray(mapped_rgb_frames)
		img.save("quarterwave_image.png")
		#img.show()

		# Convert the RGB-formatted version of the frames to BGR-formatted (Blue-Green-Red) by flipping the individual pixels RGB values
		mapped_bgr_frames = np.flip(mapped_rgb_frames, axis=2)

		# The OpenCV VideoWriter requires that the frame be at least two rows tall
		#out_video = cv2.VideoWriter("quarterwave_video.avi", cv2.VideoWriter_fourcc(*"DIVX"), 30, (mapped_bgr_frames.shape[1], 2))
		out_video = cv2.VideoWriter("quarterwave_video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (mapped_bgr_frames.shape[1], 2))
		for i in range(mapped_rgb_frames.shape[0]):
			out_video.write(np.array([mapped_bgr_frames[i], mapped_bgr_frames[i]]))

		out_video.release()


if (__name__ == "__main__"):
	# This Python script was invoked directly, call this script's main() method
	main()
