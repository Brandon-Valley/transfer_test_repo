import subprocess
import argparse


if __name__ == "__main__": 
    from   sms.file_system_utils import file_system_utils as fsu
    from   sms.exception_utils   import exception_utils   as eu
    from   sms.msg_box_utils     import msg_box_utils     as mbu
    from   sms.git_tools         import Git_Repo
    from   sms.logger            import json_logger
    import                              common_vars       as cv
else:
    from . sms.file_system_utils import file_system_utils as fsu
    from . sms.exception_utils   import exception_utils   as eu
    from . sms.msg_box_utils     import msg_box_utils     as mbu
    from . sms.git_tools         import Git_Repo
    from . sms.logger            import json_logger
    from .                       import common_vars as cv



REPO_TYPE_KEY_L = [cv.REPO_TYPE_KEY__IP, cv.REPO_TYPE_KEY__PIC, cv.REPO_TYPE_KEY__OTHER]



def setup_new_repo(repo_type, local_ip_repo_dir_path, repo_remote_url, app_id = 'None', skip_ip_update = False):
    
    # correct skip_ip_update if needed
    if   skip_ip_update == 'True':  skip_ip_update = True
    else:                           skip_ip_update = False 
    
    # correct app_id if needed
    if app_id == 'None':  app_id = None
    
    # read in parent PID list now, in case a duplicate process overwrites it
    parent_guis_pid_l = json_logger.read(cv.PARENT_PID_L_JSON_ABS_PATH, return_if_file_not_found = [])
    
    
    
    def kill_parent_guis():
        for parent_gui_pid in parent_guis_pid_l:
            cmd = 'taskkill /PID ' + str(parent_gui_pid) + ' /F '
            print(cmd)
            subprocess.Popen(cmd)
    
    
    
    def kill_gui():
        fsu.delete_if_exists(cv.TEMP_DIR_PATH)
        exit()
    
    
    
    def check_if_inputs_valid(repo_type, local_ip_repo_dir_path, repo_remote_url):
        eu.error_if_param_key_not_in_whitelist (repo_type, REPO_TYPE_KEY_L)
        
        eu.error_if_param_type_not_in_whitelist(local_ip_repo_dir_path, ['str'])
        eu.error_if_not_is_dir                 (local_ip_repo_dir_path + '//.git', custom_msg = 'ERROR:  IP Repo Does Not Exist:  "' + str(local_ip_repo_dir_path) + '" must point to an existing Git repo.')
        eu.error_if_not_is_dir                 (local_ip_repo_dir_path + '//.git')
        
        eu.error_if_param_type_not_in_whitelist(repo_remote_url, ['str'])
        eu.error_if_path_ext_not_in_whitelist  (repo_remote_url, ['.git'])
        
        eu.error_if_param_type_not_in_whitelist(app_id, ['str', 'NoneType'])
    
    
    
    def get_repo_name_from_url(repo_remote_url):
        url_basename = fsu.get_basename_from_path(repo_remote_url)
        return url_basename.split('.')[0] # cut off extension
    
    
    
    def get_new_repo_path(repo_type, new_repo_name):
        
        # other and pic are both treated the same
        repo_parent_dir_path = cv.TEMP_DIR_PATH
        
        if repo_type == cv.REPO_TYPE_KEY__IP:
            repo_parent_dir_path = local_ip_repo_dir_path
            
        return repo_parent_dir_path + '\\' + new_repo_name
    
    
    
    # if repo path already exists, ask user if they want to delete it to continue, if user clicks no, ends script
    def prompt_user_and_delete_existing_repo_if_needed(new_repo_path, new_repo_name):
        
        # prompt the user if they want to retry when they get a permission error, probably caused by having a terminal open to the repo location
        def prompt_user_perm_error_retry(e, new_repo_path):
            title = 'Permission Error'
            msg = 'Received the following permission error while trying to delete existing repository.\n\n' + str(e) + '\n\nOne possible cause for this error could be from a terminal open to this location.\n\nPlease close the blocking process and retry.'
            output_define_d = {'retry'   : True,
                               'cancel'  : False}
            print(cv.WAITING_FOR_USER_INPUT_MSG)
            
            retry_cmd = mbu.msg_box__RETRY_CANCEL(title, msg, icon = 'stop', output_define_d = output_define_d, app_id = app_id)
            
            if not retry_cmd:
                kill_gui()

        
        if fsu.is_dir(new_repo_path):
            title = 'Existing Repository Conflict'
            msg = 'The directory that will be created by cloning ' + new_repo_name + ' already exists.\n\nWould you like to delete the following directory in order to continue?  \n\n"' + new_repo_path + '"'
            output_define_d = {'yes' : True,
                               'no'  : False}
            print(cv.WAITING_FOR_USER_INPUT_MSG)
            
            delete_existing_dir = mbu.msg_box__YES_NO(title, msg, icon = "exclaim", output_define_d = output_define_d, app_id = app_id)

            if delete_existing_dir:
                while(True):
                    try:
                        print('\n>> Deleting existing directory at "' + new_repo_path + '"...')
                        fsu.delete_if_exists(new_repo_path)
                        return 
                    except PermissionError as e:
                        prompt_user_perm_error_retry(e, new_repo_path)
            else:
                kill_gui()
    
    
    
    def init_git_flow(new_repo):
        print("\n>> Making a possibly empty commit to allow Git Flow to be initialized even if this is a new repository...")
        new_repo.run_git_cmd('git commit --allow-empty -m "Initialized Git Flow"', print_output = True, print_cmd = True, run_type = 'call', shell = False)
        
        print("\n>> Initializing Git Flow with default branch names...")
        new_repo.run_git_cmd('git flow init -d', print_output = True, print_cmd = True, run_type = 'call')
        
        print("\n>> Pushing and adding remote for new develop branch...")
        new_repo.run_git_cmd('git push --set-upstream origin develop', print_output = True, print_cmd = True, run_type = 'call')
        
        print("\n>> Pushing all branches...")
        new_repo.run_git_cmd('git push --all', print_output = True, print_cmd = True, run_type = 'call')
        
        
        
    # if the cloned repo already has commits, ask the user if they would like to skip the init git flow step
    def prompt_user_if_cloned_repo_has_commits_if_skip_init_git_flow_step(new_repo):
        
        # create a local tracking branch for all remote branches so you will be able to tell if a "develop" branch already exists
        print('\n>> Creating a local tracking branch for all remote branches...')
        new_repo.track_all_remote_branches(print_output = True, print_cmd = True, run_type = 'call')
        
        # get repo info
        num_commits = new_repo.get_num_commits()
        branch_l = new_repo.get_branch_l(trimmed = True, run_type = 'popen')
                
        # if there are previous commits, need to show a popup
        if num_commits != 0:
            title = 'Not a New Repository'
            msg = new_repo.name + ' is not a new repository.\n'
            msg += new_repo.name + ' already has ' + str(num_commits) + ' commit(s).\n'
            msg += new_repo.name + ' contains the following branches: \n' + str(branch_l) + '\n\n' 
                        
            if 'develop' in branch_l:
                msg += 'Because ' + new_repo.name + ' already contains a "develop" branch, even if you would like to continue the new repository setup process, it is recommended that you skip the "Initialize Git Flow" step.'
            else:
                msg += 'Because ' + new_repo.name + ' does not already contain a "develop" branch, if you would like to continue the new repository setup process, it is recommended that you do not skip the "Initialize Git Flow" step.'
            
            msg += '\n\nWould you like to skip the "Initialize Git Flow" step?'
            
            print(cv.WAITING_FOR_USER_INPUT_MSG)
            
            msg_box_out_str = mbu.msg_box__YES_NO_CANCEL(title, msg, icon = 'exclaim', app_id = app_id)
            
            # handle popup output
            if msg_box_out_str == 'yes':
                return True
            elif msg_box_out_str == 'no':
                return False
            elif msg_box_out_str == 'cancel':
                kill_gui()
            else:
                raise Exception('ERROR: Invalid msg_box_out_str:  ' + msg_box_out_str)
        else:
            return False
        
        
        
    def get_ip_repo(repo_type, local_ip_repo_dir_path):     
        ip_repo = None
        if repo_type == cv.REPO_TYPE_KEY__IP:
            ip_repo = Git_Repo.Git_Repo(local_ip_repo_dir_path)
        return ip_repo
            
            
            
    # if repo_type is IP and new_repo_name already exists in given ip_repo's list of submodules, ask if the user would like to continue, end script if no
    def prompt_user_if_continue_if_ip_and_sm_exists(ip_repo, new_repo_name):
        if ip_repo != None:
            sm_name_l = ip_repo.get_submodule_name_l()
            
            if new_repo_name in sm_name_l:
                title = 'Repository Already Exists as Submodule'
                msg = new_repo_name + ' already exists as a submodule of your local ip_repo located at:\n\n"' + ip_repo.path + '"\n\nWould you like to continue anyway?'
                output_define_d = {'yes' : True,
                                   'no'  : False}
                print(cv.WAITING_FOR_USER_INPUT_MSG)
                
                continue_new_repo_setup = mbu.msg_box__YES_NO(title, msg, icon = 'exclaim', output_define_d = output_define_d, app_id = app_id)
    
                if continue_new_repo_setup:
                    return
                else:
                    kill_gui()
                
                
                
    # add new_repo as a submodule of ip_repo and set .branch in .gitmodules to develop
    def add_as_sm_and_set_dot_branch(ip_repo, new_repo):
        ip_repo.run_git_cmd('git submodule add -b develop https://ba-bit.web.boeing.com/scm/mnfcf/' + new_repo.name + '.git ' + new_repo.name, print_output = True, print_cmd = True, run_type = 'call')
        
        
        
    def all_submodules_pull(ip_repo):
        cmd_out = ip_repo.run_git_cmd('git submodule foreach git pull --recurse-submodules', print_output = True, print_cmd = True,  run_type = 'call')
        
        if cmd_out == None or 'You are not currently on a branch. - Please specify which branch you want to merge with.' in cmd_out:
            ip_repo.run_git_cmd('git submodule foreach git checkout develop', run_type = 'call')
            ip_repo.run_git_cmd('git submodule foreach git pull --recurse-submodules', run_type = 'call')



    def prompt_user_to_set_develop_branch(new_repo, repo_type):
        title = 'Set Default Branch!'
        msg = '\n\n' + new_repo.name
        
        if repo_type == cv.REPO_TYPE_KEY__IP:
            msg += ' has been configured and added as a submodule of ip_repo.\n\nAll changes to ip_repo have been pushed, so all watchers will receive an email.'
        else:
            msg += ' has been configured and pushed to its remote.\n\nIf this is a new repository with no watchers, you will need to manually notify any concerned parties that ' + new_repo.name + ' is ready to be cloned.'
        
        msg += '\n\nThe final step to set the default branch to "develop" for this repository.\n\nba-bit.web.boeing.com > projects > MNFCF > ' + new_repo.name + " > Repository settings > Repository details\n\nDon't forget to press the save button!"

        output_define_d = {'ok'     : True,
                           'cancel' : False}

        print(cv.WAITING_FOR_USER_INPUT_MSG)
        
        destroy_gui = mbu.msg_box__OK_CANCEL(title, msg, icon = 'exclaim', app_id = app_id, output_define_d = output_define_d)
        
        # if user clicks cancel, leave everything up, could be useful to go back and check terminal
        if destroy_gui:
            kill_gui() 
                   
        
        
    def prompt_user_push_failed(push_result_str):
        title = 'Push Failed'
        msg = 'Unable to push all branches.\n\nEncountered the following error\n\n' + push_result_str

        print(cv.WAITING_FOR_USER_INPUT_MSG)
        
        mbu.msg_box__OK(title, msg, icon = 'stop', app_id = app_id)




        
    # raise exception if any inputs not valid
    check_if_inputs_valid(repo_type, local_ip_repo_dir_path, repo_remote_url)
    
    # return None if repo_type is not IP
    ip_repo = get_ip_repo(repo_type, local_ip_repo_dir_path)
    
    # get basename of repo with no .git ext
    new_repo_name = get_repo_name_from_url(repo_remote_url)
    
    # if repo_type is IP and new_repo_name already exists in given ip_repo's list of submodules, ask if the user would like to continue, end script if no
    prompt_user_if_continue_if_ip_and_sm_exists(ip_repo, new_repo_name)
    
    # get local path repo will be cloned to
    new_repo_path = get_new_repo_path(repo_type, new_repo_name)
    
    # create new git repo obj
    new_repo = Git_Repo.Git_Repo(new_repo_path)
    new_repo.url = repo_remote_url
    
    # if repo path already exists, ask user if they want to delete it to continue, if user clicks no, ends script
    prompt_user_and_delete_existing_repo_if_needed(new_repo.path, new_repo.name)
    
    # create dir and clone
    fsu.make_dir_if_not_exist(new_repo_path)

    print('\n>> Cloning ' + new_repo.name + ' into "' + new_repo.path + '"...')
    new_repo.clone_to_cwd(print_output = True, print_cmd = True, run_type = 'call')

    # if the cloned repo already has commits, ask the user if they would like to skip the init git flow step, init git flow if not
    skip_init_git_flow_step = prompt_user_if_cloned_repo_has_commits_if_skip_init_git_flow_step(new_repo)    
    if not skip_init_git_flow_step:
        init_git_flow(new_repo)
        
    # set new_repo as submodule of ip_repo, check for more changes, push all changes of ip_repo
    push_result_l = []
    if repo_type == cv.REPO_TYPE_KEY__IP:
        
        if skip_ip_update:
            print('\n>> skip_ip_update == True, so NOT pulling most recent changes for all submodules of ip_repo...')
        else:
            print('\n>> Pulling most recent changes for all submodules of ip_repo...')
            all_submodules_pull(ip_repo)
        
        # add new_repo as a submodule of ip_repo and set .branch in .gitmodules to develop
        print('\n>> Adding ' + new_repo.name + ' as submodule of ip_repo located at: "' + ip_repo.path + '"...')
        add_as_sm_and_set_dot_branch(ip_repo, new_repo)
        
        print('\n>> Committing changes to ip_repo...')
        ip_repo.commit_simple('initialized ' + new_repo.name, print_output = True, print_cmd = True, run_type = 'call')
        
        print('\n>> Pushing changes to ip_repo...')
        push_result_l = ip_repo.push_all_branches(print_output = True, print_cmd = True, shell = True)
    
    # get printable error string in case there was an error on push
    push_result_str = '\n'.join(push_result_l)

    if 'error' in push_result_str:
        prompt_user_push_failed(push_result_str)
    else:
        prompt_user_to_set_develop_branch(new_repo, repo_type)

    print('\n>> Cleaning up...')
    fsu.delete_if_exists(cv.TEMP_DIR_PATH)
    
    
    
    

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--repo_type'             , default = 'IP')
parser.add_argument('-i', '--local_ip_repo_dir_path', default = "C:\\Users\\mt204e\\Documents\\test_ip_repo_2_CE4 - Copy (2)")
parser.add_argument('-r', '--repo_remote_url'       , default = 'https://ba-bit.web.boeing.com/scm/mnfcf/tsm15.git')
parser.add_argument('-a', '--app_id'                , default = 'None')
parser.add_argument('-s', '--skip_ip_update'        , default = 'False')
args = parser.parse_args()

setup_new_repo(
               args.repo_type, 
               args.local_ip_repo_dir_path,
               args.repo_remote_url,
               args.app_id,
               args.skip_ip_update
              )




