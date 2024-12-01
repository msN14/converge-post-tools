import os
import post as pt

# create output folder
outdir = "./plots/contours/"
if os.path.isdir(outdir) == False:
    os.mkdir(outdir)

# SECTION 01
# h5 file directory
indir = "../output"
# list files
dl = pt.listH5Files(indir)
# show file variables
pt.listH5variables(dl[-1])
# pt.listH5variablesWithInfo(dl[-1])
 
# velocity x
gx, gy, gv = pt.getGrid(file=dl[-1], var="VELOCITY_X", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.1f", "Velocity X [m/s]", outdir+"vx.png")
# cfl u
gx, gy, gv = pt.getGrid(file=dl[-1], var="CFL_U", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [0,1], 20, 10, "%1.1f", "CFL U", outdir+"cfl-u.png")
# pressure
gx, gy, gv = pt.getGrid(file=dl[-1], var="PRESSURE", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.1f", "Pressure [Pa]", outdir+"pressure.png")
# vorticity x
gx, gy, gv = pt.getGrid(file=dl[-1], var="VORTICITY_Z", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "Vorticity Z", outdir+"wz.png")
# y+
gx, gy, gv = pt.getGrid(file=dl[-1], var="YPLUS", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "Y+", outdir+"yplus.png")

# tke
gx, gy, gv = pt.getGrid(file=dl[-1], var="TKE", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "TKE", outdir+"tke.png")
# eps
gx, gy, gv = pt.getGrid(file=dl[-1], var="EPS", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "EPS", outdir+"eps.png")
# nut
gx, gy, gv = pt.getGrid(file=dl[-1], var="TURB_VISCOSITY", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.1e", "nu T", outdir+"nut.png")

# yh2
gx, gy, gv = pt.getGrid(file=dl[-1], var="EQUIV_RATIO", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [0,0.4], 20, 10, "%1.1f", "Equivalence Ratio", outdir+"phi.png")
# temperature
gx, gy, gv = pt.getGrid(file=dl[-1], var="TEMPERATURE", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "Temperature [K]", outdir+"temp.png")
# yh2
gx, gy, gv = pt.getGrid(file=dl[-1], var="MASSFRAC_H2", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.4f", "YH2", outdir+"yh2.png")
# yoh
gx, gy, gv = pt.getGrid(file=dl[-1], var="MASSFRAC_OH", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.4f", "YOH", outdir+"yoh.png")
# yh2
gx, gy, gv = pt.getGrid(file=dl[-1], var="MASSFRAC_H2O", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [gv.min(),gv.max()], 20, 10, "%1.4f", "YH2O", outdir+"yh2o.png")

# temperature
gx, gy, gv = pt.getGrid(file=dl[-1], var="TEMPERATURE", z=0, xyscale=125, sigma=2)
pt.contourfWithGrid(gy, gx, gv, [300,1500], 20, 13, "%1.0f", "Temperature [K]", outdir+"temp.png", draw='nozzle')


# Cross Plane Plot
# read the specified variable
# X, Y, Z, T = pt.readvar3dh5(dl[-1], "BAR.Y.OH", xyzscale=125)
# gx, gy, gv = pt.slice3dgetgrid(Y, Z, X, T, zslice=0, sigma=3)
# pt.contourfWithGrid(gx, gy, gv, [gv.min(),gv.max()], 20, 10, "%1.4f", "var", outdir+"var.png", draw='nil',cb=[0.3,1.02])

# template
# gx, gy, gv = pt.getGrid(file=dl[-1], var="var", z=0, xyscale=125, sigma=2)
# pt.contourfWithGrid(gx, gy, gv, [gv.min(),gv.max()], 20, 10, "%1.0f", "var", outdir+"var.png", draw='nil')

