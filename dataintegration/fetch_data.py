import json
from collections import defaultdict

import pylast
import os
import sys
import sqlite3

API_KEY = "ba92613bbd5220636c51359dd355e3a0"
API_SECRET = "6908d88be6a2a3171b0bba738cb7765"

username = "shivam31093"
pw_hash = pylast.md5("shivam118!")


class db_config(object):
    lastfm_tags_db = ''
    lastfm_tags_similars = ''

    def __init__(self):
        self.lastfm_tags_db = os.path.join(
            'H:' + os.sep + "Tutorials" + os.sep + "Minor Project" + os.sep + "part1" + os.sep + "databases",
            'lastfm_tags.db')
        self.lastfm_tags_similars = os.path.join(
            'H:' + os.sep + "Tutorials" + os.sep + "Minor Project" + os.sep + "part1" + os.sep + "databases",
            'lastfm_similars.db')

    def get_database(self, key):
        db = ''
        if key == 'tags':
            db = self.lastfm_tags_db
        else:
            db = self.lastfm_tags_similars

        return db


def sanitize(tag):
    tag = tag.replace("'", "''")
    return tag


def get_database(db):
    return sqlite3.connect(db)


def create_list_of_tracks(moodterms):
    track_dict = defaultdict(set)
    for category, tag_list in moodterms.items():
        no_of_tracks = 0
        for tag in tag_list:
            print('Get the list of tracks for tag:%s whose count is >=100' % tag)
            query = "SELECT tids.tid FROM tid_tag, tids, tags WHERE tids.ROWID=tid_tag.tid AND tid_tag.tag=tags.ROWID " \
                    "AND tid_tag.val >= 100.0 AND tags.tag='%s' ORDER BY tid_tag.val DESC" % sanitize(tag)
            try:
                res = conn.execute(query)
                data = res.fetchall()
                for track in data:
                    for ids in track:
                        track_dict[category].add(ids)
                no_of_tracks += len(data)
                print(len(data), "tracks added.")
            except Exception as e:
                print("error? ", e)
        print(no_of_tracks, ' tracks added to the category %s' % category)

    track_dict = dict((k, list(v)) for k, v in track_dict.items())
    with open('./track_list_prime.json', mode='w') as fp:
        json.dump(track_dict, fp)


if __name__ == '__main__':
    ob = db_config()
    dbfile = ob.get_database('tags')
    conn = get_database(db=dbfile)
    with open("taxonomy_prime.json") as fp:
        dic = json.load(fp)
    create_list_of_tracks(dic)
