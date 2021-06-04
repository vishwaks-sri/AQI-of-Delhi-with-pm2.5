#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import streamlit as st
data=pd.read_excel(r"C:\Users\vishw\Downloads\Delhi .xlsx", header=2)
data.sort_values(by='date', inplace=True)
data.reset_index(drop=True, inplace=True)
data['pm25'].replace(to_replace='-', value=np.nan, inplace=True)
data['pm25'].interpolate(method='linear', inplace=True)
#data1=data.set_index('date')
data.head()


# In[2]:


import statsmodels.api as sma
from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.filterwarnings('ignore')


# In[3]:


model=ARIMA(data['pm25'], order=(5,0,4))
result=model.fit(disp=0)
result.summary


# In[4]:


x=np.arange(2375,2399,1)
future = pd.DataFrame(index=x, columns=data.columns)
data1=pd.concat([data, future])
#data1.tail(24)


# In[5]:


data1['forecast'] = result.predict(2374,2398)
#data1['forecast'].tail(24)


# In[6]:


datax = data1.loc[:,('pm25','forecast')]
#datax.tail(24)


# In[7]:


st.title('DELHI PM2.5 FORECASTING FOR NEXT 24 HOURS')
from PIL import Image
st.sidebar.header('HeatMap of 4 Months')
image = Image.open(r'C:\Users\vishw\Downloads\myapp\PM_Hour.png')
st.sidebar.image(image, caption='HEATMAP')

st.sidebar.header('Box Plot Hourly')
image = Image.open(r'C:\Users\vishw\Downloads\myapp\Box Plot Hourly.png')
st.sidebar.image(image, caption='BOXPLOT')

st.sidebar.header('Line Plot of 4 Months')
image = Image.open(r'C:\Users\vishw\Downloads\myapp\line_plot.png')
st.sidebar.image(image,caption='LINEPLOT')


# In[8]:


st.subheader('Forecast for 24 hours')
st.line_chart(datax[['pm25','forecast']][2000:], width=24, height=5)


# In[11]:


import datetime
from dateutil.relativedelta import relativedelta, MO
start = datetime.datetime.strptime("2018-04-20 01:00:00", "%Y-%m-%d %H:%M:%S")
date_list = [start + relativedelta(hours=x) for x in range(0,24)]
df = pd.DataFrame({'x':x, 'y':date_list})
st.header('User Input Parameters')
date_and_hour = st.selectbox('date / Time',(df.y))
a = df['x'][df['y'] == date_and_hour].values[0]
st.write(datax['forecast'][a])


# In[ ]:




