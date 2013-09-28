from parseTrackletXML import *
from scipy import stats
import matplotlib as plot

"""
Read the file and re-arrange them in frames
"""
tracklets = parseXML('../data/tracklet_labels_0001.xml')

frames = {}
for trackletObj in tracklets:
	for translation, rotation, state, occlusion, truncation, amtOcclusion, amtBorders,absoluteFrameNumber in trackletObj:
		obj = {'type': trackletObj.objectType, 'l':translation}
		if not frames.has_key(absoluteFrameNumber):
			frames[absoluteFrameNumber] = []
		frames[absoluteFrameNumber].append(obj)

"""
Enumerate each pair of objects.
Or enumerate over "Rods"
"""
rods = []
for frame in frames.itervalues():
  for i in range(len(frame)):
    for j in range(len(frame)):
      if i != j:
      	rods.append({'T1':frame[i]['type'], \
      				 'T2': frame[j]['type'], \
      				 'l': frame[j]['l'] - frame[i]['l']})

"""
Estimate the probability distribution function of the vector
"""
xs = np.array([r['l'][0] for r in rods])
ys = np.array([r['l'][1] for r in rods])
xmin = xs.min()
xmax = xs.max()
ymin = ys.min()
ymax = ys.max()

points = np.vstack([xs, ys])
pdf = stats.gaussian_kde(points)

x,y = np.mgrid[slice(xmin, xmax, 0.5), slice(ymin, ymax, 0.5)]
z = pdf([x,y])
plt.pcolormesh(x,y,z)