import csv

home_directory = '/home/hanne'


def main():
    dataset = home_directory + '/git/ICYBM121-p1/database/E13/'
    tweets_dataset = dataset + 'tweets_adapted_encoding.csv'
    with open(tweets_dataset) as tweets_file:
        tweets_reader = csv.reader(tweets_file, delimiter=',')
        next(tweets_reader, None)
        for tweet_row in tweets_reader:
            tweet = tweet_row
    print("DONE")

if __name__ == "__main__":
    main()
