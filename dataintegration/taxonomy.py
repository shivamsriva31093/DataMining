from collections import defaultdict
import json

__author__ = 'sHIVAM'
import nltk
from nltk.corpus import wordnet as wn


class Vocabulary(object):
    moods = dict()
    vocab = dict()

    def __init__(self):
        # self.moods = {
        #     'happy': ['happy', 'joy', 'cheerful', 'fun', 'enjoyable', 'chirpy', 'cheery', 'joyous', 'merry',
        #               'light-hearted', 'celebration', 'fortunate', 'playful'],
        #     'sad': ['sad', 'cheerless', 'melancholy', 'dark', 'sorry', 'bad', 'tearful', 'tragic',
        #             'gloomy', 'boring', 'depressing', 'bittersweet', 'sentimental'],
        #     'angry': ['angry', 'rage', 'stormy', 'mad', 'heavy', 'intense',
        #               'irritating', 'displeasing', 'aggressive'],
        #     'calm': ['calm', 'relaxed', 'spiritual', 'tranquil', 'serene', 'quiet', 'peaceful', 'balmy', 'soothing',
        #              'dreamy', 'composed', 'cool', 'smooth', 'still', 'gentle', 'sleepy']
        # }
        with open('./taxonomy_prime.json', 'r') as fp:
            self.moods = json.load(fp)
        nltk.data.path.append('../nltk_data/')

    def create_vocabulary(self):
        moods = self.moods
        vocab1 = defaultdict(set)
        # vocab_set = list(chain.from_iterable([ss.lemma_names() for mood in moods for ss in wn.synsets(mood)]))
        # print(vocab_set)
        for mood, syn in moods.items():
            for e in syn:
                for ss in wn.synsets(e):
                    for synonym in ss.lemma_names():
                        vocab1[mood].add(synonym)

        self.vocab = dict((k, tuple(v)) for k, v in vocab1.items())

    def print_vocabulary(self):
        for k1, v1 in self.vocab.items():
            print(k1, v1)

    def get_mood_taxonomy(self):
        return self.vocab

    def get_mood_taxonomy_as_csv(self):
        return None

    def store_vocabulary(self):
        self.vocab = dict((k2, tuple(v2)) for k2, v2 in self.vocab.items())
        with open('./taxonomy_prime_list.json', 'w') as outline:
            json.dump(self.vocab, outline)


if __name__ == '__main__':
    ob = Vocabulary()
    ob.create_vocabulary()
    ob.print_vocabulary()
    vocab = ob.get_mood_taxonomy()
    from nltk.stem import WordNetLemmatizer

    stemmer = WordNetLemmatizer()
    temp = defaultdict(set)
    for k, v in vocab.items():
        for terms in v:
            import re

            if bool(re.search(r'^[^_-]+$', terms)):
                stem = stemmer.lemmatize(terms, wn.VERB)
                temp[k].add(terms)
    vocab = dict((k, tuple(v)) for k, v in temp.items())
    for k, v in vocab.items():
        for terms in v:
            import re

            if bool(re.search(r'^[^_-]+$', terms)):
                stem = stemmer.lemmatize(terms, wn.NOUN)
                temp[k].add(terms)
    vocab = dict((k, tuple(v)) for k, v in temp.items())
    for k, v in vocab.items():
        for terms in v:
            import re

            if bool(re.search(r'^[^_-]+$', terms)):
                stem = stemmer.lemmatize(terms, wn.ADJ)
                temp[k].add(terms)
    vocab = dict((k, tuple(v)) for k, v in temp.items())
    for k, v in vocab.items():
        for terms in v:
            import re

            if bool(re.search(r'^[^_-]+$', terms)):
                stem = stemmer.lemmatize(terms, wn.ADV)
                temp[k].add(terms)
    vocab = dict((k, tuple(v)) for k, v in temp.items())
    for k, v in vocab.items():
        for terms in v:
            import re

            if bool(re.search(r'^[^_-]+$', terms)):
                stem = stemmer.lemmatize(terms, wn.ADJ_SAT)
                temp[k].add(terms)

    ob.vocab = temp
    ob.store_vocabulary()
