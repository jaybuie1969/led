'''
This module contains a CSV-based data fetcher that returns one data frame (i.e. CSV file line) at a time
As this project grows, other data fetchers may find a home in here
'''

class DataFetcher():
    def __init__(self, csv_file_name:str):
        '''
        Basic initialization method for DataFetcher-class objects

        Parameters
        ----------
        csv_file_name : str
            The path to the CSV file being used by this data fetcher
        '''

        # Save the file name and an opened file object as object attributes
        self.csv_file_name = csv_file_name
        self.csv_file = open(self.csv_file_name, "r")

    def fetch(self):
        '''
        This method fetches the next frame of data (i.e. line of the CSV file) and returns it as a list
        If the end of the source CSV file is determined to have been reached, the file is closed and further calls to this method will return
        nothing but None values
        '''

        return_list = None

        if (self.csv_file != None):
            # This object has an open CSV file, read the next line from it and try to convert the string of comma-separated values to a
            # Python list
            line = self.csv_file.readline()
            line_list = None

            if (line == ""):
                # The line returned is completely empty, assume that the end of the file has been reached
                # Close the file object and clear its attribute
                self.csv_file.close()
                self.csv_file = None
            else:
                # The line returned is not empty, remove all newlines and carriage returns at the end of it
                if (line[-1] == "\n"):
                    line = line[0 : -1]

                if (line[-1] == "\r"):
                    line = line[0 : -1]

                # Initialize the list to be returned to an empty list that will be built up in the next step
                return_list = []

                # Split the line into a list and iterate over that list to build the data frame to be returned
                line_list = line.split(",")
                for line_item in line_list:
                    if (line_item in ['', '""']):
                        # This data element is empty, add it to return_list as a None
                        return_list.append(None)
                    elif ((line_item[0] == '"') and (line_item[-1] == '"')):
                        # This data element is wrapped with double-quotes, strip them off before adding it to return_list
                        return_list.append(line_item[1 : -1])
                    elif ((line_item[0] == "'") and (line_item[-1] == '"')):
                        # This data element is wrapped with single-quotes, strip them off before adding it to return_list
                        return_list.append(line_item[1 : -1])
                    else:
                        # This data element is good as-is, add it to return_list without any modification
                        return_list.append(line_item)

        return return_list
