##Handle getting the weather from yahoo!

import requests, json

def get_weather(location):
    baseurl = baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
    url = baseurl+"q="+yql_query+"&format=json"
    r = requests.get(url)
    raw = r.text
    json_file = json.loads(raw)
    return json_file

def get_daily_forecasts(json_file):
    print("Getting daily forecasts...")
    outputList = {}
    forecastData = json_file["query"]["results"]["channel"]["item"]["forecast"]
    for i in range(len(forecastData)):
        day = forecastData[i]
        outputList[i] = day["high"]+"/"+day["low"]+" | "+day["text"]
    return outputList

def get_current_temperature(json_file):
    print("Getting current temperature...")
    return json_file["query"]["results"]["channel"]["item"]["condition"]["temp"]

        

if __name__ == "__main__":
    json_data = get_weather("reno,nv")
