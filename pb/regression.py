'''
Created on 14 Jul 2014

@author: dels
'''
import argparse
import csv
from passing_bablok import Passing_Bablok
from deming import Deming_LR

'''
 ------------------------------------------------------
 configure the parser and parse command line
'''

def setup_args():
    # configure arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--FILE", help="name of CSV file")
    parser.add_argument("--LABEL", help="name of ID field")
    parser.add_argument("--VAR1", help="name of data field 1")
    parser.add_argument("--VAR2", help="name of data field 2")
    args = parser.parse_args()
    if args.FILE:
        File = args.FILE
    else:
        File = 'Test-Data.csv'
        
    if args.LABEL:
        Label = args.LABEL
    else:
        Label = 'ID'
        
    if args.VAR1:
        Var1 = args.VAR1
    else:
        Var1 = 'M1'
        
    if args.VAR2:
        Var2 = args.VAR2
    else:
        Var2 = 'M2'
        
    return (File,Label,Var1,Var2)

def read_results(File,Label,Name1, Name2):
    Points=[]
    with open(File, 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print row
            # don't import incomplete pairs
            v1 = row.get(Name1)
            v2 = row.get(Name2)
            if v1 != '' and v2 != '':
                Points.append( ( row.get(Label), float(v1), float(v2) ) )
    return Points


'''
 --------------------------------------------------------------------------------
This is the Test controller process
 -------------------------------------------------------------------------------- 
'''
if __name__ == '__main__':
    
    # set up runtime arguments: Name1 is name of V1, Name2 is name of V2
    (File, Label, Name1, Name2) = setup_args()
    print "Var1= %s,  Var2= %s" % (Name1,Name2)
    
    # initialise data arrays from stdin (file) in .csv format
    PtTable = read_results(File, Label, Name1, Name2)
    
    # compute the slope and intercept (and CI of each) by Passing-Bablok LR
    (Beta_Est,Beta_LB,Beta_UB),(Alpha_Est,Alpha_LB,Alpha_UB) = Passing_Bablok(PtTable)
    print "Passing-Bablok\nSlope:     %10.6f\t  LB:  %10.6f\t   UB:  %10.6f" % (Beta_Est,Beta_LB,Beta_UB)
    print "Intercept: %10.6f\t  UB:  %10.6f\t   LB:  %10.6f" % (Alpha_Est,Alpha_UB,Alpha_LB)

    # compute the slope and intercept by Deming LR
    (Beta_D,Beta_D_L,Beta_D_U),(Alpha_D,Alpha_D_L,Alpha_D_U) = Deming_LR(PtTable)
    print "Deming\nSlope:     %10.6f\t  LB:  %10.6f\t   UB:  %10.6f" % (Beta_D,Beta_D_L,Beta_D_U)
    print "Intercept: %10.6f\t  UB:  %10.6f\t   LB:  %10.6f" % (Alpha_D,Alpha_D_U,Alpha_D_L)
    
    # compute the slope and intercept by OLR
    # print the results
    pass

