# FinNews

This is a package to help me with a personal project dealing with sentiment analysis and headline classification. The package has a lot of influence from the [newscatcher package](https://github.com/kotartemiy/newscatcher). While that package is great for getting general news, I need more financial related news that I wasn't getting.

This package is meant to get news from various RSS sources. Current RSS sources:
- CNBC
```python
fn.CNBC(topics=['finance', 'earnings'], save_feeds=True)
```
- Seeking Alpha
```python
# SeekingAlpha has support for RSS feeds by ticker, tickers can be passed as a topic and are denoted by $XXX
fn.SeekingAlpha(topics=['financial', '$AAPL'], save_feeds=True)
```

You can install using pip from Pypi:
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

cnbc_feed = fn.CNBC(topics=['finance', 'earnings', 'business'])
print(cnbc_feed.get_news())
print(cnbc_feed.possible_topics())
```

Todo:
- [x] CNBC
- [x] Seeking Alpha
- [ ] investing.com
- [ ] WSJ
- [ ] Yahoo Finance
- [ ] Financial Times
- [ ] Fortune
