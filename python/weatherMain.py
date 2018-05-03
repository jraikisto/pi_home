#!/usr/bin/env python3

import sys
from time import sleep
from random import randint
import unicornhat as unicorn
from weather import Weather
from pics import Pics
import math

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.175)
uh_width,uh_height=unicorn.get_shape()

def drawPic(pics):
    pic1 = pics[0]
    pic2 = pics[1]
    for h in range(uh_height):
        for w in range(uh_width):
            if w < 4:
                unicorn.set_pixel(w, h, pic1[h][w][0], pic1[h][w][1], pic1[h][w][2])
            else:
                unicorn.set_pixel(w, h, pic2[h][w-4][0], pic2[h][w-4][1], pic2[h][w-4][2])
    unicorn.show()

def weatherUpdate():
    weather = Weather()
    location = weather.lookup_by_location('tampere')
    if location == None:
        return None
    condition = location.condition()
    return condition

def mainFunction():
    while True:
        wet = weatherUpdate()
        temp = int(wet.temp()) if wet != None else -1
        if temp < 0:
            drawPic(Pics.retNum(temp, 0, 153, 255))
        else:
            drawPic(Pics.retNum(temp, 255, 255, 204))
        sleep(1800)

if __name__ == "__main__":
    mainFunction()
