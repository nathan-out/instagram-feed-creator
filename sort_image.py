from scipy.spatial import distance
import numpy as np
from PIL import Image

def NN(A, start):
    """Nearest neighbor algorithm.
    A is an NxN array indicating distance between N locations
    start is the index of the starting location
    Returns the path and cost of the found solution
    """
    path = [start]
    cost = 0
    N = A.shape[0]
    mask = np.ones(N, dtype=bool)  # boolean values indicating which 
                                   # locations have not been visited
    mask[start] = False

    for i in range(N-1):
        last = path[-1]
        next_ind = np.argmin(A[last][mask]) # find minimum of remaining locations
        next_loc = np.arange(N)[mask][next_ind] # convert to original location
        path.append(next_loc)
        mask[next_loc] = False
        cost += A[last, next_loc]

    return path, cost

def build_image(triplet, w=10, y=100):
	degrade, x_offset = Image.new('RGB', (w*(len(triplet)-1),y)), 0
	for i in range(0, len(triplet)-1):
		img = Image.new('RGB', (w, y), (triplet[i][0], triplet[i][1], triplet[i][2]))
		degrade.paste(img, (x_offset,0))
		x_offset += w
	return degrade
# visualize gradient
"""
d = build_image(colours_nn, 200, 100)
d.save(str(i)+'.png')
"""

"""
Return file name list sorted in a certain method called Nearest neighbour algorithm.
dic must be like : {'name': [r,g,b], 'image':[r,g,b]} -> [r,g,b] is the avegrage of dominant colors.
"""
def get_sorted_images(dic):
	colours = []
	#print(dic)
	for k,v in dic.items():
		colours.append(v)

	colours_length = len(colours)
	# Distance matrix
	A = np.zeros([colours_length,colours_length])
	for x in range(0, colours_length-1):
    		for y in range(0, colours_length-1):
        		A[x,y] = distance.euclidean(colours[x],colours[y])
	# Nearest neighbour algorithm
	path, cost = NN(A, 0)
	print('\tsort cost :',cost)
	# Final array
	colours_nn = []
	for i in path:
    		colours_nn.append(colours[i])
	#print('order :',colours_nn)
	# reconstruct the dic
	file_names = []
	for c in colours_nn:
		for k,v in dic.items():
			if c == v:
				#print(k, dic[k], c)
				file_names.append(k)
	return file_names
