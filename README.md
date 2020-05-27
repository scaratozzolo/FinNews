# FinNews

This is a package to help me with a personal project dealing with sentiment analysis and headline classification. The package has a lot of influence from the [newscatcher package](https://github.com/kotartemiy/newscatcher). While that package is great for getting general news, I need more financial related news that I wasn't getting.


You can install using pip by downloading directly from Pypi:
```
$ pip install FinNews
```
or from this repo:
```
$ pip install git+https://github.com/scaratozzolo/FinNews
```

Example usage:
```python
import FinNews as fn

cnbc_feed = fn.CNBC(topics=['finance', 'earnings'])
print(cnbc_feed.get_news())
print(cnbc_feed.possible_topics())

# Some feeds have support for feeds by ticker, tickers can be passed as a topic and are denoted by $XXX. These feeds will have 'ticker' as a possible topic.
fn.SeekingAlpha(topics=['financial', '$AAPL'], save_feeds=True)

# You can also pass in '*' to select all possible topic feeds.
fn.WSJ(topics=['*'], save_feeds=True)

# Selecting all topics will not add specific ticker feeds. You will have to add tickers manually.
fn.Yahoo(topics=['*']).add_topics(['$DIS', '$GOOG'])
```

Current RSS feeds:
- CNBC
- Seeking Alpha*
- Investing.com
- WSJ
- Yahoo Finance*
- Financial Times
- Fortune
- MarketWatch
- Zacks
- Nasdaq*

(* denotes ticker feed support)
