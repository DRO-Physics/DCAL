# DCAL

This contain the source code and executable of the new DCAL. This currently enables SAD calculation. Will include SSD, Wedge factor and OAR in the next couple of weeks. 

# Information
1. Input Data: ROF and PDD from Rm2 for 6X and 10X (from GH)
2. ROF and PDD are 2D-interpolated with scipy.interpolate
2. Equivalent Square Field calculated from: 
[formula1](./Images/formula1.png)
3. Python source code is compiled with PyInstaller
