# --- Part Two ---
#
# Now you're ready to decode the image. The image is rendered by stacking the layers and aligning the pixels with the
# same positions in each layer. The digits indicate the color of the corresponding pixel: 0 is black, 1 is white,
# and 2 is transparent.
#
# The layers are rendered with the first layer in front and the last layer in back. So, if a given position has a
# transparent pixel in the first and second layers, a black pixel in the third layer, and a white pixel in the fourth
# layer, the final image would have a black pixel at that position.
#
# For example, given an image 2 pixels wide and 2 pixels tall, the image data 0222112222120000 corresponds to the
# following image layers:
#
# Layer 1: 02
#          22
#
# Layer 2: 11
#          22
#
# Layer 3: 22
#          12
#
# Layer 4: 00
#          00
#
# Then, the full image can be found by determining the top visible pixel in each position:
#
#     The top-left pixel is black because the top layer is 0.
#     The top-right pixel is white because the top layer is 2 (transparent), but the second layer is 1.
#     The bottom-left pixel is white because the top two layers are 2, but the third layer is 1.
#     The bottom-right pixel is black because the only visible pixel in that position is 0 (from layer 4).
#
# So, the final image looks like this:
#
# 01
# 10

import sys

with open('day8.txt') as f:
    raw_data = f.read()

image = ['0222112222120000', 2, 2, '0110']
#image = ['123456789012', 3, 2]
image = [raw_data, 25, 6]

data = image[0]

data_size = len(data)
w = image[1]
h = image[2]

final_img = [["2"] * w for i in range(h)]

for row in final_img:
    print(row)

for i in range(data_size // (w*h)):
    layer = data[(i*w*h):(i+1)*w*h]

    for y in range(h):
        for x in range(w):
            pixel = layer[x + w*y]
            if final_img[y][x] == "2":
                final_img[y][x] = pixel

print ("-")
for row in final_img:
    print(row)

for row in final_img:
    for i in row:
        print("X" if i == "1" else " ", end='')
        print("X" if i == "1" else " ", end='')
        print("X" if i == "1" else " ", end='')
    print('')
