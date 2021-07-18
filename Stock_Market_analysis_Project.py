#!/usr/bin/env python
# coding: utf-8

# #  Stock Market Analysis

# We'll be analyzing stock data related to a few car companies (Tesla , Ford , General Motors), from Jan 1 2012 to Jan 1 2017. 

# In[1]:


#importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('default')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#importing Data
tesla = pd.read_csv('Tesla_Stock.csv' , index_col = 'Date' , parse_dates = True)
tesla.head(10)


# In[3]:


ford = pd.read_csv('Ford_Stock.csv' , index_col = 'Date' , parse_dates = True)
ford.head(10)


# In[4]:


gm = pd.read_csv('GM_Stock.csv' , index_col = 'Date' , parse_dates = True) 
gm.head(10)


# In[5]:


#Visualizing The Open Price of all the stocks
plt.figure(figsize = (16,8) , dpi = 150)
tesla['Open'].plot(label='Tesla' , color = 'orange')
gm['Open'].plot(label='GM')
ford['Open'].plot(label='Ford')
plt.title('Open Price Plot')
plt.xlabel('Years')
plt.legend();


# In[6]:


#Visualizing The Volume Of Stock Traded Each Day
plt.figure(figsize = (16,8) , dpi = 150)
tesla['Volume'].plot(label='Tesla')
gm['Volume'].plot(label='GM')
ford['Volume'].plot(label='Ford')
plt.title('Volume Traded')
plt.xlabel('Years')
plt.legend();


# We can see there is a spike in Volume Traded of Ford in late 2013.

# In[7]:


#timeStamp for this Spike
ford.iloc[ford['Volume'].argmax()]

2013-12-18 00:00:00 is the timeStamp.
What Happened On this day?
-> Ford warns that 2014 profit margins will fall
Ford shares fell sharply in early trading this morning after the company warned that its profit margins would fall next year, largely due to the cost of launching a record number of new vehicles and continuing troubles in Europe.

Source : https://www.usatoday.com/story/money/cars/2013/12/18/ford-2014-profit-warning/4110015/
# The Open Price Time Series Visualization makes Tesla look like its always been much more valuable as a company than GM and Ford. But to really understand this we would need to look at the total market cap of the company, not just the stock price. Unfortunately our current data doesn't have that information of total units of stock present. But what we can do as a simple calcualtion to try to represent total money traded would be to multply the Volume column by the Open price. Remember that this still isn't the actual Market Cap, its just a visual representation of the total amount of money being traded around using the time series

# In[8]:


#Visualizing The Total Market Capacity of the Company
tesla['Total Traded'] = tesla['Open']*tesla['Volume']
ford['Total Traded'] = ford['Open']*ford['Volume']
gm['Total Traded'] = gm['Open']*gm['Volume']


# In[9]:


tesla['Total Traded'].plot(label='Tesla',figsize=(16,8))
gm['Total Traded'].plot(label='GM')
ford['Total Traded'].plot(label='Ford')
plt.legend()
plt.ylabel('Total Traded');


# We can See there is a huge spike in Total Stocks traded of Tesla in Early 2014.

# In[10]:


tesla.iloc[tesla['Total Traded'].argmax()]

#timeStamp - 2014-02-25 00:00:00
What happened on this day?
-> Shares of the electric car maker continued to march deeper into record territory Wednesday, building on the previous day's rally, when shares surged 14%.
The stock has gained more than 30% since Tesla (TSLA) reported much stronger-than-expected profit and raised its sales targets last week.
The fourth-quarter results reignited Tesla's momentum in the stock market, which faded a bit late last year. After falling below $130 last October, Tesla shares blasted through $200 last week and rose to a high above $250 on Tuesday. Tesla debuted on the stock market in 2010 at less than $20 a share

#Source -> https://money.cnn.com/2014/02/25/investing/tesla-record-high/
# In[11]:


#Visualizing Open Price With Moving Averages (35 , 15) For Tesla
tesla['MA15'] = tesla['Open'].rolling(15).mean()
tesla['MA35'] = tesla['Open'].rolling(35).mean()
tesla[['Open','MA15','MA35']].plot(label='TLSA',figsize=(16,8))


# Now We will check if there is Any Correlation between stock of Two Comapanies(using Scatter Matrix and Heat_map), after all belong to same Industry

# In[12]:


from pandas.plotting import scatter_matrix
matrix = pd.concat([tesla['Open'],gm['Open'],ford['Open']],axis=1)
matrix.columns = ['Tesla_Open','GM_Open','Ford_Open']
#scatter Matrix
scatter_matrix(matrix,figsize=(10,10),alpha=0.1,hist_kwds={'bins':50});


# In[14]:


#Heat_map
import seaborn as sns
matrix = matrix.corr()
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(matrix, vmax=.8, square=True, cmap="Blues")


# As seen from Scatter_matrix Open Prices for Ford And Gm are highly Correlated

# # candlestick Chart 

# In[19]:


# Create a CandleStick chart for Ford in January 2012 using mpl_finance
import mplfinance as mpf
plt.figure(figsize = (30,15) , dpi = 250)

plt.style.use('ggplot')
mpf.plot(ford.loc['2012-01':'2012-01']  ,type='candle')


# In[21]:


#creating A more detailed Candlestick Chart with Moving Averages (2 , 4 and 6) along with Volume Traded
kwargs = dict(type='candle',mav=(2,4,6),volume=True,figratio=(30,15),figscale=0.9)
mpf.plot(ford.loc['2012-01':'2012-01'],**kwargs,style='charles')


# # Basic Financial Analysis

# # Daily Percentage Change
This defines r_t (return at time t) as equal to the price at time t divided by the price at time t-1 (the previous day) minus 1. Basically this just informs you of your percent gain (or loss) if you bought the stock on day and then sold it the next day. While this isn't necessarily helpful for attempting to predict future values of the stock, its very helpful in analyzing the volatility of the stock. If daily returns have a wide distribution, the stock is more volatile from one day to the next. Let's calculate the percent returns and then plot them with a histogram, and decide which stock is the most stable!
# In[23]:


#using pct_change for 1 day
tesla['returns'] = tesla['Close'].pct_change(1)
ford['returns'] = ford['Close'].pct_change(1)
gm['returns'] = gm['Close'].pct_change(1)


# In[39]:


# we will plot Histograms to Visualize the Volatility of A stock. More Wider The Distribution more Volatile a stock is.
# More volatile a stock is more drastically prices of stock can change (high_risk , high_reward)
tesla['returns'].hist(bins = 50 , color = 'red')


# In[40]:


ford['returns'].hist(bins=50 , color = 'orange')


# In[41]:


gm['returns'].hist(bins=50 , color = 'green')


# plotting All three histograms At top of one Another for better Visalization

# In[50]:


tesla['returns'].hist(bins=100,label='Tesla',figsize=(8,6),alpha=0.5)
gm['returns'].hist(bins=100,label='GM',alpha=0.5)
ford['returns'].hist(bins=100,label='Ford',alpha=0.5)
plt.legend()


# returns of Tesla are more widely Distributed ,that means Stocks of Tesla are more Volatile than Ford and Gm . We can plot kernel density estimation to verify the same

# In[51]:


tesla['returns'].plot(kind='kde',label='Tesla',figsize=(12,6))
gm['returns'].plot(kind='kde',label='GM')
ford['returns'].plot(kind='kde',label='Ford')
plt.legend()


# #  Comparing Daily Returns between Stocks

# We will use a scatter_matrix to visualize correlation between Companies wrt to Returns. This well help us to understand how related the car companies are.

# In[66]:


matrix = pd.concat([tesla['returns'],gm['returns'],ford['returns']],axis=1)
matrix.columns = ['Tesla Returns',' GM Returns','Ford Returns']
from matplotlib.ticker import FormatStrFormatter

axes = scatter_matrix(matrix, alpha=0.2, figsize=(10,10) , hist_kwds={'bins':50})
for ax in axes.flatten():
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) 


# As it can be seen Gm and Ford tend to correlate.

# # Cumulative Daily Returns
# 
# A cumulative return is the aggregate amount an investment has gained or lost over time , independent of the period of time involved

# In[67]:


tesla['Cumulative_Return'] = (1 + tesla['returns']).cumprod()
gm['Cumulative_Return'] = (1 + gm['returns']).cumprod()
ford['Cumulative_Return'] = (1 + ford['returns']).cumprod()


# In[69]:


#visualizing Cumulative_return
tesla['Cumulative_Return'].plot(label='Tesla',figsize=(16,8),title='Cumulative Return')
ford['Cumulative_Return'].plot(label='Ford')
gm['Cumulative_Return'].plot(label='GM')
plt.legend();


# In[ ]:




