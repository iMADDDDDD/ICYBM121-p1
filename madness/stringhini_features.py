import pandas as pd
from info_gain import info_gain
from numpy import *
import re
from scipy.stats import pearsonr

BAS = '../datasets/BAS/bas_users.csv'
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
    return temp_list


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
    return tmp


# The content of spambots’ tweets exhibits the so-called message similarity
def feature3():
    print("Reading datasets...")
    dataset = pd.read_csv(BAS)
    dataset_tweets = pd.read_csv(BAS_TWEETS)
    dataset_tweets.rename(columns={'Unnamed: 0': 'user_id'}, inplace=True)
    print("Done")

    users_id = dataset['id'].values

    temp = []
    similarities = []

    for i in range(len(users_id)):
        print(i)
        all_user_tweets = dataset_tweets['text'].loc[dataset_tweets['user_id'] == users_id[i]]
        similarities.append(message_similarity(all_user_tweets))

    for similarity in similarities:
        if similarity > 100:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, similarities)
    print("Information Gain: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(similarities, class_list))
    return temp


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
    return temp


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
        ratios.append(ratio)

    for i in range(len(ratios)):
        if isnan(ratios[i]):
            ratios[i] = 0

    for i in range(len(ratios)):
        if isinf(ratios[i]):
            ratios[i] = 0

    for ratio in ratios:
        if ratio < 0.1:
            temp.append(1)
        else:
            temp.append(0)

    ig = info_gain.info_gain(temp, ratios)
    print("Information Gain: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(ratios, class_list))
    return temp


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
    tweets = tweets.tolist()
    similarities = 0
    i = 1
    while i < len(tweets):
        j = -1
        while j > -16:

            if j + i < 0:
                j = -17
            else:
                firstTweet = str(tweets[i]).split()
                secondTweet = str(tweets[i + j]).split()

                for m in range(len(firstTweet)):
                    for n in range(len(secondTweet)):

                        if firstTweet[m] == secondTweet[n]:

                            try:
                                if (firstTweet[m + 1] == secondTweet[n + 1] and firstTweet[m + 2] == secondTweet[
                                    n + 2] and firstTweet[m + 3] == secondTweet[n + 3]):
                                    similarities += 1
                            except:
                                pass

                j -= 1
        i += 1
    return similarities / 2


if __name__ == '__main__':
    print("Feature 5")
    feature5()