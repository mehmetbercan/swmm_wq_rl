

import os



def UpdateTextFile(file_path, par_val, line_no, start_col_no, val_lenght):
    '''
    Parameters
    ----------
    file_path : string
        path of the text file
    par_val : float
        the value to be inserted into the text file
    line_no : integer
        the number of line (e.g. 1 is for the first line of the file)
    start_col_no : integer
        number of space (column) on the line above (e.g. 1 is for the first column of the line)
    val_lenght : integer
        length of the value in the text file (par_val gets same lenght to val_lenght)

    Returns
    -------
    Updates the text file indicated in file_path
    
    P.S.
    line_no and start_col_no can directly be read from notepad++

    '''
    # read lines from the file
    File = open(file_path, "r") # open the file
    lines = File.readlines() # Read lines
    File.close()
    
    # change indicated line value
    lines[line_no-1] = lines[line_no-1][:start_col_no-1] +\
                        str(round(par_val,2))[:val_lenght].ljust(val_lenght) +\
                            lines[line_no-1][(start_col_no-1 + val_lenght):]
    
    
    # update the lines in the text file
    os.remove(file_path) #remove the file
    File = open(file_path, "w")
    for i in range(len(lines)):
        File.write(lines[i])
    File.close()

# file_path = r'C:\PROJECTCODE\UVA_CODES\swmm_wq_rl\swmm_models\test.inp'
# par_val = -0.436
# line_no = 1937
# start_col_no = 47
# val_lenght = 5
# UpdateTextFile(file_path, par_val, line_no, start_col_no, val_lenght)