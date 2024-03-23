from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import time
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

curdir=os.path.dirname(__file__)

name="B"
refname="A"
breakcount=0
SNcount=0
try:
    while True:
        if breakcount>10 or SNcount>100:
            break
        scope = "user-read-currently-playing,user-read-recently-played"
        #url for image
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        results = sp.currently_playing()
        url=results['item']['album']['images'][0]['url']
        name=results['item']['name']
        print("10s rest")
        time.sleep(10)
        if refname == name:
            SNcount=+1
            time.sleep(10)
        elif name=="none": 
            breakcount=+1
            time.sleep(10)
        else: 
            print(name)
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
            refname = name
            print("testing art")
            print("loading art")
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
                epd7in5_V2.epdconfig.module_exit(cleanup=True)
                exit()
            except IOError as e:
                logging.info(e)
                
            except KeyboardInterrupt:    
                logging.info("ctrl + c:")
                epd7in5_V2.epdconfig.module_exit(cleanup=True)
                exit()
            time.sleep(10)
            Print("art loaded 10s rest")
            breakcount=0
            SNcount=0
            
except KeyboardInterrupt:    
    os.system(os.path.join(curdir,'clear.py'))