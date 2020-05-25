# FinNews

This is a package to help me with a personal project dealing with sentiment analysis and headline classification. The package has a lot of influence from the [newscatcher package](https://github.com/kotartemiy/newscatcher). While that package is great for getting general news, I need more financial related news that I wasn't getting.

This package is meant to get news articles from various rss feed sources. The first one implemented is CNBC. By calling the CNBC class, you'll have access to all of their rss feeds. All you need to do is specify the topics.

You can install this package using the repo link and pip:
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
- [ ] Seeking Alpha
- [ ] investing.com
- [ ] WSJ
- [ ] Yahoo Finance
- [ ] Financial Times
- [ ] Fortune
