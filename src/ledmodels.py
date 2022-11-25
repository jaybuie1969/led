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
		This method takes in the amount of current coming in from the source signal generator(s) and adds it to the antenna model

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
		new_forward[1 : ] = self.current_forward[ : -1]
		self.current_forward = new_forward

		# Shift current_backward to the left and set the last element to the value retained from current_forward
		new_backward = np.empty_like(self.current_backward)
		new_backward[-1] = value_to_move
		new_backward[ : -1] = self.current_backward[1 : ]
		self.current_backward = new_backward


class ScrollingWindow(__BaseModel__):
	'''
	This class defines a model meant to display a window that scrolls across an incoming series of numbers
	ScrollingWindow objects can scroll either to the left (default), to the right or in both directions, spreading out from a specfied point (defaulting to the center)
	'''

	# This class definition uses an attribute named "frame", thus overriding the superclass's computed "frame" property and eliminating the need to
	# set a "frame_attribute" attribute
	frame = None

	length = None

	default_direction = "left"
	direction = None

	# The input_origin parameter is only used if the direction parameter is "both" and it indicates the point in frame where a new input value is inserted
	input_origin = None

	def __init__(self, length:int, direction:str=None, input_origin:int=None):
		'''
		Parameters
		----------
		length : int
			The length of this scrolling window model in terms of the number of LEDs in a straight line
			length must be a positive integer
		'''

		length = int(length)
		if (length <= 0):
			raise Exception(f"argument length must be a positive integer, {length} is invalid")
		else:
			# length is valid, now check the direction and input_origin inputs

			if (direction != None):
				if (type(direction) != str):
					raise Exception(f'if present, argument direction must be either the string "left", "right" or "both", not an object of type {type(direction).__name__}')
				elif (direction == ""):
					raise Exception('if present, argument direction must be either the string "left", "right" or "both"')
				else:
					direction = direction.lower()
					if (direction not in ["left", "right", "both"]):
						raise Exception(f'if present, argument direction must be either the string "left", "right" or "both"')
					else:
						if (direction == "both"):
							# Only care about the input_origin argument if it is relevant, i.e. this window should scroll in both directions
							if (input_origin != None):
								if (type(input_origin) not in [int, float]):
									raise Exception(f"if present and relevant, argument input_origin must be a number between zero and one less than the argument length ({length}), not an object of type {type(input_origin).__name__}")
								else:
									input_origin = int(input_origin)
									if (input_origin < 0):
										raise Exception(f"if present and relevant, argument input_origin must be a number between zero and one less than the argument length ({length}), not {input_origin}")
									elif (input_origin >= length):
										raise Exception(f"if present and relevant, argument input_origin must be a number between zero and one less than the argument length ({length}), not {input_origin}")

			# If this set of input check has made it here without raising an exception, everything was validated, save the parameters to the object

			self.length = length
			self.direction = direction if (direction != None) else self.default_direction

			# Only worry about setting self.input_origin if the window is supposed to scroll in both directions
			if (self.direction == "both"):
				if (input_origin != None):
					self.input_origin = input_origin
				else:
					# If no input_origin was included, then set input origin to the frame's halfway point
					self.input_origin = int(self.length / 2)

			self.frame = np.zeros(self.length, dtype=float)

	def input(self, value:float=None):
		'''
		This method takes in the lastest value from its input and places it in the desired location in self.frame, scrolling the rest of the frame to
		the left and/or right, depending on self.direction and self.input_origin

		Parameters
		----------
		value : float
			The amount of current flowing into this antenna
			value has no presumed unit right now, it is simply a floating-point number, if this model evolves to include resistance, that will probably change
		'''

		if (value != None):
			if (type(value) not in [int, float]):
				raise Exception(f"argument value must be a numeric value or None, not an object of type {type(value)}")
			else:
				value = float(value)
		else:
				value = 0.0

		# If this method call gets to this point, value is either None or a numeric value, handle it

		# Initialize the array for the new data frame that will be shifted depending on self.direction
		new_frame = np.empty_like(self.frame)

		if (self.direction == "left"):
			# Shift frame to the left, forgetting the first value shifted out and and then set the last element to value
			new_frame[ : -1] = self.frame[1 : ]
			new_frame[-1] = value
		elif (self.direction == "right"):
			# Shift frame to the right, forgetting the last value shifted out and then set the first element to value
			new_frame[1 : ] = self.frame[ : -1]
			new_frame[0] = value
		else:
			# This window scrolls in both directions
			# * Shift everything in self.frame to the left of self.input_origin to the left, forgetting the first value shifted out
			# * Shift everything in self.frame to the right of self.input_origin to the right, forgetting the last value shifted out
			# * Set self.frame[self.input_origin] to value
			new_frame[ : self.input_origin] = self.frame[1 : self.input_origin + 1]
			new_frame[self.input_origin + 1 : ] = self.frame[self.input_origin : -1]
			new_frame[self.input_origin] = value

		# The frame has been shifted, now save the new version to the object
		self.frame = new_frame


