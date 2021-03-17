import streamlit as st
import pandas as pd
import numpy as np

st.title("PRU Feedback Survey Dashboard")

col1, col2 = st.beta_columns([3,1])

data = pd.read_csv('sample.csv')

# Extract the date of responses
dates = data[['Timestamp','Which Year of Study are you currently in?']].groupby(['Timestamp']).count()

col1.subheader("Response Timeline")
col1.line_chart(dates)
