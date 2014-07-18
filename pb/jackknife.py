'''
Created on 18 Jul 2014

@author: dels

 the Statistical Jackknife returns the mean, SD, and two-sided 95% confidence interval for a set of data
 inputs:
     method()    - a function that returns a single value depending on a set of data points
     points[]    - an array of tuples appropriate to the analysis function
 outputs:
     stats        - a tuple including (mean, variance, lower bound, upper bound) on the calculated quantity
'''

import math

def jackknife(method,points):
    '''
    this is a method for estimating the expected value and confidence interval for a complex calculated quantity
    the method was developed by Quenouille (1949) and Tukey (1958)
    it involves applying the 'method' on N subset of the data, where a different point is dropped each time
    the t-Statistic is then applied to the array of results
    '''
    # first generate the pseudo--samples
    (S,i) = ([],0)
    while i < len(points):
        t = points.pop()                             # remove the last point from the series
        S.append(method(points))                     # apply method to remaining points
        points.insert(0,t)                           # add it back as the first
        i += 1
    # the data is back in the original order
    
    # get the mean and variance of S
    (sumS,sumSsq,numS) = (0.0,0.0,len(S))
    for s in S:
        sumS += s
        sumSsq += s**2
    meanS = sumS / numS
    varS = (sumSsq/numS - meanS**2) * (numS/(numS-1))   # unbiased variance

    lb    = meanS - 1.96*math.sqrt(varS/numS)
    ub    = meanS + 1.96*math.sqrt(varS/numS)

    return (meanS, varS, lb, ub)
    