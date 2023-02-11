'''
This module will contain functions or classes that are particularly relevant to Flowstate activities
'''

def map_alarm_count_to_rgb(alarm_count):
    '''
    This function takes in a percentage value and maps it to an RGB code depending on its value

    Parameters
    ----------
    alarm_count : float
        a number between 0 and 100 that will be mapped to an RGB color code

    Returns
    -------
    list[int, int, int]
        an RGB code combination in the form of a list of three integers, all between 0 and 255
    '''

    return_list = [0, 0, 0]

    # Do some checking and make sure that alarm_count is either a float, an int or a None

    if (type(alarm_count) == str):
        try:
            alarm_count = float(alarm_count)
        except:
            alarm_count = None

    if ((alarm_count != None) and (type(alarm_count) not in [int, float])):
        alarm_count = None

    if (alarm_count != None):
        # alarm_count is a number, convert it to an RGB code

        if (alarm_count <= 2):
            # For an alarm_count of 2 or below, return green
            return_list = [0, 255, 0]
        elif (alarm_count <= 50):
            # For an alarm_count between 2 and 50, return a progressively brighter yellow as alarm_count increases
            red_green = (205 + int(((alarm_count - 2) / 48) * 50)) % 256
            return_list = [red_green, red_green, 0]
        elif (alarm_count <= 90):
            # For an alarm_count between 50 and 90, return a progressively brighter orange as alarm_count increases
            return_list = [(205 + int(((alarm_count - 50) / 40) * 50)) % 256, (120 + int(((alarm_count - 50) / 40) * 45)) % 256, 0]
        else:
            # For an alarm count above 90, return a progressively brighter red as alarm_count increases
            return_list = [(205 + int(((min(alarm_count, 100) - 90) / 10) * 50)) % 256, 0, 0]

    return return_list

