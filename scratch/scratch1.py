from parseTrackletXML import *

tracklets = parseXML('../data/tracklet_labels_0001.xml')

for trackletObj in tracklets:
	for translation, rotation, state, occlusion, truncation, amtOcclusion, amtBorders,absoluteFrameNumber in trackletObj:
		obj = {'type': trackletObj.objectType, 'l':translation}

