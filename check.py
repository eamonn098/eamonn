from PIL import Image


#set canvas size of eink
Canv_size= (800,460)
#blank canvas for screen
Canv= Image.new("L",Canv_size, color=255)
#open chonsen image
im = Image.open("7in5_V2.bmp")
im2 = Image.open("tester.bmp")

#get image info
print(im.format, im.size, im.mode)
print(im2.format, im2.size, im2.mode)



