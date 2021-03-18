import streamlit as st
import pandas as pd
import numpy as np

st.title("PRU Feedback Survey Dashboard")

col1, col2 = st.beta_columns([3,1])

data = pd.read_csv('sample.csv')

# Extract the date of responses
data.Timestamp = data.Timestamp.apply(lambda x:pd.to_datetime(x[:10]))
dates = df_1.Timestamp.value_counts().sort_index()

timeindex = pd.date_range(start=dates.index[0],end=dates.index[-1])
all_dates = pd.DataFrame(columns=['Number_of_replies'],index=timeindex)

for i in timeindex:
  if i in dates.index:
    all_dates.loc[i,'Number_of_replies'] = dates[i]
  else:
    all_dates[i] = 0

col1.subheader("Response Timeline")
col1.line_chart(all_dates)
