from argparse import ArgumentParser, Namespace

class Configuration:
	'''
	THIS CLASS IS NOT INTENDED TO BE INSTANTIATED DIRECTLY
	This class definition is intended to be used as a parent class for a particular LED project's configuration
	This class defines the minimal configuration object for a run of a script within this application
	It takes in a set of defaults and defines an initial set of command-line arguments for parsing
	'''

	time_series_file = None
	image_file = None
	video_file = None

	argument_parser = ArgumentParser()
	configured = False
	errors = []

	def __init__(self, **kwargs):
		'''
		As this initialiation method executes, it attempts to set an expected group object-level parameters
		Any error messages accumulated during this initialization
		IN THE CHILD CLASS, THIS METHOD SHOULD BE OVER-RIDDEN AND THEN EXPLICITLY CALLED BEFORE DOING ANYTHING ELSE

		**kwargs : dict
			A set of named incoming parameters
		'''

		required_kwargs = [
			{
				"name": "default_time_series_file",
				"attribute": "time_series_file",
				"type": str,
			},
			{
				"name": "default_image_file",
				"attribute": "image_file",
				"type": str,
			},
			{
				"name": "default_video_file",
				"attribute": "video_file",
				"type": str,
			},
		]

		for kwarg in required_kwargs:
			if (kwarg["name"] not in kwargs):
				self.errors.append(f"Configuration object requires named argument {kwarg['name']} of type {kwarg['type'].__name__}")
			elif (kwargs[kwarg["name"]] == None):
				self.errors.append(f"The {kwarg['name']} named argument must be a non-empty string, not None")
			elif (type(kwargs[kwarg["name"]]) != kwarg["type"]):
				self.errors.append(f"The {kwarg['name']} named argument must be of type {kwarg['type'].__name__}, not of type {type(kwargs[kwarg['name']]).__name__}")
			elif ((kwarg['type'] == str) and (kwargs[kwarg["name"]] == "") and (("can_be_empty" not in kwarg) or (not bool(kwarg["can_be_empty"])))):
				self.errors.append(f"The {kwarg['name']} named argument must be a non-empty string")
			else:
				# This named argument is syntactically valid, save it as an object parameter
				setattr(self, kwarg["attribute"], kwargs[kwarg["name"]])

		if (len(self.errors) == 0):
			# No errors have been generated so far, now check any incoming command-line parameters to potentially replace the parameters that came in as named arguments
			self.argument_parser.add_argument("-t", "--time_series", "--time-series", "--timeseries", type=str, help=f"Optional destination file name for generated time-series data (replaces {self.time_series_file})")
			self.argument_parser.add_argument("-i", "--image", type=str, help=f"Optional destination file name for generated image (replaces {self.image_file})")
			self.argument_parser.add_argument("-v", "--video", type=str, help=f"Optional destination file name for generated video (replaces {self.video_file})")


		# If there are no error messages, this base confiuration ojbect is configured successfully
		self.configured = len(self.errors) == 0

	def check_parsed_arguments(self, arguments:Namespace):
		'''
		This method handles looking for the base set of command-line parameters permitted or required by this base configuration object
		IN THE CHILD CLASS, THIS METHOD SHOULD BE CALLED AS SOON AS self.argument_parser IS FULLY SET UP

		Parameters
		----------
			arguments : argparser.Namespace
				The set of command-line arguments retrieved by the argument parser
		'''

		if (type(arguments) == Namespace):
			if (arguments.time_series != None):
				self.time_series_file = arguments.time_series

			if (arguments.image != None):
				self.image_file = arguments.image

			if (arguments.video != None):
				self.video_file = arguments.video
