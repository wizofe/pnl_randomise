import nibabel as nb
from pathlib import Path
import numpy as np
import pandas as pd

"""
This script is used to compare the order of 3d skeletons in the merged 4d
skeleton output from the TBSS to that of the order in the caselist.
It calculates mean of the skeleton in each volume of the merged 4d and 
compares to that of separate 3d skeleton files of each subject. Then it 
selects most similar individual 3d skeleton to that of the 3d within the 
merged skeleton, returning the subject name.

# example
skeletonDir = check_orders.SkeletonDir(
    '/data/pnl/kcho/Lupus/TBSS/individual_FA_in_tbss_skeleton/FA/5_skeletonize',
    '_', 0)

ANCOVA_MergedData = check_orders.MergedData(
    '/data/pnl/kcho/Lupus/TBSS/etc/final/all_FA.nii.gz',
    '/data/pnl/kcho/Lupus/TBSS/etc/final/caselist.txt')

ANCOVA_MergedData.get_order_in_skeleton(skeletonDir)
ANCOVA_MergedData.assert_caselist()

print(ANCOVA_MergedData.df)
"""


class SkeletonDir:
    def __init__(self, data_dir, split_by='_', subject_index=0):
        '''Object for a individual skeleton dir

        Key arguments:
            data_dir: str or Path, location of the individual skeleton files
            split_by: str, character to split the file name to return subject
                      name that matches the format given in the caselist
            subject_index: int, index of the string in the list of strings
                           created by spliting the skeleton file name by 
                           split_by variable given to the function

        self.averages : list, mean of the intensity in each skeleton file
        self.subjects : list, string of subject names deduced from the file 
                        name
        '''
        self.skeleton_dir = Path(data_dir)
        self.skeletons = list(self.skeleton_dir.glob('*nii.gz'))

        self.averages = []
        self.subjects = []
        for skeleton in self.skeletons:
            subject = skeleton.name.split(split_by)[subject_index]
            data = nb.load(str(skeleton)).get_data()
            self.averages.append(data.mean())
            self.subjects.append(subject)
        
class MergedData:
    def __init__(self, data_loc, caselist_loc):
        '''Object for a merged skeleton file

        Key arguments:
            data_loc: str or Path, location of the merged skeleton file
            caselist_loc: str or Path, location of the caselist text file

        '''
        self.merged_data_loc = data_loc
        self.merged_data = nb.load(str(data_loc)).get_data()
        self.merged_averages = np.mean(self.merged_data, axis=(0,1,2))

        try:
            with open(caselist_loc, 'r') as f:
                self.caselist = [x.strip() for x in f.readlines()]
        except:
            pass

    def get_order_in_skeleton(self, skeletonDir):
        '''Estimate which file the each skeleton came from'''
        self.estimated_subject_order = []
        for merged_average in self.merged_averages:
            diff_array = np.abs(
                np.array(skeletonDir.averages) - merged_average)
            min_diff_value = diff_array.min()
            assert min_diff_value == 0

            min_diff_index = diff_array.argmin()
            min_diff_subject = skeletonDir.subjects[min_diff_index]
            self.estimated_subject_order.append(min_diff_subject)

        # pandas dataframe
        self.df = pd.DataFrame({
            'caselist':self.caselist,
            'caselist in 4d':self.estimated_subject_order
        })

    def assert_caselist(self):
        '''Check caselists are matching'''
        assert self.caselist == self.estimated_subject_order, 'Caselists do not match'

