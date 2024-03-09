#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing,user-read-recently-played"
#url for image
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
results = sp.currently_playing()
url=results['item']['album']['images'][0]['url']
name=results['item']['album']['name']
print(name)

#set canvas size of eink
Canv_size= (800,480)
#blank canvas for screen
Canv= Image.new("L",Canv_size, color=255)
#open chonsen image from spotify url
im = Image.open(requests.get(url, stream=True).raw)
#get image info
print(im.format, im.size, im.mode)
#image to BW
im = im.convert("P")
#sq fit to scren
im = im.resize((460,460))
#overlay
Canv.paste(im, (160,10))
Canv.show()
print(im.format, im.size, im.mode)
Canv.save(picdir'tester.bmp')

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


    logging.info("read bmp file on window")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'tester.bmp'))
    Himage2.paste(bmp, (50,10))
    epd.display(epd.getbuffer(Himage2))
    time.sleep(180)


    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()