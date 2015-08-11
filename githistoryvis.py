# This Python file uses the following encoding: utf-8
import subprocess

class git_history:
    """ Common base class for all git history.

        Inizialization:

        foo = git_history(PATH)

        At the inizialitation the attribute self.path
        that point to the git respository in PATH.

        Also def_states (and def_states_explain) are defined
        at inizialitation. They are used to transform the state
        in the dataframe to number for visualization and define
        the legend. You can overwrite them at your own risk.

        def_states = {
            'A' : 120.,
            'M' : 180.,
            'S' : 255., # custom value, Static
            'D' : 240.,
            'N' : 128., # custom value, Non existent
        }

        def_states_explain = {
            'A' : 'Added',
            'D' : 'Deleted',
            'M' : 'Modified',
            'S' : 'Static',
            'N' : 'Non existent'
        }


        Methods:

        The method

        foo.get_history([prettyformat='%h'])

        extract the git log, and define:

        - foo.all_commits = the whole git log
        - foo.commits     = the commits SHA-1
        - foo.all_files   = all the unique file ever existed

        Prettyformat
        This is optional, you can define one of the git
        prettyformat from http://git-scm.com/docs/pretty-formats.
        I can for example get the whole commit text and write your
        own parser for sel.decodelog().
        Deafault is '%h' of the short SHA-1 of the commit.

        Status

        From the official git-log Documentation, http://git-scm.com/docs/git-log
        for files status:

        - A : file **A**dded
        - D : file **D**eleted
        - M : file **M**odified

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
        'A' : 120.,
        'M' : 180.,
        'S' : 255., # custom value, Static
        'D' : 240.,
        'N' : 128., # custom value, Non existent
    }

    def_states_explain = {
        'A' : 'Added',
        'D' : 'Deleted',
        'M' : 'Modified',
        'S' : 'Static',
        'N' : 'Non existent'
    }

    def __init__(self, repo_path):
        self.path = repo_path

    def get_history(self,**kwargs):
        if 'prettyformat' in kwargs:
            prettyformat = kwargs['prettyformat']
        else:
            prettyformat = "%h"

        # get the whole git history
        p = subprocess.check_output(
            ["git -C "+self.path+""" --no-pager log --reverse --name-status --oneline --pretty='format:C\t'"""+prettyformat]
            , shell=True, universal_newlines=True)
        # now it is truly pythonic not dependant from machine beneath, as long as git command is available
        self.all_commits = [i.split('\t') for i in p.split('\n') if '\t' in i]

        self.decodelog()

    def decodelog(self):
        # get all the commits SHA-1
        self.commits = [i[1] for i in self.all_commits if i[0] == 'C']

        # get all the file in the history
        self.all_files = sorted(set([i[1] for i in self.all_commits if i[0] != 'C']))

    def definedatamatrix(self):
        import pandas as pd

        all_filenames = pd.DataFrame(pd.DataFrame(list(self.all_files)),columns=self.commits, index=self.all_files)

        # fill NaN
        all_filenames.fillna('N', inplace=True)

        actual_commit = previous_commit = 0

        for i in self.all_commits:
            # set the commit number
            state,commit_label = i
            if state == 'C':
                commit_label_len = len(commit_label)
                #print '-'*(commit_label_len+5)+'+'+'-'*30
                #print '>',state,commit_label,
                # starting at the second commit see which file exist in the previous commit
                tmp_commit = commit_label
                if tmp_commit != all_filenames.columns[0]:
                    previous_commit = actual_commit
                actual_commit = tmp_commit
                # assig 1 to file not null un the previous commit
                if previous_commit != 0:
                    all_filenames[actual_commit][
                        (all_filenames[previous_commit] != 'N') & (all_filenames[previous_commit] != 'D')] = 'S'
                #print  "| previous %s : actual %s" % (previous_commit,actual_commit)
            else:
                all_filenames.ix[commit_label,actual_commit] = state
                #print ' '*(commit_label_len+4),'|',state,commit_label
        self.datamatrix = all_filenames
