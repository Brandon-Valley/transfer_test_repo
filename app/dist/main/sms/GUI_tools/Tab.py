from tkinter import *
import sys
import os

if __name__ == '__main__':
    from   custom_widgets import File_System_Browse_WG
    from   custom_widgets import Font_Config_WG
    from   custom_widgets import Color_Select_WG
    from   custom_widgets import Trim_WG
    import                       Tool_Tip
else:
    from . custom_widgets import File_System_Browse_WG
    from . custom_widgets import Font_Config_WG
    from . custom_widgets import Color_Select_WG
    from . custom_widgets import Trim_WG
    from .                import Tool_Tip    



DIGITS = '0123456789.-'



class Tab():
    def __init__(self, master, tab_control = None, photo_img_path = None, app_id = None):
        self.master         = master
        self.tab_control    = tab_control
        self.photo_img_path = photo_img_path
        self.app_id         = app_id
        
        self.tabs = None
        self.widget_str_var_d = {}
        
        self.widget_var_d = {}
        
        self.digits_only = (self.master.register(self.validate), DIGITS, '%P')
         
    def validate(self, allowed_chars, value_if_allowed):
        #need this to make delete work
        if (value_if_allowed == ''):
            return True
    
        for char in value_if_allowed:
            if char not in allowed_chars:
                return False
        return True
    
    
    
    # sets var to widget and puts it in self.widget_var_d so bind_to_update will work
    def set_var(self, widget, var):
        # returns a string saying which variable type is needed for the given widget
        def _var_type(widget):
            if   isinstance(widget, Label) or \
                 isinstance(widget, Entry) or \
                 isinstance(widget, Spinbox):
                return 'textvariable'
            elif isinstance(widget, Listbox):
                return 'listvariable'
            elif isinstance(widget, Radiobutton) or \
                 isinstance(widget, Checkbutton) or \
                 isinstance(widget, Scale):
                return 'variable'
            else:
                raise Exception('FUNC INCOMPLETE:  In Tab.py in set_var() in _var_type(), the given widget type does not have a variable type assigned yet, please update, type(widget): ', type(widget))

        widget[_var_type(widget)] = var
        self.widget_var_d[widget] = var
            
        
    # MIGHT GET WEIRD WITH STUFF LIKE LISTBOX AND SPINBOX
    #bind keys to widget such that func gets called any time the contents of the widget change
    def bind_to_update(self, widget, func):
        # get contents of widget in such a way that they can be assigned to a Variable
        def _get_widget_contents(widget):
            if isinstance(widget, Label):
                return widget['text']
            else:
                try:
                    return widget.get()
                except AttributeError:
                    raise Exception('ERROR:  Tried to use self.bind_to_update() on a widget without .get() (without having a var), to use this func, you must first use self.set_var() to set a Variable to the widget, type(widget): ', type(widget))
                
                
        
        
        
#         try:
#             print('in tab, at top of bind_to_update, widget["textvariable"] ' , widget['textvariable'], type(widget['textvariable']))#`````````````````````````````````````````````````````````````````````````````````````            
#         except:
#             pass
        
#         # add new trace to StringVar if you have already used this func on this widget before
#         if widget in self.widget_str_var_d.keys():
        if widget in self.widget_var_d.keys():
             
             
#             sv = self.widget_str_var_d[widget]
            var = self.widget_var_d[widget]
#             var.trace("w", lambda name, index, mode, var=var: func())
        else:
            widget_contents = _get_widget_contents(widget)
            var = Variable(value = widget_contents)
            self.set_var(widget, var)
            
        var.trace("w", lambda name, index, mode, var=var: func())

    
    
    def bind_to_edit(self, widget, func):
        widget.bind("<KeyRelease>", func)
        widget.bind("<KeyRelease-BackSpace>", func)
        widget.bind("<KeyRelease-Delete>", func)
        widget.bind("<KeyRelease-space>", func)
        
    def bind_to_click(self, widget, func):
        widget.bind("<ButtonRelease>", func)
        widget.bind("<Enter>", func)
        
    def scroll_to_end_always(self, widget):
        def xview_event_handler(e):
            e.widget.update_idletasks()
            e.widget.xview_moveto(1)
            e.widget.unbind('<Expose>')
            
        widget.bind('<Expose>', xview_event_handler)#scrolls text to end if needed
        widget.bind('<Enter>' , xview_event_handler)#scrolls text to end if needed
        widget.bind('<Leave>' , xview_event_handler)#scrolls text to end if needed
        widget.bind('<FocusIn>' , xview_event_handler)#scrolls text to end if needed
        
    # returns length of longest str in a list,
    # useful for making combo boxes match length of contents
    # if useing for a combo box, will need to add + 1 so V part
    # of box doesnt cover end of longest str
    def max_str_len_in_l(self, str_list):
        len_max = 0
        for m in str_list:
            if len(m) > len_max:
                len_max = len(m)
        return len_max + 1

    # fills list box widget from list of strings in order
    def fill_list_box(self, list_box_widget, str_list):
        if str_list != None:
            for str in str_list:
                list_box_widget.insert(END, str)

# DONT DELETE UNTIL YOU KNOW IT WONT BE NEEDED EVER AGAIN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def path_tb_browse_btn_clk(self, path_txt_box_widget, browse_for, file_type = None):
        from tkinter import filedialog
        #get file path and place it in text box
         
        if browse_for == 'file':
            if file_type == None:
                file_system_item = filedialog.askopenfilename()
 
            else:
                file_system_item = filedialog.askopenfilename(filetypes = (("Images", "*" + file_type), ("All files", "*")))#filetypes = (("Images", '*.png|*.jpg'), ("All files", "*")))#"*" + file_types   #,("Template files", '*.jpg'), 
        elif browse_for == 'dir':
            file_system_item = filedialog.askdirectory()
        else:
            raise Exception('ERROR:  In Tab.py, in path_tb_browse_btn_clk, invalid value for browse_for: ', browse_for)
        path_txt_box_widget.delete(0, "end")
        path_txt_box_widget.insert(END, file_system_item)
         
#         output_path_text_box_updated()
        
        
    def Tool_Tip(self, 
                 widget,
                 text        ='widget info',
                 wait_time   = 500,
                 wrap_length = 180,
                 show_tip    = True          ):
        
        return Tool_Tip.Tool_Tip(widget, text, wait_time, wrap_length)
        
        
        
    def File_System_Browse_WG(   self,
                                 master,
                                 lbl_txt, 
                                 tb_width              = None, 
                                 browse_for            = 'dir',  # 'dir' or 'file'
                                 file_type             = None,   # '.jpg', '.mp4', etc...
                                 init_path             = None, 
                                 focus_tb_after_browse = False,
                                 tb_edit_func          = None,
                                 browse_btn_txt        = 'Browse...'):
        
        return File_System_Browse_WG.File_System_Browse_WG(master, lbl_txt, tb_width, browse_for, file_type, init_path, focus_tb_after_browse, tb_edit_func, browse_btn_txt)
        
        
        
    def Font_Config_WG(  self,
                         master,
                         fonts_dir_path         = None, 
                         default_font_size      = 20,
                         default_font           = None,
                         font_size_sbox_command = None,
                         font_size_sbox_width   = 5,
                         max_font_size          = 9999,
                         min_font_size          = 0,
                         font_size_sbox_lbl_txt = 'Font Size:',
                         font_cbox_lbl_txt      = 'Font:'):

        return Font_Config_WG.Font_Config_WG(
                                             master,
                                             fonts_dir_path, 
                                             default_font_size,
                                             default_font,
                                             font_size_sbox_command,
                                             font_size_sbox_width,
                                             max_font_size,
                                             min_font_size,
                                             font_size_sbox_lbl_txt,
                                             font_cbox_lbl_txt,
                                             self.digits_only,
                                             self.max_str_len_in_l)
         
        
    def Color_Select_WG(self,
                    master,
                    lbl_txt,
                    default_rgb_tup = (255, 255, 255),
                    btn_txt = 'Change Color'):
    
        wg = Color_Select_WG.Color_Select_WG(
                        master,
                        lbl_txt,
                        default_rgb_tup,
                        btn_txt)
        return wg
    

    def Trim_WG( self,
                 master, 
                 max,
                 min = 0,
                 min_diff = 0,
                 start_set = None,
                 end_set = None,
                 update_func = None,
                 diff_leading_txt = '',
                 display_type = 'time'):
        
        wg = Trim_WG.Trim_WG(
                             master, 
                             max,
                             min,
                             min_diff,
                             start_set,
                             end_set,
                             update_func,
                             diff_leading_txt,
                             display_type,
                             self.set_var,
                             self.bind_to_update)
        return wg        
     
        
        
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()



# import GUI #only need for testing
# 
# 
# DIGITS = '0123456789.-'
# 
# 
# class Tab():
#     def __init__(self, master):
#         self.master = master
#         self.tabs = None
#         
#         self.digits_only = (self.master.register(self.validate), DIGITS, '%P')
#          
#     def validate(self, allowed_chars, value_if_allowed):
#         #need this to make delete work
#         if (value_if_allowed == ''):
#             return True
#     
#         for char in value_if_allowed:
#             if char not in allowed_chars:
#                 return False
#         return True
#     
#     #bind keys to widget such that func gets called any time the contents of the widget change
#     def bind_to_edit(self, widget, func):
#         widget.bind("<KeyRelease>", func)
#         widget.bind("<KeyRelease-BackSpace>", func)
#         widget.bind("<KeyRelease-Delete>", func)
#         widget.bind("<KeyRelease-space>", func)
#         
#     def bind_to_click(self, widget, func):
#         widget.bind("<ButtonRelease>", func)
#         widget.bind("<Enter>", func)
# 
#     
# 
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
# if __name__ == '__main__':
#     GUI.main()