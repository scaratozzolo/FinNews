import feedparser
import time
import sqlite3
import pkg_resources
import pandas as pd
import json
from .feed import Feed
from .source_object import _Source

class CNBC(_Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('CNBC', save_feeds)
        self.add_topics([x for x in list(set(topics)) if x in self.get_possible_topics()])
