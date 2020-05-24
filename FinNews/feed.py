import feedparser
import time

class Feed(object):
    """Object for maintaining various attributes of a single RSS feed"""
    def __init__(self, url: str, feed_source: str, feed_name: str, save_feeds=False):
        """save_feeds: save all entries and all feeds every time feed is parsed"""
        self.__url = url
        self.__feed_source = feed_source
        self.__feed_name = feed_name

        self.__save_feeds = save_feeds
        self.__feed = None
        self.__newest_entries = []
        self.__updated = None

        # if save_feeds
        self.__all_entries = []
        self.__all_feeds = []


    def get_news(self):
        """Returns a list of dictionaries, each of which refers to an entry from the RSS feed"""
        self.__feed = feedparser.parse(self.__url)
        self.__newest_entries = self.__feed['entries']
        try:
            self.__updated = self.__feed['feed']['updated_parsed']
        except:
            self.__updated = None

        if self.__save_feeds:
            self.__all_entries.extend(self.__feed['entries'])
            self.__all_feeds.append(self.__feed)

        return self.__newest_entries

    def get_url(self):
        """Returns feed url"""
        return self.__url

    def get_feed_source(self):
        """Returns feed source"""
        return self.__feed_source

    def get_feed_name(self):
        """Returns feed name"""
        return self.__feed_name

    def get_feed(self):
        """Returns the most recent feed since calling get_news"""
        return self.__feed

    def get_newest_entries(self):
        """Returns the most recent entries since calling get_news"""
        return self.__newest_entries

    def get_updated(self):
        """Returns a time struct with the time the feed was updated"""
        return self.__updated

    def time_to_timestamp(self, x):
        """Given a time struct, returns a timestamp"""
        try:
            return int(mktime(x))
        except:
            return None

    def get_all_entries(self):
        """Returns the list of all entries"""
        return self.__all_entries

    def get_all_feeds(self):
        """Returns a list of all parsed feeds"""
        return self.__all_feeds

    def set_save_feeds(self, save_feeds: bool):
        self.__save_feeds = save_feeds

    def entry_keys(self):
        """Returns a list of keys that can be used on each entry dict"""
        if self.__newest_entries != []:
            return list(self.__newest_entries[0].keys())
        else:
            return []

    def similar_keys(self, keys_list):
        """Given a list of Feed objects or a list of lists of entry keys, returns a list of keys that the rss entries have in common"""
        keys = []
        if keys_list == []:
            return keys

        if isinstance(keys_list[0], Feed):
            keys = keys_list[0].entry_keys()
            for i in keys_list[1:]:
                keys = list(set(i.entry_keys()) & set(keys))
        else:
            keys = keys_list[0]
            for i in keys_list[1:]:
                keys = list(set(i) & set(keys))

        return keys