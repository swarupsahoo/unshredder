from PIL import Image
import sys

in_pic = 'sample_shredded.png'
#in_pic = 'TokyoPanoramaShredded.png'

## useful constants
tolerance = 10
threshold = 20

## if filename is passed at command line
if len(sys.argv) > 1:
    in_pic = sys.argv[1]

image = Image.open(in_pic)
shredded = Image.new("RGBA", image.size)
width, height = image.size
data = image.getdata()

def get_pixel_value(x, y):
    pixel = data[y * width + x]
    return pixel

def get_delta_rgb(d1, d2):
    r1, g1, b1, a1 = d1
    r2, g2, b2, a2 = d2
    d = (abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))
    return d

l = []
# run through all the pixel columns
for x in range(0, width-1):
    count = 0
    # check if the current pixel column doesn't
    # deserve to be neighbour of next column 
    for y in range(0, height):
        p1 = get_pixel_value(x, y)
        p2 = get_pixel_value(x+1, y)
        d = get_delta_rgb(p1, p2)
        # so they resemble a lot? then its not shred border.
        if d[0] < tolerance and d[1] < tolerance and d[2] < tolerance:
            count += 1
    ratio = (float(count)/height) * 100
    ratio = int(ratio)
    l.append(ratio)
#print l

# find out pixel column pairs those do
# not deserve to be neighbours
blist = []
for i in range(0, len(l)):
    if l[i] < threshold:
        #print i, l[i]
        # add 1 to adjust the 0 index, 0..31 = 31+1
        blist.append(i+1)

# find the gap between pixel pairs (may be shred border)
# those do not deserve to be neighbours.
# that gap is the width we want.
m = {}
for i in range(0, len(blist)-1):
    w = blist[i+1] - blist[i]
    #print w
    if w not in m:
        m[w] = 1
    else:
        m[w] = m[w] + 1

# find the gap/width which is a majority
# majority gap value is the width
# all other minority gap/width are fake widths
max = 0
width = 0
for k in m.keys():
    if m[k] > max:
        width = k
        max = m[k]

print "width => ", width
