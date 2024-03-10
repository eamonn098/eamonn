from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image,ImageDraw,ImageFont
import time
import sys
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
            Canv.save(os.path.join(picdir, 'tester.bmp'))
            refname = name
            os.system(os.path.join(curdir,'show_art.py'))
            breakcount=0
            SNcount=0
            time.sleep(10)

    os.system(os.path.join(curdir,'clear.py'))

except KeyboardInterrupt:    
    os.system(os.path.join(curdir,'clear.py'))


