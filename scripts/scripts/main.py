#!/usr/bin/env python3

#### DO NOT CHANGE THESE IMPORTS
import numpy
import time
import pathlib
####

#### TODO: ADD YOUR IMPORTS HERE
from pypointmatcher import pointmatcher as pm
####

def model(ref_data,input_data,config_file):
    PM = pm.PointMatcher
    DP = PM.DataPoints

    # data load
    ref = DP(DP.load(ref_data))
    data = DP(DP.load(input_data))

    # Create the default ICP algorithm
    icp = PM.ICP()

    # load YAML config
    icp.loadFromYaml(config_file)

    # compute transformation matrix
    T = icp(data, ref)

    return T


def main():
    data_list = ["bag", "basketball", "computercluster1", "corner2", "lab1", "sofalong", "sofawhole", "threechair", "threemonitor"]

    repo_location = pathlib.Path(__file__).parent.parent.absolute()
    data_folder = repo_location / '../data'
    config_file = repo_location /'config.yaml'

    for location in data_list:
        path_to_ply1 = data_folder / location / 'kinect.ply'
        path_to_ply2 = data_folder / location / 'sfm.ply'


        start_time = time.time()
        # TODO: Add your code here

        T_gt = data_folder / location / 'T_gt.txt'
        ground_truth = numpy.loadtxt(f'{T_gt}')

        # algorithm
        T = model(f'{path_to_ply1}', f'{path_to_ply2}',f'{config_file}')

        # compute the mean diffrance between ground truth and computed matrix
        MSE = numpy.square(numpy.subtract(T, ground_truth)).mean()
        print('Mean Square Error in {}: {}'.format(location, MSE))
        print ('Execution time : {}'.format(time.time() - start_time))

if __name__ == "__main__":
    main()
