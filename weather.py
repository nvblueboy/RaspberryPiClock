##Handle getting the weather from yahoo!

import requests, json

import logger

import time

def get_weather(location):
    baseurl = baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
    url = baseurl+"q="+yql_query+"&format=json"
    r = requests.get(url)
    raw = r.text
    json_file = json.loads(raw)
    return json_file

def get_daily_forecasts(json_file):
    logger.log("Getting daily forecasts...")
    outputList = {}
    forecastData = json_file["query"]["results"]["channel"]["item"]["forecast"]
    for i in range(len(forecastData)):
        day = forecastData[i]
        outputList[i] = day["high"]+"/"+day["low"]+" | "+day["text"]
    return outputList

def get_current_temperature(json_file):
    logger.log("Getting current temperature...")
    return json_file["query"]["results"]["channel"]["item"]["condition"]["temp"]

def get_sunrise_sunset(location):
    ##Get the weather, get the times.
    json_file = get_weather(location)
    astronomy = json_file["query"]["results"]["channel"]["astronomy"]
    strings = (astronomy["sunrise"],astronomy["sunset"])

    ##strptime has a habit of setting the date to the 1900s. Make a string to adjust.
    adjust = time.strftime("%d %m %Y")
    sunrise = time.strptime(adjust + " "+strings[0],"%d %m %Y %I:%M %p")
    sunset = time.strptime(adjust + " "+strings[1],"%d %m %Y %I:%M %p")
    
    return (sunrise, sunset)
        

if __name__ == "__main__":
    json_data = get_weather("reno,nv")
