##Get a calendar's events and display the next 3 on the screen.

import configuration

from pytz import timezone

import requests, icalendar, pytz

import logger

from datetime import datetime, date

def getCalendar():
    logger.log("Getting calendar data...")
    outList = []
    ##Load the config file.
    config = configuration.Config()
    ##Get the current time UTC and convert it to the config's timezone, dropping the time.
    current_time = datetime.now(tz=pytz.utc).astimezone(timezone(config.timezone)).date()
    ##Retrieve the ical file specified in the config file.
    ical = config.ical
    r = requests.get(ical)
    text = r.text
    ##Parse that file and iterate over each component.
    cal = icalendar.Calendar.from_ical(text)
    for component in cal.walk():
        ##If the component is an event, add it to the list.
        if component.name == "VEVENT":
            dateTime = component.get("dtstart").dt
            ##If there is a time associated, adjust for timezones and drop the time.
            if type(dateTime) == datetime:
                dateTime = dateTime.astimezone(timezone(config.timezone)).date()
            ##If the event is later than the current date, add it to the list.
            if dateTime >= current_time:
                outList.append((dateTime, str(component.get("summary"))))
    ##Sort the list by date and return a list of strings.
    outList = sorted(outList, key=lambda x: x[0])
    strList = []
    for i in range(0, min([config.numEvents,len(outList)])):
        e = outList[i]
        strList.append(dateToString(e[0])+": "+e[1])
    return strList
        
def dateToString(d):
    ##Use str(int(x)) to get rid of leading zeroes.
    year = str(int(d.year))
    month = str(int(d.month))
    day = str(int(d.day))
    return month+"/"+day+"/"+year
    
if __name__ == "__main__":
    for i in getCalendar():
        print(i)
