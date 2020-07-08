# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN
# https://stackoverflow.com/questions/27257018/python-messagebox-with-icons-using-ctypes-and-windll


import ctypes


if __name__ == "__main__": 
    from   usms.exception_utils import exception_utils as eu 
else:
    from . usms.exception_utils import exception_utils as eu



TYPE_NUM__OK                 = 0 
TYPE_NUM__OK_CANCEL          = 1 
TYPE_NUM__ABORT_RETRY_IGNORE = 2 
TYPE_NUM__YES_NO_CANCEL      = 3 
TYPE_NUM__YES_NO             = 4
TYPE_NUM__RETRY_CANCEL       = 5 
TYPE_NUM__CRITICAL_MSG_ICON  = 16
 
TYPE_NUM__STOP_ICON          = 0x10
TYPE_NUM__QUESTION_ICON      = 0x20
TYPE_NUM__EXLAIM_ICON        = 0x30
TYPE_NUM__INFO_ICON          = 0x40
 
ICON_KEY_TYPE_NUM_D = {
                        'stop'    : TYPE_NUM__STOP_ICON    ,
                        'question': TYPE_NUM__QUESTION_ICON,
                        'exclaim' : TYPE_NUM__EXLAIM_ICON  ,
                        'info'    : TYPE_NUM__INFO_ICON     
                      }
BTN_NUM_NAME_D = {
                   1 : 'ok'    , # also X for OK
                   2 : 'cancel', # also X for anything with CANCEL btn
                   3 : 'abort' ,
                   4 : 'retry' ,
                   5 : 'ignore',
                   6 : 'yes'   ,
                   7 : 'no'    
                 }
 
 
 
''' Internal '''
def root_msg_box(type_num, title, msg, icon, output_define_d, app_id):
    eu.error_if_param_type_not_in_whitelist(msg, ['str'])
    eu.error_if_param_type_not_in_whitelist(icon, ['str', 'NoneType'])
    eu.error_if_param_key_not_in_whitelist(icon, [None] + list(ICON_KEY_TYPE_NUM_D.keys()))
    eu.error_if_param_type_not_in_whitelist(output_define_d, ['dict', 'NoneType'])
    eu.error_if_param_type_not_in_whitelist(app_id, ['str', 'NoneType'])
     
     
    # add icon if given
    if icon != None:
        type_num = type_num | ICON_KEY_TYPE_NUM_D[icon]
     
    # sets tool bar icon to match parent's if any
    if app_id != None:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
     
     
    # create msg_box
    MessageBox = ctypes.windll.user32.MessageBoxW
    out_num = MessageBox(None, msg, title, type_num)
    out_str = BTN_NUM_NAME_D[out_num]
 
     
    # change return if output_define_d given
    if output_define_d == None:
        return out_str
    else:
        if out_str in output_define_d.keys():
            return output_define_d[out_str]
        else:
            raise Exception('ERROR:  "' + out_str + '" returned by the msg box is not a key in given output_define_d: ' + output_define_d)
         
         
 
''' External '''        
def msg_box__OK                 (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__OK                 , title, msg, icon, output_define_d, app_id)        
def msg_box__OK_CANCEL          (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__OK_CANCEL          , title, msg, icon, output_define_d, app_id)        
def msg_box__ABORT_RETRY_IGNORE (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__ABORT_RETRY_IGNORE , title, msg, icon, output_define_d, app_id)        
def msg_box__YES_NO_CANCEL      (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__YES_NO_CANCEL      , title, msg, icon, output_define_d, app_id)        
def msg_box__YES_NO             (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__YES_NO             , title, msg, icon, output_define_d, app_id)        
def msg_box__RETRY_CANCEL       (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__RETRY_CANCEL       , title, msg, icon, output_define_d, app_id)        
def msg_box__CRITICAL_MSG_ICON  (title, msg, icon = None, output_define_d = None, app_id = None): return root_msg_box(TYPE_NUM__CRITICAL_MSG_ICON  , title, msg, icon, output_define_d, app_id)        
      
 
         
         
         
 
if __name__ == '__main__':
    print('In Main:  msg_box_utils')
     
    
     
     
     
    title = 'test title'
    msg = 'test msg'
    output_define_d = {'yes': True,
                       'no' : False,
                       'cancel': False
                       }
     
    icon = 'question'
     
#     print(root_msg_box(type_num, title, msg, output_define_d))
    print(msg_box__YES_NO(title, msg, icon ))
#     print(msg_box__WARNING_MSG_ICON(title, msg, output_define_d))
     
     
     
     
     