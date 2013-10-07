from parseTrackletXML import *
import os

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

def read_allframes_from_directory(dir_name):
  all_frames = []
  for root, sub_dir, files in os.walk(dir_name):
    for fn in fnmatch.filter(files, '*.xml'):
      f = os.path.join(root, fn)
      frames = read_frames_from_file(f)
      all_frames.append(frames)

  return all_frames
