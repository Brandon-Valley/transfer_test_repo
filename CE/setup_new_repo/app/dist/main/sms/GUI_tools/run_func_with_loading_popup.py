from tkinter import *
import tkinter.ttk as ttk
import threading
import ctypes


if __name__ == '__main__':
    import        GUI_tools_utils as gtu
else:
    from . import GUI_tools_utils as gtu



# the given message with a bouncing progress bar will appear for as long as func is running, returns same as if func was run normally
# a pb_length of None will result in the progress bar filling the window whose width is set by the length of msg
# Ex:  run_func_with_loading_popup(lambda: task('joe'), photo_img_path)  
def run_func_with_loading_popup(func, msg, window_title = None, bounce_speed = 8, pb_length = None, photo_img_path = None, app_id = None, run_as_master = False):
    func_return_l = []
 
    class Main_Frame(object):
        def __init__(self, top, window_title, bounce_speed, pb_length):
            self.func = func
            
            # save root reference
            self.top = top
            
            # set title bar
            self.top.title(window_title)
            
            self.bounce_speed = bounce_speed
            self.pb_length = pb_length
      
            self.msg_lbl = Label(top, text=msg)
            self.msg_lbl.pack(padx = 10, pady = 5)
      
            # the progress bar will be referenced in the "bar handling" and "work" threads
            self.load_bar = ttk.Progressbar(top)
            self.load_bar.pack(padx = 10, pady = (0,10))
      
            self.bar_init()
              
     
        def bar_init(self):
            
            # first layer of isolation, note var being passed along to the self.start_bar function
            # target is the function being started on a new thread, so the "bar handler" thread
            self.start_bar_thread = threading.Thread(target=self.start_bar, args=())
            
            # start the bar handling thread
            self.start_bar_thread.start()
     
        def start_bar(self):
            
            # the load_bar needs to be configured for indeterminate amount of bouncing
            self.load_bar.config(mode='indeterminate', maximum=100, value=0, length = self.pb_length)
            self.load_bar.start(self.bounce_speed)            
            
            self.work_thread = threading.Thread(target=self.work_task, args=())
            self.work_thread.start()
            
            # close the work thread
            self.work_thread.join()
            
            self.top.quit()
#             # stop the indeterminate bouncing
#             self.load_bar.stop()
#             # reconfigure the bar so it appears reset
#             self.load_bar.config(value=0, maximum=0)
     
        def work_task(self):
            func_return = func()            
            func_return_l.append(func_return)


    # highest level GUI must always use TK(), not Toplevel(), PhotoImage can only work after TK(), but if this has already been called in a higher level GUI, use Toplevel()
    # running with Toplevel as your root GUI will also make a blank window appear
    if run_as_master:
        root = Tk()
    else:
        root = Toplevel() 
    
    gtu.set_child_tk_gui_iconphoto_and_app_id(root, photo_img_path, app_id)
    
    # call Main_Frame class with reference to root as top
    Main_Frame(root, window_title, bounce_speed, pb_length)
    root.mainloop() 
    root.destroy()
    return func_return_l[0]
    
    
    
    
    
if __name__ == '__main__':
#     import time
#     def task(i):
#         # The window will stay open until this function call ends.
#         for x in range(10):
#             print('hi: ' + i)
#             time.sleep(.5) # Replace this with the code you want to run
#         return "this is the func return"
#          
#     msg = 'running func...'        
#          
#     bounc_speed = 9
#     pb_length = 200
#     window_title = "Wait"
# #     photo_img_path = "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\version_control_scripts\\CE\\imgs\\git.png"
#          
#     r = run_func_with_loading_popup(lambda: task('joe'), msg, window_title, bounc_speed, pb_length)
#  
#     print('return of test: ', r)    

    
     
    import keyboard as k
    from pynput.keyboard import Key
    from pynput.keyboard import Controller
    from pynput.keyboard import Listener
    import time
    import _tkinter
    from pynput import keyboard
    from func_timeout import func_timeout, FunctionTimedOut
     
    def any_key_pressed(timeout = 0.1):
        def wait_for_key_pressed():
            def on_press(key):
                return False
              
            def on_release(key):
                return False
          
              
            listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release)
            listener.start()
            listener.join()
     
        try:
            doitReturnValue = func_timeout(timeout, wait_for_key_pressed)
            return True
          
        except FunctionTimedOut:
            return False
          
        except Exception as e:
            raise
         
         
    def wait_until_no_keys_pressed(to_return = "TEST RETURN !!!!!!!!!!!"):
        while(any_key_pressed() == True):
#             print('waiting for no')
            pass
        return to_return
          
          
          
    run_func_with_loading_popup(wait_until_no_keys_pressed, msg = 'hi', window_title = 'title', bounce_speed = 8, pb_length = None, photo_img_path = None, app_id = None, run_as_master = True)
          
#     wait_until_no_keys_pressed()
          
          
          
          
          



    import time
    def task(i):
        # The window will stay open until this function call ends.
        for x in range(10):
            print('hi: ' + i)
            time.sleep(.5) # Replace this with the code you want to run
        return "this is the func return"
         
    msg = 'running func...'        
         
    bounc_speed = 9
    pb_length = 200
    window_title = "Wait"
#     photo_img_path = "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\version_control_scripts\\CE\\imgs\\git.png"
         
#     r = run_func_with_loading_popup(lambda: task('joe'), msg, window_title, bounc_speed, pb_length)

    time.sleep(3) # remove !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     r = run_func_with_loading_popup(wait_until_no_keys_pressed, msg, window_title, bounc_speed, pb_length)
    r = run_func_with_loading_popup(wait_until_no_keys_pressed, msg, window_title, bounc_speed, pb_length)
 
    print('return of test: ', r)    
         
         
         
         
         
        