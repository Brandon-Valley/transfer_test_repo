import os         
import subprocess 
from win32com.client import Dispatch            

from usms.file_system_utils import file_system_utils as fsu

import update_app_params as uap



TOP_LVL_FILE_BASENAME_NO_EXT = fsu.get_basename_from_path(uap.TOP_LEVEL_FILE__PATH, include_ext = False)
NUM_DECIMAL_DIGITS = 3


def build_cmd():
    cmd = 'pyinstaller '
    cmd +='  {} '                        .format(uap.TOP_LEVEL_FILE__PATH)
    cmd +=' --clean '
        
    
    if uap.APP_DIR__PATH != None:    
        cmd +='  --specpath="{}" '       .format(uap.APP_DIR__PATH)
        cmd +='  --distpath="{}" '       .format(uap.DIST_DIR_PATH)
        cmd +='  --workpath="{}" '       .format(uap.BUILD_DIR_PATH)
            
    if uap.ICON__PATH != None:
        cmd +=' --icon="{}" '            .format(uap.ICON__PATH)   
             
    return cmd



def copy_files_to_dist_dir():
    
    if uap.COPY_INTO_DIST__INCLUDE_PATHS_L != []:
        print('\nCopying files to dist...')
                
    # build init root_abs_path__rel_paths_to_copy_ld before trimming
    for root_abs_path in uap.COPY_INTO_DIST__INCLUDE_PATHS_L:        
        abs_path_l = fsu.get_dir_content_l(root_abs_path, object_type = 'all', content_type = 'abs_path', recurs_dirs = True, rel_to_path = root_abs_path)
            
        # trim
        trimmed_abs_path_l = abs_path_l
        for removal_mode, to_remove_str_or_l in uap.COPY_INTO_DIST__EXCLUDE_PATHS_LD.items():
            trimmed_abs_path_l = fsu.path_l_remove(trimmed_abs_path_l, to_remove_str_or_l, removal_mode)
            
        # copy over each file / dir without contents to avoid including a trimmed path while not loosing empty dirs
        for abs_path in trimmed_abs_path_l:
            rel_to_root_path = fsu.get_rel_path_from_compare(abs_path, root_abs_path)
            
            # build dest path
            rel_to_root_parent_dir_path = fsu.get_parent_dir_path_from_path(rel_to_root_path)
            dist_dest_abs_path = '{}//{}//{}'.format(uap.DIST_DIR_PATH, TOP_LVL_FILE_BASENAME_NO_EXT, rel_to_root_parent_dir_path)
             
            fsu.copy_objects_to_dest(abs_path, dist_dest_abs_path, copy_dir_content = False)
            
            
            
def create_app_shortcut():           
     
    def create_shortcut(dest_path, target_path, working_dir_path = None, icon_path = None):    
        shell = Dispatch('WScript.Shell')
        
        shortcut = shell.CreateShortCut(dest_path)
        shortcut.Targetpath = target_path
        
        if working_dir_path != None:
            shortcut.WorkingDirectory = working_dir_path
            
        # if making a shortcut to an exe, this img will override the exe's icon
        # must be .ico    
        if icon_path != None:
            shortcut.IconLocation = icon_path
        
        shortcut.save()    
        
    
    if uap.ADD_SHORTCUT:
        print('\nCreating shortcut...')
        exe_path = '"{}//{}//{}"'.format(uap.DIST_DIR_PATH, TOP_LVL_FILE_BASENAME_NO_EXT, TOP_LVL_FILE_BASENAME_NO_EXT + '.exe')

        create_shortcut(dest_path        = uap.SHORTCUT_DEST_PATH, 
                        target_path      = exe_path, 
                        working_dir_path = uap.SHORTCUT_WORKING_DIR_PATH, 
                        icon_path        = uap.ICON__PATH)



def get_size(start_path = '.'):
    def bytes_to_megabytes(i):
        return i / 1000000
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return round(bytes_to_megabytes(total_size), NUM_DECIMAL_DIGITS)





def main(): 
    cmd = build_cmd()
    print(cmd)
    
    if not uap.DRY_RUN:
        
        # delete previous app if exists        
        if uap.APP_DIR__PATH != None:
            print('\nDeleting old app...')
            try:
                fsu.delete_if_exists(uap.APP_DIR__PATH)
            except OSError:
                fsu.delete_if_exists(uap.APP_DIR__PATH) 
          
        # call the cmd to create the new app
        print('\nCreating new app...')        
        subprocess.call(cmd, shell = True)
          
        # delete __pycache__ created by making the new app
        if uap.DELETE_PYCACHE:
            print('\nDeleting __pycache__...')    
            fsu.delete_if_exists('__pycache__')
              
        # copy src files into dist to allow for relative paths to non-binary files (like images), also for record keeping        
        copy_files_to_dist_dir()      

        # create shortcut
        create_app_shortcut()
        
        print('\nFinal App Size: ', get_size(uap.APP_DIR__PATH), 'MB')

    input('\nPress Enter to continue')
    




if __name__ == '__main__':
    main()       