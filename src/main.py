# In Case the Shortcut or Executable Does Not Work
#    
#     Easy Run:
#    
#        - main.py is the top level file
#    
#        - Run the top level file from command line, double clicking on the file, from a
#          shortcut that only contains the absolute path to the top level file, etc.
#    
#        - The top level file can be run from eclipse with the included .project, but stderr
#          will not populate correctly in the displayed terminal
#    
#        tl;dr "python main.py" in cmd from this directory
#    
#    
#    
#     Intended Use by Cognizant Engineer:
#    
#        - Make a shortcut to main.py
#    
#        - If you have python set up correctly, just the absolute path should be enough.  Try
#          double clicking the shortcut.  If the GUI does not appear, change the shortcut to
#             "python <abs_path_to_main.py>
#    
#        - Rename the shortcut to something like "Setup New Repo GUI"
#    
#        - Pin shortcut to Start
#    
#        - If the "Pin to Start" option does not appear after right clicking your shortcut:
#    
#            - Copy your shortcut to the Programs directory located at: 
#              C:\Users\<YOUR_USER_NAME>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs
#    
#            - Click Start
#    
#            - Begin to type the name of your shortcut, it should appear and give you the 
#              option to pin to start
#    
#        - Now just click the shortcut from the start menu any time a new repo needs to be set 
#          up, all further instructions will appear in the GUI



# if __name__ == "__main__": 
from   sms.file_system_utils import file_system_utils as fsu
from   sms.exception_utils   import exception_utils   as eu
from   sms.msg_box_utils     import msg_box_utils     as mbu
from   sms.git_tools         import Git_Repo
from   sms.logger            import json_logger
import                              common_vars       as cv
# else:
#     from . sms.file_system_utils import file_system_utils as fsu
#     from . sms.exception_utils   import exception_utils   as eu
#     from . sms.msg_box_utils     import msg_box_utils     as mbu
#     from . sms.git_tools         import Git_Repo
#     from . sms.logger            import json_logger
#     from .                       import common_vars as cv




#     print('In Main:  msg_box_utils')
     
    
     
     
     






from sms.production_utils import production_utils as prdu


def run_gui():
    
    title = 'test title'
    msg = 'test msg'
    output_define_d = {'yes': True,
                       'no' : False,
                       'cancel': False
                       }
     
    icon = 'question'
     
#     print(root_msg_box(type_num, title, msg, output_define_d))
    print(mbu.msg_box__YES_NO(title, msg, icon ))
#     print(msg_box__WARNING_MSG_ICON(title, msg, output_define_d))
    
    import GUI
    GUI.main()
    

if __name__ == '__main__':
    prdu.show_popup_on_uncaught_exception__if__is_production(run_gui, is_production = True)
    
    