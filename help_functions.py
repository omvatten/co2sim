import numpy as np
from scipy.optimize import fsolve

def KHCO2(temp):
    k = -6.53*(10**-5)*temp**2 + 1.55*(10**-2)*temp + 1.12
    return 10**-k

def Ka1(temp):
    k = 1.48*(10**-4)*temp**2 - 1.29*(10**-2)*temp + 6.58
    return 10**-k

def Ka2(temp):
    k = 1.19*(10**-4)*temp**2 - 1.50*(10**-2)*temp + 10.63
    return 10**-k

def KspCaCO3(temp):
    k = -3.58*(10**-5)*temp**2 + 1.37*(10**-2)*temp + 8.02
    return 10**-k

def Kw(temp):
    k = 0.0001705*temp**2 - 0.0420541*temp + 14.9406004
    return 10**-k

def Ktan(temp):
    k = 2706/(temp+273.15) + 0.139
    return 10**-k

def Davies_eq(z, IS, temp):
    water_dielectric = 87.740 - 0.4008*temp + 9.398*(10**-4)*temp**2 - 1.41*(10**-6)*temp**3 
    A = 1.82*(10**6)*(water_dielectric*(temp+273.15))**(-3/2)
    f = -A*(z**2)*((IS**0.5)/(1+IS**0.5)-0.2*IS)
    return 10**f

#http://users.mhu.edu/facultystaff/mnewman/environ%20chem/Lab/solids/Relationships%20between%20Measurable%20Properties%20of%20Water.htm
def get_IS(TDS=0, cond=0): #TDS in mg/L, cond in uS/cm
    if TDS>0:
        IS = 2.5*(10**-5)*TDS
    elif cond>0:
        IS = 1.6*(10**-5)*cond
    else:
        IS = 0
    return IS

def C_from_pH(ph, alk, temp, tds=0, cond=0):
    ionS = get_IS(tds, cond)
    g1 = Davies_eq(1, ionS, temp)
    g2 = Davies_eq(2, ionS, temp)

    a = np.array([[0, 1, 2, 1],
                  [-Ka1(temp), (g1**2)*(10**-ph), 0, 0],
                  [0, -g1*Ka2(temp), g1*g2*(10**-ph), 0],
                  [0, 0, 0, (g1**2)*(10**-ph)]])
    b = np.array([[alk + (10**-ph)],
                  [0],
                  [0],
                  [Kw(temp)]])
    x = np.linalg.solve(a, b) #[CO2, HCO3, CO32-, TAN, OH-] mol/L
    x = np.append(x, 10**-ph)
    return x.flatten()

def C_from_CT(ct, alk, temp, C, tds=0, cond=0):
    ionS = get_IS(tds, cond)
    g1 = Davies_eq(1, ionS, temp)
    g2 = Davies_eq(2, ionS, temp)

    def func(x): #x=[co2, hco3-, co32-, oh-, h+]
        return [x[0]+x[1]+x[2]-ct,
                x[1]+2*x[2]+x[3]-x[4]-alk,
                -Ka1(temp)*x[0]+(g1**2)*x[4]*x[1],
                -g1*Ka2(temp)*x[1]+g1*x[4]*g2*x[2],
                (g1**2)*x[4]*x[3]-Kw(temp)]
    root = fsolve(func, C)
    return root

def get_ct_ph_alk(conc, temp):
    ct = sum(conc[:3])
    ph = -np.log10(conc[4])
    alk = conc[1] + 2*conc[2] + conc[3] - conc[4]
    return ct, ph, alk



    
