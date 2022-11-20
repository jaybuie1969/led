from math import pi, sin

class SineWaveGenerator:
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

	counter = 0
	current_value = None

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

	@property
	def current(self):
		'''
		This computed property is the current value of this sine wave generator
		If this object has not been started with a next() method call, it will return a None

		Returns
		-------
		float
			The current value of this sine wave generator
		'''
		return self.current_value

	@property
	def next(self):
		'''
		This computed property is the next value of this sine wave and saves the new value into the object's parameters


		Returns
		-------
		float
			The next value from this sine wave generator
		'''

		# Use the object's current sample counter to compute the next sine value
		self.current_value = self.amplitude * sin((2.0 * pi * self.counter / self.wavelength) + self.phase)

		# Increment counter for the next next() call
		self.counter = self.counter + 1

		return self.current_value
