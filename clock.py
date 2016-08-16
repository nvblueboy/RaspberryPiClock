## Handle the clock itself.

import time

from window import *
import weather
import configuration

class Clock():

    modes = ["clock","forecast"]
    
    def __init__(self):
        ##Pull in the configuration file.
        self.config = configuration.Config()
        
        
        ##Initialize the window, setting the resolution to 800x600, and create the labels.
        self.win = Window()
        self.win.root.geometry("800x480")

        self.win.root.bind("<Button-1>",self.switchMode)

        self.createMainFrame()
        self.createForecastFrame()

        self.updateWeather()

        self.mode = 0
        ##self.mainFrame.tkraise()
        
        ##Register the screen's update system.
        self.win.root.after(100,self.updateSelf)

    def switchMode(self, *args):
        self.mode += 1
        if self.mode == len(self.modes):
            self.mode = 0
        current_mode = self.modes[self.mode]
        if current_mode == "clock":
            print("Going to clock")
            self.mainFrame.tkraise()
        if current_mode == "forecast":
            print("Going to forecast")
            self.forecastFrame.tkraise()
        
    def createMainFrame(self):
        self.mainFrame = Frame(self.win.root, bg = "black")
        self.mainFrame.pack()
        ##Set the variable to hold the time string and the label to show it.
        self.timeStr = StringVar()
        self.timeLabel = Label(self.mainFrame, textvariable=self.timeStr,
                               font=("Helvetica", 60, "bold"), fg = "white", bg = "black")
        self.timeLabel.pack(pady=(50,10))

        ##Set the variable to hold the date string and the label to show it.
        self.dateStr = StringVar()
        self.dateLabel = Label(self.mainFrame, textvariable=self.dateStr,
                                font=("Helvetica", 30), fg = "white", bg = "black")
        self.dateLabel.pack()

        self.tempStr = StringVar()
        self.tempLabel = Label(self.mainFrame, textvariable=self.tempStr,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.tempLabel.pack(pady=(50,10))

        self.forecastStr = StringVar()
        self.forecastLabel = Label(self.mainFrame, textvariable=self.forecastStr,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.forecastLabel.pack()

        
    def createForecastFrame(self):
        self.forecastFrame = Frame(self.win.root, bg = "black")
        
        forecastData = weather.get_daily_forecasts(weather.get_weather(self.config.location))
        
        self.todayVar = StringVar()
        self.tomorrowVar = StringVar()
        self.twoDaysVar = StringVar()
        self.todayLabel = Label(self.forecastFrame, textvariable=self.todayVar,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.tomorrowLabel = Label(self.forecastFrame, textvariable=self.tomorrowVar,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.twoDaysLabel = Label(self.forecastFrame, textvariable=self.twoDaysVar,
                               font=("Helvetica", 30), fg = "white", bg = "black")
        self.todayLabel.pack()
        self.tomorrowLabel.pack()
        self.twoDaysLabel.pack()
        
    def updateSelf(self):
        
        ##Update the text on the screen and register the next update.
        self.timeStr.set(self.timeString())
        self.dateStr.set(self.dateString())

        if (int(time.time()) % 60 == 0):
            self.updateWeather()
        
        self.win.root.after(100, self.updateSelf)


    def updateWeather(self):
        ##Use the user-defined location to get weather data.
            weather_data = weather.get_weather(self.config.location)

            ##Update the weather strings.
            self.tempStr.set(weather.get_current_temperature(weather_data) + " F")
            self.forecastStr.set(weather.get_daily_forecasts(weather_data)[0])

            ##Update the forecasts.
            self.todayVar.set("It works")

        
    def timeString(self):
        t = time.localtime()
        return time.strftime("%I:%M %p",t)

    def dateString(self):
        t = time.localtime()
        return time.strftime("%A, %B %d, %Y",t)
