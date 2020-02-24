import csv



def camisani_calzolari_algorithm(users_dataset, tweets_dataset):
    with open(users_dataset) as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
            human_points = 0
            bot_points = 0
            rule_1 = False
            rule_2 = False
            rule_3 = False
            rule_4 = False
            rule_5 = False
            rule_6 = False
            rule_9 = False
            rule_10 = False
            rule_11 = False
            user_id = row[0]
            name = row[1]
            followers_count = row[4]
            favorites_count = row[6]
            listed_count = row[7]
            url = row[9]
            location = row[12]
            profile_image_url = row[16]
            description = row[31]

#1. the profile contains a name
def check_rule_1(name):
    if name != '':
        rule_1 = True
    else:
        rule_1 = False
    return rule_1

#2. the profile contains an image
def check_rule_2(profile_image_url):
    if profile_image_url != '':
        rule_2 = True
    else: 
        rule_2 = False
    return rule_2

#3. the profile contains a physical address
def check_rule_3(location):
    if location != '':
        rule_3 = True
    else: 
        rule_3 = False
    return rule_3

#4. the profile contains a biography
def check_rule_4(description):
    if description != '':
        rule_4 = True
    else: 
        rule_4 = False
    return rule_4

#5. the account has at least 30 followers
def check_rule_5(followers_count):
    if followers_count != '':
        rule_5 = True
    else: 
        rule_5 = False
    return rule_5

#6. it has been inserted in a list by other Twitter users
def check_rule_6(listed_count):
    if listed_count != '':
        rule_6 = True
    else: 
        rule_6 = False
    return rule_6


def points_found_in_tweets(tweets_dataset, user_id):
    with open(tweets_dataset) as tweets_file:
        tweets_reader = csv.reader(tweets_file, delimiter=',')
        next(tweets_reader, None)
        rule_7 = False
        rule_8 = False
        rule_11 = False
        rule_12 = False
        rule_13 = False
        rule_14 = False
        rule_15 = False 
        rule_16 = False
        rule_17 = False
        rule_18 = False
        rule_20 = False
        rule_21 = False
        rule_22 = False
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
