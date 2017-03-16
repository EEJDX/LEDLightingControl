import os
from time import sleep
from pysolar.solar import *
from astral import Astral
import datetime
import pytz

city_name = 'Dallas'
latitude_deg = 32.8 # positive in the northern hemisphere
longitude_deg = -96.8 # negative reckoning west from prime meridian in Greenwich, England
RedChannel = 22
GreenChannel = 27
BlueChannel = 17
CurrentRedPWM = 0
CurrentGreenPWM = 0
CurrentBluePWM = 0
SleepInterval = 1 #0.01 for quick demo


def LEDLighting():
    TranslateColorToPWM(0, 0, 0)
    DaylightSync()


def DaylightSync():
    #Initialize
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    print('Information for %s/%s\n' % (city_name, city.region))
    timezone = city.timezone
    print('Timezone: %s' % timezone)
    print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
    global TimeCheck
    global TomorrowMorning
    global Dawn
    global Sunrise
    global Noon
    global Sunset
    global Dusk
    global MoonPhase

    #Check to see what datetime is
    #If current time is before dusk, set intensity appropriately and initiate LED timer
    #Else set sleep timer until tomorrow and then initate LED timer
    CalculateSyncTimes()
    SecondsUntilTomorrowMorning = (datetime.datetime.combine(TomorrowMorning.date(), datetime.time(3,0,0)) - datetime.datetime.now()).total_seconds()
    SecondsUntilDawn = (Dawn - datetime.datetime.now(pytz.timezone('US/Central'))).total_seconds()
    sun = city.sun(date = TimeCheck, local = True)

    DawnToSunrise = (Sunrise - Dawn).total_seconds()
    SunriseToNoon = (Noon - Sunrise).total_seconds()
    NoonToSunset = (Sunset - Noon).total_seconds()
    SunsetToDusk = (Dusk - Sunset).total_seconds()
    Moonlight = (MoonPhase / 28)

    if (TimeCheck - Dusk).total_seconds() > 1:
      print('It is after dusk.  Sleeping for (%s seconds), then running at dawn.' % str(SecondsUntilTomorrowMorning))
      sleep(SecondsUntilTomorrowMorning)
      DaylightSync()
      return
    elif (TimeCheck - Sunset).total_seconds() > 1:
      print('It is after sunset.  Running until dusk.')
      RunSunsetToDusk()
      RunMoonlight()
      DaylightSync()
      return
    elif (TimeCheck - Noon).total_seconds() > 1:
      print('It is after noon.  Running until sunset.')
      RunNoonToSunset()
      DaylightSync()
      return
    elif (TimeCheck - Sunrise).total_seconds() > 1:
      print('It is after sunrise.  Running until noon.')
      RunSunriseToNoon()
      DaylightSync()
      return
    elif (TimeCheck - Dawn).total_seconds() > 1:
      print('It is after dawn.  Running until sunrise.')
      RunDawnToSunrise()
      DaylightSync()
      return
    else:
      print('It is not yet dawn.  Sleeping until dawn, then running.')
      sleep(SecondsUntilDawn)
      DaylightSync()
      return

def CalculateSyncTimes():
    #Initialize
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    print('Information for %s/%s\n' % (city_name, city.region))
    timezone = city.timezone
    print('Timezone: %s' % timezone)
    print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
    global TimeCheck
    global TomorrowMorning
    global Dawn
    global Sunrise
    global Noon
    global Sunset
    global Dusk
    global MoonPhase

    #Check to see what datetime it is
    #If current time is before dusk, set intensity appropriately and initiate LED timer
    #Else set sleep timer until tomorrow and then initate LED timer
    TimeCheck = datetime.datetime.now(pytz.timezone('US/Central'))
    TomorrowMorning = TimeCheck + datetime.timedelta(days = 1)
    SecondsUntilTomorrowMorning = (datetime.datetime.combine(TomorrowMorning.date(), datetime.time(3,0,0)) - datetime.datetime.now()).total_seconds()
    sun = city.sun(date = TimeCheck, local = True)
    Dawn = sun['dawn']
    Sunrise = sun['sunrise']
    Noon = sun['noon']
    Sunset = sun['sunset']
    Dusk = sun['dusk']
    MoonPhase = city.moon_phase(date = TimeCheck)
    print('Dawn:    %s' % str(Dawn))
    print('Sunrise: %s' % str(Sunrise))
    print('Noon:    %s' % str(Noon))
    print('Sunset:  %s' % str(Sunset))
    print('Dusk:    %s' % str(Dusk))
    print('Moon Phase:    %s' % str(MoonPhase))
    print('Time Now:    %s' % str(TimeCheck))

#def RunFastDaylightDemo():
    #CalculateSyncTimes()

    #Moonlight = (MoonPhase / 28)

    #DawnToSunrise = DawnToSunrise / 10
    #SunriseToNoon = SunriseToNoon / 100
    #NoonToSunset = NoonToSunset / 100
    #SunsetToDusk = SunsetToDusk /10

    #MoonlightTime = 14400 #300


def RunDawnToSunrise():    
    DawnToSunrise = (Sunrise - datetime.datetime.now(pytz.timezone('US/Central'))).total_seconds()
    print('DawnToSunrise: %s seconds' % str(DawnToSunrise))
    TranslateColorToPWM(0, 0, 0)
    R = 150 / DawnToSunrise
    G = 150 / DawnToSunrise
    B = 200 / DawnToSunrise
    for i in range(1, int(DawnToSunrise)):
        TranslateColorToPWM(R, G, B)
        R = R + (150 / DawnToSunrise)
        G = G + (150 / DawnToSunrise)
        B = B + (200 / DawnToSunrise)
        sleep(SleepInterval)
    TranslateColorToPWM(150, 150, 200)

def RunSunriseToNoon():    
    SunriseToNoon = (Noon - datetime.datetime.now(pytz.timezone('US/Central'))).total_seconds()
    print('SunriseToNoon: %s seconds' % str(SunriseToNoon))
    R = 150
    G = 150
    B = 200
    for i in range(1, int(SunriseToNoon)):
        TranslateColorToPWM(R, G, B)
        R = R + ((255 - 150) / SunriseToNoon)
        G = G + ((255 - 150) / SunriseToNoon)
        B = B + ((255 - 200) / SunriseToNoon)
        sleep(SleepInterval)
    TranslateColorToPWM(255, 255, 255)

def RunNoonToSunset():    
    NoonToSunset = (Sunset - datetime.datetime.now(pytz.timezone('US/Central'))).total_seconds()
    print('NoonToSunset: %s seconds' % str(NoonToSunset))
    R = 255
    G = 255
    B = 255
    for i in range(1, int(NoonToSunset)):
        TranslateColorToPWM(R, G, B)
        R = R - ((255 - 200) / NoonToSunset)
        G = G - ((255 - 150) / NoonToSunset)
        B = B - ((255 - 150) / NoonToSunset)
        sleep(SleepInterval)
    TranslateColorToPWM(200, 150, 150)

def RunSunsetToDusk():    
    SunsetToDusk = (Dusk - datetime.datetime.now(pytz.timezone('US/Central'))).total_seconds()
    print('SunsetToDusk: %s seconds' % str(SunsetToDusk))
    R = 200
    G = 150
    B = 150
    for i in range(1, int(SunsetToDusk)):
        TranslateColorToPWM(R, G, B)
        R = R - ((200 - 0) / SunsetToDusk)
        G = G - ((150 - 0) / SunsetToDusk)
        B = B - ((150 - 0) / SunsetToDusk)
        sleep(SleepInterval)
    TranslateColorToPWM(0, 0, 0)

def RunMoonlight():    
    Moonlight = (MoonPhase / 28)
    MoonlightTime = 14400
    print('Moonlight: %s seconds' % str(Moonlight))
    R = 0
    G = 0
    B = 0
    for i in range(1, int(MoonlightTime / 2)): #2 hours of increasing moonlight
        TranslateColorToPWM(R, G, B)
        R = R + ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        G = G + ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        B = B + ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        sleep(SleepInterval)
    for i in range(1, int(MoonlightTime / 2)): #2 hours of decreasing moonlight
        TranslateColorToPWM(R, G, B)
        R = R - ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        G = G - ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        B = B - ((100 * (Moonlight / 28)) / (MoonlightTime / 2))
        sleep(SleepInterval)
    TranslateColorToPWM(0, 0, 0)
    
def TranslateColorToPWM(RedVal, GreenVal, BlueVal):
    SetColor(RedChannel, RedVal/255.0)
    SetColor(GreenChannel, GreenVal/255.0)
    SetColor(BlueChannel, BlueVal/255.0)

def FadeColors(RedVal, GreenVal, BlueVal):
    global CurrentRedPWM
    global CurrentGreenPWM
    global CurrentBluePWM
    MaxColorChange = abs(RedVal - CurrentRedPWM)
    if MaxColorChange < abs(GreenVal - CurrentGreenPWM):
        MaxColorChange = abs(GreenVal - CurrentGreenPWM)
    if MaxColorChange < abs(BlueVal - CurrentBluePWM):
        MaxColorChange = abs(BlueVal - CurrentBluePWM)
    if MaxColorChange > 0:
        for i in range(0, MaxColorChange):
            if (RedVal > CurrentRedPWM):
                CurrentRedPWM = CurrentRedPWM + 1
                if CurrentRedPWM > RedVal:
                    CurrentRedPWM = RedVal
                SetColor(RedChannel, float(CurrentRedPWM)/255.0)
            elif (RedVal < CurrentRedPWM):
                CurrentRedPWM = CurrentRedPWM - 1
                if CurrentRedPWM < RedVal:
                    CurrentRedPWM = RedVal
                SetColor(RedChannel, float(CurrentRedPWM)/255.0)
            if (GreenVal > CurrentGreenPWM):
                CurrentGreenPWM = CurrentGreenPWM + 1
                if CurrentGreenPWM > GreenVal:
                    CurrentGreenPWM = GreenVal
                SetColor(GreenChannel, float(CurrentGreenPWM)/255.0)
            elif (GreenVal < CurrentGreenPWM):
                CurrentGreenPWM = CurrentGreenPWM - 1
                if CurrentGreenPWM < GreenVal:
                    CurrentGreenPWM = GreenVal
                SetColor(GreenChannel, float(CurrentGreenPWM)/255.0)
            if (BlueVal > CurrentBluePWM):
                CurrentBluePWM = CurrentBluePWM + 1
                if CurrentBluePWM > BlueVal:
                    CurrentBluePWM = BlueVal
                SetColor(BlueChannel, float(CurrentBluePWM)/255.0)
            elif (BlueVal < CurrentBluePWM):
                CurrentBluePWM = CurrentBluePWM - 1
                if CurrentBluePWM < BlueVal:
                    CurrentBluePWM = BlueVal
                SetColor(BlueChannel, float(CurrentBluePWM)/255.0)
            time.sleep(1.0/255.0)

def SetColor(Channel, PWMVal):
    os.system('echo "' + str(Channel) + '=' + str(PWMVal) + '" > /dev/pi-blaster') 
    
