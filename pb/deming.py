'''
Created on 17 Jul 2014

@author: dels
'''
import math
from jackknife import jackknife


'''
 --------------------------------------------------------------------------------
This is the Deming regression process
 -------------------------------------------------------------------------------- 
'''
def Deming(PtTable):
    '''
    from Matlab
    n            = length(y);  % Number of elements
    m_x          = mean(x);    % Mean value of x
    m_y          = mean(y);    % Mean value of y
    c_xy         = cov(x,y);   % Covariance matrix of x and y
    s_xx         = c_xy(1);    % Variance of x
    s_xy         = c_xy(2);    % Covarince of x and y
    s_yy         = c_xy(4);    % Variance of y
    % Assign slope an intercept (in closed-form)
    b(2)         = (s_yy - lambda*s_xx + sqrt((s_yy - lambda*s_xx).^2 + 4*lambda*s_xy^2)) ./ ...
                   (2*s_xy);
    b(1)         = m_y - b(2)*m_x;
    
    '''

    # calculate Slopes for all pairs of Var1,Var2 : estimated Slope is the median
    lamda = 1.0
    n = len(PtTable)
    xBar = 0.0
    yBar = 0.0
    for i in range(n):
        xBar += float(PtTable[i][1])/n
        yBar += float(PtTable[i][2])/n
    (Sxx,Sxy,Syy) = (0.0,0.0,0.0)
    for i in range(n):
        Sxx += (PtTable[i][1]-xBar)**2 / (n-1)
        Syy += (PtTable[i][2]-yBar)**2 / (n-1)
        Sxy += (PtTable[i][1]-xBar)*(PtTable[i][2]-yBar) / (n-1)

    # slope
    beta = (Syy - lamda*Sxx + math.sqrt( (Syy - lamda*Sxx)**2 + 4*lamda*(Sxy**2)) ) / (2*Sxy)
    # intercept
    alpha = yBar - beta*xBar
    
    return (beta, alpha, xBar, yBar)

def Deming_S(Points):
    (slope,a,b,c) = Deming(Points)
    return slope

'''
   Deming_LR applies the Statistical Jackknife 
   to find confidence limits on the Deming regression coefficients
'''
def Deming_LR(PtTable):
    # compute the expected slope and intercept
    (slope,intercept,xBar,yBar) = Deming(PtTable)
    
    # compute the 95% confidence interval
    (sBar, sVar, sLB, sUB) = jackknife(Deming_S,PtTable)
    iUB = yBar - sLB*xBar
    iLB = yBar - sUB*xBar
    
    #return slope and intercept with confidence limits
    return (slope,sLB,sUB),(intercept,iLB,iUB)
    
    return
