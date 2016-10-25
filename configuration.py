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
            self.daycolors = config.get("display","daycolors").split(" ")
            self.nightcolors = config.get("display","nightcolors").split(" ")
            self.timeout = int(config.get("display","timeout"))
            self.email = config.get("email","address")
            self.password = config.get("email","password")
            self.imap = config.get("email","server")
            self.cutext = config.get("countup","text")
            self.cu2text = config.get("countup","text2")

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
    ##Being this module gets used a lot, make sure it runs quickly.
    import time
    start = time.time()
    for i in range(100):
        config = Config()
    end = time.time()
    print(end-start)
    
