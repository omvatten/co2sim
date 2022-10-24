import streamlit as st
from PIL import Image

st.title('co2sim')
st.subheader('Simulation of pH, alkalinity, and inorganic carbon in water')
st.markdown('The carbonate system is a series of chemical equilibria between inorganic carbon compounds '
            ' and controls the pH of most natural waters. '
            'It is affected by the dissolution of salts as well as the respiration of living organisms. '
            'Here you can simulate how the carbonate system affects water quality both in simple examples with acids, bases, and salts added to pure water, '
            'and in complex systems where the metabolisms of fish and bacteria affect water quality.')

st.subheader('The carbonate system')
image = Image.open('data/start_fig.png')
st.image(image)
