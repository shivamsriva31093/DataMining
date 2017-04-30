from urllib.request import urlopen
import json
import os


def get_json(url):
    return urlopen(url, timeout=7000).readall().decode('utf8')


def create_path_from_trackid(trackid, folder):
    main_dir = 'H:\Tutorials\Minor Project\part1\DataMining\Essentia_data'
    path = os.path.join(main_dir, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    t_p = trackid
    path = os.path.join(path, t_p)
    return path


def get_data_from_acousticbrainz(mbid):
    try:
        url = 'https://acousticbrainz.org/api/v1/' + mbid + '/low-level'
        data = get_json(url)
        if len(data) == 1:
            return None
        return data
    except Exception as e:
        print(e)
        return None


def get_low_level_data():
    with open('./cleaned_track_list.json', 'r', encoding='utf8') as fp:
        song_dic = json.load(fp)

    # for k, v in song_dic.items():
        for track in song_dic['angry']:
            trackid = track['tid']
            mbid = track['mbid']
            try:
                path1 = create_path_from_trackid(trackid, 'sad')

                low_level_data = get_data_from_acousticbrainz(mbid)
                if not low_level_data:
                    print('json empty!')
                    continue
                low_level_data = json.loads(low_level_data)
                if not os.path.exists(path1):
                    os.makedirs(path1)
                t_p = path1 + os.sep + trackid + '.json'
                with open(t_p, 'w', encoding='utf8') as fp:
                    json.dump(low_level_data, fp, ensure_ascii=False)
                print(trackid+' done!')
            except Exception as e:
                print(e)
                if os.path.exists(path1):
                    os.removedirs(path1)

if __name__ == '__main__':
    get_low_level_data()