import inspect
import json

from os.path import exists
from pathlib import Path

import led.src.signalgenerators as generators

from led.src.baseclasses import SignalAggregator as __BaseAggregator__, SignalGenerator as __ParentGenerator__


class SimpleAggregator(__BaseAggregator__):
	'''
	This class represents a simple agregator that takes multiple signals, handling their incrementing and outputting their values as an organized list
	'''

	def __init__(self, signal_file:Path, project_folder:str=""):
		'''
		Parameters
		----------
		signal_file : subclass of pathlib.Path
			The file that is used to read in the set of signal generators and arguments for each signal to be handled by this aggregator
		project_folder : str
			The folder in which the project using this aggregator is located, used as the presumed location for signal files that do not include any path information
		'''

		self.generators = []

		if (signal_file == None):
			raise Exception("argument signal_file cannot be None")
		elif (not issubclass(signal_file.__class__, Path)):
			raise Exception(f"argument signal_file must be a parsed pathlib.Path child object, not an object of type {type(signal_file).__name__}")
		elif (not signal_file.is_file()):
			raise Exception(f"argument signal_file {signal_file} is not a path to a file")

		# Copy the signal file name to the object parameters and attempt to read its contents into self.signal_set
		self.signal_file = signal_file
		with open(self.signal_file) as file_in:
			self.signal_set = json.load(file_in)

		if (type(self.signal_set) != list):
			raise Exception(f"signal_file argument {self.signal_file} must contain a JSON-formatted list, not a JSON formatted {type(self.signal).__name__}")
		elif (len(self.signal_set) == 0):
			raise Exception(f"signal_file argument {self.signal_file} must contain at least one signal")

		# Make sure that project_folder is a valid string (even an empty string is valid)
		self.project_folder = str(project_folder) if (project_folder != None) else ""

		# If this method call has made it here without crashing, signal_file is syntactically valid, attempt to read each signal's details and initialize its generator

		exceptions = []
		for i, signal in enumerate(self.signal_set):
			signal_exceptions = []
			if (type(signal) != dict):
				signal_exceptions.append(f"signal #{i + 1} in {self.signal_file} must be a dictionary, not an object of type {type(signal).__name__}")
			else:
				# Signal is a dict object, make sure that it is syntactically valid
				if ("generator" not in signal):
					signal_exceptions.append(f'signal #{i + 1} in {self.signal_file} must must have a "generator" attribute that specifies a class in led.src.signalgenerators')
				elif (type(signal["generator"]) != str):
					signal_exceptions.append(f"generator attribute for signal #{i + 1} in {self.signal_file} must be a string that specifies a class in led.src.signalgenerators, not an object of type {type(signal['generator']).__name__}")
				elif (signal["generator"] == ""):
					signal_exceptions.append(f"generator attribute for signal #{i + 1} in {self.signal_file} must be a string that specifies a class in led.src.signalgenerators, it cannot be empty")
				elif (not hasattr(generators, signal["generator"])):
					signal_exceptions.append(f'generator attribute for signal #{i + 1} in {self.signal_file} must be a string that specifies a class in led.src.signalgenerators, "{signal["generator"]}" does not match any relevant classes')
				elif (not inspect.isclass(getattr(generators, signal["generator"]))):
					signal_exceptions.append(f'generator attribute for signal #{i + 1} in {self.signal_file} must be a string that specifies a class in led.src.signalgenerators, "{signal["generator"]}" is not a class in led.src.signalgenerators')

				if ("arguments" not in signal):
					signal_exceptions.append(f'signal #{i + 1} in {self.signal_file} must must have an "arguments" list attribute that specifies the initialization arguments for its associated signal generator')
				elif (type(signal["arguments"]) != list):
					signal_exceptions.append(f'arguments attribute in signal #{i + 1} in {self.signal_file} must be a list that specifies the initialization arguments for its associated signal generator')
				elif (signal["generator"] in ["MorseCodeGenerator", "SignalRepeater"]):
					# Signal generators of these classes require that their first argument be an object of subclass pathlib.Path, check to make sure

					if (signal["arguments"] == []):
						signal_exceptions.append(f"{signal['generator']} in signal #{i + 1} in {self.signal_file} must have a first argument that is the path to its data file")
					elif (type(signal["arguments"][0]) != str):
						signal_exceptions.append(f"{signal['generator']} in signal #{i + 1} in {self.signal_file} must have a first argument that is a string specifying its data file, not a value of type {type(signal['arguments'][0]).__name__}")
					elif (signal["arguments"][0] == ""):
						signal_exceptions.append(f"{signal['generator']} in signal #{i + 1} in {self.signal_file} must have a first argument that is a string specifying its data file, not an empty string")
					else:
						# This generator's first argument is syntactically valid, now check and see if it is an actual file path

						single_signal_file = signal["arguments"][0] if ((signal["arguments"][0].find("/") + signal["arguments"][0].find("\\")) >= 0) else f"{self.project_folder}/{signal['arguments'][0]}"
						if (not exists(single_signal_file)):
							self.errors.append(f"-s (--signalset/--messageset) argument {single_signal_file} is not a valid file path")
						else:
							single_signal_path = Path(single_signal_file)
							if (not single_signal_path.is_file()):
								self.errors.append(f"-s (--signalset/--messageset) argument {single_signal_file} is not a valid file path")
							else:
								signal["arguments"][0] = single_signal_path

			if (signal_exceptions != []):
				# At least one problem was found with this signal definition, add the eception(s) generated to exceptions
				exceptions.extend(signal_exceptions)

		if (exceptions != []):
			raise Exception("\n{}".format("\n".join(exceptions)))
		else:
			# No syntactic exceptions were found in the signal definitions, attempt to instantiate each generator, keep track of which ones are assumed to be finite
			# and initialize the set of current values
			self.generators = [getattr(generators, signal["generator"])(*signal["arguments"]) for signal in self.signal_set]

			self.finite_signals = []
			self.current_values = []
			for generator in self.generators:
				if (hasattr(generator, "end_of_signal")):
					self.finite_signals.append(generator)

				self.current_values.append(generator.current)
