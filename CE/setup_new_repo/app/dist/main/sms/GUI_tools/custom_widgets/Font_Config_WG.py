from tkinter.ttk import *
from tkinter import *

from os import listdir
from os.path import isfile, join





class Font_Config_WG():
    def __init__(self, 
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
                 digits_only,
                 max_str_len_in_l):
        
        self.sbox_lbl = Label(master, text = font_size_sbox_lbl_txt)
        self.cbox_lbl = Label(master, text = font_cbox_lbl_txt)
        
        # font size spin box
        self.sbox = Spinbox(master, from_ = min_font_size, to = max_font_size, width = font_size_sbox_width,
                               validate = 'key', validatecommand = digits_only, command = font_size_sbox_command) 
        self.sbox.delete(0, "end") #gets rid of 0 so the next line makes the default value 40 instead of 400
        self.sbox.insert(0, default_font_size) #default 
      
        
        # build self.font_list
        self.font_list = []

        if fonts_dir_path != None:
            raw_font_filename_list = [f for f in listdir(fonts_dir_path) if isfile(join(fonts_dir_path, f))]
            for raw_filename in raw_font_filename_list:
                font_name = raw_filename[0:-4]
                self.font_list.append(font_name)
            
        # font select combo box
        self.cbox = Combobox(master, state = 'readonly', values = self.font_list, width = max_str_len_in_l(self.font_list))
        
        if fonts_dir_path != None:
            default_font_index = self.cbox['values'].index(default_font) #default
            self.cbox.current(default_font_index) #set the selected item
        
        
            
        
        
        

    
    
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..\\..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()
    
    
    