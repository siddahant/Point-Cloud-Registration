#!/usr/bin/env python3

#### DO NOT CHANGE THESE IMPORTS
import numpy
import time 
import pathlib
####

#### TODO: ADD YOUR IMPORTS HERE

####

def main():
    data_list = ["bag", "basketball", "computercluster1", "corner2", "lab1", "sofalong", "sofawhole", "threechair", "threeemonitor"]

    repo_location = pathlib.Path(__file__).parent.parent.absolute()
    data_folder = repo_location / 'data'

    for location in data_list:
        path_to_ply1 = data_folder / location / 'kinect.ply'
        path_to_ply2 = data_folder / location / 'sfm.ply'

        start_time = time.time()
        
        # TODO: Add your code here

        print ('Execution time : {}'.format(time.time() - start_time))

if __name__ == "__main__":
    main()
