import tkinter
from tkinter.ttk import *
from tkinter import *

import sys
import string
import ctypes
import os
import json


if __name__ == '__main__':
    import        GUI_tools_utils as gtu
else:
    from . import GUI_tools_utils as gtu



# this file must remain a .pyw
def run_func_in_tk_terminal(func, photo_img_path = None, parent_gui_pid_l_json_path = None):
    
    # because I'm to lazy to add a submodule
    def is_dir(in_path):
        return os.path.isdir(in_path)

    def is_file(in_path):
        return os.path.isfile(in_path)
    
    def get_parent_dir_path_from_path(path):
        return os.path.dirname(path)
    
    def get_abs_path_from_rel_path(in_rel_path):
        return os.path.abspath(in_rel_path)
    
    def make_dir_if_not_exist(dir_path):
        abs_dir_path = get_abs_path_from_rel_path(dir_path)
        if not os.path.exists(abs_dir_path):
            os.makedirs(abs_dir_path)
            
    def make_file_if_not_exist(file_path):
        if not is_file(file_path):
            parent_dir_path = get_parent_dir_path_from_path(file_path)
            make_dir_if_not_exist(parent_dir_path)
            file = open(file_path, "w") 
            file.close() 
        
    def json_write(data, output_file_path, indent = 4):
        make_file_if_not_exist(output_file_path)
         
        with open(output_file_path, 'w') as outfile:  
            json.dump(data, outfile, indent = indent)
            outfile.close()  
            
    def json_read(json_file_path, return_if_file_not_found = "raise_exception"):    
        try:
            with open(json_file_path, "r") as read_file:
                data = json.load(read_file)           
            read_file.close()
        except FileNotFoundError as e:
            if return_if_file_not_found != "raise_exception":
                return return_if_file_not_found
            else:
                raise e
            
        return data
    
    
    class DbgText:
        Dbgtopwin=None
        Dbgwidget=None
        DbgRoot=None
        
        def _kill_topwin(self):
            DbgText.Dbgwidget=None
            if DbgText.Dbgtopwin != None:
                DbgText.Dbgtopwin.destroy()
            DbgText.Dbgtopwin=None
           
        def __init__(self,kind=''):
            self.kind=kind
            self.window=None
            self.widget=None
            self.called=0
            self.hide=0
            self.buffer=''
    
        def __del__(self):
            "On deletion, wait for user to see the output"
            if DbgText.Dbgtopwin != None:
                See()
            self._kill_topwin()
        
        def write(self,charstr):
            "write text to buffer or window"
            if self.hide:
                self.buffer.append(charstr)
            else:
                if self.window == None:
                    if DbgText.Dbgtopwin == None:
#                         DbgText.Dbgtopwin=tkinter.Tk()
                        DbgText.Dbgtopwin=tkinter.Toplevel()

                        GUI_tools_utils.center_window(DbgText.Dbgtopwin)
                        
                        # set icon if given path
                        if photo_img_path != None:
                            # sets tool bar icon to be the same as iconphoto
                            myappid = 'mycompany.myproduct.subproduct.version3' # arbitrary string
                            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                            
                            # sets iconphoto
                            photo_img = PhotoImage(file = photo_img_path)
                            DbgText.Dbgtopwin.iconphoto(DbgText.Dbgtopwin, photo_img)
                        
                        DbgText.Dbgtopwin.protocol('WM_DELETE_WINDOW',Dbg_kill_topwin)
                        DbgText.Dbgwidget=tkinter.Text(DbgText.Dbgtopwin, background = "black", foreground = 'white')
                        DbgText.Dbgwidget.pack(expand=1)
                    top=DbgText.Dbgtopwin
                    wid=DbgText.Dbgwidget
                    
                else:
                    if self.widget == None:
                        self.widget=tkinter.Text(self.window)
                    top=self.window
                    wid=self.widget
                if self.kind != '':
                    ep=wid.index('end')
                    sp=string.split(ep,'.')
                    # determine length of 'previous' line
                    prevl=int(sp[0])
                    tx='\n'
                    if prevl:
                        pl='%d.0' % (prevl-1)
                        tx=wid.get(pl,ep)
                    # if this is start of a new line
                    if tx[0] == '\n':
                        wid.insert('end',self.kind)
                wid.insert('end',charstr)     
            self.called=1
            top.update()
    
    def Dbg_kill_topwin():
        f=DbgText()
        f._kill_topwin()
        
    def Take_stdout():
        "DIsplay stdout in text widget"
        if not isinstance(sys.stdout,DbgText):
            f=DbgText()
            f.prev=sys.stdout
            sys.stdout=f
    
    def Take_stderr():
        "DIsplay stderr in text widget"
        if not isinstance(sys.stderr,DbgText):
            f=DbgText('*')
            f.prev=sys.stderr
            sys.stderr=f
        
    def Restore_stdout():
        f=sys.stdout
        if isinstance(f,DbgText):
            sys.stdout=f.prev
            del f
    
    def Restore_stderr():
        f=sys.stderr
        if isinstance(f,DbgText):
            sys.stderr=f.prev
            del f
    
    def Define_Root():
        root=tkinter.Tk()
        root.withdraw()
        DbgText.DbgRoot=root
    
    def See():
        db=DbgText()
        if db.Dbgtopwin != None:
            db.Dbgtopwin.mainloop() # loop for me to see
    
    def Take_all():
        "send stderr/stdout to Tkinter text window/widget"
        Take_stdout()
        Take_stderr()
    
    def Restore_all():
        "restore stderr/stdout"
        Restore_stdout()
        Restore_stderr()
    

    Take_stdout()
    
    # track the PIDs of all processes so they can all be killed at once
    if parent_gui_pid_l_json_path != None:
        pid_l = json_read(parent_gui_pid_l_json_path, return_if_file_not_found = [])
        pid_l.append(os.getpid())
        json_write(pid_l, parent_gui_pid_l_json_path)
    
    # depending on the function, you may never get past this func
    func()
    
    Dbg_kill_topwin()
        
    
    
    
    
if __name__ == '__main__':
    import setup_new_repo
    repo_type = 'IP'
    local_ip_repo_dir_path = "C:\\Users\\mt204e\\Documents\\test_ip_repo_3"
    repo_remote_url = 'https://ba-bit.web.boeing.com/scm/mnfcf/tsm15.git'
    
#     photo_img = PhotoImage(file = "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\version_control_scripts\\CE\\imgs\\git.png")
    #     subprocess.call('setup_new_repo.py', shell = True)
    run_func_in_tk_terminal(lambda: setup_new_repo.setup_new_repo(repo_type, local_ip_repo_dir_path, repo_remote_url), photo_img = None)
    
    
    
    
    
    
    