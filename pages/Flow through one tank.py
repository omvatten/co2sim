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
col1, col2, col3, col4 = st.columns(4)
with col1:
    Q_in = float(st.text_input('Flow (m3/d)', value=3.5))
with col2:
    pH_in = float(st.text_input('pH', value=7))
    alk_in = float(st.text_input('Alkalinity (mM)', value=2))
with col3:
    temp_in = float(st.text_input('Temperature influent (C)', value=25))
with col4:
    st.markdown('One of the following:')
    tds_in = float(st.text_input('Total dissolved salts (mg/L)', value=0))
    cond_in = float(st.text_input('Conductivity (mg/L)', value=0))

st.subheader('Rearing tank')
col1, col2, col3, col4 = st.columns(4)
with col1:
    fr = float(st.text_input('Feed rate (kg/d)', value=0.5))
with col2:
    vol = float(st.text_input('Tank volume (m3)', value=10))
with col3:
    ge = float(st.text_input('Gas exchange KLa (d-1)', value=0))
with col4:
    temp = float(st.text_input('Temperature (C)', value=25))

st.subheader('Simulation')
col1, col2, col3 = st.columns(3)
with col1:
    sim_time = float(st.text_input('Simulation time (d)', value=10))

dt = 0.1
tsteps = int(sim_time/dt)+1
df = pd.DataFrame(pd.NA, index=range(tsteps), columns=['Time', 'CT', 'pH', 'Alk', 'CO2', 'HCO3', 'CO32-', 'TAN'])

if st.button('Run simulation'):
    dt = 0.1
    tsteps = int(sim_time/dt)+1
    df = pd.DataFrame(pd.NA, index=range(tsteps), columns=['Time', 'CT', 'pH', 'Alk', 'CO2', 'HCO3', 'CO32-', 'TAN'])
    C_in = hf.C_from_pH(ph=pH_in, alk=alk_in/1000, temp=temp_in, tds=0, cond=0)
    N_in = np.array([0, 0, 0, 0]) #TAN, NH4+, NH3, NO3-
    C = C_in.copy(); N = N_in.copy()

    for i in range(tsteps):
        ct, ph, alk = hf.get_ct_ph_alk(C, temp)
        df.loc[i, :] = [i*dt, ct, ph, alk, C[0]*44*1000, C[1], C[2], N[0]*14*1000]

        #Calculate next C and N
        C = C + dt*Q_in*(C_in - C)/vol
        C[0] = C[0] + dt*fr*(200*1.3/44)/(vol*1000)
        ct, ph, alk = hf.get_ct_ph_alk(C, temp)
        C = hf.C_from_CT(ct, alk, temp, C)
        
        N = N + dt*Q_in*(N_in - N)/vol
        N[0] = N[0] + dt*fr*(30/14)/(vol*1000)

    fig1 = alt.Chart(df).mark_line().encode(
          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
          y=alt.Y('pH:Q',axis=alt.Axis(title='pH'))
          ).properties(width=400, height=200)
    fig2 = alt.Chart(df).mark_line().encode(
          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
          y=alt.Y('CO2:Q',axis=alt.Axis(title='CO2 (mg/L)'))
          ).properties(width=400, height=200)
    fig3 = alt.Chart(df).mark_line().encode(
          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
          y=alt.Y('Alk:Q',axis=alt.Axis(title='Alk (mM)'))
          ).properties(width=400, height=200)
    fig4 = alt.Chart(df).mark_line().encode(
          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
          y=alt.Y('TAN:Q',axis=alt.Axis(title='TAN (mg/L)'))
          ).properties(width=400, height=200)
    st.altair_chart((fig1 | fig2) & (fig3 | fig4))



