'''
Created on 17 Jul 2014

@author: dels
'''
import math


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
    SV.sort()
    return ( SV,K )

'''
 --------------------------------------------------------------------------------
This is the Passing-Bablok analysis process
 -------------------------------------------------------------------------------- 
'''
def Passing_Bablok(PtTable):
    # calculate Slopes for all pairs of Var1,Var2 : estimated Slope is the median
    (SV,K) = calc_slopes(PtTable)

    # find the estimated slope and confidence limits
    M0 = (len(SV)-1) / 2.
    if M0 == int(M0):
        Beta_Est = SV[K+int(M0)]    # odd count
    else:
        Beta_Est = 0.5*(SV[K+int(M0-0.5)]+SV[K+int(M0+0.5)])
    (M1,M2) = calc_CI ( SV,K,len(PtTable) )
    (Beta_LB,Beta_UB) = (SV[K+M1],SV[K+M2])
    print "N: %d,  n: %d,   M0:  %d,  M1:  %d, M2:  %d, K:  %d" % (len(SV),len(PtTable),M0,M1,M2,K)

    # calculate the intercept
    Alpha_Est = calc_intercept(PtTable, Beta_Est)
    Alpha_LB = calc_intercept(PtTable, Beta_UB)
    Alpha_UB = calc_intercept(PtTable, Beta_LB)
    
    return (Beta_Est,Beta_LB,Beta_UB),(Alpha_Est,Alpha_LB,Alpha_UB)
    
    
