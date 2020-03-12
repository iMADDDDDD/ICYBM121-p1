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
        yang_csv = yang_csv.append({'index': ids[i], 'age': feature1[i], 'following_rate': feature9[i]}, ignore_index=True)

    yang_csv.to_csv('../datasets/ML/yang_classification.csv', index=False, encoding='utf-8-sig')


def concat():
    stringhini_csv = pd.read_csv('../datasets/ML/stringhini_classification.csv')
    yang_csv = pd.read_csv('../datasets/ML/yang_classification.csv')

    ages = yang_csv['age'].values.tolist()
    rates = yang_csv['following_rate'].values.tolist()

    stringhini_csv['age'] = ages
    stringhini_csv['following_rate'] = rates

    stringhini_csv.to_csv('../datasets/ML/yang_stringhini_classification.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    yang()
    concat()
