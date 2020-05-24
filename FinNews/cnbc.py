import feedparser
import time
import sqlite3
import os
from .feed import Feed
from pathlib import Path

class CNBC(object):
    """Object for maintaining CNBC rss feeds"""

    def __init__(self, topics=[], save_feeds=False):

        self.__conn = sqlite3.connect(os.path.join(Path(__file__).parent, 'rss.db'))
        self.__c = self.__conn.cursor()

        self.__possible_topics = []
        for row in self.__c.execute("SELECT topic FROM feeds WHERE source = 'CNBC'").fetchall():
            self.__possible_topics.append(row[0])

        self.__current_topics = [x for x in list(set(topics)) if x in self.__possible_topics]
        self.__save_feeds = save_feeds


        self.__current_feeds = []
        for topic in self.__current_topics:
            url = self.__c.execute("SELECT url FROM feeds WHERE source = 'CNBC' AND topic = '{}'".format(topic)).fetchone()[0]
            self.__current_feeds.append(Feed(url, feed_source="CNBC", feed_topic=topic, save_feeds=self.__save_feeds))

    def get_news(self):
        """Returns a list of all entries from feed"""
        entries = []
        for feed in self.__current_feeds:
            entries.extend(feed.get_news())

        return entries
    def get_current_feeds(self):
        """Returns a list of all current Feed objects"""
        return self.__current_feeds

    def possible_topcs(self):
        """Returns a list of possible topics from this source"""
        return self.__possible_topics

    def entry_keys(self):
        """Returns a list of lists containing the possible keys in each feed, only run after get_news is called"""
        keys = []
        for feed in self.__current_feeds:
            keys.append(feed.entry_keys())

        return keys

    def all_entry_keys(self):
        """Returns a list of all keys used across the current feeds"""
        keys_list = self.entry_keys()
        keys = keys_list[0]
        for i in keys_list[1:]:
            keys = list(set(i) & set(keys))

        return keys

    def similar_keys(self, keys_list=[]):
        """Given a list of Feed objects or a list of lists of entry keys, returns a list of keys that the rss entries have in common"""
        if self.__current_feeds != []:
            if keys_list == []:
                if len(self.__current_feeds) > 1:
                    return self.__current_feeds[0].similar_keys(self.__current_feeds[1:])
                else:
                    return self.all_entry_keys()
            else:
                return self.__current_feeds[0].similar_keys(keys_list)
        else:
            return []
