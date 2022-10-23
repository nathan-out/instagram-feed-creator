import images as i
import sys,os,shutil,sort_image

debug = []

def help():
	print("[INSTAGRAM FEED GENERATOR]\n\n\tThis tool sort images into the 'images' directory in order to create color gradient with images. The tool create a copy of 'images' directory named 'sorted' which contains all the images sorted to make a colour gradient, for an instagram feed for example.\n\nTo launch the script type 'python3 main.py make_feed'.\n\nFiletype accepted : png or jpg.")

"""
Renvoie un dictionnaire avec comme clef le nom de chaque fichier png ou jpg dans le dossier courant et comme valeur une liste 2D avec les 5 couleurs dominantes dans l'image et pour chacune d'entre elle son pourcentage :
de la forme : {'filename.png': [ [pourcentage, R, G, B], [...] ], 'filename2.png': [ [pourcentage, R, G, B], [...] ]}
"""
def get_files_with_dominant_colors():
	images_and_dominant_colors = {}
	"""
	de la forme : {'filename.png': [ [pourcentage, R, G, B], [...] ]}
	"""
	for e in sorted(os.listdir()):
		if os.path.isfile(e):
			if not os.path.exists(e):
				raise ValueError('Error : file '+e+' does not exist. Porgramm stopped.')
			if len(e.split('.'))>2:
				raise ValueError('Error : file "'+e+'" have problem in its name. Filename MUST NOT have more than one dot (.) in its name. Programm stopped.')
			if e.split('.')[1] == 'png' or e.split('.')[1] == 'jpg':
				print('\tprocessing '+e+' please wait this could be long...')
				images_and_dominant_colors[e] = i.most_dominant_color(e)
				print(e+' \tprocessing complete.')
			else:
				print('\twarning file '+e+' is not jpg or png. This file have been ignored by the program.')
	return images_and_dominant_colors

"""
Calculate the distance between two lists (RGB average).
t1 : [x1, y1, z1]
t2 : [x2, y2, z2]
d = ((x2-x1)+(y2-y1)+(z2-z1))/3
"""	
def calculate_distance(t1, t2):
	#print(t1)
	#print(t2)
	average_r1, average_g1, average_b1 = 0,0,0
	average_r2, average_g2, average_b2 = 0,0,0
	for i in range(0,len(t1)):
		average_r1 += (t1[i][0]/100)*t1[i][1]
		average_g1 += (t1[i][0]/100)*t1[i][2]
		average_b1 += (t1[i][0]/100)*t1[i][3]
		
		average_r2 += (t2[i][0]/100)*t2[i][1]
		average_g2 += (t2[i][0]/100)*t2[i][2]
		average_b2 += (t2[i][0]/100)*t2[i][3]
	#print(average_r1, average_g1, average_b1)
	#print(average_r2, average_g2, average_b2)
	if not [int(average_r1), int(average_g1), int(average_b1)] in debug:
		debug.append([int(average_r1), int(average_g1), int(average_b1)])
	#print('['+str(int(average_r1))+','+str(int(average_g1))+','+str(int(average_b1))+']')
	d = 0
	x1, y1, z1 = average_r1, average_g1, average_b1
	x2, y2, z2 = average_r2, average_g2, average_b2
	d = abs(x2-x1)+abs(y2-y1)+abs(z2-z1)
	#print(x1,y1,z1,'|',x2,y2,z2,d)
	return int(d)

"""
Copy files from the current directory to 'sorted' directory in the order of list_of_files.
Names of files will be saved 'image_name.png' saved as '00001-images_name.png'.
"""
def save_ordered_files(list_of_files):
	i = 0
	file_name = ''
	for file in list_of_files:
		file_name = str(i).zfill(5)+'-'+file
		shutil.copy(file, 'sorted/'+file_name)
		#print(file_name)
		i+=1

def make_feed():
	print("Processing all of images...")
	images_and_dominant_colors = get_files_with_dominant_colors()
	print("Processing complete")
	print("Sorting files this could be long too...")
	list_of_files = sort_image.get_sorted_images(i.get_average_most_dominant_color(images_and_dominant_colors))
	#print(debug)
	print("Saving files into 'sorted' directory...")
	save_ordered_files(list_of_files)
	print("\nProgram complete ! You can view the images into the 'sorted' directory !")
	
	

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'make_feed': make_feed()
		else: help() 
	else: help()
