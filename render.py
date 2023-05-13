import numpy as np
from fill_triangles import flats, gourauds

M = 512
N = 512

def render(verts2d, faces, vcolors, depth, shade_t):
    # grab useful quantities
    k = len(faces) 
    l = len(depth)

    # construct initial image
    img = np.ones((M, N, 3))

    # find all triangles, with the proper order according to depth
    # constuct cog depths hashmap
    cog_depths = np.zeros((k))
    cog_depths = {}
    for i in range(k):
        # first coordinate
        idx_a = faces[i][0]
        idx_b = faces[i][1]
        idx_c = faces[i][2]

        # find points
        point_a_depth = depth[idx_a]
        point_b_depth = depth[idx_b]
        point_c_depth = depth[idx_c]

        # calculate cog coordinate in z axis (depth)
        cog_depth = (point_a_depth + point_b_depth + point_c_depth) / 3.0

        # store depth (z coordinate) in hashmap
        cog_depths[str(cog_depth)] = i

    # determine coloring method
    triangle_function = None
    if shade_t == "flat":
        triangle_function = flats
    if shade_t == "gouraud":
        triangle_function = gourauds

    # color all triangles
    # obtain all depths (keys of dictionary, strings)
    depths = list(cog_depths.keys())
    # sort in reverse, since we want further triangles
    # (higher depth) to be colored firsts
    # sort by numerical value
    depths.sort(key=lambda x: float(x), reverse=True)
    # iterate and draw triangle
    for depth in depths:
        # get index
        faces_idx = cog_depths[depth]
        # get point idices
        point_idx = faces[faces_idx]

        # get vertices
        triangle = np.array(verts2d[point_idx])
        # get vertices' colors
        colors = np.array(vcolors[point_idx])

        # return img
        # paint triangle over canvas
        img = triangle_function(img, triangle, colors)

    # return image
    return img
