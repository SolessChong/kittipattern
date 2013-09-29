from parseTrackletXML import *
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_frames_from_file(file_name):

  """
  Read the file and re-arrange them in frames
  """
  tracklets = parseXML(file_name)

  frames = {}
  for trackletObj in tracklets:
  	for translation, rotation, state, occlusion, truncation, amtOcclusion, amtBorders,absoluteFrameNumber in trackletObj:
  		obj = {'type': trackletObj.objectType, 'l':translation}
  		if not frames.has_key(absoluteFrameNumber):
  			frames[absoluteFrameNumber] = []
  		frames[absoluteFrameNumber].append(obj)
  return frames

def drawPDFFromFrames(frames):
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
  pdf = stats.gaussian_kde(points)

  # draw function and plot
  xmin = xs.min()
  xmax = xs.max()
  ymin = ys.min()
  ymax = ys.max()

  points = np.vstack([xs, ys])
  pdf = stats.gaussian_kde(points)

  px = np.linspace(xmin, xmax, 300)
  py = np.linspace(ymin, ymax, 300)
  mx, my = np.meshgrid(px, py)

  z = np.array([pdf([x,y]) for x,y in zip(np.ravel(mx), np.ravel(my))])
  Z = np.reshape(z, mx.shape)

  ## used when "surface plot"
  # fig = plt.figure()
  # ax = fig.add_subplot(111, projection='3d')

  plt.pcolormesh(mx,my,Z, cmap=plt.get_cmap('YlOrRd'))
  plt.show()

  return

# for as-script runs
if __name__ == "__main__":
  frames = read_frames_from_file('../data/tracklet_labels_0001.xml')
