# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:02:09 2019

@author: sibra
"""

## perform search on CREODIAS API
#set wd

import os, shutil
import json
import pandas as pd
import geojson

os.chdir('C:/Users/Administrator/Documents/ClujTrainingCourse_S5P')

#load local functions
from RestoSearch_S5P_Function import s5psearch
from Harp_Proc_Function import harpProc

#set date range
dates = pd.date_range(start='20191201', end='today')
#weekly timerange
dates = pd.date_range(start='20200112', end='today', freq = '2D')

#choose r5solution in degrees
res = 0.05
res = 0.25


# import json
geoj = 'aus.geojson'

proj_dir = f'''export_{geoj.split('.')[0]}'''

if os.path.exists(proj_dir):
    shutil.rmtree(proj_dir)
os.mkdir(proj_dir)

prod = 'L2__AER_AI'
#prod = 'L2__SO2___'
prod = 'L2__NO2___'
prod = 'L2__CO____'

#set export directory
exp_dir = f'{proj_dir}/{prod}'

if os.path.exists(exp_dir):
    shutil.rmtree(exp_dir)
os.mkdir(exp_dir)

#extract bbox values
with open(geoj) as f:
    aoi = json.load(f)
    
def Bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     return box

bb = Bbox(list(geojson.utils.coords(aoi)))

#daily averages
for i in dates:
    
    paths = s5psearch(geoj = geoj, dateSt = i, dateEnd = i, prod = prod)
    
    harpProc(pathlist = paths, prod = prod, bb = bb, res = res, dateSt = i, dateEnd = i, exp_dir = exp_dir)
    
    print(i)

#multi-day averages
for i in dates:
    
    paths = s5psearch(geoj = geoj, dateSt = i, dateEnd = (i + 1), prod = prod)
    
    harpProc(pathlist = paths, prod = prod, bb = bb, res = res, dateSt = i, dateEnd = (i + 1), exp_dir = exp_dir)
        
    print(i)
    
#attempt to run R script from Python    
def gif_creation(exp_dir):
    import subprocess
    subprocess.run(
            ["C:/Program Files/R/R-3.6.1/bin/Rscript.exe",  "Giff_creation_Function.R", exp_dir], 
                                  shell=True, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stderr 

gif_creation(exp_dir = exp_dir)


