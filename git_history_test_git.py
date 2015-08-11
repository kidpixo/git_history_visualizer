
# coding: utf-8

# In[7]:

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

# In[8]:

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

# In[9]:

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

# In[10]:

import matplotlib
from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[11]:

def plot_history_df(plot_df,**kwargs):

    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = 500
        
    if 'figsize' in kwargs:
        figsize = kwargs['figsize']
    else:
        figsize = [10,12]
        
    if 'linewidths' in kwargs:
        linewidths = kwargs['linewidths']
    else:
        linewidths = 3
        
    h = plot_df.applymap(lambda x: gt.def_states[x]).values.copy()
    h[h == gt.def_states['N']] = float('nan')

    fig = plt.figure(figsize=figsize)

    ax = plt.subplot(111)
    for i in range(len(plot_df.index)):
        x = range(len(plot_df.columns))
        y = [i for kk in x]
        ax.scatter(x, y, s = size, c=h[i,:], alpha=1, marker='o',linewidths = linewidths , cmap = plt.cm.spectral,vmin = 0, vmax = 255)
        ax.plot(x, y, lw = 3, c='k', zorder=0)

    ax.set_xticks(range(h.shape[1]))
    ax.set_xticklabels(plot_df.columns,rotation=90)

    ax.set_xlabel('commits sha-1 (time arrow to the right ->)')
    ax.set_xlim([-.5,len(plot_df.columns)-0.5])
    ax.set_ylabel('file names')
    ax.set_yticks(range(h.shape[0]))
    ax.set_yticklabels(plot_df.index.tolist())
    ax.set_yticks = 0.1
    # set 0 to bounding box width
    [i.set_linewidth(0.0) for i in ax.spines.itervalues()]
    # see http://stackoverflow.com/a/20416681/1435167
    # erase x ticks
    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    #     tic.label1On = tic.label2On = False
    # erase y ticks
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    #     tic.label1On = tic.label2On = False

    ax2 = fig.add_axes([0.25, .9, 0.5, 0.075])

    colors = [i if i != gt.def_states['N'] else float('nan') for i in gt.def_states.values()]

    x = range(len(colors))
    y = [1 for kk in x]
    ax2.scatter(x, y, s = size, c=colors, alpha=1, marker='o',linewidths = 3, cmap = plt.cm.spectral,vmin = 0, vmax = 255)
    ax2.plot(x, y, lw = 3, c='k', zorder=0)

    ax2.set_xticks(x)
    ax2.set_xticklabels(gt.def_states_explain.values())
    ax2.set_xlabel('Legend')
    ax2.set_xlim([-.5,len(x)-0.5])
    ax2.set_ylim([0.99,1.01])
    # set 0 to bounding box width
    [i.set_linewidth(0.0) for i in ax2.spines.itervalues()]
    # # see http://stackoverflow.com/a/20416681/1435167
    # erase x ticks
    for tic in ax2.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    # erase y ticks
    for tic in ax2.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False

    if 'outpath' in kwargs:
        fig.savefig(kwargs['outpath'],bbox_inches='tight', pad_inches=0)
        plt.close()


# In[12]:

gt.datamatrix
plot_history_df(gt.datamatrix,size= 300, figsize = [10,14])
plot_history_df(gt.datamatrix,size= 300, figsize = [10,14],outpath=path+os.sep+'images/complete_visual_history.png')


# In[13]:

# filtering the history on:
# a commit range
plot_df_commit_range = gt.datamatrix.ix[:,'a4cb9a1':'1222c5e']
plot_history_df(plot_df_commit_range,size= 300, figsize= [3,13])
plot_history_df(plot_df_commit_range,size= 300, figsize= [3,13], outpath=path+os.sep+'images/commit_range.png')


# In[14]:

# filtering the history on:
# a file range: all files not ending with txt
plot_df_file_range = gt.datamatrix[~gt.datamatrix.index.str.contains('txt$')]
plot_history_df(plot_df_file_range,size= 300, figsize= [10,11.5])
plot_history_df(plot_df_file_range,size= 300, figsize= [10,11.5], outpath=path+os.sep+'images/file_range.png')


# In[15]:

# filtering the history on:
# a commit range AND a file range: all files not ending with txt
plot_df_commit_file_range = gt.datamatrix.ix[:,'a4cb9a1':'1222c5e'][~gt.datamatrix.index.str.contains('txt$')]
plot_history_df(plot_df_commit_file_range,size= 300,figsize= [3,12])
plot_history_df(plot_df_commit_file_range,size= 300,figsize= [3,12],outpath=path+os.sep+'images/commit_file_range.png')


# In[16]:

# filtering the history on:
# a commit range AND a file range: all files not ending with txt
plot_df_state_filter = gt.datamatrix[gt.datamatrix[gt.datamatrix.columns[-1]] != 'N']
plot_history_df(plot_df_state_filter,size= 300,figsize= [10,10])
plot_history_df(plot_df_state_filter,size= 300,figsize= [10,10],outpath=path+os.sep+'images/state_filter.png')

