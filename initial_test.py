
#imports
import Scripts
import time

from lib import epd7in5_V2

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing,user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))


#vars
#init vars
currenttrack="none"
inac=0
#this variable is how long before the loop times out looking for a new track( 3x in seconds)
timeoutct = 100

# print(Scripts.currenttrack)

try:
    while inac<timeoutct and Scripts.trackplaying()==True:

        if Scripts.trackinfo()[1]==currenttrack:
            inac+=1
            time.sleep(10)
            print(inac)
        else:
            print(Scripts.trackinfo()[1])
            currenttrack=Scripts.trackinfo()[1]
            inac=0
            Scripts.newart()
            time.sleep(10)


except KeyboardInterrupt:
    print("stop")
    Scripts.sleep()


