import feedparser
import time
import sqlite3
import pkg_resources
import pandas as pd
import json
from .feed import Feed

class _Source(object):

    def __init__(self, source, save_feeds=True):
        """
        Base class for cources like CNBC, SeekingAlpha.
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will only the newest entries
        """
        self.__source = source
        self.__possible_topics = []
        self.__save_feeds = save_feeds
        self.__current_feeds = []
        self.__current_topics = []

        self.__conn = sqlite3.connect(pkg_resources.resource_filename("FinNews", "rss.db"))
        self.__c = self.__conn.cursor()

        for row in self.__c.execute("SELECT topic FROM feeds WHERE source = '{}'".format(self.__source)).fetchall():
            self.__possible_topics.append(row[0])

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

    def get_possible_topics(self):
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
            # TODO check if source allows for ticker feeds
            if topic[0] != '$':
                if topic in self.__possible_topics and topic not in self.__current_topics:
                    new_topics.append(topic)
            else:
                if topic not in self.__current_topics:
                    new_topics.append(topic)

        new_topics = list(set(new_topics))
        for topic in new_topics:
            if topic[0] != '$':
                url = self.__c.execute("SELECT url FROM feeds WHERE source = '{}' AND topic = '{}'".format(self.__source, topic)).fetchone()[0]
            else:
                url = self.__ticker_url.format(topic[1:])

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

    def add_feed(self, url, source_name, topic_name):
        """Allows you to add a feed from a url not provided or from a different source"""
        self.__current_feeds.append(Feed(url, feed_source=source_name, feed_topic=topic_name, save_feeds=self.__save_feeds))

        self.__current_topics.append(topic_name)

    def to_pandas(self, remove_duplicates=True):
        """Returns a pandas dataframe of the most recent news entries"""
        df = pd.DataFrame(self.get_news())
        if remove_duplicates:
            df.drop_duplicates(subset=["link"], inplace=True)
        return df

    def to_sqlite3(self, db_path, table_name, if_exists="append", remove_duplicates=True):
        """Converts the most recent entries into an sqlite3 table using pandas.DataFrame.to_sql function"""

        conn = sqlite3.connect(db_path)
        df = self.to_pandas(remove_duplicates)
        df = df.drop(['links','title_detail','summary_detail', 'published_parsed'], axis=1)
        df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)

        # if remove_duplicates:
        #     c = conn.cursor()
        #     c.execute("DELETE FROM {} WHERE ROWID not in (SELECT rowid FROM {} GROUP BY link)".format(table_name, table_name))
        #     c.execute("DELETE FROM {} WHERE ROWID not in (SELECT rowid FROM {} GROUP BY title)".format(table_name, table_name))
        #     conn.commit()
        #     conn.close()

        return True

    def to_json(self, file_path):
        """Converts entries to a json file"""
        with open(file_path, 'w') as f:
            json.dump(self.get_news(), f)

        return True
