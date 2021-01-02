"""

This project looks at the various MDA and the appropriate reactions to those MDAs.

The 200 MDA will provide a buy/sell signal on a particular stock.

"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup


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



def get_MDA(entries, days):
    pass




if __name__ == '__main__':

    finviz_url = "https://www.finviz.com/screener.ashx?v=111&r="
    ticker_collection = get_tickers(finviz_url)

    print(ticker_collection)
    for i in ticker_collection:
        yahoo_url = f"https://finance.yahoo.com/quote/{i}/history?"
        close_entries = scrape_data(yahoo_url)
        get_MDA(50)
"""
get yahoo ticker
then collect the data (depending on how many days there are)
then create a MDA for that
"""


"""
    Stock price above the 50-day moving average is considered bullish.
    Stock price below 50-day moving average is considered bearish.
    If the price meets the 50 day SMA as support and bounces upwards, you should think long.
    Stock price meets the 50-day SMA as resistance and bounces downwards, you should think short.
    If the price breaks the 50-day SMA downwards, you should switch your opinion to bearish.
    If the price breaks the 50-day SMA upward, you should switch your opinion to bullish.

"""