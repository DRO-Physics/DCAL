# DCAL

This contain the source code and executable of the new DCAL. 

# Physics 
1. Input Data: ROF and PDD from Rm2 for 6X and 10X (from GH)
2. ROF and PDD are 2D-interpolated with scipy.interpolate
2. Equivalent Square Field calculated from: 

<p align="center">
  <img src="./Images/formula1.png" />
</p>

3. TMR is calculated using the formula from Khan Medical Physics Eqn. (10.4)

<p align="center">
  <img src="./Images/formula2.png" />
</p>

4. The MU for SAD setting is calculated using formula fromKhan Medical Physics Eqn. (10.13)

<p align="center">
  <img src="./Images/formula3.png" />
</p>

# Software
This is written using python. The GUI is constructed with pysimplegui and compiled with pyinstaller module. There are two main modes of distribution. One is a single exe file but is slow to start up due to unpacking of dependency to TEMP folder (could be worsen with anti-virus scanning through each file). The second is an exe with a host of dependency files. This is faster but file size is larger. The GUI is the main reason for the huge dependency library. If only Console exe is required, a single exe file will be way faster. 

# To-do Lists: 
1) Include SSD set-up
2) Include Wedge Factor
3) Include OAR
