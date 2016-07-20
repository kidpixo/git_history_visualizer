# This Python file uses the following encoding: utf-8


class git_history:
    """ Common base class for all git history.

        Inizialization:

        foo = git_history(PATH, get_history=False, definedatamatrix=False)

        Optionally, set get_history and  definedatamatrix to True
        to have all the process done in place, instead of calling
        each method.

        At the inizialitation the attribute self.path
        that point to the git respository in PATH.

        Also def_states (and def_states_explain) are defined
        at inizialitation. They are used to transform the state
        in the dataframe to number for visualization and define
        the legend. You can overwrite them at your own risk.

        # this is used as colorcode in the datamatrix
        def_states = {
            u'A': 120,
            u'C': 25,
            u'B': 51,
            u'D': 240,
            u'M': 180,
            u'R': 102,
            u'U': 204,
            u'T':  76,
            u'X': 153,
            u'S': 255,   # custom value, Static
            u'N': None,  # custom value, Non existent
        }

        # this is only a humand readable format
        def_states_explain = {
            u'A': u'added',
            u'C': u'copied',
            u'D': u'deleted',
            u'M': u'modified',
            u'R': u'renamed',
            u'T': u'type changed',
            u'U': u'unmerged',
            u'X': u'unknown',
            u'B': u'pairing broken',
            u'S': u'Static',
            u'N': u'Non existent'
        }


        Methods:

        The method

        foo.get_history([prettyformat='%h'],[gitcommitlist=False])

        extract the git log, and define:

        - foo.all_commits = the whole git log
        - foo.commits     = the commits SHA-1
        - foo.all_files   = all the unique file ever existed

        Arguments

        prettyformat, default %h

        optional, accept one of the git prettyformat, see
        http://git-scm.com/docs/pretty-formats.
        For example, get the whole commit text with '%s' and write
        your own parser for sel.decodelog().
        Deafault is '%h' of the short SHA-1 of the commit.

        gitcommitlist, default False

        optional, if present should be a string withthe result of:

        git -C PATH --no-pager log --reverse --name-status --oneline --pretty="format:COMMIT%x09%h"

        For example, execute this command in remote and store the result in a file,
        read the content

        with open('gitoutput', 'r') as file:
            data = file.read()

        and pass the result to get_history method:

        gt.get_history(gitcommitlist=data)


        Status

        From the official git-log Documentation, http://git-scm.com/docs/git-log
        for files status:

        - A : file **A**dded
        - D : file **D**eleted
        - M : file **M**odified
        - C : **C**opied
        - R : **R**enamed
        - T : **T**ype changed
        - U : **U**nmerged
        - X : unknown
        - B : pairing **B**roken


        Custom defined status:

        - S : file is **S**tatic (nothing happen)
        - N : file is **N**on existent

        See http://git-scm.com/docs/git-log :

        .......

        --diff-filter=[(A|C|D|M|R|T|U|X|B)…[*]]

        Select only files that are Added (A), Copied (C), Deleted (D),
        Modified (M), Renamed (R), have their type (i.e. regular file,
        symlink, submodule, …) changed (T), are Unmerged (U), are
        Unknown (X), or have had their pairing Broken (B). Any combination
        of the filter characters (including none) can be used. When *
        (All-or-none) is added to the combination, all paths are selected if
        there is any file that matches other criteria in the comparison;
        if there is no file that matches other criteria, nothing is selected.
        .......

    """
    def_states = {
        u'A': 120,
        u'C': 25,
        u'B': 51,
        u'D': 240,
        u'M': 180,
        u'R': 102,
        u'U': 204,
        u'T':  76,
        u'X': 153,
        u'S': 255,   # custom value, Static
        u'N': None,  # custom value, Non existent
    }

    def_states_explain = {
        u'A': u'added',
        u'C': u'copied',
        u'D': u'deleted',
        u'M': u'modified',
        u'R': u'renamed',
        u'T': u'type changed',
        u'U': u'unmerged',
        u'X': u'unknown',
        u'B': u'pairing broken',
        u'S': u'Static',
        u'N': u'Non existent'
    }

    def __init__(self, repo_path, get_history=False, definedatamatrix=False):
        self.path = repo_path
        if get_history:
            self.get_history()
        if definedatamatrix:
            self.definedatamatrix()

    def get_history(self, gitcommitlist=False, **kwargs):
        import re
        import subprocess

        if 'prettyformat' in kwargs:
            prettyformat = kwargs['prettyformat']
        else:
            prettyformat = "%h"

        if not gitcommitlist:
            # get the whole git history
            p = subprocess.check_output(['git -C "{}" --no-pager log --reverse --name-status --oneline --pretty="format:COMMIT\t{}"'.format(self.path, prettyformat)], shell=True, universal_newlines=True)
        else:
            p = gitcommitlist

        # import ipdb
        # ipdb.set_trace()

        # old list version
        # self.all_commits = [i.split('\t') for i in p.split('\n') if '\t' in i]

        # new iterator version
        self.all_commits = [i.group(0).split('\t') for i in re.finditer(r'[^\r\n]+', p) if '\t' in i.group(0)]

        self.decodelog()

    def decodelog(self):
        # get all the commits SHA-1
        self.commits = [i[1] for i in self.all_commits if i[0] == 'COMMIT']

        # get all the file in the history
        self.all_files = sorted(set([i[1] for i in self.all_commits if i[0] != 'COMMIT']))

    def definedatamatrix(self):
        import pandas as pd

        all_filenames = pd.DataFrame(columns=self.commits, index=self.all_files)

        # fill NaN
        all_filenames.fillna('N', inplace=True)

        actual_commit = previous_commit = 0

        for i in self.all_commits:
            # set the commit number
            state, commit_label = i
            if state == 'COMMIT':
                commit_label_len = len(commit_label)
                # print '-'*(commit_label_len+5)+'+'+'-'*30
                # print '>', state, commit_label,
                # starting at the second commit see which file exist in the previous commit
                tmp_commit = commit_label
                if tmp_commit != all_filenames.columns[0]:
                    previous_commit = actual_commit
                actual_commit = tmp_commit
                # assig 1 to file not null un the previous commit
                if previous_commit != 0:
                    all_filenames[actual_commit][
                        (all_filenames[previous_commit] != 'N') & (all_filenames[previous_commit] != 'D')] = 'S'
                # print  "| previous %s : actual %s" % (previous_commit, actual_commit)
            else:
                all_filenames.ix[commit_label, actual_commit] = state
                # print ' '*(commit_label_len+4), '|', state, commit_label
        self.datamatrix = all_filenames.apply(lambda x: x.astype('category'))

    def plot_history_df(self, plt, dataframe, **kwargs):
        """
        Visualize the data

        The data from the pandas DataFrame in self.datamatrix could be visualized by this simple example routine.
        The arguments are:

        - plt : the imported name of matplotlib.pyplot.
        - size (default 200) : the size of the pyplot.scatteplot.
        - figsize (default [9, 7]) : size of the pyplot.figure.
        - linewidths (default 3) : width of the pyplot.scatteplot outer lines.
        - outpath : if defined, the figure will be saved without visualization.
        - legend : if defined to any value, will show a bad legend.
        """
        if 'size' in kwargs:
            size = kwargs['size']
        else:
            size = 500

        if 'figsize' in kwargs:
            figsize = kwargs['figsize']
        else:
            figsize = [10, 12]

        if 'linewidths' in kwargs:
            linewidths = kwargs['linewidths']
        else:
            linewidths = 3

        h = dataframe.applymap(lambda x: self.def_states[x]).values.copy()

        fig = plt.figure(figsize=figsize)

        ax = plt.subplot(111, frameon=False)
        for i in range(len(dataframe.index)):
            x = range(len(dataframe.columns))
            y = [i for kk in x]
            ax.scatter(x, y, s=size, c=h[i, :], alpha=1, marker='o', linewidths=linewidths, cmap=plt.cm.spectral, vmin=0, vmax=255)
            ax.plot(x, y, lw=3, c='k', zorder=0, linewidth=linewidths)

        ax.set_xticks(range(h.shape[1]))
        ax.set_xticklabels(dataframe.columns, rotation=90)

        ax.set_xlabel('commits sha-1 (time arrow to the right ->)')
        ax.set_xlim([-.5, len(dataframe.columns)-0.5])
        ax.set_ylabel('file names')
        ax.set_ylim([-.5, len(dataframe.index)+0.5])
        ax.tick_params(axis='both', which='both', length=0, width=0)

        ax.set_yticks(range(h.shape[0]))
        ax.set_yticklabels(dataframe.index.tolist())
        ax.set_yticks = 0.1

        if 'legend' in kwargs:
            xsize, ysize = fig.get_size_inches()
            w = 0.3
            l = (1.-w)/2.
            ax2 = fig.add_axes([(1.-w)/2., -.01, w, 0.035], frameon=False)

            colors = [i if i != self.def_states['N'] else float('nan') for i in self.def_states.values()]

            x = range(len(colors))
            y = [1 for kk in x]
            ax2.scatter(x, y, s=size, c=colors, alpha=1, marker='o', linewidths=linewidths, cmap=plt.cm.spectral, vmin=0, vmax=255)
            ax2.plot(x, y, lw=3, c='k', zorder=0, linewidth=linewidths)

            ax2.set_xticks(x)
            ax2.set_xticklabels(self.def_states_explain.values())
            ax2.set_xlabel('Legend')
            ax2.set_xlim([-.5, len(x)-0.5])
            ax2.set_ylim([0.99, 1.01])
            ax2.tick_params(axis='both', which='both', length=0, width=0, labelleft='off')

        if 'outpath' in kwargs:
            fig.savefig(kwargs['outpath'], bbox_inches='tight', pad_inches=0)
            plt.close()
