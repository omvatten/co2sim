import numpy as np
from scipy.optimize import fsolve

#https://omvatten.se/textbook/kap4
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
def get_IS(TDS=0, cond=0, IS=0): #TDS in mg/L, cond in uS/cm
    if IS>0:
        ionS = IS
    elif TDS>0:
        ionS = 2.5*(10**-5)*TDS
    elif cond>0:
        ionS = 1.6*(10**-5)*cond
    else:
        ionS = 0
    return ionS

def C_closed(ct, alk, temp, tds=0, cond=0, IS=0):
    ionS = get_IS(tds, cond, IS)
    g1 = Davies_eq(1, ionS, temp)
    g2 = Davies_eq(2, ionS, temp)

    if ct == 0 and alk == 0:
        co2 = 0
        hco3 = 0
        co3 = 0
        hplus = (Kw(temp)/(g1**2))**0.5
        oh = hplus
    elif alk > 0:
        r3 = -(g1**2)*g2*Ka2(temp)
        r2 = 3*ct*(g1**2)*g2*Ka2(temp)-Kw(temp)*(g2**2)-alk*(g1**2)*g2*Ka2(temp)+(Ka2(temp)**2)*(g1**2)
        r1 = 2*ct*Kw(temp)*(g2**2)-2*(g1**2)*g2*Ka2(temp)*(ct**2)+ct*alk*(g1**2)*g2*Ka2(temp)
        r0 = -Kw(temp)*(g2**2)*(ct**2)
        hco3_roots = list(np.roots([r3, r2, r1, r0]))
        for r in hco3_roots:
            if r > 0 and ct-r > 0:
                hco3 = r
                co3 = ct-hco3
        hplus = Ka2(temp)*hco3/(g2*co3)      
        oh = Kw(temp)/((g1**2)*hplus)
        co2 = (g1**2)*hco3*hplus/Ka1(temp)
    else:
        a = g1**2
        b = (g1**2)*alk+Ka1(temp)
        c = Ka1(temp)*(alk-ct)
        hplus = max((-b+(-4*a*c+b**2)**0.5)/(2*a), 0)
        hco3 = alk + hplus
        co2 = ct - alk - hplus
        co3 = Ka2(temp)*hco3/(g2*hplus)
        oh = Kw(temp)/((g1**2)*hplus)
    return [co2, hco3, co3, oh, hplus]

def C_open(co2, alk, temp, tds=0, cond=0, IS=0):
    ionS = get_IS(tds, cond, IS)
    g1 = Davies_eq(1, ionS, temp)
    g2 = Davies_eq(2, ionS, temp)

    if co2 == 0 and alk == 0:
        co2 = 0
        hco3 = 0
        co3 = 0
        hplus = (Kw(temp)/(g1**2))**0.5
        oh = hplus
    elif alk > 0:
        a = 2*Ka2(temp)*(g1**2)
        b = Ka1(temp)*g2*co2
        c = -Ka1(temp)*g2*co2*alk
        hco3 = max((-b+(-4*a*c+b**2)**0.5)/(2*a), 0)
        co3 = 0.5*(alk-hco3)
        hplus = Ka1(temp)*co2/((g1**2)*hco3)
        oh = Kw(temp)/((g1**2)*hplus)
    else:
        a = g1**2
        b = (g1**2)*alk
        c = -Ka1(temp)*co2
        hplus = max((-b+(-4*a*c+b**2)**0.5)/(2*a), 0)
        hco3 = alk + hplus
        co3 = Ka2(temp)*hco3/(g2*hplus)
        oh = Kw(temp)/((g1**2)*hplus)
    return [co2, hco3, co3, oh, hplus]

def C_ph_alk(ph, alk, temp, tds=0, cond=0, IS=0):
    ionS = get_IS(tds, cond, IS)
    g1 = Davies_eq(1, ionS, temp)
    g2 = Davies_eq(2, ionS, temp)

    hplus = (10**-ph)/g1
    oh = Kw(temp)/((g1**2)*hplus)
    co3 = Ka2(temp)*(alk-oh+hplus)/(g2*hplus+2*Ka2(temp))
    hco3 = hplus*g2*co3/Ka2(temp)
    co2 = (g1**2)*hplus*hco3/Ka1(temp)
    return [co2, hco3, co3, oh, hplus]

###
# def get_ct_ph_alk(C, temp, tds=0, cond=0, IS=0):
#     ionS = get_IS(tds, cond, IS)
#     g1 = Davies_eq(1, ionS, temp)
#     ct = sum(C[:3])
#     ph = -np.log10(g1*C[4])
#     alk = C[1] + 2*C[2] + C[3] - C[4]
#     return ct, ph, alk

# def C_from_pH(ph, alk, temp, tds=0, cond=0, IS=0):
#     ionS = get_IS(tds, cond, IS)
#     g1 = Davies_eq(1, ionS, temp)
#     g2 = Davies_eq(2, ionS, temp)

#     a = np.array([[0, 1, 2, 1],
#                   [-Ka1(temp), (g1**2)*(10**-ph), 0, 0],
#                   [0, -Ka2(temp), g2*(10**-ph), 0],
#                   [0, 0, 0, (g1**2)*(10**-ph)]])
#     b = np.array([[alk + (10**-ph)/g1],
#                   [0],
#                   [0],
#                   [Kw(temp)]])
#     x = np.linalg.solve(a, b) #[CO2, HCO3, CO32-, OH-] mol/L
#     x = np.append(x, 10**-ph)
#     return x.flatten()

# def C_from_CT(ct, alk, temp, C, tds=0, cond=0, IS=0):
#     ionS = get_IS(tds, cond, IS)
#     g1 = Davies_eq(1, ionS, temp)
#     g2 = Davies_eq(2, ionS, temp)

#     def func(x): #x=[co2, hco3-, co32-, oh-, h+]
#         return [x[0]+x[1]+x[2]-ct,
#                 x[1]+2*x[2]+x[3]-x[4]-alk,
#                 -Ka1(temp)*x[0]+(g1**2)*x[4]*x[1],
#                 -Ka2(temp)*x[1]+x[4]*g2*x[2],
#                 (g1**2)*x[4]*x[3]-Kw(temp)]
#     root = fsolve(func, C)
#     return root

    
