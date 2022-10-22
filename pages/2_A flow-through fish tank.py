import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from PIL import Image
import help_functions as hf

st.subheader('Flow through one tank')
image1 = Image.open('data/case1.png')
st.image(image1)

st.subheader('Influent characteristics')
col1, col2, col3 = st.columns(3)
with col1:
    Q_in = float(st.text_input('Flow (m\u00B3/h)', value=2))
    temp_in = float(st.text_input('Temperature influent (C)', value=25))
with col2:
    pH_in = float(st.text_input('pH', value=7))
    alk_in = float(st.text_input('Alkalinity (mM)', value=2))/1000
with col3:
    st.markdown('One of the following:')
    tds_in = float(st.text_input('Total dissolved salts (mg/L)', value=0))
    cond_in = float(st.text_input('Conductivity (uS/cm)', value=0))

st.subheader('Fish tank')
col1, col2, col3 = st.columns(3)
with col1:
    mfish = float(st.text_input('Fish amount (kg)', value=300))
    vol = float(st.text_input('Tank volume (m\u00B3)', value=15))
with col2:
    temp = float(st.text_input('Temperature (C)', value=15))
    kla = float(st.text_input('Gas exchange KLa (h\u207B\u00B9)', value=0))
with col3:
    rO2 = float(st.text_input('O\u2082 consumption (gO\u2082/kg.h)', value=0.83))
    rCO2 = float(st.text_input('CO\u2082 production (gCO\u2082/kg.h)', value=1.08))
    rN = float(st.text_input('TAN production (gTAN/kg.h)', value=0.13))

st.subheader('Results')
st.markdown('Calculate the concentrations of inorganic carbon in the fish tank')
if st.button('Run simulation'):
    #Influent and starting conditions
    Cin = hf.C_ph_alk(pH_in, alk_in, temp_in, tds=tds_in, cond=cond_in)
    ct_in = sum(Cin[:3])
    co2_air = hf.KHCO2(temp)*(412*10**-6)
    Ctank = Cin
    net_prod_ct = rCO2*mfish/(44*vol*1000) + kla*(co2_air-Ctank[0])

    #If there is a net production, calculate steady-state values
    if abs(net_prod_ct) > 0:
        dt = 0.25*ct_in/abs(net_prod_ct)
        ct = ct_in
        diff = 0

        #Use finite difference method to reach steady state Ct
        for i in range(50):
            ct_new = sum(Ctank[:3]) + dt*((Q_in/vol)*(ct_in-sum(Ctank[:3])) + rCO2*mfish/(44*vol*1000) + kla*(co2_air-Ctank[0]))
            Ctank = hf.C_closed(ct_new, alk_in, temp, tds=tds_in, cond=cond_in)

            #Update dt
            net_prod_ct = (Q_in/vol)*(ct_in-sum(Ctank[:3])) + rCO2*mfish/(44*vol*1000) + kla*(0-Ctank[0])
            diff_new = ct_new-ct
            if diff_new == 0:
                break
            elif diff/diff_new < 0 and i > 3:
                dt = 0.1*dt
            else:
                dt = min(0.25*sum(Ctank[:3])/abs(net_prod_ct), 1.5*dt)
            ct = ct_new
            diff = diff_new

    #Print results
    st.markdown('Steady-state concentrations:')
    IS = hf.get_IS(TDS=tds_in, cond=cond_in)
    g1 = hf.Davies_eq(1, IS, temp)
    st.markdown('pH = '+str(round(-np.log10(g1*Ctank[4]),2)))

    if 1000*alk_in < 0.01 and 1000*alk_in > -0.01:
        p_alk1 = f'{1000*alk_in:.2e}'
        p_alk2 = f'{1000*100.0869*alk_in:.2e}'
    else:
        p_alk1 = str(round(1000*alk_in, 2))
        p_alk2 = str(round(1000*100.0869*alk_in, 2))
    st.markdown('Alk = '+p_alk1+' mM = '+p_alk2+ ' mg/L as CaCO\u2083')

    if IS < 10**-20:
        p_IS = '0'
    elif 1000*IS < 0.01:
        p_IS = f'{1000*IS:.2e}'
    else:
        p_IS = str(round(1000*IS, 2))
    st.markdown('Ionic strength = '+p_IS+' mM')

    if Ctank[0] < 10**-20:
        p_co2 = '0 mM = 0 mg/L'
    elif 1000*Ctank[0] < 0.01:
        p_co2 = f'{1000*Ctank[0]:.2e} mM = '+ f'{1000*44*Ctank[0]:.2e} mg/L'
    else:
        p_co2 = str(round(1000*Ctank[0], 2)) + ' mM = ' + str(round(1000*44*Ctank[0], 2)) + ' mg/L'
    st.markdown('[CO<sub>2</sub>(aq)] = '+p_co2, unsafe_allow_html=True)

    if Ctank[1] < 10**-20:
        p_hco3 = '0 mM'
    elif 1000*Ctank[1] < 0.01:
        p_hco3 = f'{1000*Ctank[1]:.2e} mM'
    else:
        p_hco3 = str(round(1000*Ctank[1], 2)) + ' mM'
    st.markdown('[HCO<sub>3</sub><sup>-</sup>] = '+p_hco3, unsafe_allow_html=True)

    if Ctank[2] < 10**-20:
        p_co3 = '0 mM'
    elif 1000*Ctank[2] < 0.01:
        p_co3 = f'{1000*Ctank[2]:.2e} mM'
    else:
        p_co3 = str(round(1000*Ctank[2], 2)) + ' mM'
    st.markdown('[CO<sub>3</sub><sup>2-</sup>] = '+p_co3, unsafe_allow_html=True)


