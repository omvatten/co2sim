import streamlit as st
from PIL import Image

st.title('Simulation of CO2 concentrations in aquaculture')

st.subheader('Flow through one tank')
image1 = Image.open('data/case1.png')
st.image(image1)

st.subheader('Recirulation with nitrification')
image2 = Image.open('data/case2.png')
st.image(image2)


# image1 = Image.open('data/case1.png')
# st.image(image1)

# st.subheader('Influent characteristics')
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     Q_in = float(st.text_input('Flow (m3/d)', value=3.5))
# with col2:
#     pH_in = float(st.text_input('pH', value=7))
# with col3:
#     alk_in = float(st.text_input('Alkalinity (mM)', value=2))
# with col4:
#     temp = float(st.text_input('Temperature (C)', value=25))

# st.subheader('Rearing tank')
# col1, col2, col3 = st.columns(3)
# with col1:
#     fr = float(st.text_input('Feed rate (kg/d)', value=2))
# with col2:
#     vol = float(st.text_input('Tank volume (m3)', value=10))
# with col3:
#     ge = float(st.text_input('Gas exchange KLa (d-1)', value=0))

# st.subheader('Simulation')

# tsteps = 100
# dt = 0.1
# df = pd.DataFrame(pd.NA, index=range(tsteps), columns=['Time', 'CT', 'pH', 'Alk', 'CO2', 'HCO3'])
# X_in = get_Cspec(pH_in, alk_in/1000, temp, tan=0, tds=0, cond=0)
# X = X_in

# for i in range(tsteps):
#     ct, ph, alk = get_ct_ph_alk(X)
#     df.loc[i, :] = [i*dt, ct, ph, alk, X[0]*48/1000, X[1]]
#     X = X + dt*Q_in*(X_in - X) + np.array([0.1, 0, 0, 0, 0, 0])
#     ct, ph, alk = get_ct_ph_alk(X)
#     X = get_Hplus(ct, alk, temp, X)
#     st.write(-np.log10(X[1]*10**-ph/X[0]))
# st.table(df)




# # concsIN = 
# # df.loc[0, ['Time', 'pH', 'Alk', 'CO2']] = [0, -np.log10(concsIN[-1]), alk_in, 48*concsIN[0]/1000]
# # df.loc[0, ['0', '1', '2', '3', '4', '5']] = concsIN
# # for i in range(1, xmax):
# #     concsR = dt*Q_in*(concsIN - df.loc[i-1, ['0', '1', '2', '3', '4', '5']])
# #     concsR[0] = concsR[0] + 0.1
# #     ct, alk = get_ct_alk(concsR)
# #     st.write(concsR)
# #     concsR = get_Hplus(ct, alk, temp, concsR, tan=0, tds=0, cond=0)
# #     df.loc[i, :] = [i, -np.log10(concsR[-1]), alk_in, 48*concsR[0]/1000]

# #     linespH, linesCO2 = plot_animation(df.iloc[:i])
# #     line_plot_pH = line_plot.altair_chart(linespH)
# #     line_plot_CO2 = line_plot.altair_chart(linesCO2)
# #     time.sleep(0.5)


# # #%% Plot
# # linespH = alt.Chart(df).mark_line().encode(
# #      x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
# #      y=alt.Y('pH:Q',axis=alt.Axis(title='pH'))
# # ).properties(
#     width=400,
#     height=200
# )

# linesCO2 = alt.Chart(df).mark_line().encode(
#      x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
#      y=alt.Y('CO2:Q',axis=alt.Axis(title='pH'))
# ).properties(
#     width=400,
#     height=200
# )

# def plot_animation(df):
#     linespH = alt.Chart(df).mark_line().encode(
#          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
#          y=alt.Y('pH:Q',axis=alt.Axis(title='pH'))
#     ).properties(
#         width=600,
#         height=300
#     )
#     linesCO2 = alt.Chart(df).mark_line().encode(
#          x=alt.X('Time:Q',axis=alt.Axis(title='Time')),
#          y=alt.Y('pH:Q',axis=alt.Axis(title='pH'))
#     ).properties(
#         width=600,
#         height=300
#     )
#     return linespH, linesCO2

# col1, col2 = st.columns(2)
# with col1:
#     line_plot_pH = st.altair_chart(linespH)
# with col2:
#     line_plot_CO2 = st.altair_chart(linesCO2)
