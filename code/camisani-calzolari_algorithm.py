import csv



def camisani_calzolari_algorithm(users_dataset, tweets_dataset):
    with open(users_dataset) as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
            user_id = row[0]
            name = row[1]
            followers_count = row[4]
            favorites_count = row[6]
            listed_count = row[7]
            url = row[9]
            location = row[12]
            profile_image_url = row[16]
            description = row[31]
            with open(tweets_dataset) as tweets_file:
                tweets_reader = csv.reader(tweets_file, delimiter=',')
                next(tweets_reader, None)
                    for tweet_row in tweets_reader:
                        user_id_tweet = tweet_row[4]
                        if user_id == user_id_tweet:
                            source = tweet_row[3]
                            geo = tweet_row[8]
                            retweet_count = tweet_row[12]
                            num_hashtags = tweet_row[15]
           
    


def main():
    #table 6: results of running the algorithm over the complete dataset
    dataset = '~/git/ICYBM121-p1/databases/E13/'
    users_dataset = dataset + 'users.csv'
    tweets_dataset = dataset + 'tweets.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset)


if __name__ == "__main__":
    main()
