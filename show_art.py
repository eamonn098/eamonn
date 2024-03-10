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
import get_art
logging.basicConfig(level=logging.DEBUG)



try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


    logging.info("pasting image")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'art.bmp'))
    Himage2.paste(bmp, (0,0))
    draw = ImageDraw.Draw(Himage2)
    epd.display(epd.getbuffer(Himage2))
    time.sleep(3)

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
print('image updated')