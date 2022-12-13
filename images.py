import cv2, numpy as np
from sklearn.cluster import KMeans
import time

def visualize_colors(cluster, centroids):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    start = 0
    for (percent, color) in colors:
        print(color, "{:0.2f}%".format(percent * 100))
        end = start + (percent * 300)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      color.astype("uint8").tolist(), -1)
        start = end
    return rect

"""
retoune les 5 couleurs dominantes et leur pourcentage dans les clusters.
De la forme : [ [pourcentage, R, G, B], [...] ]
"""
def get_data(cluster, centroids):
    ret = []
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((100, 600, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    start = 0
    for (percent, color) in colors:
        #print(color, "{:0.2f}%".format(percent * 100))
        temp = []
        temp.append(int((percent*100)))
        temp.append(int(color[0]))
        temp.append(int(color[1]))
        temp.append(int(color[2]))
        ret.append(temp)
    # renvoie le pourcentage le plus élevé en premier
    return ret[::-1]

"""
Redimensionne l'image image en gardant le ratio à une largeur width
"""
def resize_image(image, width):
    r = width / float(image.shape[1])
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized

"""
renvoie les 5 couleurs dominantes dans l'image file_name
"""
def most_dominant_color(file_name, n_clusters=5, max_iter=5, max_width=2000):
	# Load image and convert to a list of pixels
    # c'est ici qu'on redimensionne au besoin l'image avant le clustering
	image = cv2.imread(file_name)
	if image.shape[0] > max_width:
		image = resize_image(cv2.imread(file_name), max_width)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	reshape = image.reshape((image.shape[0] * image.shape[1], 3))	

	# Find and display most dominant colors
	cluster = KMeans(n_clusters=n_clusters, max_iter=max_iter).fit(reshape)
	r = get_data(cluster, cluster.cluster_centers_)
	#print(cluster.cluster_centers_)
	"""visualize = visualize_colors(cluster, cluster.cluster_centers_)
	visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
	cv2.imshow('visualize', visualize)
	cv2.waitKey(10000)"""
	return r

"""
Return a list of the ponderated average of the 5 most dominant colors.
"""
def average_dominant_colors(dominant_colors):
	average_r1,average_g1,average_b1 = 0,0,0
	for i in range(0,len(dominant_colors)):
		average_r1 += (dominant_colors[i][0]/100)*dominant_colors[i][1]
		average_g1 += (dominant_colors[i][0]/100)*dominant_colors[i][2]
		average_b1 += (dominant_colors[i][0]/100)*dominant_colors[i][3]
	return [int(average_r1),int(average_g1),int(average_b1)]

"""
Return {'name': [r,g,b], 'image':[]}
"""
def get_average_most_dominant_color(dic):
	#print(dic)
	ret = {}
	for k,v in dic.items():
		ret[k] = average_dominant_colors(v)
	#print(ret)
	return ret
