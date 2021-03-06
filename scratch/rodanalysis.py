import sys
sys.path.append('../utilities')
from parseTrackletXML import *
from frames import *
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import os
import fnmatch
import pickle

class Rod:

  def __init__(self, T1, T2, vec):
    """
    Init by types of obj1 and obj2, 
    and a vector describing the relation between these two
    """
    self.T1 = T1
    self.T2 = T2
    self.vec = vec

# End of Class Rod

def get_rods_from_directory(dir_name):
  """
  Read frames from a directory.
  This method searches all the ".xml" files recursively and try to parse them.
  """
  all_frames = read_allframes_from_directory(dir_name)
      
  all_rods = []
  for frames in all_frames:
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
          rod = Rod(frame[i]['type'], frame[j]['type'], \
                    frame[j]['l'] - frame[i]['l'])
          rods.append(rod)

  return rods

def get_PDF_from_rods(rods, T1, T2, intDraw=2):  

  """
  Estimate the probability distribution function of the vector
  Filtered by T1 and T2, string
  T1 and T2 should be like this:
    'Car_Pedestrian_Van'
  since they are:
    1) when filtering, they are used by substring containing operation
    2) used in generating filename of the file containing the PDF function

  Parameters:
    intDraw:
        0: no show
        1: save to image
        2: plt.show
  """
  rods_filtered = [r for r in rods if r.T1 in T1 and r.T2 in T2]
  if len(rods_filtered) < 10:
    print "No such pair occured or too few samples"
    print "T1 = " + T1 + ", T2 = " + T2
    return None
  xs = np.array([r.vec[0] for r in rods_filtered])
  ys = np.array([r.vec[1] for r in rods_filtered])
  points = np.vstack([xs, ys])
  pdf = stats.gaussian_kde(points)

  # save PDF function generated during this run
  PDF_filename = 'pdf/last_pdf_' + T1 + '--' + T2 + '.pk'
  with open(PDF_filename, 'wb') as output:
    pickle.dump(pdf, output, pickle.HIGHEST_PROTOCOL)

  plt.clf();
  if intDraw > 0:
    # draw function and plot
    xmin = xs.min()
    xmax = xs.max()
    ymin = ys.min()
    ymax = ys.max()

    px = np.linspace(xmin, xmax, 30)
    py = np.linspace(ymin, ymax, 30)
    mx, my = np.meshgrid(px, py)

    z = np.array([pdf([x,y]) for x,y in zip(np.ravel(mx), np.ravel(my))])
    Z = np.reshape(z, mx.shape)

    ## used when "surface plot"
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    plt.pcolormesh(mx,my,Z, cmap=plt.get_cmap('YlOrRd'))
    if intDraw == 2:
      plt.show()
    if intDraw == 1:
      fig_filename = 'pdf/last_pdf_' + T1 + '--' + T2 + '.jpg'
      plt.savefig(fig_filename)

  return pdf

def get_all_possible_types(all_frames):
  """
  Get all possible types occured in frames
  """
  types = []
  for frames in all_frames:
    for frame in frames.itervalues():
      for obj in frame:
        types.append(obj['type'])
  types = list(set(types))

  return types

# for as-script runs
if __name__ == "__main__":
  #frames = read_frames_from_file('../data/tracklet_labels_0001.xml')
  dir_name = '../data/part'

  all_rods = get_rods_from_directory('../data/part')
  pdf = get_PDF_from_rods(all_rods, '', '')
  
