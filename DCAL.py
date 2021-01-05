#####################################################################################
'''
This is a new DCAL to calculate MU required



Author: HQTan
Date: 03/1/21
'''
#####################################################################################

import numpy as np
import os
from util import BeamData
from scipy import interpolate

class DCAL:
    def __init__(self, energy, depth, fs_x_list, fs_y_list, shielding=0, ssd=[False, 100]):
        ### Print inputs
        # print('----------------------------Input--------------------------------')
        # print('Energy: %s' %(energy))
        # print('Field Size: %f x %f cm' %(fs_x, fs_y))
        # print('Pin Depth: %f cm' %(depth))
        # print('Shielding: %f' %(shielding))

        ## Define parameters
        beamdata = BeamData().data
        self.dmax = 0
        self.energy = None
        FLAG_SSD = ssd[0]
        ssd_val = ssd[1]
        shielding = shielding / 100.0
        fs_x = fs_x_list[0] + fs_x_list[1]
        fs_y = fs_y_list[0] + fs_y_list[1]

        ### Actual Algo
        if energy == '6X':
            self.dmax = 1.5 # in cm
            self.energy = '6X'
            ### Calculate OAR first
            if (fs_x_list[0] == fs_x_list[1]) and (fs_y_list[0] == fs_y_list[1]):
                oar = 1
            else: 
                oar = self._CalculateOAR(beamdata['Profile-6MV'], fs_x_list, fs_y_list, depth)

            if self._CheckInput(depth, fs_x_list, fs_y_list, shielding) == -1:
                if FLAG_SSD: 
                    self.results = self._Calculate_MU_SSD(beamdata['PDD-6MV'], beamdata['ROF-6MV'], depth, fs_x, fs_y, oar, shielding, float(ssd_val))
                else:
                    self.results = self._Calculate_MU_SAD(beamdata['PDD-6MV'], beamdata['ROF-6MV'], depth, fs_x, fs_y, oar, shielding)
            else:
                self.results = self._CheckInput(depth, fs_x_list, fs_y_list, shielding)

        elif energy == '10X':
            self.dmax = 2.5 #in cm
            self.energy = '10X'
            ### Calculate OAR first
            if (fs_x_list[0] == fs_x_list[1]) and (fs_y_list[0] == fs_y_list[1]):
                oar = 1
            else: 
                oar = self._CalculateOAR(beamdata['Profile-10MV'], fs_x_list, fs_y_list, depth)

            if self._CheckInput(depth, fs_x_list, fs_y_list, shielding) == -1:
                if FLAG_SSD: 
                    self.results = self._Calculate_MU_SSD(beamdata['PDD-10MV'], beamdata['ROF-10MV'], depth, fs_x, fs_y, oar, shielding, float(ssd_val))
                else:
                    self.results = self._Calculate_MU_SAD(beamdata['PDD-10MV'], beamdata['ROF-10MV'], depth, fs_x, fs_y, oar, shielding)
            else:
                self.results = self._CheckInput(depth, fs_x_list, fs_y_list, shielding)

    def _Calculate_MU_SAD(self, data_pdd, data_rof, depth, fs_x, fs_y, oar, shielding):
        ESQ = self._GetESQ(fs_x, fs_y)   # Field Size at SAD 100cm
        ESQ_surface = ESQ * ( 100 - depth ) / 100    # Field Size at surface of phantom

        # Grab PDD and ROF
        pdd_surface = self._GetPDD(data_pdd, ESQ_surface, depth)
        pdd_iso = self._GetPDD(data_pdd, ESQ, depth)
        rof = self._GetROF(data_rof, fs_x, fs_y)
        tmr = self._GetTMR(pdd_surface, ESQ_surface, depth)

        ## Calculate MU and all relevant quantities
        spd = 100.0 # Prescribe at Iso
        scd = 100.0
        dist_factor = (scd / spd) ## according to Khan notation
        MU = 100 / ((1-shielding) * tmr * rof * dist_factor**2 * oar)
        # self.PrintOutput(oar, ESQ, tmr, pdd_iso, rof, MU)

        return {'OAR':oar, 'ESQ':ESQ, 'ROF':rof, 'TMR':tmr, 'MU':MU}

    def _Calculate_MU_SSD(self, data_pdd, data_rof, depth, fs_x, fs_y, oar, shielding, ssd):
        ESQ = self._GetESQ(fs_x, fs_y)   # Field Size at SAD 100cm
        ESQ_surface = ESQ * ( ssd ) / 100    # Field Size at surface of phantom

        # Grab PDD and ROF
        pdd_surface = self._GetPDD(data_pdd, ESQ_surface, depth)
        pdd_iso = self._GetPDD(data_pdd, ESQ, depth)
        rof = self._GetROF(data_rof, fs_x * np.sqrt(ssd) / 10  , fs_y * np.sqrt(ssd) / 10  )
        tmr = 1.00

        ## Calculate MU and all relevant quantities
        spd = ssd + self.dmax # Prescribe at Iso
        scd = 100.0
        dist_factor = (scd / spd) ## according to Khan notation
        MU = 100 / ((1-shielding) * tmr * rof * dist_factor**2 * oar)
        # self.PrintOutput(oar, ESQ, tmr, pdd_iso, rof, MU)

        return {'OAR':oar, 'ESQ':ESQ_surface, 'ROF':rof, 'TMR':tmr, 'MU':MU, 'PDD':pdd_iso}

    def _GetPDD(self, data_pdd, ESQ, depth):
        ## Get PDD via 2d interpolation
        FS = data_pdd['FS']
        pdd_depth = np.arange(0, len(data_pdd['Data'][:,0])*0.1, 0.1) # Depth at step of 0.1 cm
        f = interpolate.interp2d(FS, pdd_depth, (data_pdd['Data']), kind='linear')
        pdd = f(ESQ, depth)
        if len(pdd) == 1:
            return pdd[0]
        else:
            raise Exception('Invalid PDD values')

    def _GetROF(self, data_rof, fs_x, fs_y):
        FS = data_rof['FS']
        f = interpolate.interp2d(FS, FS, (data_rof['Data']), kind='linear')
        rof = f(fs_x, fs_y)
        if len(rof) == 1:
            return rof[0]
        else:
            raise Exception('Invalid PDD values')

    def _GetTMR(self, pdd, ESQ_surface, depth):
        ssd = 100 - depth
        f = ssd ## to be consistent with Khan equation
        r_depth = ESQ_surface * (f + depth) / f
        r_max = ESQ_surface * (f + self.dmax) / f
        Sp_max = self._GetPhantomScatter(r_max)
        Sp_depth = self._GetPhantomScatter(r_depth)
        TMR = (pdd / 100) * ((f+depth)/(f+self.dmax))**2 * (Sp_max/Sp_depth)
        return TMR

    def _GetPhantomScatter(self, fs):
        ## Method 1 by GH
        Sp = (1.03222 * fs) / (fs + 0.27344)
        ## Method 2 by GH
        Sp = (0.2205 * fs) / (5.883 + fs) + 0.8597
        return Sp

    def _GetESQ(self, fs_x, fs_y):
        return 2 * (fs_x * fs_y) / (fs_x + fs_y)

    def _CalculateOAR(self, profile, fs_x_list, fs_y_list, depth):
        depth_arr = profile['Depth']
        offaxis_arr = profile['Off-axis']
        FS_arr = profile['FS']
        ## Calculate the calculation point
        fs_x = fs_x_list[0] + fs_x_list[1]
        fs_y = fs_y_list[0] + fs_y_list[1]
        ESQ = self._GetESQ(fs_x, fs_y)
        if fs_x_list[0] == fs_x_list[1]:
            offaxis = abs(fs_y_list[0] - fs_y_list[1]) / 2.
        else: 
            offaxis = abs(fs_x_list[0] - fs_x_list[1]) / 2.
        point = (depth, ESQ, offaxis)
        # Interpolation
        oar = interpolate.interpn( (depth_arr, FS_arr, offaxis_arr), profile['Data'], point, method='linear')
        return oar[0] / 100.0

    def PrintOutput(self, OAR, ESQ, TMR, pdd, ROF, MU):
        print('----------------------------Output-------------------------------')
        print('OAR: %f' %OAR)
        print('Equivalent Square Field: %f cm' %(ESQ))
        print('TMR: %f ' %(TMR))
        print('PDD: %f ' %(pdd))
        print('Relative Output Factor: %f' %(ROF))
        print('MU for 100 cGy: %f' %(MU))
        print('-----------------------------------------------------------------')

    def _CheckInput(self, depth, fs_x_list, fs_y_list, shielding):
        fs_x = fs_x_list[0] + fs_x_list[1]
        fs_y = fs_y_list[0] + fs_y_list[1]
        msg = -1
        if depth < self.dmax or depth>30.0 or depth is None:
            msg = 'Depth is less than dmax or more than 30.0 cm'
        if fs_x < 3.0 or fs_x> 40.0 or fs_x is None:
            msg = 'Field Size X is smaller than 3 cm or greater than 40.0 cm'
        if fs_y < 3.0 or fs_y> 40.0 or fs_y is None:
            msg = 'Field Size Y is smaller than 3 cm or greater than 40.0 cm'
        if shielding < 0 or shielding >10.0 or shielding is None:
            msg = 'Shielding is smaller than 0 or greater than 10 percent'
        if fs_x_list[0]!=fs_x_list[1] and fs_y_list[0]!=fs_y_list[1]:
            msg = 'OAR cannnot be calculated with asymmetric X and Y jaw!'
        return msg

    def GrabResults(self):
        return self.results

if __name__ == '__main__':
    DCAL('10X', 5, [10, 20], [15,15], 0.0)
    DCAL('10X', 10.0, [0, 10], [5,5], 0.0)
