# Postprocessing Converge CFD Simulation Data

## Contour Plots

Files are:
    - .h5 files in "/outputs_original/output"
    
Variables are:
    1. Velocity
    2. Vorticity
    3. Pressure
    4. Turbulence (TKE, TDR, etc.)

Categories are:
    - Means
    - Instantaneous 
    - Calculated

## Line Plots

Files are:
    - .out files in "/outputs_original/stream0/"

- mass_balance.out
    - Net_Mass_Flow_Rate
- turbulence.out
    - TKE
    - EPS
- thermo.out
    - Mean_Temp
    - HR_Rate
- statistics.out
    - BAR.U_mean
    - BAR.T_mean
- species_mass.out
    - H2O
    
    
## Note issues and resolutions

- glob based files list is not sorted, so use sorted() to sort the list of files.

- there are some .out files with end column contains strings and inhomgeneous
  columns when split with space. - cut with specific column number for time.out file.
  
- 
    

