##Get the configuration file.

import configparser, os

class Config():
    def __init__(self, filename="./config.ini"):
        #If the file exists, run config parser.
        if os.path.isfile(filename):
            config = configparser.ConfigParser()
            config.read(filename)
            self.location = config.get("weather","location")
            self.ical = config.get("calendar","ical")
            self.numEvents = int(config.get("calendar","number"))
            self.timezone = config.get("calendar", "timezone")
            self.nytapi = config.get("news","key")
            self.nyttags = config.get("news","sections").split(" ")
            

def keyvals(dictionary):
    output = []
    for key in dictionary.keys():
        if type(dictionary[key]) == dict:
            output += keyvals(dictionary[key])
        elif type(dictionary[key]) == list:
            output += [keyvals(i) for i in dictionary[key]]
        else:
            output.append((key,dictionary[key]))
    return output


if __name__ == "__main__":
    config = Config()
    
