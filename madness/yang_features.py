import re
import ngram
import pandas as pd
import datetime
from info_gain import info_gain
from numpy import *

BAS = '../datasets/BAS/bas_users.csv'
BAS_TWEETS = '../datasets/BAS/baseline_tweets.csv'


# Age of the account
def feature1():
    dataset = pd.read_csv(BAS)
    creation_date = dataset['created_at'].values
    current_year = 2020

    temp = []
    age = []

    for date in creation_date:
        year = date.split()[5]
        difference = current_year - int(year)
        if difference < 8:
            temp.append(0)
        else:
            temp.append(1)
        age.append(difference)

    ig = info_gain.info_gain(temp, age)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(age, class_list))
    return temp


# Bidirectional links
def feature2():
    E13_followers = '../datasets/E13/followers.csv'
    FSF_followers = '../datasets/FSF/followers.csv'
    INT_followers = '../datasets/INT/followers.csv'
    TFP_followers = '../datasets/TFP/followers.csv'
    TWT_followers = '../datasets/TWT/followers.csv'

    dataset = pd.read_csv('../datasets/BAS/bas_users.csv')
    e13_followers = pd.read_csv(E13_followers)
    fsf_followers = pd.read_csv(FSF_followers)
    int_followers = pd.read_csv(INT_followers)
    tfp_followers = pd.read_csv(TFP_followers)
    twt_followers = pd.read_csv(TWT_followers)

    bas_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values
    bas_friends = dataset['friends_count'].values

    ratios = []
    temp = []

    for i in range(0, len(bas_ids)):
        count = 0
        print(i)
        try:
            if bas_dataset[i] == 'E13':
                followers_of_id = e13_followers['source_id'].loc[e13_followers['target_id'] == bas_ids[i]].values
                for id in followers_of_id:
                    try:
                        forward = e13_followers['target_id'].loc[e13_followers['source_id'] == id].values
                        if forward[0] == bas_ids[i]:
                            count += 1
                        else:
                            pass
                    except KeyError:
                        pass

                ratio = count / bas_friends[i]
                ratios.append(ratio)
            elif bas_dataset[i] == 'TFP':
                followers_of_id = tfp_followers['source_id'].loc[tfp_followers['target_id'] == bas_ids[i]].values
                for id in followers_of_id:
                    try:
                        forward = tfp_followers['target_id'].loc[tfp_followers['source_id'] == id].values
                        if forward[0] == bas_ids[i]:
                            count += 1
                        else:
                            pass
                    except KeyError:
                        pass

                ratio = count / bas_friends[i]
                ratios.append(ratio)
            elif bas_dataset[i] == 'FSF':
                followers_of_id = fsf_followers['source_id'].loc[fsf_followers['target_id'] == bas_ids[i]].values
                for id in followers_of_id:
                    try:
                        forward = fsf_followers['target_id'].loc[fsf_followers['source_id'] == id].values
                        if forward[0] == bas_ids[i]:
                            count += 1
                        else:
                            pass
                    except KeyError:
                        pass

                ratio = count / bas_friends[i]
                ratios.append(ratio)
            elif bas_dataset[i] == 'INT':
                followers_of_id = int_followers['source_id'].loc[int_followers['target_id'] == bas_ids[i]].values
                for id in followers_of_id:
                    try:
                        forward = int_followers['target_id'].loc[int_followers['source_id'] == id].values
                        if forward[0] == bas_ids[i]:
                            count += 1
                        else:
                            pass
                    except KeyError:
                        pass

                ratio = count / bas_friends[i]
                ratios.append(ratio)
            elif bas_dataset[i] == 'TWT':
                followers_of_id = twt_followers['source_id'].loc[twt_followers['target_id'] == bas_ids[i]].values
                for id in followers_of_id:
                    try:
                        forward = twt_followers['target_id'].loc[twt_followers['source_id'] == id].values
                        if forward[0] == bas_ids[i]:
                            count += 1
                        else:
                            pass
                    except KeyError:
                        pass

                ratio = count / bas_friends[i]
                ratios.append(ratio)
        except:
            pass

    for ratio in ratios:
        if isnan(ratio):
            ratio = 0
        else:
            pass

    for ratio in ratios:
        if ratio < 0.5:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, ratios)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(ratios, class_list))
    return temp


# Average number of followers of friends
def feature3():
    E13_friends = '../datasets/E13/friends.csv'
    FSF_friends = '../datasets/FSF/friends.csv'
    INT_friends = '../datasets/INT/friends.csv'
    TFP_friends = '../datasets/TFP/friends.csv'
    TWT_friends = '../datasets/TWT/friends.csv'

    dataset = pd.read_csv(BAS)
    e13_friends = pd.read_csv(E13_friends)
    fsf_friends = pd.read_csv(FSF_friends)
    int_friends = pd.read_csv(INT_friends)
    tfp_friends = pd.read_csv(TFP_friends)
    twt_friends = pd.read_csv(TWT_friends)

    bas_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    followers_count = []
    averages = []
    temp = []

    for i in range(len(bas_ids)):
        print(i)
        if bas_dataset[i] == 'E13':
            friends = e13_friends['target_id'].loc[e13_friends['source_id'] == bas_ids[i]].values

            for friend in friends:
                friend_followers = dataset['followers_count'].loc[dataset['id'] == friend].values
                if friend_followers:
                    followers_count.append(friend_followers)
                else:
                    pass
            averages.append(average(followers_count))
        elif bas_dataset[i] == 'FSF':
            friends = fsf_friends['target_id'].loc[fsf_friends['source_id'] == bas_ids[i]].values

            for friend in friends:
                friend_followers = dataset['followers_count'].loc[dataset['id'] == friend].values
                if friend_followers:
                    followers_count.append(friend_followers)
                else:
                    pass
            averages.append(average(followers_count))
        elif bas_dataset[i] == 'INT':
            friends = int_friends['target_id'].loc[int_friends['source_id'] == bas_ids[i]].values

            for friend in friends:
                friend_followers = dataset['followers_count'].loc[dataset['id'] == friend].values
                if friend_followers:
                    followers_count.append(friend_followers)
                else:
                    pass
            averages.append(average(followers_count))
        elif bas_dataset[i] == 'TFP':
            friends = tfp_friends['target_id'].loc[tfp_friends['source_id'] == bas_ids[i]].values

            for friend in friends:
                friend_followers = dataset['followers_count'].loc[dataset['id'] == friend].values
                if friend_followers:
                    followers_count.append(friend_followers)
                else:
                    pass
            averages.append(average(followers_count))
        elif bas_dataset[i] == 'TWT':
            friends = twt_friends['target_id'].loc[twt_friends['source_id'] == bas_ids[i]].values

            for friend in friends:
                friend_followers = dataset['followers_count'].loc[dataset['id'] == friend].values
                if friend_followers:
                    followers_count.append(friend_followers)
                else:
                    pass
            averages.append(average(followers_count))

    for mean_value in averages:
        if mean_value < 25000:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, averages)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(averages, class_list))
    return temp


def feature4():
    E13_followers = '../datasets/E13/followers.csv'
    FSF_followers = '../datasets/FSF/followers.csv'
    INT_followers = '../datasets/INT/followers.csv'
    TFP_followers = '../datasets/TFP/followers.csv'
    TWT_followers = '../datasets/TWT/followers.csv'

    dataset = pd.read_csv(BAS)
    e13_followers = pd.read_csv(E13_followers)
    fsf_followers = pd.read_csv(FSF_followers)
    int_followers = pd.read_csv(INT_followers)
    tfp_followers = pd.read_csv(TFP_followers)
    twt_followers = pd.read_csv(TWT_followers)

    bas_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    tweets_count = []
    global_tweets_count = []
    temp = []

    for i in range(len(bas_ids)):
        print(i)
        if bas_dataset[i] == 'E13':
            id_followers = e13_followers['target_id'].loc[e13_followers['source_id'] == bas_ids[i]].values

            for follower in id_followers:
                tweets = dataset['statuses_count'].loc[dataset['id'] == follower].values
                if tweets:
                    tweets_count.append(tweets)
                else:
                    pass
            global_tweets_count.append(average(tweets_count))
        elif bas_dataset[i] == 'FSF':
            id_followers = fsf_followers['target_id'].loc[fsf_followers['source_id'] == bas_ids[i]].values

            for follower in id_followers:
                tweets = dataset['statuses_count'].loc[dataset['id'] == follower].values
                if tweets:
                    tweets_count.append(tweets)
                else:
                    pass
            global_tweets_count.append(average(tweets_count))
        elif bas_dataset[i] == 'INT':
            id_followers = int_followers['target_id'].loc[int_followers['source_id'] == bas_ids[i]].values

            for follower in id_followers:
                tweets = dataset['statuses_count'].loc[dataset['id'] == follower].values
                if tweets:
                    tweets_count.append(tweets)
                else:
                    pass
            global_tweets_count.append(average(tweets_count))
        elif bas_dataset[i] == 'TFP':
            id_followers = tfp_followers['target_id'].loc[tfp_followers['source_id'] == bas_ids[i]].values

            for follower in id_followers:
                tweets = dataset['statuses_count'].loc[dataset['id'] == follower].values
                if tweets:
                    tweets_count.append(tweets)
                else:
                    pass
            global_tweets_count.append(average(tweets_count))
        elif bas_dataset[i] == 'TWT':
            id_followers = twt_followers['target_id'].loc[twt_followers['source_id'] == bas_ids[i]].values

            for follower in id_followers:
                tweets = dataset['statuses_count'].loc[dataset['id'] == follower].values
                if tweets:
                    tweets_count.append(tweets)
                else:
                    pass
            global_tweets_count.append(average(tweets_count))
    for mean_value in global_tweets_count:
        if mean_value < 9000:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, global_tweets_count)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(global_tweets_count, class_list))
    return temp


def feature5():
    E13_followers = '../datasets/E13/followers.csv'
    FSF_followers = '../datasets/FSF/followers.csv'
    INT_followers = '../datasets/INT/followers.csv'
    TFP_followers = '../datasets/TFP/followers.csv'
    TWT_followers = '../datasets/TWT/followers.csv'

    e13_followers = pd.read_csv(E13_followers)
    fsf_followers = pd.read_csv(FSF_followers)
    int_followers = pd.read_csv(INT_followers)
    tfp_followers = pd.read_csv(TFP_followers)
    twt_followers = pd.read_csv(TWT_followers)

    dataset = pd.read_csv(BAS)
    user_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    medians = []
    friends_count = []

    for i in range(len(user_ids)):
        print(i)
        id_followers = []
        if bas_dataset[i] == 'E13':
            source_ids = e13_followers['target_id'].loc[e13_followers['source_id'] == user_ids[i]]
            friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values
            friends_count.append(friends[0])

            for id in source_ids:
                source_source_ids = e13_followers['target_id'].loc[e13_followers['source_id'] == id].values
                for source_id in source_source_ids:
                    followers_count = dataset['followers_count'].loc[dataset['id'] == source_id].values
                    if followers_count:
                        id_followers.append(followers_count)
                    else:
                        pass
            medians.append(median(id_followers))
        elif bas_dataset[i] == 'FSF':
            source_ids = fsf_followers['target_id'].loc[fsf_followers['source_id'] == user_ids[i]]
            friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values
            friends_count.append(friends[0])

            for id in source_ids:
                source_source_ids = fsf_followers['target_id'].loc[fsf_followers['source_id'] == id].values
                for source_id in source_source_ids:
                    followers_count = dataset['followers_count'].loc[dataset['id'] == source_id].values
                    if followers_count:
                        id_followers.append(followers_count)
                    else:
                        pass
            medians.append(median(id_followers))
        elif bas_dataset[i] == 'INT':
            source_ids = int_followers['target_id'].loc[int_followers['source_id'] == user_ids[i]]
            friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values
            friends_count.append(friends[0])

            for id in source_ids:
                source_source_ids = int_followers['target_id'].loc[int_followers['source_id'] == id].values
                for source_id in source_source_ids:
                    followers_count = dataset['followers_count'].loc[dataset['id'] == source_id].values
                    if followers_count:
                        id_followers.append(followers_count)
                    else:
                        pass
            medians.append(median(id_followers))
        elif bas_dataset[i] == 'TFP':
            source_ids = tfp_followers['target_id'].loc[tfp_followers['source_id'] == user_ids[i]]
            friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values
            friends_count.append(friends[0])

            for id in source_ids:
                source_source_ids = tfp_followers['target_id'].loc[tfp_followers['source_id'] == id].values
                for source_id in source_source_ids:
                    followers_count = dataset['followers_count'].loc[dataset['id'] == source_id].values
                    if followers_count:
                        id_followers.append(followers_count)
                    else:
                        pass
            medians.append(median(id_followers))
        elif bas_dataset[i] == 'TWT':
            source_ids = twt_followers['target_id'].loc[twt_followers['source_id'] == user_ids[i]]
            friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values
            friends_count.append(friends[0])

            for id in source_ids:
                source_source_ids = twt_followers['target_id'].loc[twt_followers['source_id'] == id].values
                for source_id in source_source_ids:
                    followers_count = dataset['followers_count'].loc[dataset['id'] == source_id].values
                    if followers_count:
                        id_followers.append(followers_count)
                    else:
                        pass
            medians.append(median(id_followers))

    for i in range(len(medians)):
        if isnan(medians[i]):
            medians[i] = 0

    temp = []
    ratios = []

    for i in range(len(medians)):
        if medians[i] == 0:
            ratio = 0
        else:
            ratio = friends_count[i] / medians[i]
        ratios.append(ratio)

    for ratio in ratios:
        if ratio < 1.5:
            temp.append(1)
        else:
            temp.append(0)

    ig = info_gain.info_gain(temp, ratios)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(ratios, class_list))
    return temp


def feature6():
    E13_tweets = '../datasets/E13/tweets.csv'
    FSF_tweets = '../datasets/FSF/tweets.csv'
    INT_tweets = '../datasets/INT/tweets.csv'
    TFP_tweets = '../datasets/TFP/tweets.csv'
    TWT_tweets = '../datasets/TWT/tweets.csv'

    e13_tweets = pd.read_csv(E13_tweets)
    fsf_tweets = pd.read_csv(FSF_tweets)
    int_tweets = pd.read_csv(INT_tweets)
    tfp_tweets = pd.read_csv(TFP_tweets)
    twt_tweets = pd.read_csv(TWT_tweets)

    dataset = pd.read_csv(BAS, low_memory=False)
    user_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    ratios = []
    temp = []

    for i in range(len(user_ids)):
        api_tweets_count = 0
        print(i)
        if bas_dataset[i] == 'E13':
            sources_from_id = e13_tweets['source'].loc[e13_tweets['user_id'] == user_ids[i]]
            tweets_count = dataset['statuses_count'].loc[dataset['id'] == user_ids[i]].values

            for source_id in sources_from_id:
                if "API" or "AutoTwitter" in source_id:
                    api_tweets_count += 1
                else:
                    pass

            if api_tweets_count == 0:
                ratios.append(0)
            else:
                ratios.append(tweets_count[0] / api_tweets_count)
        elif bas_dataset[i] == 'FSF':
            sources_from_id = fsf_tweets['source'].loc[fsf_tweets['user_id'] == user_ids[i]]
            tweets_count = dataset['statuses_count'].loc[dataset['id'] == user_ids[i]].values

            for source_id in sources_from_id:
                if "API" or "AutoTwitter" in source_id:
                    api_tweets_count += 1
                else:
                    pass

            if api_tweets_count == 0:
                ratios.append(0)
            else:
                ratios.append(tweets_count[0] / api_tweets_count)
        elif bas_dataset[i] == 'INT':
            sources_from_id = int_tweets['source'].loc[int_tweets['user_id'] == user_ids[i]]
            tweets_count = dataset['statuses_count'].loc[dataset['id'] == user_ids[i]].values

            for source_id in sources_from_id:
                if "API" or "AutoTwitter" in source_id:
                    api_tweets_count += 1
                else:
                    pass

            if api_tweets_count == 0:
                ratios.append(0)
            else:
                ratios.append(tweets_count[0] / api_tweets_count)
        elif bas_dataset[i] == 'TFP':
            sources_from_id = tfp_tweets['source'].loc[tfp_tweets['user_id'] == user_ids[i]]
            tweets_count = dataset['statuses_count'].loc[dataset['id'] == user_ids[i]].values

            for source_id in sources_from_id:
                if "API" or "AutoTwitter" in source_id:
                    api_tweets_count += 1
                else:
                    pass

            if api_tweets_count == 0:
                ratios.append(0)
            else:
                ratios.append(tweets_count[0] / api_tweets_count)
        elif bas_dataset[i] == 'TWT':
            sources_from_id = twt_tweets['source'].loc[twt_tweets['user_id'] == user_ids[i]]
            tweets_count = dataset['statuses_count'].loc[dataset['id'] == user_ids[i]].values

            for source_id in sources_from_id:
                if "API" or "AutoTwitter" in source_id:
                    api_tweets_count += 1
                else:
                    pass

            if api_tweets_count == 0:
                ratios.append(0)
            else:
                ratios.append(tweets_count[0] / api_tweets_count)

    for i in range(len(ratios)):
        if isnan(ratios[i]):
            ratios[i] = 0

    for ratio in ratios:
        print(ratio)
        if ratio > 1.03:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, ratios)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(ratios, class_list))
    pass


def feature7():
    E13_tweets = '../datasets/E13/tweets.csv'
    FSF_tweets = '../datasets/FSF/tweets.csv'
    INT_tweets = '../datasets/INT/tweets.csv'
    TFP_tweets = '../datasets/TFP/tweets.csv'
    TWT_tweets = '../datasets/TWT/tweets.csv'

    e13_tweets = pd.read_csv(E13_tweets)
    fsf_tweets = pd.read_csv(FSF_tweets)
    int_tweets = pd.read_csv(INT_tweets)
    tfp_tweets = pd.read_csv(TFP_tweets)
    twt_tweets = pd.read_csv(TWT_tweets)

    dataset = pd.read_csv(BAS, low_memory=False)
    user_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    ratios = []
    temp = []

    for i in range(len(user_ids)):
        api_tweetsurl_count = 0
        api_tweets = []
        print(i)
        if bas_dataset[i] == 'E13':
            tweets = e13_tweets['text'].loc[e13_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            for api_tweet in api_tweets:
                if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(api_tweet)):
                    api_tweetsurl_count += 1
            if api_tweetsurl_count == 0:
                ratios.append(0)
            else:
                ratios.append(api_tweetsurl_count / len(api_tweets))
        elif bas_dataset[i] == 'FSF':
            tweets = fsf_tweets['text'].loc[fsf_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            for api_tweet in api_tweets:
                if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(api_tweet)):
                    api_tweetsurl_count += 1
            if api_tweetsurl_count == 0:
                ratios.append(0)
            else:
                ratios.append(api_tweetsurl_count / len(api_tweets))
        elif bas_dataset[i] == 'INT':
            tweets = int_tweets['text'].loc[int_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            for api_tweet in api_tweets:
                if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(api_tweet)):
                    api_tweetsurl_count += 1
            if api_tweetsurl_count == 0:
                ratios.append(0)
            else:
                ratios.append(api_tweetsurl_count / len(api_tweets))
        elif bas_dataset[i] == 'TFP':
            tweets = tfp_tweets['text'].loc[tfp_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            for api_tweet in api_tweets:
                if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(api_tweet)):
                    api_tweetsurl_count += 1
            if api_tweetsurl_count == 0:
                ratios.append(0)
            else:
                ratios.append(api_tweetsurl_count / len(api_tweets))
        elif bas_dataset[i] == 'TWT':
            tweets = twt_tweets['text'].loc[twt_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            for api_tweet in api_tweets:
                if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(api_tweet)):
                    api_tweetsurl_count += 1
            if api_tweetsurl_count == 0:
                ratios.append(0)
            else:
                ratios.append(api_tweetsurl_count / len(api_tweets))

    for ratio in ratios:
        if ratio > 0.8:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, ratios)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print(corrcoef(ratios, class_list))
    pass


def feature8():
    timenow = datetime.datetime.now()
    E13_tweets = '../datasets/E13/tweets.csv'
    FSF_tweets = '../datasets/FSF/tweets.csv'
    INT_tweets = '../datasets/INT/tweets.csv'
    TFP_tweets = '../datasets/TFP/tweets.csv'
    TWT_tweets = '../datasets/TWT/tweets.csv'

    e13_tweets = pd.read_csv(E13_tweets)
    fsf_tweets = pd.read_csv(FSF_tweets)
    int_tweets = pd.read_csv(INT_tweets)
    tfp_tweets = pd.read_csv(TFP_tweets)
    twt_tweets = pd.read_csv(TWT_tweets)

    dataset = pd.read_csv(BAS, low_memory=False)
    user_ids = dataset['id'].values
    bas_dataset = dataset['dataset'].values

    total = []
    temp = []

    for i in range(len(user_ids)):
        api_tweets = []
        if bas_dataset[i] == 'E13':
            tweets = e13_tweets['text'].loc[e13_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            similarity_count = message_similarity(api_tweets)
            total.append(similarity_count)
        elif bas_dataset[i] == 'FSF':
            tweets = fsf_tweets['text'].loc[fsf_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            similarity_count = message_similarity(api_tweets)
            total.append(similarity_count)
        elif bas_dataset[i] == 'INT':
            tweets = int_tweets['text'].loc[int_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            similarity_count = message_similarity(api_tweets)
            total.append(similarity_count)
        elif bas_dataset[i] == 'TFP':
            tweets = tfp_tweets['text'].loc[tfp_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            similarity_count = message_similarity(api_tweets)
            total.append(similarity_count)
        elif bas_dataset[i] == 'TWT':
            tweets = twt_tweets['text'].loc[twt_tweets['user_id'] == user_ids[i]]
            for tweet in tweets:
                if "API" or "AutoBot" in tweet:
                    api_tweets.append(tweet)
                else:
                    pass
            similarity_count = message_similarity(api_tweets)
            total.append(similarity_count)

    for i in range(len(total)):
        if isnan(total[i]):
            total[i] = 0

    for count in total:
        if count > 10:
            temp.append(0)
        else:
            temp.append(1)
    
    ig = info_gain.info_gain(temp, total)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print("PEARSON CORRELATION COEFFICIENT: " + str(corrcoef(total, class_list)[0][1]))

    timeend = datetime.datetime.now()
    print("TIME TAKEN: " + str(timeend - timenow))
    pass


def feature9():
    dataset = pd.read_csv(BAS, low_memory=False)
    user_ids = dataset['id'].values
    current_year = 2015

    ratios = []
    temp = []

    for i in range(len(user_ids)):
        friends = dataset['friends_count'].loc[dataset['id'] == user_ids[i]].values[0]
        created = dataset['created_at'].loc[dataset['id'] == user_ids[i]].values[0]

        year = created.split()[5]
        difference = current_year - int(year)

        ratios.append(friends / difference)

    for ratio in ratios:
        if ratio > 100:
            temp.append(0)
        else:
            temp.append(1)

    ig = info_gain.info_gain(temp, ratios)
    print("INFORMATION GAIN: " + str(ig))

    class_list = read_dataset()
    print("PEARSON CORRELATION COEFFICIENT: " + str(corrcoef(ratios, class_list)[0][1]))
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
    feature9()
