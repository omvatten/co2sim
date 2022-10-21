import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from PIL import Image
import time
import help_functions as hf

st.subheader('Flow through one tank')
image2 = Image.open('data/case2.png')
st.image(image2)
