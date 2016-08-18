## Handle the clock itself.

import time

from window import *
import weather
import calendarLib
import configuration
import news
import logger


class Clock():

    modes = ["clock","forecast","calendar","news"]

    def __init__(self):
        ##Pull in the configuration file.
        self.config = configuration.Config()


        ##Initialize the window, setting the resolution to 800x600, and create the labels.
        self.win = Window()
        self.win.root.geometry("800x480")

        ##Set the touch screen/left click to switch modes.
        self.win.root.bind("<Button-1>",self.switchMode)

        logger.log("Creating slides....")
        ##Create the frames and their respective widgets.
        self.createMainFrame()
        self.createForecastFrame()
        self.createCalendarFrame()
        self.createNewsFrame()

        logger.log("Filling frames...")
        ##Update all information and strings.
        self.updateCalendar()
        self.updateWeather()
        self.updateNews()

        self.mode = 0
        self.mainFrame.tkraise()

        ##Register the screen's update system.
        self.win.root.after(100,self.updateSelf)
        logger.log("Ready to go!")
        return

    def switchMode(self, *args):

        ##Todo: Make switching work.
        self.mode += 1
        if self.mode == len(self.modes):
            self.mode = 0
        current_mode = self.modes[self.mode]
        if current_mode == "clock":
            logger.log("Switching to Clock")
            self.mainFrame.tkraise()
        if current_mode == "forecast":
            logger.log("Switching to Forecast")
            self.forecastFrame.tkraise()
        if current_mode == "calendar":
            logger.log("Switching to Calendar")
            self.calendarFrame.tkraise()
        if current_mode == "news":
            logger.log("Switching to News")
            self.newsFrame.tkraise()

    def createMainFrame(self):
        self.mainFrame = Frame(self.win.root, bg = "black", width=800, height = 480, cursor="none")
        self.mainFrame.place(relx=.5,rely=.5, anchor=CENTER,relheight=1, relwidth=1)
        ##Set the variable to hold the time string and the label to show it.
        self.timeStr = StringVar()
        self.timeLabel = Label(self.mainFrame, textvariable=self.timeStr,
                               font=("Helvetica", 100, "bold"), fg = "white", bg = "black")
        self.timeLabel.place(relx=.5, rely=.25, anchor=CENTER)

        ##Set the variable to hold the date string and the label to show it.
        self.dateStr = StringVar()
        self.dateLabel = Label(self.mainFrame, textvariable=self.dateStr,
                                font=("Helvetica", 45), fg = "white", bg = "black")
        self.dateLabel.place(relx=.5, rely=.45, anchor=CENTER)

        self.tempStr = StringVar()
        self.tempLabel = Label(self.mainFrame, textvariable=self.tempStr,
                               font=("Helvetica", 45, "bold"), fg = "white", bg = "black")
        self.tempLabel.place(relx=.5, rely=.65, anchor=CENTER)

        self.forecastStr = StringVar()
        self.forecastLabel = Label(self.mainFrame, textvariable=self.forecastStr,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.forecastLabel.place(relx=.5, rely=.75, anchor=CENTER)


    def createForecastFrame(self):
        self.forecastFrame = Frame(self.win.root, bg = "black", width=800, height = 480, cursor="none")
        self.forecastFrame.place(relx=.5,rely=.5, anchor=CENTER,relheight=1, relwidth=1)

        forecastData = weather.get_daily_forecasts(weather.get_weather(self.config.location))

        self.forecastsVar = StringVar()
        self.forecastsLabel = Label(self.forecastFrame, textvariable=self.forecastsVar,
                               font=("Helvetica", 25), fg = "white", bg = "black")
        self.forecastsLabel.place(relx = .5, rely=.5, anchor=CENTER)

    def createCalendarFrame(self):
        self.calendarFrame = Frame(self.win.root, bg = "black", width=800, height = 480, cursor="none")
        self.calendarFrame.place(relx=.5,rely=.5, anchor=CENTER,relheight=1, relwidth=1)


        self.eventsVar = StringVar()
        self.eventsLabel = Label(self.calendarFrame, textvariable = self.eventsVar,
                                 font=("Helvetica", 30), fg = "white", bg = "black")
        self.eventsLabel.place(relx = .5, rely=.5, anchor=CENTER)


    def createNewsFrame(self):
        self.newsFrame = Frame(self.win.root, bg = "black", width=800, height = 480, cursor="none")
        self.newsFrame.place(relx=.5,rely=.5, anchor=CENTER,relheight=1, relwidth=1)

        self.newsVar = StringVar()
        self.newsLabel = Label(self.newsFrame, textvariable = self.newsVar, wraplength=800,
                                 font=("Helvetica", 25), fg = "white", bg = "black")
        self.newsLabel.place(relx = .5, rely=.5, anchor=CENTER)

    def updateSelf(self):

        ##Update the text on the screen and register the next update.
        self.timeStr.set(self.timeString())
        self.dateStr.set(self.dateString())

        if (int(time.time()) % 60 == 0):
            ##Do this every minute so as to not slow down the application.
            self.updateWeather()
            self.updateCalendar()
        if (int(time.time()) % 600 == 0):
            ##As it turns out, the Times only allows 1000 calls a day. Don't call every minute.
            self.updateNews()
            
        
        self.win.root.after(100, self.updateSelf)

    def updateCalendar(self):
        ##Separate every calendar string by a new line and set the variable.
        calendarStrings = calendarLib.getCalendar()
        outputString = ""
        for string in calendarStrings:
            outputString += string + "\n"
        self.eventsVar.set(outputString)

    def updateNews(self):
        ## Get the news.
        newsStrings = news.getNews()
        totalStr = ""
        for string in newsStrings:
            totalStr += string+"\n"
        self.newsVar.set(totalStr)


    def updateWeather(self):
        ##Use the user-defined location to get weather data.
            weather_data = weather.get_weather(self.config.location)

            ##Update the weather strings.
            self.tempStr.set(weather.get_current_temperature(weather_data) + "° F")
            self.forecastStr.set(weather.get_daily_forecasts(weather_data)[0])

            totalString = ""
            ##Update the forecasts.
            for i in range(1,len(weather.get_daily_forecasts(weather_data))):
                day = weather.get_daily_forecasts(weather_data)[i]
                dayInt = (time.localtime()[6] + i) % 7
                totalString += intToDay(dayInt) + ": "+day + "\n"
            self.forecastsVar.set(totalString)

    def timeString(self):
        t = time.localtime()
        hour = int(t[3]) % 12
        if hour == 0:
            hour = 12
        return str(hour)+time.strftime(":%M %p",t)

    def dateString(self):
        t = time.localtime()
        return time.strftime("%A, %B %d, %Y",t)




def intToDay(num):
    if num==0: return "Monday"
    elif num==1: return "Tuesday"
    elif num==2: return "Wednesday"
    elif num==3: return "Thursday"
    elif num==4: return "Friday"
    elif num==5: return "Saturday"
    elif num==6: return "Sunday"
    else: return "Invalid Day"
