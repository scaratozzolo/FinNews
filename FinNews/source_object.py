import feedparser
import time
import sqlite3
import pkg_resources
import pandas as pd
import json
from .feed import Feed

class Source(object):

    def __init__(self, source, save_feeds=True):
        """
        Base class for cources like CNBC, SeekingAlpha...
        save_feeds: Feed objects can save all previous news entries if this is True, otherwise the object will save only the newest entries
        """
        self.__source = source
        self.__possible_topics = []
        self.__possible_sources = []
        self.__save_feeds = save_feeds
        # Get saved feeds
        self.__current_feeds = []
        self.__current_topics = []

        conn = sqlite3.connect(pkg_resources.resource_filename("FinNews", "rss.db"))
        c = conn.cursor()

        for row in c.execute("SELECT topic FROM feeds WHERE source = '{}'".format(self.__source)).fetchall():
            self.__possible_topics.append(row[0])

        for row in c.execute("SELECT DISTINCT source FROM feeds").fetchall():
            self.__possible_sources.append(row[0])

        try:
            self.__ticker_url = c.execute("SELECT url FROM feeds WHERE source = '{}' and topic='ticker'".format(self.__source)).fetchone()[0]
        except:
            self.__ticker_url = ''

        conn.commit()
        conn.close()

        # TODO
        self.__sqlite_columns_to_drop = []

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

    def get_possible_sources(self):
        """Returns a list of possible sources from this source"""
        return self.__possible_sources

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

    def disimilar_keys(self, keys_list=[]):
        """Given a list of Feed objects or a list of lists of entry keys, returns a list of keys that the rss entries dont have in common"""
        if self.__current_feeds != []:
            if keys_list == []:
                if len(self.__current_feeds) > 1:
                    return self.__current_feeds[0].disimilar_keys(self.__current_feeds[1:])
                else:
                    return []
            else:
                return self.__current_feeds[0].disimilar_keys(keys_list)
        else:
            return []

    def add_topics(self, topics=[]):
        """Given a list of topics, creates and adds new feeds to current feeds with given topic, as long as they are valid and a feed isn't already made
            Returns new topics added"""
        conn = sqlite3.connect(pkg_resources.resource_filename("FinNews", "rss.db"))
        c = conn.cursor()
        # TODO check if source allows tickers
        new_topics = []
        for topic in topics:
            # TODO check if len is greater than 1, other items in list are tickers
            if topic == '*':
                new_topics = self.__possible_topics
                try:
                    new_topics.remove('ticker')
                except:
                    pass
                break

            if topic[0] != '$':
                if topic in self.__possible_topics and topic not in self.__current_topics:
                    new_topics.append(topic)
            else:
                if topic not in self.__current_topics:
                    new_topics.append(topic)

        new_topics = list(set(new_topics))
        for topic in new_topics:
            if topic[0] != '$':
                url = c.execute("SELECT url FROM feeds WHERE source = '{}' AND topic = '{}'".format(self.__source, topic)).fetchone()[0]
            else:
                url = self.__ticker_url.format(topic[1:])

            self.__current_feeds.append(Feed(url, feed_source=self.__source, feed_topic=topic, save_feeds=self.__save_feeds))

        self.__current_topics.extend(new_topics)

        conn.commit()
        conn.close()
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

    def time_to_timestamp(self, x):
        """takes in a time.struct and returns a timestamp"""
        try:
            return int(time.mktime(x))
        except:
            return None

    def to_pandas(self, remove_duplicates=True):
        """Returns a pandas dataframe of the most recent news entries"""
        news = self.get_news()
        if news == []:
            return pd.DataFrame()

        df = pd.DataFrame(news)
        if remove_duplicates:
            df.drop_duplicates(subset=["link"], inplace=True)

        if self.__source != 'Reddit':
            df['timestamp'] = df['published_parsed'].apply(self.time_to_timestamp)
        else:
            df['timestamp'] = df['updated_parsed'].apply(self.time_to_timestamp)

        return df

    def to_sqlite3(self, db_path, table_name, if_exists="append", remove_duplicates=True, convert_to_string=True):
        """Converts the most recent entries into an sqlite3 table using pandas.DataFrame.to_sql function"""
        conn = sqlite3.connect(db_path)
        df = self.to_pandas(remove_duplicates)

        # turn possible columns into an outer join funtion to get the list
        # outer join from feeds
        possible_columns = ['links','title_detail','summary_detail', 'source', 'media_content', 'media_text', 'media_credit', 'published_parsed', 'updated_parsed', 'tags', 'authors', 'author_detail', 'post-id', 'content', 'nasdaq_partnerlink', 'media_thumbnail']
        for col in possible_columns:
            try:
                if convert_to_string:
                    df[col] = df[col].apply(str)
                else:
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

    def to_json(self, file_path, remove_duplicates=True, orient='index'):
        """Converts entries to a json file using pandas to_json function"""
        df = self.to_pandas(remove_duplicates)
        df.to_json(file_path, orient=orient)

        return True
