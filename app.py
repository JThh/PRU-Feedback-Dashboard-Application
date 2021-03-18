import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("PRU Feedback Survey Dashboard")



data = pd.read_csv('sample.csv')

# Number of responses along the timeline

data.Timestamp = data.Timestamp.apply(lambda x:pd.to_datetime(x[:10]))
dates = data.Timestamp.value_counts().sort_index()

timeindex = pd.date_range(start=dates.index[0],end=dates.index[-1])
all_dates = pd.DataFrame(columns=['Number_of_replies'],index=timeindex)

for i in timeindex:
  if i in dates.index:
    all_dates.loc[i,'Number_of_replies'] = dates[i]
  else:
    all_dates.loc[i,'Number_of_replies'] = 0

st.subheader("Response Timeline")
st.line_chart(all_dates)

with st.beta_expander("Demography Analysis"):

  st.subheader('Distribution of Respondent Home Faculty')
  df_faculty = data['Which Faculty are you from? (Indicate your home faculty if you are in a double-degree programme)'].value_counts()
  pie = plt.figure(figsize=[10,6])
  labels = df_faculty.index
  plt.pie(x=df_faculty, autopct="%.1f%%", explode=[0.05]*df_faculty.index.shape[0], labels=labels, pctdistance=0.5)
  plt.title("Distribution of Home Faculty", fontsize=14)
  plt.show()
  
  st.subheader('Distribution of Respondent Year of Study')
  st.bar_chart(data['Which Year of Study are you currently in?'].value_counts())

