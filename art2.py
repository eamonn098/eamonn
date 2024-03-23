import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#logging.basicConfig(level=logging.DEBUG)

currenttrack=0

def imageurl():
    print("imageurl")

def trackinfo():
    #set spotify scope for auth
    scope = "user-read-currently-playing,user-read-recently-played"
    #url for image
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.currently_playing()
    if results == None:
        return ["nothing playing",0]
    else: 
        trackurl=results['item']['album']['images'][0]['url']
        trackname=results['item']['name']
        return [trackurl,trackname]
    

time.sleep(2)
if currenttrack==(trackinfo()[1] or 0):
    print("no refresh")
    if currenttrack==0:
        print("nothing playing")
else: 
    currenttrack=trackinfo()[1]
    print(currenttrack)


