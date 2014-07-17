'''
Created on 14 Jul 2014

@author: dels
'''
import argparse, math
import csv

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
------------------------------------------------------------
 calculate the index of the upper and lower confidence bounds
'''
def calc_CI(SSlope,K,n):
    w = 1.96
    N = len(SSlope)
    CI = w * math.sqrt( (n*(n-1)*(2*n+5))/18 )
    M1 = int(round((N-CI)/2))     #pythen lists are 0-based
    M2 = N-M1-1
    print "N: %d,  n: %d,  CI:  %d,  M1:  %d, M2:  %d, K:  %d" % (N,n,CI,M1,M2,K)
    
    return (M1,M2)

'''
--------------------------------------------------------------------------------
  calculate intercept given slope
'''
def calc_intercept(Points,Slope):
    temp = []
    for i in range(len(Points)):
        temp.append( Points[i][2] - Slope * Points[i][1] )
    return median(temp)



'''
---------------------------------------------------------------
 find the median of a list of numbers
 sort them and return the value in the middle
 if there are an even number, average the two middle values
'''
def median( DataList ):
    temp = DataList
    temp.sort()
    Num = len(temp)
    if Num % 2:
        return temp[(Num-1)/2]   # odd
    else:
        return (temp[Num/2-1]+temp[Num/2])/2.0

'''
---------------------------------------------------------------
 calculate the slope of the line between each pair of points
 ignore pairs that are identical
 exclude slopes equal to -1
 sort slopes in ascending order
 return the table of slopes, and the number of values less than -1
'''
def calc_slopes(Points):
    # Points is a list of 3-tuples (ID,Var1,Var2)
    def calc(Pt1,Pt2):
        dy = Pt2[2]-Pt1[2]
        dx = Pt2[1]-Pt1[1]
        if dx != 0:
            slope = dy/dx
        elif dy < 0:
            slope = -1.e+23
        elif dy > 0:
            slope = 1.e+23
        else:
            slope = None    
        return slope
    
    SV = []
    K=0
    for i in range(len(Points)-1):
        for j in range(i+1,len(Points)):
            slope = calc(Points[i],Points[j])
            if slope != None:
                SV.append ( slope )
                K += (slope < -1)
    return ( SV.sort(),K )

'''
 --------------------------------------------------------------------------------
This is the Passing-Bablok analysis process
 -------------------------------------------------------------------------------- 
'''
def Passing_Bablok(PtTable):
    # calculate Slopes for all pairs of Var1,Var2 : estimated Slope is the median
    (SV,K) = calc_slopes(PtTable)

    # find the estimated slope and confidence limits
    M0 = len(SV) / 2.
    (M1,M2) = calc_CI ( SV,K,len(PtTable) )
    (Beta_Est,Beta_LB,Beta_UB) = (SV[M0],SV[M1],SV[M2])

    # calculate the intercept
    Alpha_Est = calc_intercept(PtTable, Beta_Est)
    Alpha_LB = calc_intercept(PtTable, Beta_UB)
    Alpha_UB = calc_intercept(PtTable, Beta_LB)
    
    return (Beta_Est,Beta_LB,Beta_UB),(Alpha_Est,Alpha_LB,Alpha_UB)
    
    

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
    print "Slope:     %10.6f\t  LB:  %10.6f\t   UB:  %10.6f" % (Beta_Est,Beta_LB,Beta_UB)
    print "Intercept  %10.6f\t  UB:  %10.6f\t   LB:  %10.6f" % (Alpha_Est,Alpha_UB,Alpha_LB)
    
    # compute the slope and intercept by OLR
    # compute the slope and intercept by Deming LR
    # print the results
    pass

