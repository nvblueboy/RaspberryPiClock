##Get the top headlines in specified sections from the New York Times.

import configuration

import requests, json


def getTopHeadline(category, config):
    print("Getting news for "+category)
    #Get the API Key from the config file and create the URL with the category and key.
    apikey = config.nytapi
    url = "https://api.nytimes.com/svc/topstories/v2/"+category+".json?api-key="+apikey
    #use requests to get and parse the JSON data.
    r = requests.get(url)
    json_raw = r.text
    try:
        json_data = json.loads(json_raw)
    except:
        print("Something went wrong. \n\n\n"+json_raw)
    ##Return the top headline.
    return json_data["results"][0]["title"]
    

    
def getNews():
    headlines = []
    config = configuration.Config()
    for category in config.nyttags:
        headlines.append(capitalize(category)+":  "+getTopHeadline(category,config))
    return headlines
    
def capitalize(string):
    return string[0].upper()+string[1:]

if __name__ == "__main__":
    config = configuration.Config()
    for i in getNews():
        print(i)
