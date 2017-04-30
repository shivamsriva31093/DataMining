import json
import os
import pandas as pd
import numpy as np
import pickle

class_mood = []
keys = set()


def get_keys():
    with open('H:\Tutorials\Minor Project\part1\DataMining\Essentia_data\\not sad\TRAEIKW128F1456B1A\TRAEIKW128F1456B1A.json', 'r', encoding='utf8') as fp:
        dic = json.load(fp)
    global keys
    keys = set(dic['lowlevel'].keys())
    print(keys)


def get_relevant_data(zcr_mean, file, key):
    with open(file, 'r', encoding='utf8') as fp:
        dic = json.load(fp)
    try:

        zcr_mean.fill(dic['lowlevel'][key]['mean'])
    except Exception as e:
        # print(e)
        return


def open_files_in_folder(folder, key):
    path = 'H:'+os.sep+'Tutorials'+os.sep+'Minor Project'+os.sep+'part1'+os.sep+'DataMining'+os.sep+'Essentia_data'+os.sep+folder
    zcr_mean = np.zeros(shape=len(os.listdir(path)))
    for track_folder in os.listdir(path):
        path1 = os.path.join(path, track_folder)
        for file in os.listdir(path1):
            get_relevant_data(zcr_mean, os.path.join(path1, file), key)
    return [zcr_mean.mean(), zcr_mean.std()]


get_keys()
print(keys.__len__())
keys = keys.difference(
    {'melbands', 'gfcc', 'spectral_contrast_valleys', 'spectral_contrast_coeffs', 'mfcc', 'erbbands', 'barkbands',
     'erbbands_flatness_db'})
print(keys.__len__())
valid_extractors = []
for k in keys:
    class_mood.append(open_files_in_folder('not sad', key=k))
    class_mood.append(open_files_in_folder('sad', key=k))

    df = pd.DataFrame(class_mood, index=['not sad', 'sad'], columns=[k+'_mean', k+'_std'])
    df.fillna(0)
    if abs(df.iloc[0, 0]-df.iloc[1, 0]) > (df.iloc[0, 1]+df.iloc[1, 1]):
        valid_extractors.append(k)
    class_mood = []

print(valid_extractors)

with open('./useful_descriptors.txt', 'w', encoding='utf8') as fp:
    for v in valid_extractors:
        fp.write('%s\n' % v)

