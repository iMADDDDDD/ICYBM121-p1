import pandas as pd
from info_gain import info_gain
from numpy import *
import re


BAS = '../datasets/BAS/users.csv'
BAS_TWEETS = '../datasets/BAS/baseline_tweets.csv'


# Spambots do not have thousands of friends
def feature1():
    dataset = pd.read_csv(BAS)
    temp_list = []
    friends_list = dataset['friends_count'].values

    for friends_count in friends_list:
        if friends_count >= 1000:
            temp_list.append(1)
        else:
            temp_list.append(0)

    ig = info_gain.info_gain(temp_list, friends_list)

    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()

    print(corrcoef(friends_list, class_list))
    pass


# Spambots have sent less than 20 tweets
def feature2():
    dataset = pd.read_csv(BAS)
    dataset_tweets = pd.read_csv(BAS_TWEETS)
    dataset_tweets.rename(columns={'Unnamed: 0': 'user_id'}, inplace=True)

    users_id = dataset['id'].values
    users_id_tweets = dataset_tweets['user_id'].values
    users_id_tweets_list = users_id_tweets.tolist()

    tmp = []
    tweets_count = []

    # Checking if each ID appears more than 20 times in users_id_tweets
    for id in users_id:
        count = users_id_tweets_list.count(id)
        if count >= 20:
            tmp.append(1)
        else:
            tmp.append(0)
        tweets_count.append(count)

    ig = info_gain.info_gain(tmp, tweets_count)
    print("Information Gain: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(tweets_count, class_list))
    pass


# The content of spambots’ tweets exhibits the so-called message similarity
def feature3():
    dataset = pd.read_csv(BAS)
    dataset_tweets = pd.read_csv(BAS_TWEETS)
    dataset_tweets.rename(columns={'Unnamed: 0': 'user_id'}, inplace=True)

    users_id = dataset['id'].values
    users_id_tweets = dataset_tweets['user_id'].values

    all_user_tweets = dataset_tweets['text'].loc[dataset_tweets['user_id'] == 3610511]
    message_similarity(all_user_tweets)

    # TODO
    # Find a way for message similarity
    pass


# Spambots have a high URL ratio
def feature4():
    dataset = pd.read_csv(BAS)
    dataset_tweets = pd.read_csv(BAS_TWEETS)
    dataset_tweets.rename(columns={'Unnamed: 0': 'user_id'}, inplace=True)

    users_id = dataset['id'].values

    url_ratios = []
    temp = []

    for id in users_id:
        user_tweets = dataset_tweets['text'].loc[dataset_tweets['user_id'] == id]
        tweet_url_count = 0
        for tweet in user_tweets:
            if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(tweet)):
                tweet_url_count += 1
        try:
            ratio = tweet_url_count / len(user_tweets)
        except ZeroDivisionError:
            ratio = 0
        print(ratio)
        url_ratios.append(ratio)

    for ratio in url_ratios:
        if ratio >= 0.6:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, url_ratios)
    print("Information Gain: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(url_ratios, class_list))
    pass


# Spambots have a high friends/followers ratio
def feature5():
    dataset = pd.read_csv(BAS)

    friends_list = dataset['friends_count'].values
    followers_list = dataset['followers_count'].values

    ratios = []
    temp = []

    for i in range(0, len(friends_list)):
        try:
            ratio = (friends_list[i] / (followers_list[i] ** 2))
        except RuntimeWarning:
            ratio = 0
        except ZeroDivisionError:
            ratio = 0
        print("------ " + str(friends_list[i]) + " / " + str(followers_list[i]) + "^2" + " = " + str(ratio))
        ratios.append(ratio)

        if ratio < 20:
            temp.append(1)
        else:
            temp.append(0)

    print(ratios)

    ig = info_gain.info_gain(temp, ratios)
    print("Information Gain: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(class_list, ratios))
    pass


def read_dataset():
    tmp = []
    dataset = pd.read_csv(BAS)

    dataset_values = dataset['dataset'].values

    for value in dataset_values:
        if value == 'E13' or value == 'TFP':
            tmp.append(1)
        else:
            tmp.append(0)
    return tmp


def message_similarity(tweets):
    tweets_list = tweets.tolist()
    last15 = tweets_list[-15:]
    pass


if __name__ == '__main__':
    feature5()
