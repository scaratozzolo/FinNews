from .source_object import Source

class CNBC(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('CNBC', save_feeds)
        self.add_topics(list(set(topics)))


class SeekingAlpha(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining Seeking Alpha rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('Seeking Alpha', save_feeds)
        self.add_topics(list(set(topics)))


class Investing(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining Investing.com rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('Investing.com', save_feeds)
        self.add_topics(list(set(topics)))


class WSJ(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining WSJ rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('WSJ', save_feeds)
        self.add_topics(list(set(topics)))


class Yahoo(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining Yahoo Finance rss feeds. Honestly their rss feeds are pretty weird and looks like every feed is the same.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('Yahoo Finance', save_feeds)
        self.add_topics(list(set(topics)))


class FT(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('FT', save_feeds)
        self.add_topics(list(set(topics)))


class Fortune(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('Fortune', save_feeds)
        self.add_topics(list(set(topics)))


class MarketWatch(Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('MarketWatch', save_feeds)
        self.add_topics(list(set(topics)))
