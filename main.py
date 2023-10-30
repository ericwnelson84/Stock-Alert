import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = '94XSIHY2PNYREFFL'
NEWS_API_KEY = '89b12999aedc405ba4eefc83e60633d8'
TWILLIO_SID = 'ACc099acdaa96a4b62c6c6f31d0f090f75'
TWILLIO_TKN = '73b1da2470bde90f9f8daece9f8d0211'

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data['4. close']

#TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_close = data_list[1]['4. close']

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = abs(float(yesterday_close) - float(day_before_yesterday_close))

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_difference = (difference/float(yesterday_close)) * 100

print(percentage_difference)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if percentage_difference > 2:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    three_articles = articles[:3]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.


    formatted_articles = [f'Headline: {article["title"]}. \nBrief: {article["description"]}' for article in three_articles]

#TODO 9. - Send each article as a separate message via Twilio. 

    client = Client(TWILLIO_SID, TWILLIO_TKN)

#Optional TODO: Format the message like this:

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18559214065",
            to="+15125160603"
        )
        print(message.sid)
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

