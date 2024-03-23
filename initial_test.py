
#imports
import Scripts
import time
#vars

currenttrack="none"
inac=0
#this variable is how long before the loop times out looking for a new track( 3x in seconds)
timeoutct =10
# if Scripts.currenttrack==True:
#     print(Scripts.trackinfo()[1])

# else:
#     print("nothing playing")


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

except KeyboardInterrupt:
    print("stop")

