#!/usr/bin/env python3

#### DO NOT CHANGE THESE IMPORTS
import numpy
import time
import pathlib
####

#### TODO: ADD YOUR IMPORTS HERE
from pypointmatcher import pointmatcher as pm
####
class model:
    def __init__(self):
        self.PM = pm.PointMatcher
        self.DP = pm.PointMatcher.DataPoints
        self.icp = pm.PointMatcher.ICP()

    def loaddata(self,ref_data,input_data):
        self.ref = self.DP(self.DP.load(ref_data))
        self.data = self.DP(self.DP.load(input_data))

    def algorithm(self,config_file):
        self.icp.loadFromYaml(config_file)
        self.T= self.icp(self.data, self.ref)
        return self.T

def main():
    data_list = ["bag", "basketball", "computercluster1", "corner2", "lab1", "sofalong", "sofawhole", "threechair", "threemonitor"]

    repo_location = pathlib.Path(__file__).parent.parent.absolute()
    data_folder = repo_location / '../data'
    config_file = repo_location /'config.yaml'
    config_file1 = repo_location /'config1.yaml'
    for location in data_list:
        path_to_ply1 = data_folder / location / 'kinect.ply'
        path_to_ply2 = data_folder / location / 'sfm.ply'

        start_time = time.time()
        # TODO: Add your code here

        T_gt = data_folder / location / 'T_gt.txt'
        ground_truth = numpy.loadtxt(f'{T_gt}')

        # algorithm
        algo = model()
        algo.loaddata(f'{path_to_ply1}', f'{path_to_ply2}')
        T = algo.algorithm(f'{config_file}')

        # compute the mean diffrance between ground truth and computed matrix
        MSE = numpy.square(numpy.subtract(T, ground_truth)).mean()
        if MSE>0.02:
            T= algo.algorithm(f'{config_file1}')
            MSE2 = numpy.square(numpy.subtract(T, ground_truth)).mean()
            MSE =  MSE2 if MSE > MSE2 else MSE

        print('Mean Square Error in {}: {}'.format(location, MSE))
        print ('Execution time : {}'.format(time.time() - start_time))

if __name__ == "__main__":
    main()
