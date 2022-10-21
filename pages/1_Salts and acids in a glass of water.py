import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from PIL import Image
import help_functions as hf

first = st.container()
second = st.container()
third = st.container()

with first:
    st.title('Salts, acids and bases in a glass of water')
    st.markdown('Calculate how the addition of salts, acids and bases, and exposure to CO<sub>2</sub> '
                'affect pH, alkalinity, and concentrations of inorganic carbon compounds in water.', unsafe_allow_html=True)
    st.markdown('Specify concentrations and temperature below. Click *Calculate* to see results.')
    image0 = Image.open('data/case0.png')
    st.image(image0)

with second:
    st.subheader('Input')
    col1, col2, col3 = st.columns(3)
    with col1:
        nacl = float(st.text_input('NaCl (mmol/L)', value=0))/1000
    with col2:
        hcl = float(st.text_input('HCl (mmol/L)', value=0))/1000
        naoh = float(st.text_input('NaOH (mmol/L)', value=0))/1000
    with col3:
        hco3 = float(st.text_input('NaHCO3 (mmol/L)', value=0))/1000
        co3 = float(st.text_input('Na2CO3 (mmol/L)', value=0))/1000
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Closed or open?\n'
                    'In an open system, we assume that the CO<sub>2</sub> concentration '
                    'in water is in equilbrium with the CO<sub>2</sub> partial pressure in the atmosphere.', unsafe_allow_html=True)
        open_closed = st.radio('Closed or open', options=['Closed', 'Open'], label_visibility='collapsed')
        pco2 = float(st.text_input('CO2 partial pressure (atm)', value=0.0004))
        if pco2 == 0:
            pco2 = 10**-14
    with col2:
        temp = float(st.text_input('Temperature (C)', value=25))

#Calculation section
def closed_calc(nacl, hcl, naoh, hco3, co3, temp):
    alk = hco3+2*co3+naoh-hcl
    IS_est = 0.5*(nacl*2 + hcl + naoh + hco3*2 + co3*2+co3*4)
    ct = hco3 + co3
    conc = hf.C_closed(ct, alk, temp, IS=IS_est)
    for i in range(3):
        IS = 0.5*(nacl+naoh+hco3+2*co3+hcl+conc[1]+conc[2]*4+conc[3]+conc[4])
        conc = hf.C_closed(ct, alk, temp, IS=IS)
    return conc, ct, alk, IS

def open_calc(nacl, hcl, naoh, pco2, hco3, co3, temp):
    alk = hco3+2*co3+naoh-hcl
    IS_est = 0.5*(nacl*2 + hcl + naoh + hco3*2 + co3*2+co3*4)
    co2 = hf.KHCO2(temp)*pco2
    conc = hf.C_open(co2, alk, temp, IS=IS_est)
    for i in range(3):
        IS = 0.5*(nacl+naoh+hco3+2*co3+hcl+conc[1]+conc[2]*4+conc[3]+conc[4])
        conc = hf.C_open(co2, alk, temp, IS=IS)
    return conc, sum(conc[:3]), alk, IS

with third:
    st.subheader('Results')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('Calculate results based on the input parameters specified above.')
        if st.button('Calculate'):
            if open_closed == 'Closed':
                conc, ct, alk, IS = closed_calc(nacl, hcl, naoh, hco3, co3, temp)
                co2 = conc[0]            
           
            elif open_closed == 'Open':
                conc, ct, alk, IS = open_calc(nacl, hcl, naoh, pco2, hco3, co3, temp)
                co2 = conc[0]            
    
            #Print results
            g1 = hf.Davies_eq(1, IS, temp)
            st.markdown('pH = '+str(round(-np.log10(g1*conc[4]),2)))

            if 1000*alk < 0.01 and 1000*alk > -0.01:
                p_alk = f'{1000*alk:.2e}'
            else:
                p_alk = str(round(1000*alk, 2))
            st.markdown('Alk = '+p_alk+' mM')
    
            if IS < 10**-20:
                p_IS = '0'
            elif 1000*IS < 0.01:
                p_IS = f'{1000*IS:.2e}'
            else:
                p_IS = str(round(1000*IS, 2))
            st.markdown('Ionic strength = '+p_IS+' mM')
    
            if co2 < 10**-20:
                p_co2 = '0 mM = 0 mg/L'
            elif 1000*co2 < 0.01:
                p_co2 = f'{1000*co2:.2e} mM = '+ f'{1000*44*co2:.2e} mg/L'
            else:
                p_co2 = str(round(1000*co2, 2)) + ' mM = ' + str(round(1000*44*co2, 2)) + ' mg/L'
            st.markdown('[CO<sub>2</sub>(aq)] = '+p_co2, unsafe_allow_html=True)
    
            if conc[1] < 10**-20:
                p_hco3 = '0 mM'
            elif 1000*conc[1] < 0.01:
                p_hco3 = f'{1000*conc[1]:.2e} mM'
            else:
                p_hco3 = str(round(1000*conc[1], 2)) + ' mM'
            st.markdown('[HCO<sub>3</sub><sup>-</sup>] = '+p_hco3, unsafe_allow_html=True)
    
            if conc[2] < 10**-20:
                p_co3 = '0 mM'
            elif 1000*conc[2] < 0.01:
                p_co3 = f'{1000*conc[2]:.2e} mM'
            else:
                p_co3 = str(round(1000*conc[2], 2)) + ' mM'
            st.markdown('[CO<sub>3</sub><sup>2-</sup>] = '+p_co3, unsafe_allow_html=True)

        #Relationships
        with col2:
            st.markdown('Examine the effect of one parameter. Choose parameter below and specify the range of values to examine. '
                        'The rest of the parameters will be kept at the values specified above.')
            par = st.radio('Choose parameter', options=['NaCl', 'HCl', 'NaOH', 'NaHCO3', 'Na2CO3', 'Temperature', 'CO2 partial press.'])
            op_cl = st.radio('Open or closed system?', options=['Closed', 'Open'])

            min_val = float(st.text_input('Min. value', value=0))
            max_val = float(st.text_input('Max. value', value=10))
            yvals = [[par, 'pH', 'alk', 'ct', 'CO2', 'HCO3', 'CO3']]
            if par == 'NaCl':
                xvals = np.linspace(min_val/1000, max_val/1000, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(x, hcl, naoh, hco3, co3, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(x, hcl, naoh, pco2, hco3, co3, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([1000*x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'HCl':
                xvals = np.linspace(min_val/1000, max_val/1000, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, x, naoh, hco3, co3, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, x, naoh, pco2, hco3, co3, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([1000*x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'NaOH':
                xvals = np.linspace(min_val/1000, max_val/1000, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, hcl, x, hco3, co3, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, hcl, x, pco2, hco3, co3, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([1000*x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'NaHCO3':
                xvals = np.linspace(min_val/1000, max_val/1000, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, hcl, naoh, x, co3, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, hcl, naoh, pco2, x, co3, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([1000*x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'Na2CO3':
                xvals = np.linspace(min_val/1000, max_val/1000, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, hcl, naoh, hco3, x, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, hcl, naoh, pco2, hco3, x, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([1000*x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'Temperature':
                xvals = np.linspace(min_val, max_val, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, hcl, naoh, hco3, co3, x)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, hcl, naoh, pco2, hco3, co3, x)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])
            elif par == 'CO2 partial press.':
                xvals = np.linspace(min_val, max_val, num=20)
                for x in xvals:
                    if op_cl == 'Closed':
                        conc, ct, alk, IS = closed_calc(nacl, hcl, naoh, hco3, co3, temp)
                    elif op_cl == 'Open':
                        conc, ct, alk, IS = open_calc(nacl, hcl, naoh, x, hco3, co3, temp)
                    g1 = hf.Davies_eq(1, IS, temp)
                    pH = -np.log10(g1*conc[4])
                    yvals.append([x, pH, 1000*alk, 1000*ct, 1000*conc[0], 1000*conc[1], 1000*conc[2]])

            #['pH', 'alk', 'ct', 'CO2', 'HCO3', 'CO3']
            yvals = pd.DataFrame(yvals[1:], columns=yvals[0])
            if st.button('Show relationships'):
                base_chart = alt.Chart(yvals).mark_line().encode(x=alt.X(par, axis=alt.Axis(title=par))).properties(width=150, height=100)
                ph_c = base_chart.encode(y=alt.Y('pH', axis=alt.Axis(title='pH')))
                alk_c = base_chart.encode(y=alt.Y('alk', axis=alt.Axis(title='Alk (mM)')))
                ct_c = base_chart.encode(y=alt.Y('ct', axis=alt.Axis(title='CT (mM)')))
                co2_c = base_chart.encode(y=alt.Y('CO2', axis=alt.Axis(title='Carbon dioxide (mM)')))
                hco3_c = base_chart.encode(y=alt.Y('HCO3', axis=alt.Axis(title='Bicarbonate (mM)')))
                co3_c = base_chart.encode(y=alt.Y('CO3', axis=alt.Axis(title='Carbonate (mM)')))
                fig = (ph_c | alk_c ) & (ct_c | co2_c ) & (hco3_c | co3_c)
                st.altair_chart(fig)
                
                st.write(yvals)

            