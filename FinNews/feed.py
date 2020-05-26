import feedparser
import time
import pandas as pd
import sqlite3
import json

class Feed(object):

    def __init__(self, url: str, feed_source: str, feed_topic: str, save_feeds=True):
        """
        Object for maintaining various attributes of a single RSS feed
        url: the url to the rss feed
        feed_source: where the rss feed is coming from (CNBC, Seeking Alpha...)
        feed_topic: what the topic of this feed is
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        self.__url = url
        self.__feed_source = feed_source
        self.__feed_topic = feed_topic

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
        else:
            self.__all_entries = self.__newest_entries
            self.__all_feeds = self.__feed

        return self.__newest_entries

    def get_url(self):
        """Returns feed url"""
        return self.__url

    def get_feed_source(self):
        """Returns feed source"""
        return self.__feed_source

    def get_feed_topic(self):
        """Returns feed topic"""
        return self.__feed_topic

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
        # TODO isinstance of cnbc, seekingalpha...
        if isinstance(keys_list[0], Feed):
            keys = keys_list[0].entry_keys()
            for i in keys_list[1:]:
                keys = list(set(i.entry_keys()) & set(keys))
        else:
            keys = keys_list[0]
            for i in keys_list[1:]:
                keys = list(set(i) & set(keys))

        return keys

    def time_to_timestamp(self, x):
        """takes in a time.struct and returns a timestamp"""
        try:
            return int(time.mktime(x))
        except:
            return None

    def to_pandas(self, all_entries=True, remove_duplicates=True):
        """Returns a pandas dataframe of the most recent news entries or all saved entries"""
        # TODO update before converting?
        if self.__all_entries == []:
            return pd.DataFrame()

        if all_entries:
            df = pd.DataFrame(self.__all_entries)
        else:
            df = pd.DataFrame(self.__newest_entries)

        if remove_duplicates:
            df.drop_duplicates(subset=['link'], inplace=True)

        df['timestamp'] = df['published_parsed'].apply(self.time_to_timestamp)
        df['topic'] = self.__feed_topic

        return df

    def to_sqlite3(self, db_path, table_name, all_entries=True, if_exists="append", remove_duplicates=True):
        """Converts entries into an sqlite3 table using pandas.DataFrame.to_sql function"""

        conn = sqlite3.connect(db_path)

        df = self.to_pandas(all_entries, remove_duplicates)

        possible_columns = ['links','title_detail','summary_detail', 'source', 'media_content', 'media_text', 'media_credit', 'published_parsed', 'tags', 'authors', 'author_detail', 'post-id', 'content', 'credit']
        for col in possible_columns:
            try:
                df = df.drop([col], axis=1)
            except:
                pass

        df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)

        if remove_duplicates:
            c = conn.cursor()
            c.execute("DELETE FROM {} WHERE ROWID not in (SELECT rowid FROM {} GROUP BY link)".format(table_name, table_name))
            c.execute("DELETE FROM {} WHERE ROWID not in (SELECT rowid FROM {} GROUP BY title)".format(table_name, table_name))

        conn.commit()
        conn.close()


        return True

    def to_json(self, file_path, all_entries=True, remove_duplicates=True, orient='index'):
        """Converts entries to a json file using pandas to_json function"""
        # TODO update before converting?
        df = self.to_pandas(all_entries, remove_duplicates)
        df.to_json(file_path, orient=orient)

        return True
