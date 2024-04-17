from __future__ import division, print_function, absolute_import
import re
import glob
import os.path as osp
import warnings
import os
import pandas as pd
from ..dataset import ImageDataset
import torchreid

class EndoCV(ImageDataset):
    """EndoCV.

    Reference:
        Cao Thanh Tung
    Dataset statistics:
        - identities: 4
        - images: 830 (train) + 54 (query) + 223 (gallery).
    """
    #_junk_pids = [0, -1]
    dataset_dir = 'endocv'
    dataset_url = 'https://drive.google.com/file/d/13I-Juawl9RTbN3TN1E4vlPLa_EwvHTtE/view?usp=sharing'

    def __init__(self, root='', **kwargs):
        self.root = osp.abspath(osp.expanduser(root))
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
    
        #===========================================================
    
        # extract csv info
    
        folder_path = "reid-data/endocv/" # Change the path to the dataset
        refs  = pd.read_csv("{}references.csv".format(folder_path))
        paths  = os.listdir(folder_path)
    
        # Get some data
        pid_pics = refs[" number_pics"] # Number of pics per id
        pids = refs.shape[0] # Number of identities
    
        # Generate batches of paths by its person id
        batches = list()
        for i in range(pids):
            batches.append([folder_path+path for path in paths if path.startswith("{}-".format(i+1))])
        
        # Create a random split shuffle of the query/gallery paths 

        query_paths = list()
        gallery_paths = list()

        split_size = 0.8 # Query-Gallery split, usually 0.2 : 0.8 

        for i in range(pids):
            gallery_elements = int(len(batches[i])*split_size)
            gallery_paths.append(random.sample(batches[i], gallery_elements))
            query_paths.append([e for e in batches[i] if e not in gallery_paths[i]])
        
        # Generate the required variables

        #train = list()
        query = [(e, i, 0) for i in range(pids) for e in query_paths[i]]
        gallery = [(e, i, 1) for i in range(pids) for e in gallery_paths[i]]
        train = copy.deepcopy(query) + copy.deepcopy(gallery) # dummy variable

    
        super(EndoCV, self).__init__(train, query, gallery, **kwargs)
