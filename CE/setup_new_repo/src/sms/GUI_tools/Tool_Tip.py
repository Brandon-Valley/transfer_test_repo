import tkinter as tk
   
# Ex:        
# button2_ttp = CreateToolTip(btn2, \
# "First thing's first, I'm the realest. Drop this and let the whole world "
# "feel it. And I'm still in the Murda Biz. I could hold you down, like ")        
class Tool_Tip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info', wait_time = 500, wrap_length = 180, show_tip = True):
        self.show_tip = show_tip
        self.waittime = wait_time     #milliseconds
        self.wraplength = wrap_length   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        if self.show_tip and self.text != '':
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 20
            # creates a toplevel window
            self.tw = tk.Toplevel(self.widget)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(self.tw, text=self.text, justify='left',
                           background="#ffffff", relief='solid', borderwidth=1,
                           wraplength = self.wraplength)
            label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()        