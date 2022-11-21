from math import pi, sin

from led.src.baseclasses import SignalGenerator as __BaseGenerator__


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
