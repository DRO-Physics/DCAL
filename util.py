'''
This code contains all the helper function and the beam data for MU Calculation.
The Beam data is based on Truebeam Golden beam data and is preprocessed and stored
in json format.
The beam data required are:
    PDD
    ROF
    Profile
'''

import os
import json
import numpy as np

def CheckData(FS, data):
    ## This function to ensure the input beam data is well-
    if len(FS) != len(data[0,:]):
        raise Exception('Length of Stated Field Size not equal to input data!')

class BeamData:
    def __init__(self):
        with open('Golden_Beam_Data.json') as json_file:
            self.beamdata = json.load(json_file)
        self.data = {}
        self.data['PDD-6MV'] = self._PDD_6MV_GB()
        self.data['PDD-10MV'] = self._PDD_10MV_GB()
        self.data['ROF-6MV'] = self._ROF_6MV_GB()
        self.data['ROF-10MV'] = self._ROF_10MV_GB()
        self.data['Profile-6MV'] = self._Profile_6MV_GB()
        self.data['Profile-10MV'] = self._Profile_10MV_GB()

    def _PDD_6MV_GB(self):
        FS = [3,4,6,8,10,20,30,40] # Field Size in cm
        ## Depth in step of 0.1 cm
        # PDD data : Distance x Field Size
        data = [self.beamdata['6MV PDD']['FS'][key] for key in self.beamdata['6MV PDD']['FS']]
        data = np.array(data).T
        CheckData(FS, data)
        return {'FS': FS, 'Data': data}

    def _PDD_10MV_GB(self):
        FS = [3,4,6,8,10,20,30,40] # Field Size in cm
        ## Depth in step of 0.1 cm
        # PDD data : Distance x Field Size
        data = [self.beamdata['10MV PDD']['FS'][key] for key in self.beamdata['10MV PDD']['FS']]
        data = np.array(data).T
        CheckData(FS, data)
        return {'FS': FS, 'Data': data}

    def _ROF_6MV_GB(self):
        ## FS x FS
        FS = [3, 4, 5, 7, 10, 15, 20, 30, 40]
        data = [self.beamdata['6MV ROF']['FS'][key] for key in self.beamdata['6MV ROF']['FS']]
        data = np.array(data)
        CheckData(FS, data)
        return {'FS': FS, 'Data': data}

    def _ROF_10MV_GB(self):
        ## FS x FS
        FS = [3, 4, 5, 7, 10, 15, 20, 30, 40]
        data = [self.beamdata['10MV ROF']['FS'][key] for key in self.beamdata['10MV ROF']['FS']]
        data = np.array(data)
        CheckData(FS, data)
        return {'FS': FS, 'Data': data}

    def _Profile_6MV_GB(self):
        ## This is for OAR calculation up to FS 25 cm
        ## Data: Depth x FS x Off-axis distance
        FS =  [3,4,6,8,10,20,30,40] # Field Size in cm
        offaxis = np.arange(0, 25.0, 0.1) # in step of 0.1cm
        depth = [2.4, 5.0, 10, 20, 30] # in cm
        data_max = [self.beamdata['6MV profile 1.5cm']['FS'][key][0:250] for key in self.beamdata['6MV profile 1.5cm']['FS']]
        data_5cm = [self.beamdata['6MV profile 5cm']['FS'][key][0:250] for key in self.beamdata['6MV profile 5cm']['FS']]
        data_10cm = [self.beamdata['6MV profile 10cm']['FS'][key][0:250] for key in self.beamdata['6MV profile 10cm']['FS']]
        data_20cm = [self.beamdata['6MV profile 20cm']['FS'][key][0:250] for key in self.beamdata['6MV profile 20cm']['FS']]
        data_30cm = [self.beamdata['6MV profile 30cm']['FS'][key][0:250] for key in self.beamdata['6MV profile 30cm']['FS']]
        data = np.array([data_max, data_5cm, data_10cm, data_20cm, data_30cm])
        return {'FS': FS, 'Data': data, 'Depth': depth, 'Off-axis': offaxis}

    def _Profile_10MV_GB(self):
        ## This is for OAR calculation up to FS 25 cm
        ## Data: Depth x FS x Off-axis distance
        FS =  [3,4,6,8,10,20,30,40] # Field Size in cm
        offaxis = np.arange(0, 25.0, 0.1) # in step of 0.1cm
        depth = [2.4, 5.0, 10, 20, 30] # in cm
        data_max = [self.beamdata['10MV profile 2.4cm']['FS'][key][0:250] for key in self.beamdata['10MV profile 2.4cm']['FS']]
        data_5cm = [self.beamdata['10MV profile 5cm']['FS'][key][0:250] for key in self.beamdata['10MV profile 5cm']['FS']]
        data_10cm = [self.beamdata['10MV profile 10cm']['FS'][key][0:250] for key in self.beamdata['10MV profile 10cm']['FS']]
        data_20cm = [self.beamdata['10MV profile 20cm']['FS'][key][0:250] for key in self.beamdata['10MV profile 20cm']['FS']]
        data_30cm = [self.beamdata['10MV profile 30cm']['FS'][key][0:250] for key in self.beamdata['10MV profile 30cm']['FS']]
        data = np.array([data_max, data_5cm, data_10cm, data_20cm, data_30cm])
        return {'FS': FS, 'Data': data, 'Depth': depth, 'Off-axis': offaxis}
