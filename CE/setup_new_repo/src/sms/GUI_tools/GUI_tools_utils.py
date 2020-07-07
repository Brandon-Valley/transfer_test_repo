import sys
import os
import ctypes

from tkinter.ttk import *
from tkinter import *


if __name__ == "__main__": 
    from   usms.exception_utils import exception_utils as eu 
else:
    from . usms.exception_utils import exception_utils as eu



# win = master
# really quick and dirty
def center_window(win, og_w = None, og_h = None):

    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    
    # not tested enough to be confident
    try:
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
#         win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        if og_w == None and og_h == None:
            win.geometry('+{}+{}'.format( x, y))
        else:
            win.geometry('{}x{}+{}+{}'.format(og_w, og_h, x, y))
#         win.geometry('+{}+{}'.format(x, y))
        win.deiconify()
    except:
        pass
    
    
# this probably dosn't work
# runs given func and prints any stderr, works on subprocess calls
def print_stderr(func):
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        
    eprint(func())
        
        
def rel_path_to_this_file__to__abs_path__if_not_None(file_obj, rel_path):
    '''
        gtu.rel_path_to_this_file__to__abs_path(__file__, 'imgs//git.png')       

    '''
    if rel_path == None:
        return None
    
#     eu.error_if_not__file__(file_obj)  # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
#     eu.error_if_not_is_file(rel_path)  # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
    
    return os.path.dirname(os.path.abspath(file_obj)) + '//' + rel_path
        
        
        
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
'''                                                                           
        iconphoto and app_id:
        --------------------
        
        If the iconphoto is set but the app_id is not, the image in the top left of the
        Gui window will change to iconphoto (default is tk feather), but the tool bar
        image will not change.
        
        If both the iconphoto and app_id are set, these imgs will match.
'''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''       

def get_app_id_unique_to_this_file(file_obj, want_duplicate_apps_to_stack_in_toolbar = True):
    '''
        gtu.get_app_id_unique_to_this_file(__file__)       
    
        if 2 GUIs use the same iconphoto, but have different app_ids, they will show as 2 different applications in the tool bar,
        if they use the same app_id, their application windows will stack in the tool bar 
    '''
#     eu.error_if_not__file__(file_obj) # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
    eu.error_if_param_type_not_in_whitelist(want_duplicate_apps_to_stack_in_toolbar, ['bool'])
        
    if want_duplicate_apps_to_stack_in_toolbar:
        raw =  '_app_id__' + os.path.dirname(os.path.abspath(file_obj)) + '__app_id_' # arbitrary string
    else:
        raw = '_app_id__{}__{}__app_id_'.format(os.path.dirname(os.path.abspath(__file__)), os.getpid()) # arbitrary string
    
    return raw.replace('\\', '//')
    

def set_app_id(app_id):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    
  
def set_tool_bar_image_to_match_iconphoto_if_exists(file_obj, want_duplicate_apps_to_stack_in_toolbar = True ):
    '''
        gtu.set_tool_bar_image_to_match_iconphoto_if_exists(__file__, want_duplicate_apps_to_stack_in_toolbar = True)       
    
        If no iconphoto is set, all this does is set the app_id based on input.
    '''  
#     eu.error_if_not__file__(file_obj)  # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
    eu.error_if_param_type_not_in_whitelist(want_duplicate_apps_to_stack_in_toolbar, ['bool'])
    
    app_id = get_app_id_unique_to_this_file(file_obj, want_duplicate_apps_to_stack_in_toolbar)
    set_app_id(app_id)
    
    
def set_iconphoto_if_not_None(master, img_path):
    if img_path == None:
        return 
    
    eu.error_if_param_type_not_in_whitelist(master, ['tkinter.Tk', 'tkinter.Toplevel'])
#     eu.error_if_not_is_file(img_path)  # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
    
    img_path_ext = os.path.splitext(img_path)[1]
    
    if img_path_ext == '.ico':
        master.iconbitmap(img_path)
    else:    
        photo_img = PhotoImage(file = img_path)
        master.iconphoto(master, photo_img)

    

def set_child_tk_gui_iconphoto_and_app_id(master, photo_img_path, app_id):
    '''
        Parent GUI does not need to pass it's photo_img_path if it passes it's app_id - ONLY IF USING ICONPHOTO (png)
        
        can work with either .png or .ico, but if you use a .ico, you need to pass the photo_img_path down to all sub-guis,
        no clue why but will only inherit iconphoto (png), not iconbitmap(ico) from gui with same app_id  
    '''
    
    if photo_img_path != None:
#         eu.error_if_not_is_file(photo_img_path) # this broke when tried to make into an app:  ERROR: Can't be __file__ Because File Does Not Exist:  "C:\projects\version_control_scripts\CE\app\dist\main\GUI.pyc" must point to an existing file.
        pass
    eu.error_if_param_type_not_in_whitelist(app_id, ['str', 'NoneType'])
    
    if app_id != None:
        set_app_id(app_id)
    
    set_iconphoto_if_not_None(master, photo_img_path)
            
    
    
    
    

if __name__ == '__main__':    
    print('In Main:  GUI_tools_utils')
    
    
    
    
    
    
    
    
    print('End ofMain:  GUI_tools_utils')