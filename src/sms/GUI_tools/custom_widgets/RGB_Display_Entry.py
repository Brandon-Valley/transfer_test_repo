from tkinter.ttk import *
from tkinter import *




WIDTH = 13



class RGB_Display_Entry(Entry):
    def __init__(self, master=None, cnf={}):
        Entry.__init__(self, master, cnf)
        self.configure(width = WIDTH)
        self.configure(justify = 'center')
        
    def get_rgb(self):
        def _str_to_int_tup(tup_str):
            split_tup_str = re.split(r'[(,)]', tup_str)
            r, g, b = split_tup_str[1:4]
            return(int(r), int(g), int(b))
        
        return _str_to_int_tup(self.get())
        
    def set_rgb(self, rgb_tup):
        def _round_color(color_tup):
            r, g, b = color_tup
            return (int(r), int(g), int(b))
            
        def _tk_color(clr_tuple):
            return "#%02x%02x%02x" % _round_color(clr_tuple)

        
        def _highest_contrast_label_color(background_color):
            r, g, b = background_color
            
            for c in r,g,b:
                c = c / 255.0
                if c <= 0.03928:
                    c = c/12.92 
                else:
                    c = ((c+0.055)/1.055) ** 2.4
            L = 0.2126 * r + 0.7152 * g + 0.0722 * b
            
            if (255 - L) > L:
                return (255, 255, 255) #white
            else:
                return (0, 0, 0) #black


        self.configure(state = 'normal')
     
        self.delete(0, "end")
        self.insert(END, str(_round_color(rgb_tup)))
     
        # background color
        tk_rgb = _tk_color(rgb_tup)
        self.configure(readonlybackground = tk_rgb)
        
        # font color
        font_rgb_tup = _highest_contrast_label_color(rgb_tup)
        font_tk_rgb = _tk_color(font_rgb_tup)
        self.configure(fg = font_tk_rgb)
        
        self.configure(state = 'readonly')
        
        
        
    
    
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()
    
    
    