#!/usr/bin/env python

import signal
import time
from sys import exit
from PIL import Image
from threading import Thread
import unicornhat as unicorn
import sh
import colorsys
import math
import random

def swirl(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    dist = math.sqrt(pow(x, 2)+pow(y,2)) / 2.0
    angle = (step / 10.0) + (dist * 1.5)
    s = math.sin(angle);
    c = math.cos(angle);

    xs = x * c - y * s;
    ys = x * s + y * c;

    r = abs(xs + ys)
    r = r * 64.0
    r -= 20

    return (r, r + (s * 130), r + (c * 130))

def checker(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    angle = (step / 10.0)
    s = math.sin(angle);
    c = math.cos(angle);

    xs = x * c - y * s;
    ys = x * s + y * c;

    xs -= math.sin(step / 200.0) * 40.0
    ys -= math.cos(step / 200.0) * 40.0

    scale = step % 20
    scale /= 20
    scale = (math.sin(step / 50.0) / 8.0) + 0.25;

    xs *= scale
    ys *= scale

    xo = abs(xs) - int(abs(xs))
    yo = abs(ys) - int(abs(ys))
    l = 0 if (math.floor(xs) + math.floor(ys)) % 2 else 1 if xo > .1 and yo > .1 else .5

    r, g, b = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, l)

    return (r * 255, g * 255, b * 255)

def blues_and_twos(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    xs = (math.sin((x + step) / 10.0) / 2.0) + 1.0
    ys = (math.cos((y + step) / 10.0) / 2.0) + 1.0

    scale = math.sin(step / 6.0) / 1.5
    r = math.sin((x * scale) / 1.0) + math.cos((y * scale) / 1.0)
    b = math.sin(x * scale / 2.0) + math.cos(y * scale / 2.0)
    g = r - .8
    g = 0 if g < 0 else g

    b -= r
    b /= 1.4

    return (r * 255, (b + g) * 255, g * 255)

def rainbow_search(x, y, step):
    xs = math.sin((step) / 100.0) * 20.0
    ys = math.cos((step) / 100.0) * 20.0

    scale = ((math.sin(step / 60.0) + 1.0) / 5.0) + 0.2
    r = math.sin((x + xs) * scale) + math.cos((y + xs) * scale)
    g = math.sin((x + xs) * scale) + math.cos((y + ys) * scale)
    b = math.sin((x + ys) * scale) + math.cos((y + ys) * scale)

    return (r * 255, g * 255, b * 255)

def random_dots(x, y, step):
    light = bool(random.getrandbits(1))
    if (light):
        r = round(random.uniform(0, 1), 3)
        g = round(random.uniform(0, 1), 3)
        b = round(random.uniform(0, 1), 3)
    else:
        r = 0
        g = 0
        b = 0
    return (r * 255, g * 255, b * 255)

def tunnel(x, y, step):

    speed = step / 100.0
    x -= (u_width/2)
    y -= (u_height/2)

    xo = math.sin(step / 27.0) * 2
    yo = math.cos(step / 18.0) * 2

    x += xo
    y += yo

    if y == 0:
        if x < 0:
            angle = -(math.pi / 2)
        else:
            angle = (math.pi / 2)
    else:
        angle = math.atan(x / y)

    if y > 0:
        angle += math.pi

    angle /= 2 * math.pi # convert angle to 0...1 range

    shade = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 2.1
    shade = 1 if shade > 1 else shade


    angle += speed
    depth = speed + (math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 10)

    col1 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .8)
    col2 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .3)


    col = col1 if int(abs(angle * 6.0)) % 2 == 0 else col2

    td = .3 if int(abs(depth * 3.0)) % 2 == 0 else 0

    col = (col[0] + td, col[1] + td, col[2] + td)

    col = (col[0] * shade, col[1] * shade, col[2] * shade)

    return (col[0] * 255, col[1] * 255, col[2] * 255)

def renderEmulator():
    while True:
        if (emul == 'emul'):            
            effects = [tunnel, rainbow_search, checker, swirl, blues_and_twos, random_dots]
            while (emul == 'emul'):
                step = 0
                for i in range(500):
                    if (emul == 'emul'):
                        for y in range(u_height):
                            for x in range(u_width):
                                r, g, b = effects[0](x, y, step)
                                if i > 400:
                                    r2, g2, b2 = effects[-1](x, y, step)
                                    ratio = (500.00 - i) / 100.0
                                    r = r * ratio + r2 * (1.0 - ratio)
                                    g = g * ratio + g2 * (1.0 - ratio)
                                    b = b * ratio + b2 * (1.0 - ratio)
                                r = int(max(0, min(255, r)))
                                g = int(max(0, min(255, g)))
                                b = int(max(0, min(255, b)))
                                unicorn.set_pixel(x, y, r, g, b)
                        step += 1
                        unicorn.show()
                        time.sleep(0.03)
                effect = effects.pop()
                effects.insert(0, effect)
        elif (emul == '/nes'):
            for character in range (2):
                for frame in range (39): 
                    if (emul == '/nes'):
                        img = Image.open('./mariorun/frame_'+str(frame+1)+'.gif')
                        img_rgb = img.convert('RGB')
                        for x in range (8):
                            for y in range (8):
                                pixel = img_rgb.getpixel((18+x+(character*13),4+y))
                                r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                unicorn.set_pixel(x, y, r, g, b)
                        unicorn.show()
                        if (frame>=36):
                            time.sleep(0.5)
                        else:
                            time.sleep(0.1)
        else:
            lemul = emul
            if (lemul == '/snes'):
                icons = iconsSnes
            elif (lemul == '/gb'):
                icons = iconsGb
            elif (lemul == '/gbc'):
                icons = iconsGbc
            elif (lemul == '/mastersystem'):
                icons = iconsMastersystem
            elif (lemul == '/megadrive'):
                icons = iconsMegadrive
            elif (lemul == '/gamegear'):
                icons = iconsGamegear
            elif (lemul == '/atari'):
                icons = iconsAtari
            elif (lemul == '/zxspectrum'):
                icons = iconsSpectrum
            elif (lemul == '/mame'):
                icons = iconsMame
            img = Image.open('tiles.png')
            img_rgb = img.convert('RGB')
            for row in range(10):
                for col in range(10):
                    for item in range(len(icons)):
                        if (col+(row*10)==icons[item] and lemul == emul):
                            for x in range(8):
                                for y in range(8):
                                    cx = (x*5)+2+(56*col)
                                    cy = (y*5)+2+(56*row)
                                    pixel = img_rgb.getpixel((cx,cy))
                                    r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                    unicorn.set_pixel(x, y, r, g, b)
                                    unicorn.show()
                            time.sleep(2)

def checkEmulator():
    global emul
    emul = 'emul'
    while True:
        time.sleep(1)        
        found = False
        for emulator in emulators:            
            try:
                lines = 0                
                shgrep = sh.grep(sh.ps('aux', _piped=True), emulator)
                for line in shgrep:
                    lines += 1
                if (lines > 1):
                    found = True
                    emul = emulator                       
            except:
                pass
        if (not found):
            emul = 'emul'

emulators = ['/nes','/snes','/gb','/gbc','/mastersystem','/megadrive','/gamegear','/atari','/zxspectrum','/mame']
icons = [0]
iconsSnes = [0,1,2,3,4,5,6,7,8,9,10,11,12,78,79,96]
iconsGb = [81,82,83,84,85,86,87,88]
iconsGbc = [80,90,91,99,77]
iconsMastersystem = [13,14,15,16]
iconsMegadrive = [89,20,21,22,23]
iconsGamegear = [20,21,22,23]
iconsAtari = [30,31,32,33,34,35,36,37,38,39]
iconsSpectrum = [40,41,42,43,44,45,46,47,48,49,50,51,52,53]
iconsMame = [60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,97,98,24,25,26,27,28,29]
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(180)
unicorn.brightness(0.5)
u_width,u_height=unicorn.get_shape()
checkEmulator = Thread(target=checkEmulator)
renderEmulator = Thread(target=renderEmulator)
checkEmulator.start()
renderEmulator.start()