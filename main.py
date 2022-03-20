import numpy as np
import time 
from pypointmatcher import pointmatcher as pm
from utils import parse_translation, parse_rotation

def main(ref_data,input_data,config_file):
	PM = pm.PointMatcher
	DP = PM.DataPoints

	# Add an initial 3D translation before applying ICP (default: 0,0,0)
	init_translation = "0,0,0"

	# Add an initial 3D rotation before applying ICP (default: 1,0,0;0,1,0;0,0,1)
	init_rotation = "1,0,0;0,1,0;0,0,1"
	ref = DP(DP.load(ref_data))
	data = DP(DP.load(input_data))
	test_base = "3D"
	start_time=time.time()

	# Create the default ICP algorithm
	icp = PM.ICP()

	# load YAML config
	icp.loadFromYaml(config_file)

	cloud_dimension = ref.getEuclideanDim()
	assert cloud_dimension == 3, "Invalid input point clouds dimension"

	# Parse the translation and rotation to be used to compute the initial transformation
	translation = parse_translation(init_translation, cloud_dimension)
	rotation = parse_rotation(init_rotation, cloud_dimension)

	init_transfo = np.matmul(translation, rotation)

	rigid_trans = PM.get().TransformationRegistrar.create("RigidTransformation")
	
	if not rigid_trans.checkParameters(init_transfo):
	    print("Initial transformations is not rigid, identiy will be used")
	    init_transfo = np.identity(cloud_dimension + 1)

	initialized_data = rigid_trans.compute(data, init_transfo)
	
	# Compute the transformation to express data in ref
	T = icp(initialized_data, ref)
	print(f"match ratio: {icp.errorMinimizer.getWeightedPointUsedRatio():.6}")
	print(f"{test_base} ICP transformation:\n{T}".replace("[", " ").replace("]", " "))
	
	# Transform data to express it in ref
	data_out = DP(initialized_data)
	icp.transformations.apply(data_out, T)

	print ('Execution time : {}'.format(time.time() - start_time))

	output_base_directory = ""
	output_base_file = "test"
	# Save files to see the results
	ref.save(f"{output_base_directory + test_base}_{output_base_file}_ref.vtk")
	data.save(f"{output_base_directory + test_base}_{output_base_file}_data_in.vtk")
	data_out.save(f"{output_base_directory + test_base}_{output_base_file}_data_out.vtk")

if __name__ == "__main__":
   config_file = "../data/point2point.yaml"
   ref_data = "../data/Apartment/Hokuyo_0.csv"
   input_data = "../data/Apartment/Hokuyo_1.csv"

   main(ref_data,input_data,config_file)

