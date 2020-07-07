from ctypes import windll
import win32clipboard

if __name__ == "__main__": 
#     from   usms.exception_utils import exception_utils as eu 
    pass
else:
#     from . usms.exception_utils import exception_utils as eu
    pass



def get_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def set_clipboard(i):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(i)
    win32clipboard.CloseClipboard()

def clear_clipboard():
    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()



if __name__ == '__main__':
    print('In Main:  clipboard_utils')
#     a = read_from_clipboard_input()
    print(get_clipboard())
    set_clipboard('TESSSSSSSSSSSSSST')



















    print('End of Main:  clipboard_utils')        