import pandas as pd
from madness import stringhini_features, yang_features

BAS = '../datasets/BAS/bas_users.csv'
BAS_TWEETS = '../datasets/BAS/baseline_tweets.csv'


def stringhini():
    stringhini_csv = pd.DataFrame(columns=['index', 'number_of_friends', 'number_of_tweets',
                                           'content_of_tweets', 'url_ratio', 'friends_to_follower_ratio'])

    dataset = pd.read_csv(BAS)
    ids = dataset['id'].values

    print("Feature 1...")
    feature1_temp = stringhini_features.feature1()
    print("Feature 2...")
    feature2_temp = stringhini_features.feature2()
    print("Feature 3...")
    feature3_temp = stringhini_features.feature3()
    print("Feature 4...")
    feature4_temp = stringhini_features.feature4()
    print("Feature 5...")
    feature5_temp = stringhini_features.feature5()

    for i in range(len(ids)):
        stringhini_csv.append(
            {'index': ids[i], 'number_of_friends': feature1_temp[i], 'number_of_tweets': feature2_temp[i],
             'content_of_tweets': feature3_temp[i], 'url_ratio': feature4_temp[i], 'friends_to_follower_ratio':
                 feature5_temp[i]})

    stringhini_csv.to_csv('../datasets/ML/stringhini_classification.csv', index=False, encoding='utf-8-sig')
    pass


def yang():
    yang_csv = pd.DataFrame(columns=['index', 'age', 'following_rate'])

    dataset = pd.read_csv(BAS)
    ids = dataset['id'].values

    print('Feature: AGE...')
    feature1 = yang_features.feature1()
    feature9 = yang_features.feature9()

    for i in range(len(ids)):
        yang_csv = yang_csv.append({'index': ids[i], 'age': feature1[i], 'following_rate': feature9[i]},
                                   ignore_index=True)

    yang_csv.to_csv('../datasets/ML/yang_classification.csv', index=False, encoding='utf-8-sig')


def concat():
    class_a = pd.read_csv('../datasets/ML/yang_stringhini_classification.csv')
    class_c = pd.read_csv('../datasets/ML/class_c.csv')

    bilink = class_c['bilink_ratio'].values.tolist()
    nei_fol = class_c['avg_neighbors_followers'].values.tolist()
    nei_twt = class_c['avg_neighbors_twts'].values.tolist()
    med = class_c['followings_median_neighbors_followers'].values.tolist()

    class_a['bilink_ratio'] = bilink
    class_a['avg_neighbors_followers'] = nei_fol
    class_a['avg_neighbors_twts'] = nei_twt
    class_a['followings_median_neighbors_followers'] = med

    class_a.to_csv('../datasets/ML/all_features.csv', index=False, encoding='utf-8-sig')


def classc():
    yang_csv = pd.DataFrame(columns=['index', 'bilink_ratio', 'avg_neighbors_followers', 'avg_neighbors_twts',
                                     'followings_median_neighbors_followers'])

    print("Feature 2...")
    feature2 = yang_features.feature2()

    print("Feature 3...")
    feature3 = yang_features.feature3()

    print("Feature 4...")
    feature4 = yang_features.feature4()

    print("Feature 5...")
    feature5 = yang_features.feature5()

    dataset = pd.read_csv(BAS)
    ids = dataset['id'].values

    for i in range(len(ids)):
        yang_csv = yang_csv.append({'index': ids[i], 'bilink_ratio': feature2[i], 'avg_neighbors_followers': feature3[i]
                                    , 'avg_neighbors_twts': feature4[i],
                                    'followings_median_neighbors_followers': feature5[i]}, ignore_index=True)

    yang_csv.to_csv('../datasets/ML/class_c.csv', index=False, encoding='utf-8-sig')
    pass


if __name__ == '__main__':
    concat()
