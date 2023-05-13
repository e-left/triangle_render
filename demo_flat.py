import numpy as np
import matplotlib.pyplot as plt
import cv2
from render import render

# load data
data = np.load("h1.npy", allow_pickle=True)
data = data.item()

verts2d = data["verts2d"]
faces = data["faces"]
vcolors = data["vcolors"]
depth = data["depth"]

# construct the image
shade_t = "flat"
img = render(verts2d, faces, vcolors, depth, shade_t)

plt.imshow(img)
plt.show()
# pyplot and our program works with colors in [0, 1] range, 
# cv2 needs them in [0, 255]
img = img * 255.0
img = img.astype("uint8")
# also, cv2.imwrite saves image in BGR color format, not RGB,
# so we also need to convert our image
img = img[:, :, ::-1] # this means read the channels (third dimension) backwards
cv2.imwrite("flats.png", img)