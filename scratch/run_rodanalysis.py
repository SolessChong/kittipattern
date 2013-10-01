from rodanalysis import *


### Part I ###
frames = read_frames_from_file('../data/tracklet_labels.xml')
rods = get_rods_from_frames(frames)

pdf = get_PDF_from_rods(rods, 'Car', 'Pedestrain')

### Part II ###
### Get types
types = []

dir_name = '../data/part'

all_frames = read_allframes_from_directory(dir_name)
all_rods = get_rods_from_directory(dir_name)

types = get_all_possible_types(all_frames)

for T1 in types:
	for T2 in types:
		get_PDF_from_rods(all_rods, T1, T2, False)