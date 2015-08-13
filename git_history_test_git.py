
# coding: utf-8

# In[18]:

import githistoryvis as ghv


# ### Gather the data
# 
# Githistoryvis exposes the class `git_history`.
# 
# The inizialization:
# 
# ```python
# foo = git_history(PATH)
# ```
# sets the attribute `foo.path` that point to the git respository in PATH.
# 
# Also `def_states` (and `def_states_explain`) are defined at inizialitation.
# They are used to transform the state in the dataframe to number for visualization and define the legend.
# 
# You can overwrite them at your own risk.
# 
# ```python
# def_states = {
#     'A' : 120.,
#     'M' : 180.,
#     'S' : 255., # custom value, Static
#     'D' : 240.,
#     'N' : 128., # custom value, Non existent
# }
# 
# def_states_explain = {
#     'A' : 'Added',
#     'D' : 'Deleted',
#     'M' : 'Modified',
#     'S' : 'Static',
#     'N' : 'Non existent'
# }
# ```
# 
# 
# The method
# 
# ```python
# foo.get_history()
# ```
# extracts the git log, and define:
# 
# - foo.all_commits = the whole git log
# - foo.commits     = the commits SHA-1
# - foo.all_files   = all the unique file ever existed
# 
# 

# In[19]:

import os

path =  os.getcwd() # put here the desired git repo path

gt = ghv.git_history(path)

gt.get_history()


# ### Visualize the data
# 
# We define a pandas DataFrame to contain all the files (Rows) and the status (Columns).
# 
# This Grid represent the status of each file at each step or commit.
# 
# The inizial stata for all the files is `N` or `Non existent`, they are updated in the sequential reding of `git_history.all_commits` object.

# ## Deserialize and structure the data
# 
# The data gather in `githistoryvis.git_history()` object are deserialized and gathered in a pandas DataFrame by the `githistoryvis.definedatamatrix()` method.

# In[20]:

gt.definedatamatrix()
gt.datamatrix


# ## Visualize the data
# 
# The data from the pandas DataFrame coul be visualized by this simple example routine.
# 
# The arguments are:
# 
# - size (default 200) : the size of the pyplot.scatteplot.
# - figsize (default [9,7]) : size of the pyplot.figure.
# - linewidths (default 3) : width of the pyplot.scatteplot outer lines.
# - outpath : if defined, the figure will be saved without visualization.

# In[21]:

import matplotlib
from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[22]:

gt.plot_history_df(plt,gt.datamatrix,size= 300, figsize = [12,10.5])
gt.plot_history_df(plt,gt.datamatrix,size= 300, figsize = [12,10.5],outpath=path+os.sep+'images/complete_visual_history.png')


# In[24]:

# filtering the history on:
# a commit range
plot_df_commit_range = gt.datamatrix.ix[:,'a4cb9a1':'1222c5e']
gt.plot_history_df(plt,plot_df_commit_range,size= 300, figsize= [3,10])
gt.plot_history_df(plt,plot_df_commit_range,size= 300, figsize= [3,10], outpath=path+os.sep+'images/commit_range.png')


# In[25]:

# filtering the history on:
# a file range: all files not ending with txt
plot_df_file_range = gt.datamatrix[~gt.datamatrix.index.str.contains('txt$')]
gt.plot_history_df(plt,plot_df_file_range,size= 300, figsize= [11.5,8.5])
gt.plot_history_df(plt,plot_df_file_range,size= 300, figsize= [11.5,8.5], outpath=path+os.sep+'images/file_range.png')


# In[26]:

# filtering the history on:
# a commit range AND a file range: all files not ending with txt
plot_df_commit_file_range = gt.datamatrix.ix[:,'a4cb9a1':'1222c5e'][~gt.datamatrix.index.str.contains('txt$')]
gt.plot_history_df(plt,plot_df_commit_file_range,size= 300,figsize= [3.5,8.5])
gt.plot_history_df(plt,plot_df_commit_file_range,size= 300,figsize= [3.5,8.5],outpath=path+os.sep+'images/commit_file_range.png')


# In[27]:

# filtering the history on:
# a commit range AND a file range: all files not ending with txt
plot_df_state_filter = gt.datamatrix[gt.datamatrix[gt.datamatrix.columns[-1]] != 'N']
gt.plot_history_df(plt,plot_df_state_filter,size= 300,figsize= [11,6])
gt.plot_history_df(plt,plot_df_state_filter,size= 300,figsize= [11,6],outpath=path+os.sep+'images/state_filter.png')

