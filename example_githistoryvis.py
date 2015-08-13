# coding: utf-8
import githistoryvis as ghv

# put here the desired git repo path
import os
path =  os.getcwd()

# define the obejct linked to your repository
gt = ghv.git_history(path)
# get the history
gt.get_history()
# define the datamatrix
gt.definedatamatrix()

# visualization
import matplotlib
from matplotlib import pyplot as plt

# play wiht size and figsize to find yours
gt.plot_history_df(plt,gt.datamatrix,size= 300, figsize = [12,10.5],outpath=path+os.sep+'images/complete_visual_history.png')
