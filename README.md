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

cnbc_feed = fn.CNBC(topics=['*']) # '*' = all possible topics
print(cnbc_feed.get_news())
print(cnbc_feed.possible_topics())
```

Current RSS feeds and their classes:
- CNBC
```python
fn.CNBC(topics=['finance', 'earnings'], save_feeds=True)
```
- Seeking Alpha
```python
# SeekingAlpha has support for RSS feeds by ticker, tickers can be passed as a topic and are denoted by $XXX
fn.SeekingAlpha(topics=['financial', '$AAPL'], save_feeds=True)
```
- Investing.com
```python
fn.Investing(topics=['all news', 'latest news'], save_feeds=True)
```
- WSJ
```python
fn.WSJ(topics=['markets news', 'us business'], save_feeds=True)
```
- Yahoo Finance
```python
# Yahoo Finance has support for RSS feeds by ticker, tickers can be passed as a topic and are denoted by $XXX
fn.Yahoo(topics=['top stories', '$DIS'], save_feeds=True)
```

Todo:
- [x] CNBC
- [x] Seeking Alpha
- [x] Investing.com
- [x] WSJ
- [x] Yahoo Finance
- [ ] Financial Times
- [ ] Fortune
