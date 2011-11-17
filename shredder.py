from PIL import Image
from random import shuffle
import sys

in_pic = 'img1.jpg'
out_pic = 'sample_shredded.png'

## if filename is passed at command line
if len(sys.argv) > 1:
    in_pic = sys.argv[1]

SHREDS = 20

if len(sys.argv) > 2:
    SHREDS = int(sys.argv[2])

image = Image.open(in_pic)
shredded = Image.new("RGBA", image.size)
width, height = image.size
shred_width = width/SHREDS
sequence = range(0, SHREDS)
shuffle(sequence)
#print sequence

for i, shred_index in enumerate(sequence):
    shred_x1, shred_y1 = shred_width * shred_index, 0
    shred_x2, shred_y2 = shred_x1 + shred_width, height
    region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
    shredded.paste(region, (shred_width * i, 0))

shredded.save(out_pic)

