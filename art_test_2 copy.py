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
from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

logging.basicConfig(level=logging.DEBUG)

scope = "user-read-currently-playing,user-read-recently-played"
#url for image
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
results = sp.currently_playing()
url=results['item']['album']['images'][0]['url']
name=results['item']['album']['name']
print(results)

#set canvas size of eink
Canv_size= (800,480)
#blank canvas for screen
Canv= Image.new("L",Canv_size, color=255)
#open chonsen image from spotify url
im = Image.open(requests.get(url, stream=True).raw)
#get image info
#image to BW
im = im.convert("P")
#sq fit to scren
im = im.resize((460,460))
#overlay
Canv.paste(im, (170,10))
Canv.save(os.path.join(picdir, 'tester.bmp'))

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


    logging.info("read bmp file on window")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'tester.bmp'))
    Himage2.paste(bmp, (0,0))
    draw = ImageDraw.Draw(Himage2)
    draw.text((10, 0), name, font = font60, fill = 0)
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