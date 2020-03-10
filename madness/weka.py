import pandas as pd
from madness import stringhini_features, yang_features

BAS = '../datasets/BAS/users.csv'
BAS_TWEETS = '../datasets/BAS/baseline_tweets.csv'


def stringhini():
    stringhini_csv = pd.DataFrame(columns=['index', 'number_of_friends', 'number_of_tweets',
                                           'content_of_tweets', 'url_ratio', 'friends_to_follower_ratio'])

    dataset = pd.read_csv(BAS)
    ids = dataset['id'].values

    feature1_temp = stringhini_features.feature1()
    feature2_temp = stringhini_features.feature2()
    feature3_temp = stringhini_features.feature3()
    feature4_temp = stringhini_features.feature4()
    feature5_temp = stringhini_features.feature5()

    for i in range(len(ids)):
        stringhini_csv.append(
            {'index': ids[i], 'number_of_friends': feature1_temp[i], 'number_of_tweets': feature2_temp[i],
             'content_of_tweets': feature3_temp[i], 'url_ratio': feature4_temp[i], 'friends_to_follower_ratio':
                 feature5_temp[i]})

    stringhini_csv.to_csv('../datasets/ML/stringhini_classification.csv', index=True, encoding='utf-8-sig')
    pass


"""
def yang():
    yang_csv = pd.DataFrame(columns=['index', 'age', 'bidirectional', 'avg_followers_friends', 'avg_tweets_friends',
                                     'friends_median_followers', 'api_ratio', 'api_url_ratio', 'api_tweet_similarity',
                                     'following_rate'])
"""

