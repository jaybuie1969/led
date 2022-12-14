'''
This is the script that gets called when this project is called by the application's led.bat batch file
This also serves as an example project for how to set up any other projects
Command line call -- led quarterwave <<command line parameters>>
'''

from  matplotlib import pyplot as plt

import led.src.actions as actions

from configuration import Configuration
from led.src.ledmodels import QuarterWave
from led.src.signalgenerators import ConstantGenerator, SineWaveGenerator

default_time_series_file = "quarterwave_time_series.json"
default_image_file = "quarterwave_image.png"
default_video_file = "quarterwave_video.mp4"


def main():
	'''
	This is the meat of this python script
	'''

	configuration = Configuration(default_time_series_file=default_time_series_file, default_image_file=default_image_file, default_video_file=default_video_file, default_colormap="plasma")
	if (configuration.configured):
		# All required command-line parameters have been inspected and hav been found to be at least syntactically valid, attempt to run this project

		# Initialize the quarter-wave antenna model
		antenna = QuarterWave(configuration.length)

		sine_sources = []
		sine_sources.append(SineWaveGenerator(configuration.wavelength, configuration.amplitude, configuration.phase))
		#sine_sources.append(SineWaveGenerator(sine_sources[0].wavelength  / 2, None if (configuration.amplitude == None) else configuration.amplitude * 1.5, None if (configuration.phase is None) else configuration.phase + 1.57))
		#sine_sources.append(SineWaveGenerator(sine_sources[0].wavelength  / 4, None if (configuration.amplitude == None) else configuration.amplitude * 2, None if (configuration.phase is None) else configuration.phase + 3.14))
		#sine_sources.append(SineWaveGenerator(sine_sources[0].wavelength  / 8, None if (configuration.amplitude == None) else configuration.amplitude * 2.5, None if (configuration.phase is None) else configuration.phase - 1.57))

		# This source will be used to feed no signal into the antenna
		zero_source = ConstantGenerator()

		# Calculate the theoretical maximum amplitude for the current that can be running through the antenna
		current_amplitude = sum([sine_source.amplitude for sine_source in sine_sources])

		# Initialize pyplot in interactive mode and create an axis for the current flowing through the quarter-wave antenna
		# A pair of pyplot-based obects will be use to generate graphs while model is run
		plt.ion()
		figure = plt.figure()

		# Create an axis to display the current flowing through the antenna and initialize it with the antenna's initial current
		axis_current = figure.add_subplot(1, 1, 1)
		axis_current.set_ylim(-2.1 * current_amplitude, 2.1 * current_amplitude)
		line_current, = axis_current.plot(antenna.frame)

		'''
		# Do the following four times:
		# Feed one sine wave cycle into the antenna
		# Feed a zero signal in for one-fifth the length of the antenna
		for i in range(4):
			(time_series, frames) = actions.run_model(antenna, sine_sources[0], sine_sources[0].wavelength, figure, line_current)
			(time_series, frames) = actions.run_model(antenna, zero_source, antenna.length / 5, figure, line_current)
		'''

		'''
		# Run the set of sine wave generators through the antenna for the desired number of samples
		samples_to_run = int(8 * sine_sources[0].wavelength)
		(time_series, frames) = actions.run_model(antenna, sine_sources, samples_to_run, figure, line_current)
		'''

		samples_to_run = 2 * int(sine_sources[0].wavelength)
		(time_series, frames) = actions.run_model(antenna, sine_sources, samples_to_run, figure, line_current)

		# Run a zereo signal through the antenna for the amount of time it takes for any current on the antemma to propagate to ground
		samples_to_run = 2 * antenna.length
		(time_series, frames) = actions.run_model(antenna, zero_source, samples_to_run, figure, line_current, time_series, frames)

		# Create colorized versions of the data frames using the colormap in the configuration
		(rgb_frames, brg_frames) = actions.colorize_frames(frames, configuration.colormap, antenna.frame.shape)

		# Save the time-series version of the model's result to a file
		actions.save_time_series(time_series, configuration.time_series_file)

		# Save the data frames from the model's result to an image file as a "temporal contact sheet"
		image = actions.save_frames_image(rgb_frames, configuration.image_file)
		image.show()

		# Save the data frames from the model's result to a video file, with each frame of data representing a frame of video
		actions.save_frames_video(brg_frames, configuration.video_file, (brg_frames.shape[1], 2))


if (__name__ == "__main__"):
	# This Python script was invoked directly, call this script's main() method
	main()
