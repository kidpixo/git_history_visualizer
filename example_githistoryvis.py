# coding: utf-8
import githistoryvis as ghv

# put here the desired git repo path
import os
path = os.getcwd()

# define the obejct linked to your repository
# essentially add the gt.path variable
gt = ghv.git_history(path)
# get the history : define gt.all_commits, gt.commit, gt.all_file
gt.get_history()

# if the git log data are in a file somewhere,
# read the file in a string and pass it
with open('gitoutput', 'r') as file:
    data = file.read()
gt.get_history(gitcommitlist=data)

# Here is Pandas needed
# define the datamatrix : define gt.datamatrix,
# a Pandas.Dataurame with categorical columns
gt.definedatamatrix()

# new compact version
gt = ghv.git_history(path, get_history=True, definedatamatrix=True)

# visualization
import matplotlib
from matplotlib import pyplot as plt

# play wiht size and figsize to find yours
gt.plot_history_df(plt, gt.datamatrix, size=300, figsize=[12, 10.5], outpath=path+os.sep+'images/complete_visual_history.png')
