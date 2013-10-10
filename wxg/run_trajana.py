execfile('../wxg/trajana.py')

file_name = '../data/tracklet_labels.xml'
tracklets = parseXML(file_name)

traj1 = Trajectory(tracklets[0])
n1 = traj1.nodes[10]
n2 = traj1.nodes[100]
traj1.comparison_confidence(traj1)

trajs = [Trajectory(tracklet) for tracklet in tracklets[1:3]]
engine = AnalysisEngine()
engine.calculate_all(trajs)

