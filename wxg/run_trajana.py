execfile('../wxg/trajana.py')

file_name = '../data/tracklet_labels.xml'
tracklets = parseXML(file_name)

traj1 = Trajectory(tracklets[0])
n1 = traj1.nodes[10]
n2 = traj1.nodes[100]
traj1.comparison_confidence(traj1)