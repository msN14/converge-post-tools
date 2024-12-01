# imports
import os
import numpy as np
import h5py
import glob

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# import matplotlib.patches as patches
# import matplotlib.tri as tri
from scipy.interpolate import griddata

# load plot style file
plt.style.use('./one.mplstyle')

# create output folder
if os.path.isdir('./plots') == False:
    os.mkdir('./plots')

# Functions for 2D Contour Plots

# Function : list all h5 files and sort
def listH5Files(directory):
    files = glob.iglob(directory+'/*.h5')
    F = []
    for f in files:
        F.append(f)
    F = sorted(F)
    print("\n# List of h5 files:\n", F, "\n")
    return (F)

# Function : list the h5 file entries
def listH5variables(filename):
    f = h5py.File(filename, 'r')  # replace with your file name and mode
    def print_node(name):
        print(f"{name}")
    print("\n# List of h5 file variables:")   
    f.visit(print_node)

def listH5variablesWithInfo(filename):
    f = h5py.File(filename, 'r')  # replace with your file name and mode
    def print_node(name, obj):
        print(f"{name}: {type(obj).__name__}")
        if isinstance(obj, h5py.Dataset):
            print(f"  Shape: {obj.shape}")
            print(f"  Dtype: {obj.dtype}")
        elif isinstance(obj, h5py.Group):
            print(f"  Attributes: {list(obj.attrs.keys())}")
    print("\n# List of h5 file variables with detailed information:") 
    f.visititems(print_node)
    
# Function : read a variable from 3D h5 file
def readvar3dh5(filename, variable, xyzscale):
    # varible in h5 file name 
    # Temp = "TEMPERATURE"
    f = h5py.File(filename, 'r') 

    X = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_X"])*xyzscale
    Y = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_Y"])*xyzscale
    Z = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_Z"])*xyzscale
    V = np.array(f["STREAM_00"]["CELL_CENTER_DATA"][variable])
    
    return (X, Y, Z, V)


# Function : create grid data and smooth the results for a slice

def slice3dgetgrid(X, Y, Z, V, zslice, sigma):
    x1, y1, z1 = np.meshgrid(np.unique(X), np.unique(Y), np.unique(Z))
    # creating interpolation of the variable
    t1 = griddata((X, Y, Z), V, (x1, y1, z1), method='nearest') # nearest linear cubic

    # slice the data for 2D plot
    gx = x1[:,:,zslice]
    gy = y1[:,:,zslice]
    g = t1[:,:,zslice]

    # from scipy.interpolate import SmoothBivariateSpline
    # z1 = SmoothBivariateSpline((X, Y), T, (x1, y1))

    # contour smoothening using gaussian filter
    from scipy.ndimage import gaussian_filter
    # Apply Gaussian filtering
    sigma = sigma  # adjust the smoothing parameter
    gv = gaussian_filter(g, sigma)
    
    print("\nGrid data ranges:")
    print("\nX data: ", "min. = ", gx.min(), "\tmax. = ", gx.max())
    print("Y data: ", "min. = ", gy.min(), "\tmax. = ", gy.max())
    print("V data: ", "min. = ", gv.min(), "\tmax. = ", gv.max())
    
    return (gx, gy, gv)

def getGrid(file, var, z, xyscale, sigma):
    # varible in h5 file name 
    # Temp = "TEMPERATURE"
    f = h5py.File(file, 'r') 

    X = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_X"])*xyscale
    Y = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_Y"])*xyscale
    Z = np.array(f["STREAM_00"]["CELL_CENTER_DATA"]["XCEN_Z"])*xyscale
    V = np.array(f["STREAM_00"]["CELL_CENTER_DATA"][var])
    
    x1, y1, z1 = np.meshgrid(np.unique(X), np.unique(Y), np.unique(Z))
    # creating interpolation of the variable
    t1 = griddata((X, Y, Z), V, (x1, y1, z1), method='nearest') # nearest linear cubic

    # slice the data for 2D plot
    gx = x1[:,:,z]
    gy = y1[:,:,z]
    g = t1[:,:,z]

    # from scipy.interpolate import SmoothBivariateSpline
    # z1 = SmoothBivariateSpline((X, Y), T, (x1, y1))

    # contour smoothening using gaussian filter
    from scipy.ndimage import gaussian_filter
    # Apply Gaussian filtering
    sigma = sigma  # adjust the smoothing parameter
    gv = gaussian_filter(g, sigma)
    
    print("\n# Grid data ranges:")
    print("\nX data: ", "min. = ", gx.min(), "\tmax. = ", gx.max())
    print("Y data: ", "min. = ", gy.min(), "\tmax. = ", gy.max())
    print("V data: ", "min. = ", gv.min(), "\tmax. = ", gv.max())
    
    return (gx, gy, gv)

def contourfWithGrid(gx, gy, gv, limits, lev, tickslev,cbformat,labelName, filename, draw='nozzle', cb=[0.3,1.08]):
    fig, ax = plt.subplots(1, figsize=(12,12), constrained_layout=True)
    # fig, ax = plt.subplots()
    # levels = np.linspace(gv.min(), gv.max(), lev)
    levels = np.linspace(limits[0], limits[1], lev)
    # tcf = ax.contour(x1, y1, z2, levels=10, cmap = 'RdBu_r')
    tcf = ax.contourf(gx, gy, gv, levels=levels, cmap = 'RdBu_r', extend='both')

    # -- plotting using imshow
    # ax.imshow(p[500], cmap='viridis', origin='lower')

    # -- removing white intersection lines
    for c in tcf.collections:
        c.set_edgecolor("face")
        
    # -- color bar configuration
    cw, cp = cb[0], cb[1] #cbar input relative to ax
    axins = inset_axes(ax,
        # width="6%",  # width = 5% of parent_bbox width
        # width=0.3,
        width=cw,
        height="100%",  # height : 50%
        loc='lower left',
        # [left, bottom, width, height], or [left, bottom]
        # bbox_to_anchor=(1.08, 0., 1, 1), #1.02
        bbox_to_anchor=(cp, 0., 1, 1), #1.02
        bbox_transform=ax.transAxes,
        borderpad=0
        )

    # bar formates = '% 1.1f' '%.2e'
    # bar_value_format = '%1.0f'        # '% 1.4f' # '%.2e'
    bar_value_format = cbformat        # '% 1.4f' # '%.2e'
    # ticks = None
    # ticks = np.linspace(limits[0], limits[1], tickslev)
    ticks = np.linspace(levels.min(), levels.max(), tickslev)
    # ticks = [300,1500]
    cbar = fig.colorbar(tcf, cax=axins, format=bar_value_format, ticks=ticks, label = labelName)
    # cbar = fig.colorbar(tcf)
    # cbar = fig.colorbar(tcf, ax=ax)
    # cbar.ax.yaxis.set_tick_params(pad=2)
    cbar.ax.tick_params(labelsize=16)
    cbar.ax.tick_params(axis='both', which='minor', left=False, right=False, direction='out')
    cbar.ax.tick_params(axis='both', which='major', left=False, right=True, direction='out')

    # # -- scale the figure
    # ax.axis('scaled')
    ax.set_aspect('equal', adjustable='box', anchor='C')
    # ax.set_aspect('equal', anchor='C')

    ax.tick_params(axis='both', which='minor', left=False, right=False)
    ax.tick_params(axis='both', which='minor', top=False, bottom=False)
    ax.tick_params(axis='both', which='major', bottom=True, left=True, direction='out')
    
    if draw=='nozzle':
        # ax.axvline(x=0.5, ymin=0, ymax=0.1, color='b')  # draw a blue vertical line at x=3
        ax.vlines(x=-0.5, ymin=gy.min(), ymax=1, colors='k', linewidth=5)
        ax.vlines(x=0.5, ymin=gy.min(), ymax=1, colors='k', linewidth=5)
        # ax.set_xlim([0,0.3*125])
        # ax.set_ylim([-0.05*125,0.05*125])

    # fig.savefig('a.pdf', dpi=200, bbox_inches='tight')
    # fig.savefig(spath+name+'.svg', dpi=200, bbox_inches='tight')
    # fig.savefig('a.png', dpi=200, bbox_inches='tight')
    print("\n# Contour plot saved !")
    fig.savefig(filename, dpi=300)


# Functions for 2D Line Plots

# read out file into a dictionary with variable names as keys and data as items
def readoutfile2dic(filename):
    with open(filename,'r') as i:
        lines = i.readlines()
        n = 1
        Head = []
        Data = []
        for l in lines:
            if n == 3: # variable names
                var = l.strip().split()[1:]
                # print(var)
                Head.append(var)
            if n == 4: # variable units
                units = l.strip().split()[1:]
                # print(units)
                Head.append(units)
            if n == 5 and len(l) > 2: # variable location
                # print(len(l))
                loc = l.strip().split()[1:]
                # print(loc)
                Head.append(loc)
            if l[0] != '#': # data for each variable
                # l1 = l.strip().split("   ")
                data = l.strip().split()
                # print(l1)
                Data.append(data)
                # to solve time.out last column issue
                # Data.append(data[0:len(var)])
            n = n + 1
        # columns of headers
        Head = np.array(Head).T
        # R = np.char.join('', Head[0])
        Head2 = []
        # merging all header lines for each column
        for i in range(Head.shape[0]):
            j = 0
            A = ''
            for j in range(Head.shape[1]):
                A = A + '' + Head[i,j]
                j = j + 1
                # print(j, A)
            i = i + 1
            # print(A)
            Head2.append(A)
        Head = np.array(Head2)
            
    # # columns of data
    Data = np.array(Data).T
    
    di = {}
    i = 0
    for i in range(Data.shape[0]):
        # print (i)
        # di[Head[i,0]] = np.float64(Data[i])
        di[Head[i]] = np.float64(Data[i])
        i = i + 1
    print("\nKeys = ", di.keys(), "\n")
    return (di)

def readtimeoutfile2dic(filename):
    with open(filename,'r') as i:
        lines = i.readlines()
        n = 1
        Head = []
        Data = []
        for l in lines:
            if n == 3: # variable names
                var = l.strip().split()[1:]
                # print(var)
                Head.append(var)
            if n == 4: # variable units
                units = l.strip().split()[1:]
                # print(units)
                Head.append(units)
            if n == 5 and len(l) > 2: # variable location
                # print(len(l))
                loc = l.strip().split()[1:]
                # print(loc)
                Head.append(loc)
            if l[0] != '#': # data for each variable
                # l1 = l.strip().split("   ")
                data = l.strip().split()
                # print(l1)
                # Data.append(data)
                # to solve time.out last column issue
                Data.append(data[0:len(var)-1])
            n = n + 1
        # columns of headers
        Head = np.array(Head).T
        # R = np.char.join('', Head[0])
        Head2 = []
        # merging all header lines for each column
        for i in range(Head.shape[0]):
            j = 0
            A = ''
            for j in range(Head.shape[1]):
                A = A + '' + Head[i,j]
                j = j + 1
                # print(j, A)
            i = i + 1
            # print(A)
            Head2.append(A)
        Head = np.array(Head2)
            
    # # columns of data
    Data = np.array(Data).T
    
    di = {}
    i = 0
    for i in range(Data.shape[0]):
        # print (i)
        # di[Head[i,0]] = np.float64(Data[i])
        di[Head[i]] = np.float64(Data[i])
        i = i + 1
    print("\nKeys = ", di.keys(), "\n")
    return (di)


# plot line plot 

# lines and solid marker plots
def lineplot(num, x, y, xlabel, ylabel, leglabel, filename):
    # create line plot
    fig, ax1 = plt.subplots(num=num,figsize=(10,6), constrained_layout=True)
        
    ax1.plot(x, y, "ko-", linewidth=1, markersize=8, 
              markeredgewidth=1, markerfacecolor='black', label=leglabel)
    
    # ax1.set_xlabel("$\phi_{main}$")
    # ax1.set_ylabel("$\mathrm{EINO_x}$ [g/kg fuel]")
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    # ax1.set_xlim(-0.03, 0.63)
    # ax1.set_ylim(0.15, 0.60)
    # ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    # ax1.legend(loc='lower right')
    # ax1.set_xticklabels(J)
    ax1.grid(True, linestyle=(0, (5, 5)))
    # ax1.tick_params(axis='both', which='major', direction='inout')
    
    fig.savefig(filename)

# lines only plots
def lineplot2(num, x, y, xlabel, ylabel, leglabel, filename):
    # create line plot
    fig, ax1 = plt.subplots(num=num,figsize=(10,6), constrained_layout=True)
        
    ax1.plot(x, y, "k-", linewidth=1, markersize=8, 
              markeredgewidth=1, markerfacecolor='black', label=leglabel)
    
    # ax1.set_xlabel("$\phi_{main}$")
    # ax1.set_ylabel("$\mathrm{EINO_x}$ [g/kg fuel]")
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.grid(True)
    # ax1.set_xlim(-0.03, 0.63)
    # ax1.set_ylim(0.15, 0.60)
    # ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    # ax1.legend(loc='lower right')
    # ax1.set_xticklabels(J)
    ax1.grid(True, linestyle=(0, (5, 5)))
    # ax1.tick_params(axis='both', which='major', direction='inout')
    
    fig.savefig(filename)