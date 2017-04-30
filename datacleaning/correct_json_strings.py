import json
import os

main_dir = 'H:'+os.sep+'Tutorials'+os.sep+'Minor Project'+os.sep+'part1'+os.sep+'DataMining'+os.sep+'Essentia_data'


def convert_to_json(path, file):
    dicti = {}
    with open(os.path.join(path, file), 'r', encoding='utf-8') as fp:
        data = fp.read()
        dicti = json.loads(data)
        dicti = json.loads(dicti, encoding='utf-8')
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as fp:
        json.dump(dicti, fp, ensure_ascii=False)


for folder in os.listdir(main_dir):
    p1 = os.path.join(main_dir, folder)
    for f1 in os.listdir(p1):
        p2 = os.path.join(p1, f1)
        for filename in os.listdir(p2):
            for track in os.listdir(os.path.join(p2, filename)):
                try:
                    convert_to_json(os.path.join(p2, filename), track)
                except Exception as e:
                    print(e)