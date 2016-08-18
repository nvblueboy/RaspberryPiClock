##Handle logging data.

import configuration

import time

def log(message, timestamp=True):
    fileHandle = open("out.log","a")
    if timestamp:
        output = time.strftime("%m/%d/%Y %I:%M:%S %p: ") + message
    else:
        output = message
    print(output)
    fileHandle.write(output+"\n")
    fileHandle.close()
    
if __name__ == "__main__":
    start = time.time()
    for i in range(10):
        log(str(i))
    end = time.time()
    print(end-start)
    
