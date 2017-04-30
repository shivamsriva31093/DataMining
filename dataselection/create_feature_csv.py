import json
import os

import collections
import pandas as pd

data_dir = 'H:'+os.sep+'Tutorials'+os.sep+'Minor Project'+os.sep+'part1'+os.sep+'DataMining'+os.sep+'Essentia_data'
print(data_dir)
category = ['angry', 'happy', 'sad', 'calm']
prime_cat = ['not ' + k for k in category]
with open('./useful_descriptors.txt', 'r', encoding='utf8') as fp:
    feature_list = fp.read().split('\n')
feature_list.insert(0, 'track_id')
feature_list = sorted(feature_list)
feature_list.append('label')


for folder in category:
    df = pd.DataFrame(columns=feature_list)
    home_dir = os.path.join(data_dir, folder)
    frame_size = 0
    for data_type in os.listdir(home_dir):
        limit = 0
        for track in os.listdir(os.path.join(home_dir, data_type)):
            print(folder+" "+data_type+" "+track+" ", limit)
            if limit <= 60:
                limit += 1
                continue
            if limit >= 101 or frame_size >= 121:
                break

            try:
                with open(os.path.join(os.path.join(home_dir, data_type), track) + os.sep + track + '.json', 'r',
                          encoding='utf8') as fp:
                    track_data = json.load(fp)
            except Exception as e:
                print(e)
            else:
                row = []
                for feature in feature_list:
                    if feature is 'track_id':
                        val = track
                    elif feature is 'label':
                        val = folder
                        if data_type == 'negative':
                            val = 'not'+folder
                    else:
                        val = track_data['lowlevel'][feature]['mean']
                    row.append(val)
                df.loc[frame_size] = row
                limit += 1
                frame_size += 1
    df.to_csv(os.path.join(data_dir, folder + '_test.csv'))



