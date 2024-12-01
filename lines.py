import os
import post as pt
# import numpy as np
import matplotlib.pyplot as plt

plt.style.use('./one.mplstyle')

# create output folder
outdir = "./plots/lines/"
if os.path.isdir(outdir) == False:
    os.mkdir(outdir)

indir = "../stream0/"

file = "mass_balance.out"
di = pt.readoutfile2dic(indir+file)
x, y = di["Time(seconds)(none)"], di["Net_Mass_Flow_Rate(kg/s)(none)"]
pt.lineplot(1, x, y, "Time [s]", "Net Mass Flow Rate [kg/s]", "MFR", outdir+"net-mfr.png")

file = "turbulence.out"
di = pt.readoutfile2dic(indir+file)
x1, y1 = di["Time(seconds)"], di["TKE(m^2/s^2)"]
x2, y2 = di["Time(seconds)"], di["EPS(m^2/s^3)"]
pt.lineplot(2, x1, y1, "Time [s]", "TKE [$m^2/s^2$]", "TKE", outdir+"tke.png")
pt.lineplot(3, x2, y2, "Time [s]", "EPS [$m^2/s^3$]", "EPS", outdir+"eps.png")

file = "thermo.out"
di = pt.readoutfile2dic(indir+file)
x1, y1 = di["Time(seconds)"], di["Mean_Temp(K)"]
x2, y2 = di["Time(seconds)"], di["HR_Rate(J/s)"]
pt.lineplot(4, x1, y1, "Time [s]", "Mean Temperature (Space) [K]", "Avg T", outdir+"avg-temp-space.png")
pt.lineplot(5, x2, y2, "Time [s]", "HR Rate [J/s]", "HR Rate", outdir+"hr-rate.png")

file = "statistics.out"
di = pt.readoutfile2dic(indir+file)
x1, y1 = di["Time(seconds)"], di["BAR.U_Mean(m/s)"]
x2, y2 = di["Time(seconds)"], di["BAR.T_Mean(K)"]
pt.lineplot(6, x1, y1, "Time [s]", "Mean Temperature (Time) [K]", "T Mean", outdir+"mean-temp-time.png")
pt.lineplot(7, x2, y2, "Time [s]", "Mean U (Time) [m/s]", "Mean U", outdir+"mean-u.png")

file = "species_mass.out"
di = pt.readoutfile2dic(indir+file)
x, y = di["Time(seconds)"], di["H2O(kg)"]
pt.lineplot(8, x, y, "Time [s]", "Mass H2O [kg]", "H2O", outdir+"mass-h2o.png")

file = "time.out"
di = pt.readtimeoutfile2dic(indir+file)

x1, y1 = di["Time(seconds)"], di["dt(seconds)"]
x2, y2 = di["Time(seconds)"], di["Max_CFL(none)"]
pt.lineplot2(9, x1, y1, "Time [s]", "dt [s]", "dt", outdir+"dt.png")
pt.lineplot2(10, x2, y2, "Time [s]", "Max. CFL", "CFL", outdir+"max-cfl.png")



