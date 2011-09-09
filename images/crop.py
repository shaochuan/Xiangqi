import PIL.Image as Image
import glob

for f in glob.glob('*.png'):
    img = Image.open(f)
    w,h = img.size
    left = img.crop((0,0,w/2,h))
    right = img.crop((w/2+1,0, w,h))
    left.save('red/'+f)
    right.save('black/'+f)
