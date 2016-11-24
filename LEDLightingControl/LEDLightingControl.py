import os
import time

RedChannel = 22
GreenChannel = 27
BlueChannel = 17
CurrentRedPWM = 0
CurrentGreenPWM = 0
CurrentBluePWM = 0

def FadeLights():
    TranslateColorToPWM(255, 255, 255)
    TranslateColorToPWM(255, 0, 255)
    TranslateColorToPWM(255, 255, 0)
    TranslateColorToPWM(0, 255, 255)
    TranslateColorToPWM(0, 0, 0)

def TranslateColorToPWM(RedVal, GreenVal, BlueVal):
    #global CurrentRedPWM
    #global CurrentGreenPWM
    #global CurrentBluePWM
    #if (RedVal > CurrentRedPWM):
    #    for i in range(CurrentRedPWM, RedVal):
    #        SetColor(RedChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #elif (RedVal < CurrentRedPWM):
    #    for i in range(CurrentRedPWM, RedVal, -1):
    #        SetColor(RedChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #if (GreenVal > CurrentGreenPWM):
    #    for i in range(CurrentGreenPWM, GreenVal):
    #        SetColor(GreenChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #elif (GreenVal < CurrentGreenPWM):
    #    for i in range(CurrentGreenPWM, GreenVal, -1):
    #        SetColor(GreenChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #if (BlueVal > CurrentBluePWM):
    #    for i in range(CurrentBluePWM, BlueVal):
    #        SetColor(BlueChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #elif (BlueVal < CurrentBluePWM):
    #    for i in range(CurrentBluePWM, BlueVal, -1):
    #        SetColor(BlueChannel, float(i)/255.0)
    #        time.sleep(1.0/255.0)
    #CurrentRedPWM = RedVal
    #CurrentGreenPWM = GreenVal
    #CurrentBluePWM = BlueVal


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
    