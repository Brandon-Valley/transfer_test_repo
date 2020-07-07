from sms.msg_box_utils    import msg_box_utils    as mbu
from sms.production_utils import production_utils as prdu

def main():   
    title = 'Update Version Reminder'
    msg   = 'You have just checked out a release branch with 0 commits.\n\nRemember to update the version if needed.\n\nPress "OK" to continue.'
    icon  = 'exclaim'

    mbu.msg_box__OK(title, msg, icon)
    
if __name__ == "__main__":
    prdu.show_popup_on_uncaught_exception__if__is_production(main, is_production = True)