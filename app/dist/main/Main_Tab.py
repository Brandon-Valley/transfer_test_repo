# taskkill /im python.exe /F

import os
from tkinter.ttk import *
from tkinter import *
import subprocess 


from   sms.logger                                import json_logger 
from   sms.GUI_tools                             import Tab     
from   sms.GUI_tools.run_func_with_loading_popup import run_func_with_loading_popup
from   sms.clipboard_utils                       import clipboard_utils             as cbu    
from   sms.msg_box_utils                         import msg_box_utils               as mbu
import                                                  common_vars                 as cv
   


SETUP_NEW_REPO_SCRIPT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + '//setup_new_repo.py'

GUI_VARS_JSON_PATH = cv.PROGRAM_DATA_DIR_PATH + '\\setup_new_repo_gui_vars.json'

REPO_TYPE_CBOX_VALUES = [cv.REPO_TYPE_KEY__IP, cv.REPO_TYPE_KEY__PIC, cv.REPO_TYPE_KEY__OTHER]

KNOWN_ERROR_CODE_MSG_D = {128: 'fatal: remote error: Repository not found.  The requested repository does not exist, or you do not have permission to access it.'}

REMOTE_URL_TB_WIDTH = 77 # the width of the whole window is dependent on this value, as long as it is => 77
 
DEFAULT_FONT_STR              = 'Helvetica 9'
REMOTE_WARNING_FINAL_FONT_STR = 'Helvetica 10 bold'



class Main_Tab(Tab.Tab):
    def __init__(self, master, tab_control, photo_img_path = None, app_id = None):
        Tab.Tab.__init__(self, master, tab_control, photo_img_path, app_id)
         
        self.read_gui_vars()
        
        self.setup_new_repo_btn_____widget_setup()
        self.repo_type_____widget_setup()
        self.ip_repo_____widget_setup()
        self.remote_____widget_setup()
        self.update_setup_new_repo_disable_tool_tip_and_state()
        
        self.grid_init_widgets()



    def read_gui_vars(self):
        self.gui_vars_d = json_logger.read(GUI_VARS_JSON_PATH, return_if_file_not_found = None)
        
        if self.gui_vars_d == None:
            self.gui_vars_d = {}
            
    def write_gui_var(self, key_str, val):
        self.gui_vars_d[key_str] = val
        json_logger.write(self.gui_vars_d, GUI_VARS_JSON_PATH)
        
    def get_gui_var(self, key_str):
        if key_str in self.gui_vars_d.keys():
            return self.gui_vars_d[key_str]
        else:
            return ''



    def repo_type_____widget_setup(self):
        self.setup_new_repo_disable_tool_tip_reason__repo_type = ''
        
        def repo_type_cbox_updated():
            if self.repo_type_cbox.get() == cv.REPO_TYPE_KEY__IP:
                self.ip_repo_lbl_frm      .grid(column=1, row=3, padx=5, pady=5, sticky='NSWE', columnspan=3)
                self.ip_repo_lbl_frm.grid_columnconfigure(2, weight=1)   
                           
            else:
                # var won't be initialized first time through
                try:
                    self.ip_repo_lbl_frm.grid_forget()
                except AttributeError:
                    pass
                
            # disable / enable btn
            if self.repo_type_cbox.get() in REPO_TYPE_CBOX_VALUES:
                self.setup_new_repo_disable_tool_tip_reason__repo_type = ''
            else:
                self.setup_new_repo_disable_tool_tip_reason__repo_type = 'You must select a repository type.'
            
            self.update_setup_new_repo_tooltip__ip_repo()      
            self.update_setup_new_repo_disable_tool_tip_and_state()
            
        self.repo_type_lbl_frm = LabelFrame(self.master, text=" Repository Type: ")
        self.repo_type_lbl = Label(self.repo_type_lbl_frm, text="What type of repository will this be?")
        
        self.repo_type_cbox = Combobox(self.repo_type_lbl_frm, state = 'readonly', values = REPO_TYPE_CBOX_VALUES, width = self.max_str_len_in_l(REPO_TYPE_CBOX_VALUES))
        self.bind_to_update(self.repo_type_cbox, repo_type_cbox_updated)
        repo_type_cbox_updated()
        
        
        
    def remote_____widget_setup(self):
        self.setup_new_repo_disable_tool_tip_reason__remote_url = ''
        remote_reminder_lbl_string_var = StringVar()
        
        def update_setup_new_repo_disable_tool_tip_reason__remote_url(event = None):
            
            def remote_url_tb_contains_valid_git_repo_remote_url():
                url = self.remote_url_tb.get()
                return url[-4:] == '.git'
            
                
            if remote_url_tb_contains_valid_git_repo_remote_url():
                self.setup_new_repo_disable_tool_tip_reason__remote_url = ''
                self.remote_url_tool_tip.text = ''
                
                remote_reminder_lbl_string_var.set("I'm sure you remembered to make this repository from ba-bit.web.boeing.com > projects > MNFCF > Project Settings > Built-in Scripts > Clone a repository")
                self.remote_reminder_lbl.configure(font = REMOTE_WARNING_FINAL_FONT_STR)
            else:
                self.setup_new_repo_disable_tool_tip_reason__remote_url = 'You must input a valid Git remote repository url.'
                self.remote_url_tool_tip.text = "To find the remote url, open the repository in Bitbucket, click the clone icon at the top right of the screen.  If you do not see this icon, click the >> icon at the bottom left of the screen." 

                remote_reminder_lbl_string_var.set("To make a new repository, first clone the permissions of an existing repo of the desired type - ba-bit.web.boeing.com > projects > MNFCF > Project Settings > Built-in Scripts > Clone a repository.  Then paste the remote url below.")
                self.remote_reminder_lbl.configure(font = DEFAULT_FONT_STR)
            
            self.update_setup_new_repo_disable_tool_tip_and_state()
        
        
        def set_tb_as_clipboard_if_contains_valid_remote_url(event = None):
            cb = cbu.get_clipboard()
            if cb[-4:] == '.git' and self.remote_url_tb.get() == '':
                self.remote_url_tb.delete(0, 'end')
                self.remote_url_tb.insert(END, cb)
                
                update_setup_new_repo_disable_tool_tip_reason__remote_url()
            
        self.remote_reminder_lbl = Label(self.master, wraplength = 350, justify = 'left', textvariable = remote_reminder_lbl_string_var)
        
        self.remote_lbl_frm = LabelFrame(self.master, text=" Repository Remote: ")
        self.remote_url_lbl = Label(self.remote_lbl_frm, text="What is the remote url for this repository?")
        
        self.remote_url_tb = Entry(self.remote_lbl_frm, width=REMOTE_URL_TB_WIDTH)
        self.scroll_to_end_always(self.remote_url_tb)

        self.remote_url_tool_tip = self.Tool_Tip(self.remote_url_tb, text = '', wait_time = 0, wrap_length = 200)  

        set_tb_as_clipboard_if_contains_valid_remote_url()
        
        self.bind_to_click(self.remote_lbl_frm, set_tb_as_clipboard_if_contains_valid_remote_url)
        self.bind_to_click(self.master, set_tb_as_clipboard_if_contains_valid_remote_url)
        
        self.bind_to_edit(self.remote_url_tb, update_setup_new_repo_disable_tool_tip_reason__remote_url)    
        update_setup_new_repo_disable_tool_tip_reason__remote_url()
        
 
    
    def update_setup_new_repo_tooltip__ip_repo(self, event = None):
        
        def ip_repo_fsb_wg_tb_contains_path_to_existing_git_repo():
            ip_repo_path = self.ip_repo_fsb_wg.tb.get()
            dot_git_dir_path = ip_repo_path + '//.git'
            dot_git_dir_exists = os.path.isdir(dot_git_dir_path)
            return dot_git_dir_exists

        
        if self.repo_type_cbox.get() == cv.REPO_TYPE_KEY__IP:    
            if not ip_repo_fsb_wg_tb_contains_path_to_existing_git_repo():
                self.setup_new_repo_disable_tool_tip_reason__ip_repo_path = 'Local ip_repo path must point to an existing Git repository.'
            else:
                self.setup_new_repo_disable_tool_tip_reason__ip_repo_path = ''
                
            self.update_setup_new_repo_disable_tool_tip_and_state()
 
    

    def ip_repo_____widget_setup(self):
        self.setup_new_repo_disable_tool_tip_reason__ip_repo_path = ''        
        
        self.ip_repo_lbl_frm = LabelFrame(self.master, text=" ip_repo: ")
        
        self.ip_repo_fsb_wg = self.File_System_Browse_WG(self.ip_repo_lbl_frm, lbl_txt = 'Local ip_repo path:', browse_for = 'dir', 
                                                         focus_tb_after_browse = True, tb_edit_func = self.update_setup_new_repo_tooltip__ip_repo)
        
        self.ip_repo_fsb_wg.tb.delete(0, 'end')
        self.ip_repo_fsb_wg.tb.insert(END, self.get_gui_var('ip_repo_path'))

        # these will only appear when the lbl_frm is grid-ed by repo_type_cbox_updated()
        self.ip_repo_fsb_wg.lbl   .grid(column=1 , row=1, padx=5, pady=5)
        self.ip_repo_fsb_wg.tb    .grid(column=2 , row=1, padx=5, pady=5, sticky='WE')
        self.ip_repo_fsb_wg.btn   .grid(column=4 , row=1, padx=5, pady=5, sticky='E')
        
        self.update_setup_new_repo_tooltip__ip_repo()

     
 
    def setup_new_repo_btn_____widget_setup(self):         
         
        def setup_new_repo_btn_clk():
            
            def remote_url_tb_contains_valid_git_repo_remote_url():
                
                def remote_exists():
                    cmd = 'env GIT_PROXY_COMMAND=myproxy.sh GIT_TRACE=1 git ls-remote ' + self.remote_url_tb.get()
                    
                    try:
                        print('\n>> Checking source...\n')
                        cmd_out = subprocess.call(cmd, shell = True)
                        print('\n>> Finished checking source.')
                        
                        if cmd_out not in [0, True] and isinstance(cmd_out, int):
                            if cmd_out in KNOWN_ERROR_CODE_MSG_D.keys():
                                return KNOWN_ERROR_CODE_MSG_D[cmd_out]
                            else:
                                return 'Git error code: ' + str(cmd_out)
                        return True
                    except subprocess.CalledProcessError as e:
                        print(e)
                        return False
                   
                msg = 'Checking if provided url points to a valid Git remote...'        
                bounc_speed = 12
                pb_length = 300
                window_title = "Checking Source..."
                
                remote_valid = run_func_with_loading_popup(remote_exists, msg, window_title, bounc_speed, pb_length, app_id = self.app_id, photo_img_path=self.photo_img_path)
                return remote_valid
            
            
            # write gui var so it will auto-fill from now on
            self.write_gui_var('ip_repo_path', self.ip_repo_fsb_wg.tb.get())

            repo_type = self.repo_type_cbox.get()
            local_ip_repo_dir_path = self.ip_repo_fsb_wg.tb.get()
            repo_remote_url = self.remote_url_tb.get()            
            
            # track the PIDs of all processes so they can all be killed at once
            script_pid = os.getpid()
            json_logger.write([script_pid], cv.PARENT_PID_L_JSON_ABS_PATH)
            
            remote_check_output = remote_url_tb_contains_valid_git_repo_remote_url()
            
            # if the given url points to a valid url, continue
            if remote_check_output == True:
                cmd = '"{}" --repo_type {} --local_ip_repo_dir_path "{}" --repo_remote_url {} --app_id {} --skip_ip_update True'.format(SETUP_NEW_REPO_SCRIPT_ABS_PATH, repo_type, local_ip_repo_dir_path, repo_remote_url, self.app_id)
                print('\n>> Running : {}'.format(cmd))
                subprocess.call(cmd, shell = True)
            else:
                print(cv.WAITING_FOR_USER_INPUT_MSG)
                mbu.msg_box__OK('Invalid Source', 'The provided url does not point to a valid Git remote.\n\n' + str(remote_check_output), icon = 'stop', app_id = self.app_id)
            
            
        self.setup_new_repo_btn = Button(self.master, text="Setup New Repository", wraplength = 90, command = setup_new_repo_btn_clk)
 
         
         
    def update_setup_new_repo_disable_tool_tip_and_state(self):       
        
        def add_to_text_if_not_empty(text, str):
            if str == '':
                return text
            
            if text != '':
                text += '\n'
            return text+ '- ' + str
         
         
        text = ''
        
        # all vars wont already be initialized first time through
        try:
                 
            text = add_to_text_if_not_empty(text, self.setup_new_repo_disable_tool_tip_reason__repo_type)
            text = add_to_text_if_not_empty(text, self.setup_new_repo_disable_tool_tip_reason__remote_url)
            text = add_to_text_if_not_empty(text, self.setup_new_repo_disable_tool_tip_reason__ip_repo_path)
                 
            self.setup_new_repo_btn_tool_tip = self.Tool_Tip(self.setup_new_repo_btn, text = text, wait_time = 0, wrap_length = 200)
              
        except AttributeError:
            pass
        
        if text == '':
            self.setup_new_repo_btn.configure(state = 'normal') 
        else:
            self.setup_new_repo_btn.configure(state = 'disabled') 

 
 
    def grid_init_widgets(self):
        self.master.grid_columnconfigure(2, weight=1)
        
        self.repo_type_lbl_frm   .grid(column=1, row=1, padx=5, pady=5, sticky='NSW')
        self.repo_type_lbl       .grid(column=1, row=1, padx=5, pady=5)
        self.repo_type_cbox      .grid(column=2, row=1, padx=5, pady=5)
        
        self.remote_lbl_frm      .grid(column=1, row=2, padx=5, pady=5, sticky='NSWE', columnspan=3)
        self.remote_url_lbl      .grid(column=1, row=1, padx=5, pady=5)
        self.remote_url_tb       .grid(column=2, row=1, padx=5, pady=5)
        
        self.setup_new_repo_btn  .grid(column=3, row=1, padx=5, pady=5, sticky='E')
        
        self.remote_reminder_lbl.grid(column=2, row=1, padx=5, pady=5, sticky='NSWE')
        
        
        
        
 
if __name__ == '__main__':
    import GUI
    GUI.main()  