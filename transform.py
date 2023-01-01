import numpy as np

#import json

#from csv import reader

'''
signal = []
with open("bellecreek_hwy1416_alarm_pct.csv") as file_in:
	csv_reader = reader(file_in)
	header = next(csv_reader)
	if (header != None):
		signal = [float(row[2]) if (float(row[2]) <= 100.0) else 100.0 for row in csv_reader]

with open("./repeater/alarmlevel.json", "w") as file_out:
	json.dump(signal, file_out)
'''

#signal = [float(i) for i in range(101)]
#signal.extend(10 * [100])
#signal.extend([float(i) for i in range(100, -1, -1)])

#print(signal)
#with open("./repeater/ramp.json", "w") as file_out:
#	json.dump(signal, file_out)

signal = np.array(
	[
		[
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9],
		],
		[
			[11, 12, 13],
			[14, 15, 16],
			[17, 18, 19],
		],
		[
			[21, 22, 23],
			[24, 25, 26],
			[27, 28, 29],
		],
	],
	dtype=np.uint8
)

print(signal)
print(np.flip(signal, axis=2))
print(np.roll(signal, 1, axis=2))
