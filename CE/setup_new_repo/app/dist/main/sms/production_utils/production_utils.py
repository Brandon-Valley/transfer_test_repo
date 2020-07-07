import traceback
import subprocess
import os

if __name__ == "__main__": 
    from   usms.msg_box_utils import msg_box_utils as mbu 
else:
    from . usms.msg_box_utils import msg_box_utils as mbu
    

APPS_ID_FILE_PATH                          = os.path.dirname(os.path.abspath(__file__)) + '\app_ids.txt'
WRITE_APP_ID_TO_FILE__RUN_SILENT__VBS_PATH = os.path.dirname(os.path.abspath(__file__)) + '\write_app_id_to_file__run_silent.vbs'
WRITE_APP_ID_TO_FILE__PS1_PATH             = os.path.dirname(os.path.abspath(__file__)) + '\write_app_id_to_file.ps1'


def show_popup_on_uncaught_exception__if__is_production(func, is_production = True):
    
    def show_error_msg_box(e):
        title = 'Unspecified Exception'
        msg = 'An uncaught exception has occurred:\n\n' + str(e)
        
        msg_box_result = mbu.msg_box__OK(title, msg, icon = 'stop')
        
        
    try:
        func()
    except:
        error_info = traceback.format_exc()
        
        if is_production:
            show_error_msg_box(error_info)
        else:
            raise
        
        
        
    

if __name__ == '__main__':
    print('In Main:  Production_utils')
    print('End of Main: Production_utils')