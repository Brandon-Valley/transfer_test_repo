
import os.path
 
 
if __name__ == "__main__": 
    from   usms.file_system_utils import file_system_utils    as fsu
    import                               jsonplus__non_merged as json
else:
    from . usms.file_system_utils import file_system_utils    as fsu
    from . import                        jsonplus__non_merged as json
    
    
 
# changes values of headers already in the file, and appends lines with new headers to the end, or creates new file if dosn't already exist
def log_vars(log_dict, json_file_path):
    if os.path.isfile(json_file_path): 
        json_data = read(json_file_path)
    else:
        json_data = {}
 
    for log_header, log_val in log_dict.items():
        json_data[log_header] = log_val
 
    write(json_data, json_file_path)
                 
     
     
def write(data, output_file_path, indent = 4):
    fsu.make_file_if_not_exist(output_file_path)
     
    with open(output_file_path, 'w') as outfile:  
        json.dump(data, outfile, indent = indent)
        outfile.close()
 
 
 
def read(json_file_path, return_if_file_not_found = "raise_exception"):
#     with open(json_file_path, "r") as read_file:
#         
#         if return_if_file_not_found != "raise_exception":
#             try:
#                 data = json.load(read_file)
#             except FileNotFoundError:
#                 return return_if_file_not_found
#         else:
#             data = json.load(read_file)
#             
#         read_file.close()

    try:
        with open(json_file_path, "r") as read_file:
            data = json.load(read_file)           
        read_file.close()
    except FileNotFoundError as e:
        if return_if_file_not_found != "raise_exception":
            return return_if_file_not_found
        else:
            raise e
        
    return data
     
     
     
def read_fast(json_file_path):
    with open(json_file_path, "r") as read_file:
        data = json.load(read_file)
        read_file.close()
    return data
 
 

if __name__ == '__main__':
    print('In Main:  json_logger')
     
    data = {}  
    data['people'] = []  
    data['people'].append({  
        'name': 'Scott',
        'website': 'stackabuse.com',
        'from': 'Nebraska'
    })
    data['people'].append({  
        'name': 'Larry',
        'website': 'google.com',
        'from': 'Michigan'
    })
    data['people'].append({  
        'name': 'Tim',
        'website': [1,2,3,4],
        'from': 'Alabama'
    })
    # 
    #     
#     write(data,'missing_dir//json_test.jsond')
#     print(read('json_test.jsond'))
    # print(read('project_vars.json'))
     
     
    # var_data = {'a': 5,
    #             'b': 6}
    # 
    # #log_vars(var_data, 'test.json')
    # log_vars({'c': 11}, 'test.json')
     
     
     
     
     
     
     
     
     
     
     
     
    print('End of Main:  json_logger')



