import os         
import shutil
import subprocess             


TOP_LEVEL_FILE__REL_PATH = 'ver_num_reminder.pyw' 
ICON__REL_PATH           = 'imgs//icon.ico'       # None for default python icon, must be .ico
APP_DIR__REL_PATH        = 'app'                  # None for pwd
             
DRY_RUN = False # set to True to see what cmd will be executed
DELETE_PYCACHE = True



def build_cmd():
    cmd = 'pyinstaller '
    cmd +='  {} '                      .format(TOP_LEVEL_FILE__REL_PATH)
    cmd +=' --clean '
        
    
    if APP_DIR__REL_PATH != None:    
        cmd +='  --specpath="{}" '       .format(APP_DIR__REL_PATH)
        cmd +='  --distpath="{}//dist" ' .format(APP_DIR__REL_PATH)
        cmd +='  --workpath="{}//build" '.format(APP_DIR__REL_PATH)
            
    if ICON__REL_PATH != None:
        icon_abs_path = os.path.dirname(os.path.abspath(__file__)) + '//' + ICON__REL_PATH
        cmd +='  --icon="{}" '           .format(icon_abs_path)               
#         cmd +='  --icon="{}" '           .format(ICON__REL_PATH)               
             
    return cmd


        
# works for single path str or list of paths
def delete_if_exists(path_str_or_l):
    def delete_single_fs_obj_fast(path):
        def onerror(func, path, exc_info):
            """
            Error handler for ``shutil.rmtree``.
        
            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.
        
            If the error is for another reason it re-raises the error.
        
            Usage : ``shutil.rmtree(path, onerror=onerror)``
            """
            import stat
            if not os.access(path, os.W_OK):
                # Is the error an access error ?
                os.chmod(path, stat.S_IWUSR)
                func(path)
            else:
                raise
            
        if os.path.exists(path):
            if   os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=False, onerror=onerror)
            elif os.path.isfile(path):
                os.remove(path)
            else:
                raise Exception('ERROR:  Gave something that is not a file or a dir, bad path: ', path)    
    
    
    if isinstance(path_str_or_l, str):
        path_str_or_l = [path_str_or_l]
    
    for path in path_str_or_l:
        delete_single_fs_obj_fast(path)
        
        

def main(): 
    cmd = build_cmd()
    print(cmd)
    
    if not DRY_RUN:
        
        if APP_DIR__REL_PATH != None:
            try:
                delete_if_exists(APP_DIR__REL_PATH)
            except OSError:
                delete_if_exists(APP_DIR__REL_PATH) 
            
        subprocess.call(cmd, shell = True)
        
    if DELETE_PYCACHE:
        delete_if_exists('__pycache__')

    i = input('\nPress any key to continue')
    




if __name__ == '__main__':
    main()       
