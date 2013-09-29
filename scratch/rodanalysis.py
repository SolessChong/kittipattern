from parseTrackletXML import *
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import os
import fnmatch

def read_frames_from_file(file_name):

  """
  Read the file and re-arrange them in frames
  Specify by individual file
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

def get_rods_from_directory(dir_name):
  """
  Read frames from a directory.
  This method searches all the ".xml" files recursively and try to parse them.
  """
  all_rods = []
  for root, sub_dir, files in os.walk(dir_name):
    for fn in fnmatch.filter(files, '*.xml'):
      f = os.path.join(root, fn)
      frames = read_frames_from_file(f)
      all_rods.extend(get_rods_from_frames(frames))

  return all_rods

def get_rods_from_frames(frames):
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

  return rods

def get_PDF_from_rods(rods, T1, T2):  

  """
  Estimate the probability distribution function of the vector
  Filter by T1 and T2, string
  """
  xs = np.array([r['l'][0] for r in rods])
  ys = np.array([r['l'][1] for r in rods])
  points = np.vstack([xs, ys])
  pdf = stats.gaussian_kde(points)

  # draw function and plot
  xmin = xs.min()
  xmax = xs.max()
  ymin = ys.min()
  ymax = ys.max()

  px = np.linspace(xmin, xmax, 100)
  py = np.linspace(ymin, ymax, 100)
  mx, my = np.meshgrid(px, py)

  z = np.array([pdf([x,y]) for x,y in zip(np.ravel(mx), np.ravel(my))])
  Z = np.reshape(z, mx.shape)

  ## used when "surface plot"
  # fig = plt.figure()
  # ax = fig.add_subplot(111, projection='3d')

  plt.pcolormesh(mx,my,Z, cmap=plt.get_cmap('YlOrRd'))
  plt.show()

  return pdf


# for as-script runs
if __name__ == "__main__":
  #frames = read_frames_from_file('../data/tracklet_labels_0001.xml')
  all_rods = get_rods_from_directory('../data/part')
  get_PDF_from_rods(all_rods)
