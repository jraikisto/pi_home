#!/usr/bin/env python3

import sys
from time import sleep
from random import randint
import unicornhat as unicorn
from weather import Weather
from pics import Pics
import math
import threading
from flask import Flask


class WeatherDisplay:
    def __init__(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(180)
        unicorn.brightness(0.8)
        self.uh_width, self.uh_height = unicorn.get_shape()
        self.__running = False

        self.__running_lock = threading.Lock()

        thread = threading.Thread(target=self.main_function, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def show(self):
        self.__running_lock.acquire()
        try:
            self.__running = True
        finally:
            self.__running_lock.release()

    def no_show(self):
        self.__running_lock.acquire()
        try:
            self.__running = False
            unicorn.off()
        finally:
            self.__running_lock.release()

    def draw_pic(self, pics):
        pic1 = pics[0]
        pic2 = pics[1]
        for h in range(self.uh_height):
            for w in range(self.uh_width):
                if w < 4:
                    unicorn.set_pixel(w, h, pic1[h][w][0], pic1[h][w][1], pic1[h][w][2])
                else:
                    unicorn.set_pixel(w, h, pic2[h][w-4][0], pic2[h][w-4][1], pic2[h][w-4][2])
        unicorn.show()

    @staticmethod
    def weather_update():
        weather = Weather()
        location = weather.lookup_by_location('tampere')
        if location is None:
            return None
        condition = location.condition
        return condition

    def should_show_temperature(self):
        self.__running_lock.acquire()
        try:
            return self.__running
        finally:
            self.__running_lock.release()

    def main_function(self):
        while True:
            if not self.should_show_temperature():
                sleep(1)
                continue

            wet = self.weather_update()
            temp = int(wet.temp) if wet is not None else -1
            if temp < 0:
                self.draw_pic(Pics.retNum(temp, 0, 153, 255))
            else:
                self.draw_pic(Pics.retNum(temp, 255, 255, 204))
            sleep(5)


weather_display = WeatherDisplay()
app = Flask(__name__)


@app.route('/temperature/on')
def temperature_display_on():
    weather_display.show()
    return "on"


@app.route('/temperature/off')
def temperature_display_off():
    weather_display.no_show()
    return "off"
