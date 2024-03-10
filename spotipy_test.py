

from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image,ImageDraw,ImageFont
import time


name="B"
refname="A"
breakcount=0

while True:
    if breakcount>10:
        break
    scope = "user-read-currently-playing,user-read-recently-played"
    #url for image
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.currently_playing()
    url=results['item']['album']['images'][0]['url']
    name=results['item']['name']
    if refname == name:
        print("no change")

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
        print(im.format, im.size, im.mode)
        #image to BW
        im = im.convert("P")
        #sq fit to scren
        im = im.resize((460,460))
        #overlay
        Canv.paste(im, (160,10))
        draw = ImageDraw.Draw(Canv)
        draw.text((10, 0), name)
        Canv.show()
        print(im.format, im.size, im.mode)
        Canv.save("art.bmp")
        refname = name
        print("art update")
    time.sleep(10)







