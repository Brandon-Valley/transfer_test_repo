if __name__ == "__main__": 
    from   usms.file_system_utils import file_system_utils as fsu
    from   usms.exception_utils   import exception_utils   as eu
else:
    from . usms.file_system_utils import file_system_utils as fsu
    from . usms.exception_utils   import exception_utils   as eu
 
 

DEFAULT_HEADER_MARK = ': '



''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
'''                                                                           
        Simple / General Use
'''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''


def read(filePath):
    with open(filePath) as textFile:  # can throw FileNotFoundError
        out =  list(l.rstrip() for l in textFile.readlines())
    textFile.close()
    return out
        

# lines  = if not a list, will convert to string and write it as one line,
#          each element will be written as a new line in the txt file,
#          lines[0] will be first line in the file,
#          elements can be any type, will be converted to str before writing

def write(lines, filePath, write_mode = 'overwrite'):
    eu.error_if_param_key_not_in_whitelist(write_mode, ['overwrite', 'append'])
    fsu.make_file_if_not_exist(filePath)
    
    # convert to str
    if type(lines) == list or type(lines) == tuple:
        str_converted_lines = []
        for line in lines:
            str_converted_lines.append(str(line))
    else:
        str_converted_lines = [str(lines)]
    
    # write lines to file
    if   write_mode == 'overwrite':
        writeFile = open(filePath, "w") 
    elif write_mode == 'append':
        writeFile = open(filePath, "a")

    for line_num, line in enumerate(str_converted_lines):
        writeFile.write(line)
        
        # do not write newline if you just wrote the last line
        if line_num != len(str_converted_lines) - 1:
            writeFile.write('\n')
 
    writeFile.close() #to change file access modes 
  




''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
'''                                                                           
        Variable Logger - Prettier than Json Dictionary Log
'''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''

#

# MOST SIMPLE WRITE FUNCTION, MOSTLY HERE FOR EXAMPLE PURPOSES
#
# Original .TXT FILE:  (same output if no file exists)
# 
#     nameA: Harry
#     nameB: Bob
#     nameC: Mark
#     nameD: Captain Falcon
#
# INPUT:
#  
#     logDict = { 'color1': 'Blue',
#                 'color2': 'Green',     
#                 'color3': 'Red'}  
#
#     headerOrderList = ['color1', 'color2', 'color3']    
# 
# Final .TXT FILE:
# 
#     color1: Blue
#     color2: Green
#     color3: Red
#
# creates new file or overwrites existing existing file
def overwriteVarsSimple(filePath, logDict, headerOrderList, headerMark = DEFAULT_HEADER_MARK):
    f = open(filePath, 'w')
    
    for header in headerOrderList:
        f.write(header + headerMark + logDict[header] + '\n') 
        
    f.close()
    
    
    
    
# Original .TXT FILE:  (same output if no file exists)
# 
#     nameA: Harry
#     nameB: Bob
#     nameC: Mark
#     nameD: Captain Falcon
#
# INPUT:
#  
#     logDict = { 'color1': 'Blue',
#                 'color2': 'Green',     
#                 'color3': 'Dark Red'}  
#
#     headerOrderList = ['color1', 'color2', 'color3']    (optional but without it, order will be random)
# 
# Final .TXT FILE:
# 
#     color1: Blue
#     color2: Green
#     color3: Red
#
# creates new file or overwrites existing file
def overwriteVars(filePath, logDict, headerOrderList = None, headerMark = DEFAULT_HEADER_MARK):
    f = open(filePath, 'w')
    
    if headerOrderList == None:
        for header, value in logDict.items():
            f.write(header + headerMark + logDict[header] + '\n')  
    else:
        for header in headerOrderList:
            f.write(header + headerMark + logDict[header] + '\n')     
                
    f.close()
    
    
    
    
# Original .TXT FILE: 
# 
#     nameA: Harry
#     nameB: Bob
#     nameC: Mark
#     nameD: Captain Falcon
#
# INPUT:
#  
#     logDict = { 'color1': 'Blue',
#                 'color2': 'Green',     
#                 'color3': 'Dark Red',
#                 'nameB  : 'MARRY}  
#
#     headerOrderList = ['nameA', 'color1', 'color2', 'nameB', 'nameC', 'color3', 'nameD']     (optional but without it, any new lines 
#                                                                                               added will be appended to the end randomly)
# Final .TXT FILE:
# 
#     nameA: Harry
#     color1: Blue
#     color2: Green
#     nameB: MARRY
#     nameC: Mark
#     color3: Red
#     nameD: Captain Falcon
#
# changes values of headers already in the file, and appends lines with new headers to the end, or creates new file if dosn't already exist
def logVars(filePath, logDict, headerOrderList = None, headerMark = DEFAULT_HEADER_MARK):
    try:
        ogLogDict, ogHeaderOrderList = readVars(filePath, True)
    except:# if file dosn't exist yet
        ogLogDict = {}
        ogHeaderOrderList = []
    
    f = open(filePath, 'w')
    
    #add everything without a matching header to logDict
    for header, value in ogLogDict.items():
        if header not in logDict:
            logDict[header] = value

    if headerOrderList == None:
        for header in ogHeaderOrderList:
            f.write(header + headerMark + logDict[header] + '\n')
            del logDict[header] 
        
        for header, value in logDict.items():
            f.write(header + headerMark + logDict[header] + '\n') 
    else:
        for header in headerOrderList:
            f.write(header + headerMark + logDict[header] + '\n')  
        
    f.close()
    
    

# INPUT .TXT FILE:
#
#     color1: Blue
#     color2: Green
#     color3: Red
#
#
#
# OUTPUT:   (if wantHeaderOrderList == True)
#  
#      (  logDict = { 'color1': 'Blue',     ,     headerOrderList = ['color1', 'color2', 'color3']  )
#                     'color2': 'Green',     
#                     'color3': 'Red'}  
# 
# OTHERWISE, OUTPUT:
#
#     logDict = { 'color1': 'Blue',
#                 'color2': 'Green',     
#                 'color3': 'Red'} 
#
def readVars(filePath, wantHeaderOrderList = False, headerMark = DEFAULT_HEADER_MARK):
    logDict = {}
    headerOrderList = []
    
    with open(filePath) as textFile:  # can throw FileNotFoundError
        raw_lines = tuple(l.rstrip() for l in textFile.readlines())
        
    for line in raw_lines:
        header, value = line.split(headerMark)
        
        headerOrderList.append(header)
        logDict[header] = value
        
    textFile.close()
        
    if wantHeaderOrderList == True:
        return (logDict, headerOrderList)
    else:
        return logDict



    
    

if __name__ == '__main__':
    print('In Main:  txt_logger')
    
#     write('teeeeeeeeeeest.txt', [2, ' sss dfsga ', '\n\n mdmsdonhf   '])
#     write('teeeeeeeeeeest.txt', 'sdiondfolwsdnoilfn')
    
    
#     filename0 = 'examples/txt_logger_examples/colorList.txt'
#        
#     headerOrderList0 = ['color1', 'color2', 'color3']    
#         
#     logDict0 = {'color1': 'Blue',
#                 'color2': 'Green',     
#                 'color3': 'Dark Red'}
#     
#         
#     filename1 = 'examples/txt_logger_examples/nameList.txt'
#     
#     logDict1 = {'nameA': 'Harry',
#                 'nameB': 'Bob',
#                 'nameC': 'Mark',
#                 'nameD': 'Captain Falcon'}
#     
#     
#     
#     logVars(filename0, logDict0, headerOrderList0)
#     resultDict0, resultHeaderOrderList0 = readVars(filename0, True)
#     print('resultDict0: ', resultDict0)
#     print('resultHeaderOrderList0: ', resultHeaderOrderList0)
#     print('')
#     
#     logVars(filename1, logDict1,)
#     resultDict1 = readVars(filename1)
#     print('resultDict1: ', resultDict1)
#     print('')
#     
#     print('done!')
#         
#         
        
    print('End of Main:  txt_logger')
    
    
    
    
    
    
    
    
    
    
    
    
    