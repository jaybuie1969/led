from sys import path

# Before doing anything else, add this directory's parent directory to the path options for importing modules
path.append("..")

from argparse import ArgumentParser

from baseclasses import Configuration as __BaseConfiguration__

class Configuration(__BaseConfiguration__):
	'''
	This class defines a configuration object for modeling a quarter-wave single-pole antenna for a string of programmagle LED lights
	It builds upon and extends the superclass configuration object
	'''

	length = None
	wavelength = None

	def __init__(self, **kwargs):
		'''
		**kwargs : dict
			A set of named incoming parameters
		'''

		# First, call the superclass's initialization with the incoming named argument dict
		super(Configuration, self).__init__(**kwargs)

		if (self.configured):
			# The superclass's initialization did not produce any errors, re-set configured to False and begin looking for incoming parameters specific to this class
			self.configured = False

			self.argument_parser.add_argument("-l", "--length", type=int, required=True, help="Antenna length in pixels (int)")
			self.argument_parser.add_argument("-w", "--wavelength", "--wavelen", type=float, help="Sample wavelength for signal that goes into the antenna (float, allows for aperiodoc series)")

			# The parser arguments for this configuration object have been set up, now parse the command line and check for the base set of expected/available
			# arguments as defined by the superclass
			arguments = self.argument_parser.parse_args()
			super(Configuration, self).check_parsed_arguments(arguments)

			if (arguments.length <= 0):
				self.errors.append(f"The -l (--length) argument must be a positive integer, not {arguments.length}")
			else:
				self.length = arguments.length

			if (arguments.wavelength != None):
				if (arguments.wavelength < 1):
					self.errors.append(f"The -w (--wavelength) argument must be 1 or greater, not {arguments.wavelength}")
				else:
					self.wavelength = arguments.wavelength

			self.configured = len(self.errors) == 0

			if (not self.configured):
				print(f"ERROR - This LED project could not be configured.  The following error{'s' if (len(self.errors)) else ''} occurred:")
				print("\n".join(self.errors))
