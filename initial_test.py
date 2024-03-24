
#imports
import Scripts
import time


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = "user-read-currently-playing,user-read-recently-played"
#vars
#init vars
currenttrack="none"
inac=0
#this variable is how long before the loop times out looking for a new track( 3x in seconds)
timeoutct =10

# print(Scripts.currenttrack)

print()
try:
    while Scripts.currenttrack==0 and inac<timeoutct and Scripts.trackplaying()==True:

        if Scripts.trackinfo()[1]==currenttrack:
            inac+=1
            time.sleep(3)
        else:
            print(Scripts.trackinfo()[1])
            currenttrack=Scripts.trackinfo()[1]
            inac=0
            Scripts.newart()
            time.sleep(10)

except KeyboardInterrupt:
    print("stop")
    Scripts.sleep


