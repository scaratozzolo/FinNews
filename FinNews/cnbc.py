import feedparser
import time
import sqlite3
import pkg_resources
from .feed import Feed

class CNBC(object):
    """Object for maintaining CNBC rss feeds"""

    def __init__(self, topics=[], save_feeds=True):
        self.__source = 'CNBC'

        self.__conn = sqlite3.connect(pkg_resources.resource_filename("FinNews", "rss.db"))
        self.__c = self.__conn.cursor()

        self.__possible_topics = []
        for row in self.__c.execute("SELECT topic FROM feeds WHERE source = '{}'".format(self.__source)).fetchall():
            self.__possible_topics.append(row[0])

        self.__current_topics = [x for x in list(set(topics)) if x in self.__possible_topics]
        self.__save_feeds = save_feeds


        self.__current_feeds = []
        for topic in self.__current_topics:
            url = self.__c.execute("SELECT url FROM feeds WHERE source = '{}' AND topic = '{}'".format(self.__source, topic)).fetchone()[0]
            self.__current_feeds.append(Feed(url, feed_source=self.__source, feed_topic=topic, save_feeds=self.__save_feeds))

    def get_news(self):
        """Returns a list of all entries from feed"""
        entries = []
        for feed in self.__current_feeds:
            entries.extend(feed.get_news())

        return entries

    def get_current_feeds(self):
        """Returns a list of all current Feed objects"""
        return self.__current_feeds

    def get_current_topics(self):
        """Returns a list of all current Feed objects"""
        return self.__current_topics

    def possible_topics(self):
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

    def add_topics(self, topics=[]):
        """Given a list of topics, creates and adds new feeds to current feeds with given topic, as long as they are valid and a feed isn't already made
            Returns new topics added"""
        new_topics = []
        for topic in topics:
            if topic in self.__possible_topics and topic not in self.__current_topics:
                new_topics.append(topic)
        new_topics = list(set(new_topics))
        for topic in new_topics:
            url = self.__c.execute("SELECT url FROM feeds WHERE source = '{}' AND topic = '{}'".format(self.__source, topic)).fetchone()[0]
            self.__current_feeds.append(Feed(url, feed_source=self.__source, feed_topic=topic, save_feeds=self.__save_feeds))

        self.__current_topics.extend(new_topics)
        return new_topics

    def remove_topics(self, topics=[]):
        """Given a list of topics, removes them from current topics and deletes their feed from current feeds"""
        for topic in topics:
            if topic in self.__current_topics:
                self.__current_topics.remove(topic)

                for i in range(len(self.__current_feeds)):
                    if self.__current_feeds[i].get_feed_topic() == topic:
                        del self.__current_feeds[i]
                        break

        return self.__current_topics
