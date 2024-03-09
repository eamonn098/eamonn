from PIL import Image, ImageEnhance
im = Image.open("CAT-logo.jpg")
print(im.format, im.size, im.mode)
im = im.convert("L")

im.show()