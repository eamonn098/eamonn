import sys
import os
picdir = os.path.join("/home/eamon/Documents/eamonn", 'pic')
libdir = os.path.join("/home/eamon/Documents/eamonn", 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from lib import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing,user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))


import requests

logging.basicConfig(level=logging.DEBUG)

currenttrack=0



def trackplaying():
    #set spotify scope for auth
    scope = "user-read-currently-playing,user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
    results = sp.currently_playing()
    if results == None:
        output= False
    else: 
        output= True
    return output


def imageurl():
    print("imageurl")

def trackinfo():
    #set spotify scope for auth
    scope = "user-read-currently-playing,user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
    results = sp.currently_playing()
    if results == None:
        return ["nothing playing",0]
    else: 
        trackurl=results['item']['album']['images'][0]['url']
        trackname=results['item']['name']
        return [trackurl,trackname]


def newart(): 
    scope = "user-read-currently-playing,user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
    results = sp.currently_playing()
    url=results['item']['album']['images'][0]['url']
    name=results['item']['name']
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
    Canv.paste(im, (160,10))
    Canv.save(os.path.join(picdir, 'art.bmp'))
    print("Art saved")

    try:
        epd = epd7in5_V2.EPD()
        
        logging.info("init")
        epd.init()
        logging.info("Clear...")
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
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        print("image update complete")
        return
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5_V2
    return

def sleep(): 
    try:
        logging.info("epd7in5_V2 Demo")
        epd = epd7in5_V2.EPD()
        

        logging.info("init")
        epd.init()
        logging.info("Clear...")
        epd.Clear()

        logging.info("Goto Sleep...")
        print("going to sleep")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        return
