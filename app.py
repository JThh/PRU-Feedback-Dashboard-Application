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
st.markdown('Exploratory Analysis on Some Specific Questions')


data = pd.read_csv('sample.csv')

# Number of responses along the timeline

with st.beta_expander('Time Series Analysis'):
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
  
  data['count'] = 1
  
  data.rename({'Which Faculty are you from? (Indicate your home faculty if you are in a double-degree programme)':'Faculty',
              'Which Year of Study are you currently in?': 'Year of Study'}, axis='columns',inplace=True)
  df_faculty = data[['Faculty','count']].groupby(['Faculty']).count().reset_index()
  df_year = data[['Year of Study','count']].groupby(['Year of Study']).count().reset_index()
  
  fig = px.pie(
      df_faculty, 
      names="Faculty", 
      values="count", 
      color="Faculty",
      title='Which Faculty are you from?'
  )
  st.plotly_chart(fig)
  
  st.subheader('Distribution of Respondent Year of Study')
  fig = px.bar(
      df_year, 
      x="count", 
      y="Year of Study", 
      color = "Year of Study",
      orientation='h', 
      title='Which year of study are you currently in'
  )
  
  st.plotly_chart(fig)  
  
with st.beta_expander('Textual Analysis'):
  
  df_zoning = data['I feel that the zoning restrictions were ________.'].dropna()

  st.header('I feel that the zoning restrictions were ________.')
  if st.checkbox('Show n random comments',True,key='1'):
    number = st.slider('Number of comments to take a look at:', 1, 10, 5,key='1')
    sample = df_zoning.sample(number)
    st.table(sample)
  
  st.subheader('Wordcloud')
  
  def build_wordcloud(df, title):
    wordcloud = WordCloud(
        background_color='gray', 
        stopwords=set(STOPWORDS), 
        max_words=50, 
        max_font_size=40, 
        random_state=666
    ).generate(str(df))

    fig = plt.figure(1, figsize=(14,14))
    plt.axis('off')
    fig.suptitle(title, fontsize=16)
    fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    st.pyplot()
   
  clouds = st.slider('Select n comments to visualize their collective word clouds',1,df_zoning.shape[0],key='select')
  if st.button('Click to show the cloud',key='cloud'):
      build_wordcloud(df_zoning.sample(clouds), f'Word Cloud for {clouds} sampled comments')

  
#   fig, ax = plt.subplots()
#   labels = df_faculty.index
#   plt.pie(x=df_faculty, 
#           autopct="%.1f%%", 
#           explode=[0.05]*df_faculty.index.shape[0], 
#           labels=labels, 
#           pctdistance=0.5)
 
#   plt.title("Distribution of Home Faculty", fontsize=14)
#   col1.pyplot(fig)
  
#   col2.subheader('Distribution of Respondent Year of Study')
#   fig, ax = plt.subplots()
#   plt.bar(df_year.index,df_year.values,width=0.3)
#   plt.title("Distribution of Year of Study", fontsize=14)
#   col2.pyplot(fig)


# with st.beta_expander("Textual Analysis"):
  
  
  
  
