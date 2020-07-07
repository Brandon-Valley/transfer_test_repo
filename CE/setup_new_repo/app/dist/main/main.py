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


from sms.production_utils import production_utils as prdu


def run_gui():
    import GUI
    GUI.main()
    

if __name__ == '__main__':
    prdu.show_popup_on_uncaught_exception__if__is_production(run_gui, is_production = True)
    
    