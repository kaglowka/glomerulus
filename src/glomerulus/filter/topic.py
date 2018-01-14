import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
import numpy as np

class ArticleFeatureExtractor:
    def __init__(self, content):
        self.content = content

    def keywords(self):
        # Todo: first 10 words
        return self.content[:10]

    def to_features(self):
        keyword_features = {
            'is_%s_keyword' % word: True for word in self.keywords()
        }
        return keyword_features



def filter_out_by_topic(articles_name):
    with open(articles_name, 'r') as f:
        article_dicts = json.loads(f.read())

    articles = []
    for article in article_dicts:
        articles.append(ArticleFeatureExtractor(article).to_features())

    X = DictVectorizer(articles).fit_transform(articles)
    np.savetxt('features', X)
    # kmeans = KMeans(n_clusters=2, )
    # labels = kmeans.fit_predict(X)
    # print(labels)