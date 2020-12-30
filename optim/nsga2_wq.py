
#-------------------------------------------------------------------------------
# Name:        NSGA-II
# Purpose:     Calculates objective functions for NSGA-II
#
# Author:      Mehmet B. Ercan (mehmetbercan@gmail.com)
#
# Created:     12/30/2020
# Edited:      
# Copyright:   (c) Mehmet B. Ercan 2014
# Licence:     MIT
#-------------------------------------------------------------------------------


import os
from nsga2lib import nsga2, nsga2utilities

HERE = os.path.dirname(os.path.realpath(__file__))

sys.path.append(HERE)
import SWMM_utils

# Objective Function Calculator: Equvalent of Model Run and Calculate Objective Function
def Run_SWMM_Model(para_vals, para_swmm, path_swmm):
    '''
    SCH is a one parameter and two fitness problem. Optimal solution is within
    0 and 2. Upper and lower limits are -10**3 and 10**3, respectively.
    '''
    # update SWMM input file
    for par, val in para_vals.items():
        ln, col, lenght = para_swmm[par]
        SWMM_utilsUpdateTextFile(path_swmm, val, ln, col, lenght)
        
    # run SWMM model
        
    # get objective functions
    x = parvals[0]
    f1 = x**2
    f2 = (x - 2)**2
    return [f1, f2]


def CalculateObjectiveFunctions(population, para_dict):
    """
    This function must be modified by user. Fitness values in population dictionary has to be updated here.
    Objective function values are considered to be best once they get closer to zero and worst when they are closer to +1 (or +infinity)
    """
    #/*Initializing the max rank to zero*/
    population["maxrank"]=0
    
    popsize = len(population["ind"])

    ParameterValues=[]
    for i in range(popsize):
        ParameterValues.append(population["ind"][i]["xbin"]) #/* problem variables */
        
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#This part should be edited by the user based on the specific model to be calibrated.
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    #Population Loop: Paralization can be  applied here
    for i in range(popsize): 
        #Edit model input parameters using ParameterValues[i]
        parvals=ParameterValues[i]
  
        
        #Calculate Objective functions
        para_val = {}
        for j in range(len(para_dict)):
            key = list(para_dict.keys())[j]
            para_vals[key] = parvals[j]
        objectivefuncs = Run_SWMM_Model(para_vals, para_swmm)
                      
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#The user should stop editing after this line.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        #Add objective functions to population
        population["ind"][i]['fitness'] = objectivefuncs
    return;
#-------------------------------------------------------------------------------

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# Define NSGA2 Settings
setting_dict = {'PopSize': 150,
                'GenNumber': 20,
                'CrossPrb': 0.9,
                'CrossTyp': 2,
                'Bits': 16,
                'MutPrb': 0.5,
                'seed': 0.5,
                'ObjFuncNum': 2,
                'M': 1000,
                'ReadMFrmOut': 0}
# Define Parameters and their limits
para_dict = {"st1_tp": [-0.80, -0.01], "st1_tn": [-0.80, -0.01], 
             "st2_tp": [-0.80, -0.01], "st2_tn": [-0.80, -0.01]} 
# Define SWMM file location for each parameter as [line_no, start_col_no, val_lenght]
para_swmm = {"st1_tp": [1938, 46, 5], "st1_tn": [1939, 46, 5], 
                 "st2_tp": [1941, 46, 5], "st2_tn": [1942, 46, 5]}
# --------------------------------------------------------------------
# --------------------------------------------------------------------



NSGAII=nsga2.nsga2(setting_dict, para_dict, HERE) 
NSGAII.CreateInitialPopulation(CalculateObjectiveFunctions)

#Loop through generations
TotalNumGenerations = NSGAII.ngener
i=0
while i < TotalNumGenerations:
    '''
    INFO:
        NSGAII.new_pop_ptr=child population; 
        NSGAII.vlen=the no.of bits assigned to the each calibration parameters; 
        NSGAII.lim_b=range of calibration parameters (upper and lower bounds).
    '''
    
    
    print ('Running generation: {} ...'.format(i))
    
    #Thorough selection, crossover and mutation child population created from old population
    NSGAII.CreateChildPopulation() 
    
    #Turn binary calibration parameters into normal numbers
    nsga2utilities.decode(NSGAII.new_pop_ptr, NSGAII.vlen, NSGAII.lim_b); 

    
    # calculate fitness
    CalculateObjectiveFunctions(NSGAII.new_pop_ptr);
    
    # ranking based on calculated objective functions
    nsga2utilities.rankcon(NSGAII.new_pop_ptr);
    
    NSGAII.CreateParentPopulation(i+1) # Old and New populations goes throuth Elitism, crowding distances, nondominated sorting
    #and create the old population for next generation. Report is printed during this function process.

    # plot
    df = nsga2utilities.CreatePopulationDataframe(NSGAII.mate_pop_ptr, NSGAII.parname)
    df[['f1', 'f2']].plot.scatter('f1','f2', title='Generation {}'.format(i+1), figsize=(6.5,6))
    
    i+=1


print("The NSGA-II execution finished. Look at the results in NSGA2.OUT folder.");

