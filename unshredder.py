from PIL import Image
import sys

## shredded input file
#in_pic = 'TokyoPanoramaShredded.png'
in_pic = 'sample_shredded.png'

## unshredded output file
out_pic = 'sample_unshredded.jpg'

## few useful constants
NUMBER_OF_COLUMNS = 20
tolerance = 10
FIRST = -1
LAST = 1000

image = Image.open(in_pic)
width, height = image.size
data = image.getdata()
shred_width = width/NUMBER_OF_COLUMNS

def get_pixel_value(x, y):
    pixel = data[y * width + x]
    return pixel

def get_delta_rgb(d1, d2):
    r1, g1, b1, a1 = d1
    r2, g2, b2, a2 = d2
    d = (abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))
    return d

order = {}
# run through the shredded pieces
for shred_index in range(0, NUMBER_OF_COLUMNS):
    match = [0] * NUMBER_OF_COLUMNS
    # run through the left most pixels of current shred
    # vs the right most pixels of all other shredded pieces
    for i in range(0, NUMBER_OF_COLUMNS):
        if i == shred_index:
            continue
        count = 0
        for j in range(0, height-1):
            d1 = get_pixel_value(32 * shred_index + 31, j)
            d2 = get_pixel_value(32 * i, j)
            d = get_delta_rgb(d1, d2)
            # are the pixels deserve to be neighbours?
            # if so then count 
            if d[0] < tolerance and d[1] < tolerance and d[2] < tolerance:
                count += 1
        # what percent of pixels match?
        ratio = (float(count) / height) * 100
        match[i] = ratio

    # find the heighest matching ratio
    # that shredded piece might be the neighbouring piece
    max_i = 0
    for i in range(1, len(match)):
        if match[i] > match[max_i]:
            max_i = i
    # update the mapping table
    order[shred_index] = (max_i, match[max_i])

## find last shreded piece
min_i = 0
for i in range(1, len(order)):
    if order[i][1] < order[min_i][1]:
        min_i = i
## update the ordering table
order[min_i] = (LAST, 0)
#print order

## find the shreded piece which is not followed by any other piece.
## that piece might be the first piece.
s1 = set(order.keys())
s2 = set()
for v in order.values():
    s2.add(v[0])
ds = s1 - s2
## update the ordering table
order[FIRST] = (ds.pop(), 0)

## generate the sorted sequence from the ordering table
olist = []
i = FIRST
count = NUMBER_OF_COLUMNS
while order[i][0] != LAST and count > 0:
    i = order[i][0]
    olist.append(i)
    count -= 1

## Error checking (1)
if len(olist) < NUMBER_OF_COLUMNS:
    print "Sorry! Failed to unshred. Algorithm needs improvement."
    sys.exit()

## Error checking (2)
for i in range(0, NUMBER_OF_COLUMNS):
    if i not in olist:
        print "Sorry! Failed to unshred. Algorithm needs improvement."
        sys.exit()

#print olist

## start unshredding process
unshredded = Image.new("RGBA", image.size)
for i in range(0, NUMBER_OF_COLUMNS):
    x1, y1 = shred_width * olist[i], 0
    x2, y2 = x1 + shred_width, height
    source_region = image.crop((x1, y1, x2, y2))
    destination_point = (shred_width * i, 0)
    unshredded.paste(source_region, destination_point)

## save the new image
unshredded.save(out_pic, "JPEG")
