import feedparser
import time
import sqlite3
import pkg_resources
import pandas as pd
import json
from .feed import Feed
from .source_object import _Source

class SeekingAlpha(_Source):

    def __init__(self, topics=[], save_feeds=True):
        """
        Object for maintaining CNBC rss feeds.
        topics: a list of rss feed topics, must be one of the possible topics
            You can leave the list blank and call CNBC.get_possible_topics() and then add topics using CNBC.add_topics()
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        super().__init__('Seeking Alpha', save_feeds)
        self.add_topics([x for x in list(set(topics)) if x in self.get_possible_topics()])
