#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot all data from ALHIC2302 Shallow Cores

@author: Liam
"""

#%% 
# Import packages 

# general
import numpy as np
import pandas as pd

# plotting
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# my functions/classes
import sys
sys.path.append("../core_scripts/")
from ECMclass import ECM

#%% 
# User Inputs

# smoothing window, mm
window = 10

# paths
path_to_data = '../../data/'
path_to_figures = '../../../figures/basic_plots/alhic2302/'
metadata_file = 'metadata.csv'

# make colormap
my_cmap = matplotlib.colormaps['Spectral']

#%%
# Read in metadata and import data

meta = pd.read_csv(path_to_data+metadata_file)

# import each script as an ECM class item
data = []
cores = []
sections = []
faces = []
ACorDCs = []
for index,row in meta.iterrows():
    
    core = row['core']
    
    # filter for ALHIC2302 shallow ice
    if core == 'alhic2302':
        
        # pull out metadata
        section = row['section']
        face = row['face']
        ACorDC = row['ACorDC']
        print("Reading "+core+", section "+section+'-'+face+'-'+ACorDC)
        # read in data
        data_item = ECM(core,section,face,ACorDC)
        # remove last 10mm from either end
        data_item.rem_ends(10)
        # normalize outside tracks
        data_item.norm_outside()
        # apply smoothing (at specified window)
        data_item.smooth(window)
        #add to list
        data.append(data_item)
        cores.append(core)
        sections.append(section)
        faces.append(face)
        ACorDCs.append(ACorDC)

# make sections into set (remove duplicates)
sec = set(sections)

#%% 
# define plotting function
def plotquarter(y_vec,ycor,d,meas,button,axs,rescale):
    
    width = y_vec[1] - y_vec[0]
    
    for y in y_vec:
        
        
        idx = ycor==y
        
        tmeas = meas[idx]
        tbut = button[idx]
        tycor = ycor[idx]
        td = d[idx]
        
        for i in range(len(tmeas)-1):
            
            if tbut[i] == 0:
                
                axs.add_patch(Rectangle((y-(width-0.2)/2,td[i]),(width-0.2),td[i+1]-td[i],facecolor=my_cmap(rescale(tmeas[i]))))
            else:
                axs.add_patch(Rectangle((y-(width-0.2)/2,td[i]),(width-0.2),td[i+1]-td[i],facecolor='k'))
            
    return()

#%% 
# define function to find unique elements in list
def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    
    return(unique_list)



#%% 
# plot each section

# loop through sections
for sec in unique(sections):

    # print update
    print("Running Section "+sec)
    
    # set data to empty
    AC_t = None
    AC_l = None
    DC_t = None
    DC_l = None
    #loop through data 
    for d in data:
        
        # find faces
        if d.core=='alhic2302':
            if d.section==sec:
                if d.ACorDC == 'AC':
                    if d.face == 't':
                        AC_t = d
                    if d.face == 'l':
                        AC_l = d                    
                else:
                    if d.face == 't':
                        DC_t = d
                    if d.face == 'l':
                        DC_l = d
    
    # find depth max and minimum
    minvec = []
    maxvec = []
    AC_all = []
    DC_all = []
    for data_face in [AC_t,AC_l,DC_t,DC_l]:
        if data_face != None:
            minvec.append(min(data_face.depth))
            maxvec.append(max(data_face.depth))
            
            if data_face.ACorDC == 'AC':
                AC_all.extend(data_face.meas)
            else:
                DC_all.extend(data_face.meas)
    ACpltmin = np.percentile(AC_all,5)
    ACpltmax = np.percentile(AC_all,95)
    DCpltmin = np.percentile(DC_all,5)
    DCpltmax = np.percentile(DC_all,95)  
    ACrescale = lambda k: (k-ACpltmin) /  (ACpltmax-ACpltmin)
    DCrescale = lambda k: (k-DCpltmin) /  (DCpltmax-DCpltmin)
    dmin = min(minvec)
    dmax = max(maxvec)
    
   
    # make figure
    fig, ax = plt.subplots(1, 5, gridspec_kw={'width_ratios': [3, 3,2, 3, 3]},figsize=(9,6),dpi=200)
    
    # top-specific
    for a in [ax[0],ax[3]]:
        #a.yaxis.tick_right()
        a.set_xlim([120, 0])
        
    # right specific
    for a in [ax[1],ax[4]]:
        a.yaxis.tick_right()
        a.yaxis.set_label_position("right")
        a.set_xlim([0,120])
        
    # applies to all
    for a in [ax[0],ax[1],ax[3],ax[4]]:
        a.set_ylabel('Depth (m)')
        a.set_xlabel('Distance From Center (mm)',fontsize=6)
        a.set_ylim([dmax, dmin])
        
        
    for a,data_face in zip([ax[1],ax[0],ax[4],ax[3]],[AC_l,AC_t,DC_l,DC_t]):
        
        if data_face != None:
            if data_face.face == 'l':
                yall = data_face.y_right - data_face.y_s
                yvec = data_face.y_right -  data_face.y_vec
            else:
                yall = data_face.y_s -  data_face.y_left
                yvec =data_face.y_vec -  data_face.y_left
            
            if data_face.ACorDC =='AC':
                rescale = ACrescale
            else:
                rescale = DCrescale
        
        
            # plot data
            plotquarter(yvec,
                        yall,
                        data_face.depth_s,
                        data_face.meas_s,
                        data_face.button_s,
                        a,
                        rescale)
    
    # housekeeping
    fig.suptitle('ALHIC2302 - '+sec+' - '+str(window)+' mm smooth')
    ax[2].axis('off')
    ax[1].set_title('AC - Left')
    ax[0].set_title('AC - Top')
    ax[4].set_title('DC - Left')
    ax[3].set_title('DC - Top')
    
    fig.tight_layout()
    plt.subplots_adjust(wspace=0)

    # ad colorbar
    #fig.subplots_adjust(bottom=0.8)
    #    ACcbar_ax = fig.add_axes([0.08,-0.07,0.35,0.05])
    ACcbar_ax = fig.add_axes([0.07,-0.05,0.35,0.05])
    ACnorm = matplotlib.colors.Normalize(vmin=ACpltmin,vmax=ACpltmax)
    DCcbar_ax = fig.add_axes([0.58,-0.05,0.35,0.05])
    DCnorm = matplotlib.colors.Normalize(vmin=DCpltmin,vmax=DCpltmax)
    ACcbar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=ACnorm, cmap=my_cmap),cax=ACcbar_ax,
                    orientation='horizontal',label='Current (amps)')
    DCcbar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=DCnorm, cmap=my_cmap),cax=DCcbar_ax,
                    orientation='horizontal',label='Current (amps)')
    
    # save figure
    fname = path_to_figures +'alhic2302-'+sec+'.png'
    fig.savefig(fname,bbox_inches='tight')
    plt.close(fig)