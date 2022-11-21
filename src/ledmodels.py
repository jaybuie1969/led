import numpy as np

from led.src.baseclasses import LEDModel as __BaseModel__


class QuarterWave(__BaseModel__):
	'''
	This class defines a model meant to emulate current flowing in a quarter-wave antenna
	For this project, a quarter-wave antenna is intended be modeled by a straight line of programmable LEDs
	This definition models an instantaneous snapshot of current flowing through a monopole antenna made of a metal with no electrical resitance
	'''

	# Set the name of that attribute that will hold a frame of data for this model
	# In this case, it is intended to be the total current flowing through the antenna at the given moment
	frame_attribute = "current"

	length = None
	current_forward = None
	current_backward = None

	def __init__(self, length:int):
		'''
		Parameters
		----------
		length : int
			The length of this "quarter-wave antenna" model in terms of the number of LEDs in a straight line
			length must be a positive integer
		'''
		length = int(length)
		if (length <= 0):
			raise Exception(f"argument length must be a positive integer, {length} is invalid")
		else:
			# length is valid, save it and initialize empty current lists
			self.length = length
			self.current_forward = np.zeros(self.length, dtype=float)
			self.current_backward = np.zeros(self.length, dtype=float)

	@property
	def current(self):
		'''
		This computed property is the total current flowing through this antenna at the moment
		It is composed of the difference between the current moving forward and the current moving backward
		'''
		return self.current_forward - self.current_backward

	def input(self, value:float=None):
		'''
		This method takes in the about of current coming in from the source signal generator(s) and adds it to the antenna model

		Parameters
		----------
		value : float
			The amount of current flowing into this antenna
			value has no presumed unit right now, it is simply a floating-point number, if this model evolves to include resistance, that will probably change
		'''

		if (value != None):
			if (type(value) not in [int, float]):
				raise Exception(f"argument value must be a numeric value or None, not an object of type {type(value)}")

		# If this method call gets to this point, value is either None or a numeric value, handle it

		# Shift current_forward to the right, retain the value shifted out and set the first element to value
		value_to_move = self.current_forward[-1]
		new_forward = np.empty_like(self.current_forward)
		new_forward[0] = value if (value != None) else 0
		new_forward[1 :] = self.current_forward[ : -1]
		self.current_forward = new_forward

		# Shift current_backward to the left and set the last element to the value retained from current_forward
		new_backward = np.empty_like(self.current_backward)
		new_backward[-1] = value_to_move
		new_backward[ : -1] = self.current_backward[1 : ]
		self.current_backward = new_backward

