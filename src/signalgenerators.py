import json
from math import log, pi, sin
from pathlib import Path

import json

from led.src.baseclasses import SignalGenerator as __BaseGenerator__


# Define a dit/dot as a single one with a trailing zero for spacing
dit = [1, 0]

# Define a dah/dash as three ones with a trailing zero for spacing
dah = [1, 1, 1, 0]

space = [0, 0, 0, 0, 0, 0]

# Map each character to a list of dits and dahs
morse_map = {
	"a": [dit, dah],
	"b": [dah, dit, dit, dit],
	"c": [dah, dit, dah, dit],
	"d": [dah, dit, dit],
	"e": [dit],
	"f": [dit, dit, dah, dit],
	"g": [dah, dah, dit],
	"h": [dit, dit, dit, dit],
	"i": [dit, dit],
	"j": [dit, dah, dah, dah],
	"k": [dah, dit, dah],
	"l": [dit, dah, dit, dit],
	"m": [dah, dah],
	"n": [dah, dit],
	"o": [dah, dah, dah],
	"p": [dit, dah, dah, dit],
	"q": [dah, dah, dit, dah],
	"r": [dit, dah, dit],
	"s": [dit, dit, dit],
	"t": [dah],
	"u": [dit, dit, dah],
	"v": [dit, dit, dit, dah],
	"w": [dit, dah, dah],
	"x": [dah, dit, dit, dah],
	"y": [dah, dit, dah, dah],
	"z": [dah, dah, dit, dit],
	"1": [dit, dah, dah, dah, dah],
	"2": [dit, dit, dah, dah, dah],
	"3": [dit, dit, dit, dah, dah],
	"4": [dit, dit, dit, dit, dah],
	"5": [dit, dit, dit, dit, dit],
	"6": [dah, dit, dit, dit, dit],
	"7": [dah, dah, dit, dit, dit],
	"8": [dah, dah, dah, dit, dit],
	"9": [dah, dah, dah, dah, dit],
	"0": [dah, dah, dah, dah, dah],
	",": [dah, dah, dit, dit, dah, dah],
	".": [dit, dah, dit, dah, dit, dah],
	"?": [dit, dit, dah, dah, dit, dit],
	"!": [dah, dit, dah, dit, dah, dah],
	" ": [space],
}



def convert_to_morse(signal:str):
	'''
	Parameters
	----------
	signal : str
		The string of text to be converted to Morse code

	Returns
	-------
	List[List[int]]
		A list of Morse code characters encoded as lists of zeros and ones
	'''
	return [morse_map[i] for i in signal if (i in morse_map)] if (type(signal) == str) else []


class SineWaveGenerator(__BaseGenerator__):
	'''
	This class defines a signal source that generates a digital sine wave
	By default, objects defined with this class will have a wavelength of 10 samples
	'''

	default_wavelength = 10.0
	wavelength = None

	default_amplitude = 1.0
	amplitude = None

	default_phase = 0.0
	phase = None

	def __init__(self, wavelength:float=None, amplitude:float=None, phase:float=None):
		'''
		Parameters
		----------
			wavelength : float
				The number of samples per wave for this sine wave, it can be a float to generate sequences that are technically aperiodic,
				wavelength must be a positive value
			amplitude : float
				The amplitude of this wave, the generated values range between +amplitude and -amplitude
			phase : float
				The phase shift for this sine wave, in radians
		'''

		if (wavelength == None):
			self.wavelength = self.default_wavelength
		else:
			wavelength = float(wavelength)
			if (wavelength <= 0):
				raise Exception(f"argument wavelength must be a positive value, {wavelength} is invalid")
			else:
				self.wavelength = wavelength

		if (amplitude == None):
			self.amplitude = self.default_amplitude
		else:
			self.amplitude = float(amplitude)


		if (phase == None):
			self.phase = self.default_phase
		else:
			self.phase = float(phase)

	def compute_next_value(self):
		'''
		This method overrides the same method from the superclass and actually does some work
		Specifically, it computes the next value to be emitted by this sine wavegenerator

		Returns
		-------
		float
			The next value from this sine wave generator
		'''

		self.current_value = self.amplitude * sin((2.0 * pi * self.counter / self.wavelength) + self.phase)


class ConstantGenerator(__BaseGenerator__):
	'''
	This class defines a "signal" source that simply generates a single constant value
	By default, this class will return a zero
	'''

	default_value = 0.0

	def __init__(self, value:float=None):
		'''
		Parameters
		----------
		value : float
			The constant value that will always be returned by this "signal" generator (defaults to zero)
		'''

		self.current_value = float(value) if ((value != None) and (type(value) in [int, float])) else self.default_value


class MorseCodeGenerator(__BaseGenerator__):
	'''
	This class defines a Morse code source that generates dits/dots and dahs/dashes from signal message in a text file
	'''

	signal_file = None

	signal = None
	morse = []
	bitstream = []

	stream_length = 0
	end_of_signal = False

	def __init__(self, signal_file:any):
		'''
		Parameters
		----------
		signal_file : any pathlib.Path child class
			The parsed path to the input signal text file that will be converted to Morse code
		'''

		if (signal_file == None):
			raise Exception("argument signal_file cannot be None")
		elif (not issubclass(signal_file.__class__, Path)):
			raise Exception(f"argument signal_file must be a parsed pathlib.Path child object, not an object of type {type(signal_file).__name__}")
		elif (not signal_file.is_file()):
			raise Exception(f"argument signal_file {signal_file} is not a path to a file")

		# If this method call has made it here without crashing, things are good so far, now attempt to read in the signal file and convert it to Morse code
		# Newlines in the signal are replaced with spaces, and leading and trailing whitespace is trimmed
		# Since Morse code is case-insensitive, the signal is all converted to lower case

		self.signal_file = signal_file
		with open(self.signal_file) as file_in:
			self.signal = str(file_in.read()).replace("\n", " ").strip().lower()

		self.morse = convert_to_morse(self.signal)
		delta = abs(len(self.signal) - len(self.morse))
		if (delta > 0):
			raise Exception(f"argument signal_file {signal_file} contains {delta} character{'s' if (delta != 1) else ''} that could not be mapped to Morse code")

		# If this method call has made it here without crashing, the signal file has been read in, converted to Morse code and no mapped characters were encountered

		# When building the bitstream, append some zeros to each character for spacing
		self.bitstream = []
		for morse_character in self.morse:
			character_bits = [bit for didah in morse_character for bit in didah]
			character_bits.extend([0, 0, 0])
			self.bitstream.extend(character_bits)

		# Since the length of the stream is used a lot, compute and retain it
		self.stream_length = len(self.bitstream)

	def compute_next_value(self):
		'''
		This method overrides the same method from the superclass and actually does some work
		Specifically, it selects the next bit to be emitted by this Morse code generator

		Returns
		-------
		int
			The next bit from this Morse code generator
		'''

		# Before selecting the current value, make sure that this generator's counter is not beyond the length of the bitstream
		if (self.counter >= self.stream_length):
			self.end_of_signal = True

		if ((not self.end_of_signal) and (self.counter < self.stream_length)):
			self.current_value = self.bitstream[self.counter]
		else:
			self.current_value = None


class SignalRepeater(__BaseGenerator__):
	'''
	This class defines a "generator" that repeats a signal from a JSON-formatted list file
	The repeated signal can optionally be scaled up or down in magnitude
	'''

	signal_file = None
	scaling_factor = 1.0
	logarithmic = False

	signal = None
	signal_length = 0
	signal_minimum = 0
	signal_maximum = 0
	end_of_signal = False

	def __init__(self, signal_file:any, scaling_factor:float=None, logarithmic:bool=None):
		'''
		Parameters
		----------
		signal_file : any pathlib.Path child class
			The parsed path to the input signal JSON-formatted list that will be repeated by this "generator"
		scaling_factor : float
			The amount by which the repeated signal will be scaled, will default to one if not present
		logarithmic : bool
			Optional flag indicating whether this signal should be converted to a common logarithm of its current value, will default to False if not present
		'''

		if (signal_file == None):
			raise Exception("argument signal_file cannot be None")
		elif (not issubclass(signal_file.__class__, Path)):
			raise Exception(f"argument signal_file must be a parsed pathlib.Path child object, not an object of type {type(signal_file).__name__}")
		elif (not signal_file.is_file()):
			raise Exception(f"argument signal_file {signal_file} is not a path to a file")

		if (scaling_factor != None):
			if (type(scaling_factor) not in [int, float]):
				raise Exception(f"if present, argument scaling_factor must be a number, not an object of type {type(scaling_factor).__name__}")
			else:
				scaling_factor = float(scaling_factor)
				if (scaling_factor == 0.0):
					# Allow a scaling_factof of zero, but alert the user
					print("WARNING - A scaling_factor of zero will return nothing but zeros from this signal repeater")

		if (logarithmic != None):
			# If logarithmic is not None, don't worry about the type, try and see if it can be resolved to a Boolean, raising an error if it cannot
			try:
				self.logarithmic = bool(logarithmic)
			except:
				raise Exception(f"If present, logarithmic must be able to resolve to a True or False, {logarithmic} does not")

		# If this method call has made it here without crashing, things are good so far, now attempt to read in the signal file

		# Copy the initialization arguments to the object's parameters
		self.signal_file = signal_file
		if (scaling_factor != None):
			self.scaling_factor = scaling_factor

		# Attempt to read in the JSON-formatted object from signal_file and raise an Exception if it doesn't contain a list
		with open(self.signal_file) as file_in:
			self.signal = json.load(file_in)

		if (type(self.signal) != list):
			raise Exception(f"signal_file argument {self.signal_file} must contain a JSON-formatted list, not a JSON formatted {type(self.signal).__name__}")

		# If this method call has made it here without crashing, signal_file is syntactically valid, finish up initialization efforts

		if (self.scaling_factor != 1.0):
			# The incoming signal is being scaled and/or converted to a logarithm
			self.signal = [self.scaling_factor * i for i in self.signal]

		# Since the length of the signal is used in other calculations, compute and retain it
		self.signal_length = len(self.signal)

		if (self.signal_length > 0):
			# Signal minimum and maximum are useful for setting y-range parameters when graphing a signal, compute them
			self.signal_minimum = min(self.signal)
			self.signal_maximum = max(self.signal)

			if (self.logarithmic):
				# This series is supposed to be presented logarithmically, logarithms do not like numbers less than or equal to zero
				# So if necessary, this series will be shifted up so that its minimum value is 1 (because the common log of one is zero)

				if (self.signal_minimum <= 0):
					self.signal = [log(i + 1 - self.signal_minimum) for i in self.signal]
				else:
					self.signal = [log(i, 10) for i in self.signal]

				# Re-compute the minimum and maximum now that the signal has been logarithmed
				self.signal_minimum = min(self.signal)
				self.signal_maximum = max(self.signal)

	def compute_next_value(self):
		'''
		This method overrides the same method from the superclass and actually does some work
		Specifically, it selects the next bit to be emitted by this signal repeater

		Returns
		-------
		float
			The next value from the signal being repeated
		'''

		# Before selecting the current value, make sure that this "generator"'s counter is not beyond the length of the signal
		if (self.counter >= self.signal_length):
			self.end_of_signal = True

		if ((not self.end_of_signal) and (self.counter < self.signal_length)):
			self.current_value = self.signal[self.counter]
		else:
			self.current_value = None

