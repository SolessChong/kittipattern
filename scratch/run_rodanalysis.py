from rodanalysis import *


### Part I ###
frames = read_frames_from_file('../data/tracklet_labels.xml')
rods = get_rods_from_frames(frames)

pdf = get_PDF_from_rods(rods, 'Car', 'Pedestrain')

### Part II ###
### Get types
types = []

dir_name = '../data/part'

all_frames = read_frames_from_file(dir_name)

types = get_all_possible_types(all_frames)
