from __future__ import print_function

import subprocess
import os
import time


# TEMP_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '//temp.txt'

''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
'''                                                                           
        Internal Functions
'''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''


def print_cmd_if_needed(cmd, print_cmd):
    if print_cmd:
        print('\n  Running cmd:  ', cmd, '...')   
        
        

''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
'''                                                                           
        External Functions
'''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
''' [======- - - - -=================- All Utilities Standard -=================- - - - -======] '''
# to allow for relative imports
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], os.path.dirname(os.path.abspath(__file__))))
''' [======- - - - - - -=============- - - - -========- - - - -=============- - - - - - -======] '''



# if no output, returns none
# if outputs one line, returns string
# if outputs multiple lines, returns list
# try to use this first, if you get an error like below, try run_cmd_call()
    #     for arg in seq:
    # TypeError: 'bool' object is not iterable
# strip will remove all leading or trailing whitespace and newlines from each line
def run_cmd_popen(cmd, print_output = False, print_cmd = False, shell = False, decode = False, strip = False, always_output_list = False, return_stderr = True):
    def get_popen(cmd):
        return subprocess.Popen(cmd, stdout = subprocess.PIPE, bufsize = 1, shell = shell)
    
    def get_cmd_output_line_l(p):
        output_line_l = []
        
        for line in iter(p.stdout.readline, b''):
            
            if decode:
                line = line.decode("utf-8") 
                
            if strip:
                line = line.strip() 
            
            output_line_l.append(line)
            if print_output:
                print (line)
        p.stdout.close()
        p.wait()
        
        return output_line_l
    
    
    def get_stderr_line_l_and_output_line_l(cmd):
        def read(filePath):
            with open(filePath, encoding="utf8") as textFile:  # can throw FileNotFoundError
                out =  list(l.rstrip() for l in textFile.readlines())
            textFile.close()
            return out
        
        # need to do this to allow multiple programs to run at once, should be faster than using a semaphore
        def make_temp_file_and_get_path():
            temp_file_path_base = os.path.dirname(os.path.abspath(__file__)) + '//temp'
            i = 0
            
            while(True):
                temp_file_path = temp_file_path_base + str(i) + '.txt'
                
                if os.path.isfile(temp_file_path):
                    i += 1
                else:
                    with open(temp_file_path, 'w') as fp: 
                        pass
                    fp.close()
                    return temp_file_path
                
                

        temp_file_path = make_temp_file_and_get_path()
        
        with open(temp_file_path, "w") as temp_file:
            output_line_l = ['YOU SHOULD NEVER SEE THIS OUTSIDE OF SUBPROCESS UTILS']  
            try:
                p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = temp_file, bufsize = 1, shell = shell)
                output_line_l = get_cmd_output_line_l(p)
                # output, err = p.communicate() # DONT REMOVE, MIGHT BE USEFUL LATER
            except subprocess.CalledProcessError as e:
                # print(e)  # DONT REMOVE, MIGHT BE USEFUL LATER
                pass              
        stderr_line_l = read(temp_file_path)
        
#         os.remove(temp_file_path)
        try:
            os.remove(temp_file_path)
        except PermissionError:
            time.sleep(1)
            os.remove(temp_file_path)
            
        return stderr_line_l, output_line_l
    
    
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
    
    
    print_cmd_if_needed(cmd, print_cmd)
    
    
    if return_stderr:
        stderr_line_l, output_line_l = get_stderr_line_l_and_output_line_l(cmd)
        
        if stderr_line_l != []:
            for line in stderr_line_l:
                eprint(line) # prints out stderr BE CAREFUL ABOUT ADDING AN OPTION TO GET RID OF THIS, NOT HAVING ERRORS PRINT COULD MAKE DEBUGGING DIFFICULT
            
            output_line_l = stderr_line_l      
        
    else:
        p = get_popen(cmd)
        output_line_l = get_cmd_output_line_l(p)
    

    default_out = None
    if len(output_line_l) == 0:
        default_out = None
    elif len(output_line_l) == 1:
        default_out = output_line_l[0]
    else:
        default_out = output_line_l
        
    if always_output_list:
        if default_out == None:  
            return []
        elif isinstance(default_out, str):
            return [default_out]
        
    return default_out
    
    
    

# try to only use this if run_cmd_popen does not work
def run_cmd_call(cmd, print_cmd = False, shell = False):
    print_cmd_if_needed(cmd, print_cmd)
    subprocess.call(cmd, shell = shell)



# silently returns True / False if running the given command in cmd would result in a fatal error
def fatal_error(cmd):
    try:
        subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
        return False
    except(subprocess.CalledProcessError):
        return True
    
    
    
    
    
    
    
    
    
    
     
if __name__ == "__main__":
    import os

#     os.chdir('C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\repos\\ip_repo')
    
    cmd = 'tasklist'
#     cmd = 'echo hi'
    print_output = True
    print_cmd = True
    shell = False
    decode = True
    strip = True
    always_output_list = False
    stderr_exception = True
    
    out = run_cmd_popen(cmd, print_output, print_cmd, shell, decode, strip, always_output_list, stderr_exception)
    
    print('out:  ', out)
    
    
    
    
    
    
    
#     from submodules.git_tools import Git_Commit
#  
#     Git_Commit.main()
    
    
    
    
    
    
    
    
    
    
    