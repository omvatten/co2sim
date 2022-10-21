import streamlit as st
from PIL import Image

st.title('Simulation of pH, alkalinity, and inorganic carbon in water')
st.markdown('The carbonate system controls the pH of most natural waters. '
            'It is a series of chemical equilibria between inorganic carbon compounds. '
            'It is affected by the dissolution of salts as well as the respiration of living organisms. '
            'Here you can simulate how the carbonate system affects water quality in several types of systems.')

st.subheader('The carbonate system')
image = Image.open('data/start_fig.png')
st.image(image)
