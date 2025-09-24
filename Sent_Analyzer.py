import finnhub
import time
import datetime
import yfinance as yf
import requests
from datetime import datetime, timedelta
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import streamlit as st

################################################
####          Sentiment Analyzer            ####
################################################

def date_now():
  return datetime.now().strftime('%Y-%m-%d')

def one_year_ago():
  return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')


def write_headlines(tkr, from_date, to_date, finnhub_api_key):
    try:
      finnhub_client = finnhub.Client(api_key=finnhub_api_key)
      df = pd.DataFrame()
      news = finnhub_client.company_news(tkr, _from=from_date, to=to_date)
      for article in news:
        date = datetime.fromtimestamp(article['datetime'])  
        formatted_date = date.strftime("%Y-%m-%d")
        new_row = pd.DataFrame({
        'date': [formatted_date],
        'headline': [article['headline']]
        })
        df = pd.concat([df, new_row], ignore_index=True)
      return df
    except Exception as e:
      print('write_headlines error:', e)
      raise

def write_performance_dict(tkr):
  try:
    perf_dict = {}
    stock = yf.Ticker(tkr)
    hist = stock.history(period="1y")
    yf_df = pd.DataFrame(hist)
    for ts, row in yf_df.iterrows():
      info = row.to_dict()
      perc_change = (info['Close'] - info['Open']) / info['Open']
      perf_dict[ts.strftime('%Y-%m-%d')] = perc_change
    return perf_dict
  except:
    return "err"

def make_data(perf_dict, headlines_df):
  try:
    df = pd.DataFrame()
    # main_dict = {}
    for i, row in headlines_df.iterrows():
      date = row['date'].strip()
      headline = row['headline']
      pc = perf_dict.get(date, 'Undefined key')
      if(type(pc) == float):
        new_row = pd.DataFrame({
        'headline': [headline],
        'percent_change': [pc]
        })
        # main_dict[headline] = pc
        df = pd.concat([df, new_row], ignore_index=True)
    return df
  except:
    return pd.DataFrame()

def make_model(df):
  vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
  X = vectorizer.fit_transform(df['headline'])

  y = df['percent_change'].values

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)
  mse = mean_squared_error(y_test, y_pred)

  return [model, vectorizer, mse]

def predict_headline(model, vectorizer, headline):
  headline_vector = vectorizer.transform([headline])
  pc = model.predict(headline_vector)
  return pc[0]

def get_most_recent_headline(tkr, finnhub_key):
  finnhub_client = finnhub.Client(api_key=finnhub_key)
  news = finnhub_client.company_news(tkr, _from=date_now(), to=date_now())
  return news[0]['headline'] if news else None

