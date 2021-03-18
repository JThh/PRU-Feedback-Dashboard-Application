import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly.graph_objs as go
from wordcloud import WordCloud, STOPWORDS

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
  
  col1,col2 = st.beta_columns(2)

  col1.subheader('Distribution of Respondent Home Faculty')
  df_faculty = data['Which Faculty are you from? (Indicate your home faculty if you are in a double-degree programme)'].value_counts()
  df_year = data['Which Year of Study are you currently in?'].value_counts()
  
  fig, ax = plt.subplots()
  labels = df_faculty.index
  plt.pie(x=df_faculty, 
          autopct="%.1f%%", 
          explode=[0.05]*df_faculty.index.shape[0], 
          labels=labels, 
          pctdistance=0.5)
 
  plt.title("Distribution of Home Faculty", fontsize=14)
  col1.pyplot(fig)
  
  col2.subheader('Distribution of Respondent Year of Study')
  fig, ax = plt.subplots()
  plt.bar(df_year.index,df_year.values,width=0.3)
  plt.title("Distribution of Year of Study", fontsize=14)
  col2.pyplot(fig)


with st.beta_expander("Textual Analysis"):
  
  
  
  
