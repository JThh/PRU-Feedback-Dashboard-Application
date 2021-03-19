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

import nltk
nltk.download('vader_lexicon') 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Disable the warnings.
st.set_option('deprecation.showPyplotGlobalUse', False)

# Some utility functions.
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
  
def categorize(senti):
  if senti < 0:
    return 'Negative'
  elif senti == 0:
    return 'Neutral'
  else:
    return 'Positive'
  
  
 
# Set the title and basic layout of the application.
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
  
  st.dataframe(all_dates)
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
  
  df_zoning = data['I feel that the zoning restrictions were ________.'].rename_axis('comments')

  st.header('I feel that the zoning restrictions were _.')
  if st.checkbox('Show n random comments',True,key='1'):
    number = st.slider('Number of comments to take a look at:', 1, 10, 5,key='1')
    sample = df_zoning.sample(number)
    st.table(sample)
  
  st.subheader('Wordcloud')
 
   
  clouds = st.slider('Select n comments to visualize their collective word clouds',1,df_zoning.shape[0],key='select')
  if st.button('Click to show the cloud',key='cloud'):
      build_wordcloud(df_zoning.sample(clouds), f'Word Cloud for {clouds} sampled comments')
      
    
  
  st.subheader('Sentiment Analysis')
  st.markdown('The sentiment is evaluated as a polarity score ranging from -1 to 1. The lower the comment is scored, the less positive it tends to be.')
  
  sid = SentimentIntensityAnalyzer()
  scores = pd.Series([sid.polarity_scores(str(text))['compound'] for text in df_zoning.values],name='score')
  df_zoning_score = pd.concat([df_zoning, scores],axis=1)
  df_zoning_score.columns = ['comments','scores']
  if st.checkbox('Show some examples',False,key='score'):
    st.table(df_zoning_score.sample(5))
    
  df_zoning_score['category'] = df_zoning_score.scores.apply(lambda x:categorize(x))
  
  st.dataframe(df_zoning_score['category'])
    
  st.markdown('To make easier comparison, the sentiment is categoried into \'positive\', \'neutral\' and \'negative\' based on their polarity score. Now it\'s time to visualize our findings.')
  
  combined_with = st.multiselect('Combine the result with', ('Faculty','Year of Study'),key='combo')
  
  if 'Faculty' in combined_with:
    faculties = data.Faculty.unique()
    df_fac_sen = pd.concat([df_zoning_score.category, data.Faculty],axis=1)
    df_fac_sen['count'] = 1
    fac_pos = df_fac_sen.groupby(['category','Faculty']).count()
    counts = pd.DataFrame(columns = ['Negative','Neutral','Positive'], index=faculties)
    
    for i in counts.columns:
      for j in counts.index:
        if (i,j) not in fac_pos.index:
          counts.loc[j,i] = 0
        else:
          counts.loc[j,i] = fac_pos.loc[i,j]['count']
   
    fig = go.Figure(data=[
        go.Bar(name='Negative', x=faculties, y=counts['Negative']),
        go.Bar(name='Neutral', x=faculties, y=counts['Neutral']),
        go.Bar(name='Positive', x=faculties, y=counts['Positive'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)
    
  elif 'Year of Study' in combined_with:
    years = data['Year of Study'].unique()
    df_year_sen = pd.concat([df_zoning_score.category, data['Year of Study']],axis=1)
    df_year_sen['count'] = 1
    year_pos = df_year_sen.groupby(['category','Year of Study']).count()
    counts = pd.DataFrame(columns = ['Negative','Neutral','Positive'], index=years)
    
    for i in counts.columns:
      for j in counts.index:
        if (i,j) not in year_pos.index:
          counts.loc[j,i] = 0
        else:
          counts.loc[j,i] = year_pos.loc[i,j]['count']    
    
    fig = go.Figure(data=[
        go.Bar(name='Negative', x=years, y=counts['Negative']),
        go.Bar(name='Neutral', x=years, y=counts['Neutral']),
        go.Bar(name='Positive', x=years, y=counts['Positive'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)    

  


  
  
  
  
