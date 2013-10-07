execfile('../wxg/trajana.py')

file_name = '../data/tracklet_labels.xml'
tracklets = parseXML(file_name)

traj1 = Trajectory(tracklets[0])