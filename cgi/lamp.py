#!/usr/bin/env python3

# -*- coding: UTF-8 -*-# enable debugging
import cgitb
cgitb.enable()
print("asd")
from time import sleep
import unicornhat as unicorn


unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.80)
uh_width,uh_height=unicorn.get_shape()

print("Your unicornhat will now light up!")

for h in range(uh_height):
    for w in range(uh_width):
        unicorn.set_pixel(w, h, 255, 0, 0)

unicorn.show()
print("red is good")
sleep(3600)
