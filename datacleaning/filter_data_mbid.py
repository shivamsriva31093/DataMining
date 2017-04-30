import json
import os
from collections import defaultdict
import musicbrainzngs
import sqlite3

file_path = '../dataintegration/track_list_prime.json'

musicbrainzngs.set_useragent(app='DataMining', version='0.1', contact='shivam.srivastava31093@gmail.com')


def sanitize(tag):
    tag = tag.replace("'", "''")
    return tag


def get_track_metadata(track, one=False):
    database_path = os.path.join('H:' + os.sep + "Tutorials" + os.sep + "Minor Project"
                                 + os.sep + "part1" + os.sep + "databases", 'track_metadata.db')
    query = "Select title, artist_name from songs WHERE track_id='%s'" % sanitize(track)
    try:
        with sqlite3.connect(database_path) as conn:
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data[0][0], data[0][1]

    except Exception as e:
        print(e)
        return None


def search_for_mbid(response1, title1, artist1):
    record_list = response1['recording-list']
    for dicts in record_list:
        t_title = dicts['title']
        t_artist = dicts['artist-credit'][0]['artist']['name']
        t_mbid = dicts['id']
        if artist1 == t_artist and t_title == title1:
            return t_mbid
    return None


def init():

    with open(file_path, 'r', encoding='utf8') as fp:
        tracks_dic = json.load(fp)
    cleaned_track_dic = defaultdict(list)
    for category, track_list in tracks_dic.items():
        print('Working in category %s', category)
        for track in track_list:
            track_details = {}
            title, artist = get_track_metadata(track)
            print('Searching for the %s mbid', track)
            try:
                response = musicbrainzngs.search_recordings(title)
            except Exception as e:
                print(e)
                continue
            else:
                mbid = search_for_mbid(response, title, artist)
                if mbid:
                    print('success.')
                    track_details['tid'] = track
                    track_details['title'] = title
                    track_details['artist'] = title
                    track_details['mbid'] = mbid
                    cleaned_track_dic[category].append(track_details)
                else:
                    print('not found.')
    return cleaned_track_dic


if __name__ == '__main__':
    cleaned_track_dic = init()
    with open('./cleaned_track_list_prime.json', 'w', encoding='utf8') as fp1:
        json.dump(cleaned_track_dic, fp1)
