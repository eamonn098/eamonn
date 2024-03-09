

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
Canv.save("tester.bmp")


