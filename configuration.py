##Get the configuration file.

import configparser, os

class Config():
    def __init__(self, filename="./config.ini"):
        #If the file exists, run config parser.
        if os.path.isfile(filename):
            config = configparser.ConfigParser()
            config.read(filename)
            self.location = config["weather"]["location"]
            
