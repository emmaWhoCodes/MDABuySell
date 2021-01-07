"""

This project looks at the various MDA and the appropriate reactions to those MDAs.

The 50 MDA will provide a buy/sell signal on a particular stock.

"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy

def get_tickers(url):
    ticker_collection = []

    #385
    for i in range(1, 2):
        if i != 1:
            url = f'https://www.finviz.com/screener.ashx?v=111&r={str(20 * i + 1)}'

        session = HTMLSession().get(url)
        page = BeautifulSoup(session.text, features='lxml')
        tickers = page.find_all('a', class_='screener-link-primary')

        for i in tickers:
            ticker_collection.append(i.text)

    return ticker_collection


def scrape_data(url):
    session = HTMLSession().get(url)
    page = BeautifulSoup(session.text, features='lxml')
    data = page.find_all("tr", class_="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")

    all_close = []
    for i in data:

        entries = i.find_all("td")
        try:
            all_close.append(entries[3].text)
        except:
            pass

    return all_close


def get_MDA(price_entries, days):
    stock_entries = []
    if len(price_entries) >= days:
        for i in range(days, len(price_entries)):
            prices = []

            for j in range(i - days, i):

                #sometimes entries on yahoo are a - just as a known issue
                if "-" not in price_entries[j] or price_entries[j] != "-":
                    prices.append(float(price_entries[j]))

            average = numpy.average(prices)
            stock_entries.append(average)

    return stock_entries


if __name__ == '__main__':

    finviz_url = "https://www.finviz.com/screener.ashx?v=111&r="
    ticker_collection = get_tickers(finviz_url)

    print(ticker_collection)

    for i in ticker_collection:
        yahoo_url = f"https://finance.yahoo.com/quote/{i}/history?"
        close_entries = scrape_data(yahoo_url)
        close_entries = close_entries[::-1]

        _50mda = get_MDA(close_entries, 50)

        if len(close_entries) != 0:
            latest_close = float(close_entries[len(close_entries) - 1])

            if len(_50mda) != 0:
                latest_50mda = float(_50mda[len(_50mda) - 1])

        #    Stock price above the 50-day moving average is considered bullish.
                if latest_close < latest_50mda:
                    print(f"latest close is lower than 50 mda {i}")

        #    If the price breaks the 50-day SMA downwards, you should switch your opinion to bearish.
                if latest_close > latest_50mda:
                    print(f"latest close is greater than 50 mda  {i}")

"""
    Stock price below 50-day moving average is considered bearish.
    If the price meets the 50 day SMA as support and bounces upwards, you should think long.
    Stock price meets the 50-day SMA as resistance and bounces downwards, you should think short.
    If the price breaks the 50-day SMA upward, you should switch your opinion to bullish.

"""

