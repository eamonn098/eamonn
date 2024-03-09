from PIL import Image


#set canvas size of eink
Canv_size= (800,460)
#blank canvas for screen
Canv= Image.new("L",Canv_size, color=255)
#open chonsen image
im = Image.open("ALBUMIMG2.png")
#get image info
print(im.format, im.size, im.mode)
#image to BW
im = im.convert("L")
#sq fit to scren
im = im.resize((460,460))
#overlay
Canv.paste(im, (0,0)) 
Canv.show()
print(im.format, im.size, im.mode)
Canv.save("tester.bmp")

