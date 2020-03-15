import pandas as pd

BAS = '../datasets/BAS/bas_users.csv'
BAS_TWEETS = '../datasets/BAS/baseline_tweets.csv'


# Reads the dataset and retuns a classified list
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


# Returns the number of similarities in a user's tweets
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
