# Sentiment Analysis Based Algorithmic Trading Bot

## About
This project implements an algorithmic trading bot that places trades based on perceived market sentiment from news headlines on a specified asset. First, given a specified asset, a custom dataset is created by pulling the historic performance of the chosen asset and news headlines about the asset within the past year and merging them to associate each news headline with a percent change. A random forest regression model is then trained on the customized dataset and used to evaluate current news headlines to predict a positive or negative market sentiment of the underlying asset. If positive market sentiment is detected, the bot buys the underlying asset and holds it until negative market sentiment is detected. The bot uses the Alpaca API to automate placing trades on a paper account.
## Instructions to Run
In terminal, run the following commands:

**1).** pip install -r requirements.txt

**2).** streamlit run ./App.py

Note that this program requires API keys from [finnhub](https://finnhub.io/) and [Alpaca](https://alpaca.markets/). These keys are free and are reccomended to be stored locally in .env file. 

