#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import *

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

# You can import any python module as needed.
import os
import signal

# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!


class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

def zranger_chdir_handler(signal, frame):
    tmpfile = "/tmp/zranger-cwd-{}".format(os.getuid())
    with open(tmpfile, "r") as f:
        Command.fm.cd(f.readline().strip())
        os.unlink(tmpfile)
signal.signal(signal.SIGUSR1, zranger_chdir_handler)

class tmux_detach(Command):
    """
    :tmux_detach

    Detach from this tmux session (if inside tmux).
    """
    def execute(self):
        if not os.environ.get('TMUX'):
            return
        os.system("tmux detach")

class show_copy_buffer(Command):
    """
    :show_copy_buffer

    Show copy buffer in the notify bar.
    """
    def execute(self):
        self.fm.execute_console("""shell -p bash -c 'for arg in "$@"; do echo $arg; done' bash %c""")
        # for fobj in self.fm.copy_buffer:
            # self.fm.notify(fobj.path)

# class toggled(Command):
    # """
    # :toggled

    # Changes the name of currently highlighted files from foo_bar_baz.txt to
    # foo-bar-baz.txt and vice versa.
    # """

    # def execute(self):
        # from ranger.container.file import File
        # from os import access

        # # yes, this is pathetic
        # s = str(self.fm.env.cf)
        # s1 = s.replace('-', '_')
        # s2 = s.replace('_', '-')
        # new_name = ''.join([b if a != b else c for (a,b,c) in zip(s,s1,s2)])

        # if access(new_name, os.F_OK):
            # return

        # self.fm.rename(self.fm.env.cf, new_name)
        # f = File(new_name)
        # self.fm.env.cwd.pointed_obj = f
        # self.fm.env.cf = f

# class extract(Command):
    # """:extract <paths>
    # Extract archives
    # """
    # def execute(self):
        # import os
        # fail=[]
        # for i in self.fm.thistab.get_selection():
            # ExtractProg='7z x'
            # if i.path.endswith('.zip'):
                # # zip encoding issue
                # ExtractProg='unzip.py'
            # elif i.path.endswith('.tar.gz'):
                # ExtractProg='tar xvf'
            # elif i.path.endswith('.tar.xz'):
                # ExtractProg='tar xJvf'
            # elif i.path.endswith('.tar.bz2'):
                # ExtractProg='tar xjvf'
            # if os.system('{0} "{1}"'.format(ExtractProg, i.path)):
                # fail.append(i.path)
        # if len(fail) > 0:
            # self.fm.notify("Fail to extract: {0}".format(' '.join(fail)), duration=10, bad=True)
        # self.fm.redraw_window()

# from ranger.core.loader import CommandLoader

# class compress(Command):
    # def execute(self):
        # """ Compress marked files to current directory """
        # cwd = self.fm.thisdir
        # marked_files = cwd.get_selection()

        # if not marked_files:
            # return

        # def refresh(_):
            # cwd = self.fm.get_directory(original_path)
            # cwd.load_content()

        # original_path = cwd.path
        # parts = self.line.split()
        # au_flags = parts[1:]

        # descr = "compressing files in: " + os.path.basename(parts[1])
        # obj = CommandLoader(args=['apack'] + au_flags + \
                # [os.path.relpath(f.path, cwd.path) for f in marked_files], descr=descr)

        # obj.signal_bind('after', refresh)
        # self.fm.loader.add(obj)

    # def tab(self):
        # """ Complete with current folder name """

        # extension = ['.zip', '.tar.gz', '.rar', '.7z']
        # return ['compress ' + os.path.basename(self.fm.thisdir.path) + ext for ext in extension]
