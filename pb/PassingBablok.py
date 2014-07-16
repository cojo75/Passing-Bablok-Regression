'''
Created on 14 Jul 2014

@author: dels
'''
import argparse, math
import csv
'''
---------------------------------------------------------------
 generate a table of all (N*(N-1)/2)  distinct pairs of values and their difference
'''
def combine(Vector):
    CV = []
    for i in range(len(Vector)-1):
        for j in range(i+1,len(Vector)):
            CV.append ( [ Vector[i],Vector[j],Vector[j]-Vector[i] ] )
    return CV

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
 validate each row of data points, removing incomplete entries
'''
def validate( Label, Var1, Var2 ):
    for i in range(len(Label)-1,-1,-1):
        if not Var1[i] or Var1[i] == 0 or not Var2[i] or Var2[i] == 0 :
            print "Removing:", Label.pop(i), Var1.pop(i), Var2.pop(i)
    return (Label, Var1, Var2)

'''
---------------------------------------------------------------
 calculate the slope of the line between each pair of points
 ignore pairs that are identical
 exclude slopes equal to -1
 sort slopes in ascending order
 return the table of slopes, and the number of values less than -1
'''
def calc_slopes(Var1,Var2):
    SV=[]
    K=0
    for i in range(len(Var1)):
        d2 = Var2[i][2]
        d1 = Var1[i][2]
        if (d1 != 0 or d2 != 0) and (d1 != -d2):
            try:
                Slope = d2/d1
            except:
                if d2 > 0:
                    Slope = 1.e+23 
                else: 
                    Slope = -1.e+23
            K += (Slope < -1)
            SV.append(Slope)
    SV.sort()
    return (SV,K)

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
    ID = []
    Var1 = []
    Var2 = []
    with open(File, 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print row
            # don't import incomplete pairs
            v1 = row.get(Name1)
            v2 = row.get(Name2)
            if v1 != '' and v2 != '':
                ID.append(row.get(Label))
                Var1.append(float(v1))
                Var2.append(float(v2))

    return (ID,Var1,Var2)

'''
------------------------------------------------------------
 pick the LB & UB of Slope 
'''
def slope_CI(SSlope,n,N,K):
    w = 1.96
    CI = w * math.sqrt( (n*(n-1)*(2*n+5))/18 )
    M1 = int(round((N-CI)/2)) 
    M2 = N - M1
    print "N: %d,  n: %d,  CI:  %d,  M1:  %d, M2:  %d, K:  %d" % (N,n,CI,M1,M2,K)
    
    result = (SSlope[K+M1], SSlope[K+M2])
    #print "UB: %f,  LB: %f" % result
    
    return result

'''
--------------------------------------------------------------------------------
  calculate intercept given slope
'''
def calc_intercept(Var1,Var2,Slope):
    AV = []
    for i in range(len(Var1)):
        AV.append( Var2[i] - Slope * Var1[i] )
    return median(AV)

'''
 --------------------------------------------------------------------------------
This is the Passing-Bablok analysis process
 -------------------------------------------------------------------------------- 
'''
def Passing_Bablok(Var1,Var2):
    # enumerate all pairs of each measurand with their difference
    CV1 = combine(Var1)
    CV2 = combine(Var2)
    
    # calculate Slopes for all pairs of Var1,Var2 : estimated Slope is the median
    (SV,K) = calc_slopes(CV1,CV2)
    Beta_Est = median(SV[K:])
    
    # find the confidence limits on the slope
    (Beta_LB,Beta_UB) = slope_CI(SV,len(Var1),len(SV),K)
    
    # calculate the intercept
    Alpha_Est = calc_intercept(Var1, Var2, Beta_Est)
    Alpha_LB = calc_intercept(Var1, Var2, Beta_UB)
    Alpha_UB = calc_intercept(Var1, Var2, Beta_LB)
    
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
    (ID, V1, V2) = read_results(File, Label, Name1, Name2)
    
    # remove samples where either Variable is Undefined
    (ID,V1,V2) = validate(ID,V1,V2)

    # compute the slope and intercept (and CI of each) by Passing-Bablok LR
    (Beta_Est,Beta_LB,Beta_UB),(Alpha_Est,Alpha_LB,Alpha_UB) = Passing_Bablok(V1,V2)
    print "Slope:     %10.6f\t  LB:  %10.6f\t   UB:  %10.6f" % (Beta_Est,Beta_LB,Beta_UB)
    print "Intercept  %10.6f\t  UB:  %10.6f\t   LB:  %10.6f" % (Alpha_Est,Alpha_UB,Alpha_LB)
    
    # compute the slope and intercept by OLR
    # compute the slope and intercept by Deming LR
    # print the results
    pass

