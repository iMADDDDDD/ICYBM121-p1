import os
import csv
import pandas
import math
import sys
from datetime import datetime
import pytz
import time

home_directory = "/home/hanne"

def camisani_calzolari_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'classification'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    for _, row in df_csv.iterrows():
        #meaning of user fields
        #https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        user_already_classified = False
        user_id = row['id']
       
        with open(classification_file) as class_file:
            class_reader = csv.reader(class_file, delimiter=',')
            next(class_reader, None)
            for class_row in class_reader:
                class_user_id = class_row[0]
                if int(user_id) == int(class_user_id):
                    user_already_classified = True

        if not user_already_classified:
            if rule_number == 1:
                name = row['name']
                if name != '':
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 2:
                default_profile_image = row['default_profile_image']
                if isinstance(default_profile_image,float) and math.isnan(default_profile_image):
                    classification = 'human'
                elif default_profile_image == 1.0:
                    classification = 'bot'

            elif rule_number == 3:
                location = row['location']
                if isinstance(location,float) and math.isnan(location):
                    classification = 'bot'
                else:
                    classification = 'human'

            elif rule_number == 4:
                description = row['description']
                if isinstance(description,float) and math.isnan(description):
                    classification = 'bot'
                else:
                    classification = 'human'

            elif rule_number == 5:
                followers_count = row['followers_count']
                if followers_count >= 30:
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 6:
                listed_count = row['listed_count']
                if listed_count > 0:
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 7:
                statuses_count = row['statuses_count']
                if statuses_count > 50:
                    classification = 'human'
                else:
                    classification = 'bot'
            
            elif rule_number == 9:
                url = row['url']
                if isinstance(url,float) and math.isnan(url):
                    classification = 'bot'
                else:
                    classification = 'human'

            elif rule_number == 19:
                followers_count = row['followers_count']
                friends_count = row['friends_count']
                if (2*followers_count) >= (friends_count):
                    classification = 'human'
                else:
                    classification = 'bot'
            
            # needs to be checked in tweets
            elif rule_number == 8 or rule_number == 10 or rule_number == 11 or rule_number == 12 or rule_number == 13 or rule_number == 14 or rule_number == 15 or rule_number == 16 or rule_number == 17 or rule_number == 18 or rule_number == 20 or rule_number == 21 or rule_number == 22:
                classification = check_tweet_rule(tweets_dataset, rule_number, user_id)        
                
            dataset = row['dataset']
            if classification == 'human':
                human += 1
            elif classification == 'bot':
                bot += 1
            elif classification == 'neutral':
                neutral += 1
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id,dataset,classification])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('NEUTRAL')
            print(neutral)  
            print('----------------------------------------') 

def check_tweet_rule(tweets_dataset, rule_number, user_id):
    classification = 'bot'
    df_csv = pandas.read_csv(tweets_dataset, index_col=4)
    #print(df_csv)
    try:
        tweets_user = df_csv.loc[int(user_id)]
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    except:
        print("no tweets for user")
        #everything is false by default
    else:
        if isinstance(tweets_user, pandas.Series):
            df_user = pandas.DataFrame(tweets_user).T
        else:
            df_user = tweets_user
        client_count = 0
        for _, tweet_row in df_user.iterrows():
            if rule_number == 8:   
                geo = tweet_row['geo']
                if not math.isnan(geo):
                    classification = 'human'

            elif rule_number == 10:
                favorite_count = tweet_row['favorite_count']
                if favorite_count > 0:
                    classification = 'human'

            elif rule_number == 11:
                text = tweet_row['text']
                if not isinstance(text, float):
                    if '.' in text or '?' in text or '!' in text:
                        classification = 'human'
            
            elif rule_number == 12:
                num_hashtags = tweet_row['num_hashtags']
                if num_hashtags > 0:
                    classification = 'human'
            
            elif rule_number == 13:
                source = tweet_row['source']
                if source == 'iphone':
                    classification = 'human'

            elif rule_number == 14:
                source = tweet_row['source']
                if source == 'android':
                    classification = 'human'

            elif rule_number == 15:
                source = tweet_row['source']
                if source == 'foursquare':
                    classification = 'human'

            elif rule_number == 16:
                source = tweet_row['source']
                if source == 'instagram':
                    classification = 'human'

            elif rule_number == 17:
                source = tweet_row['source']
                if source == 'web':
                    classification = 'human'

            elif rule_number == 18:
                in_reply_to_user_id = tweet_row['in_reply_to_user_id']
                if in_reply_to_user_id != '':
                    classification = 'human'
            
            elif rule_number == 20:
                text = tweet_row['text']
                if not isinstance(text, float):
                #source: https://www.geeksforgeeks.org/python-check-url-string/
                    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
                    text_without_url = ''
                    for u in url:
                        text_without_url = text.replace(u,'')
                        text = text_without_url
                    if text_without_url != '':
                        classification = 'human'

            elif rule_number == 21:
                retweet_count = tweet_row['retweet_count']
                if retweet_count > 0:
                    classification = 'human'

            elif rule_number == 22:
                source = tweet_row['source']
                if source == 'iphone' or source == 'android' or source == 'foursquare' or source == 'instagram' or source == 'web':
                    client_count += 1
                if client_count > 1:
                    classification = 'human'
    return classification


def van_den_beld_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'classification'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    for _, row in df_csv.iterrows():
        #meaning of user fields
        #https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        user_already_classified = False
        user_id = row['id']
       
        with open(classification_file) as class_file:
            class_reader = csv.reader(class_file, delimiter=',')
            next(class_reader, None)
            for class_row in class_reader:
                class_user_id = class_row[0]
                if int(user_id) == int(class_user_id):
                    user_already_classified = True

        if not user_already_classified:
            if rule_number == 1:
                description = row['description']
                if not isinstance(description,float):
                    if 'bot' in description:
                        classification = 'bot'
                    else: 
                        classification = 'human'

            elif rule_number == 2:
                followers_count = row['followers_count']
                friends_count = row['friends_count']
                if friends_count >= followers_count * 100:
                    classification = 'bot'
                else: 
                    classification = 'human'

            elif rule_number == 4:
                user_profile_image_url = row['profile_image_url']
                number_same_images = df_csv.loc[df_csv.profile_image_url == user_profile_image_url, 'profile_image_url'].count()
                if number_same_images > 1:
                    classification = 'bot'
                else:
                    classification = 'human'

            #elif rule_number == 3 or rule_number == 5:

            dataset = row['dataset']
            if classification == 'human':
                human += 1
            elif classification == 'bot':
                bot += 1
            elif classification == 'neutral':
                neutral += 1
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id,dataset,classification])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('NEUTRAL')
            print(neutral)  
            print('----------------------------------------') 

def check_vdb_tweet_rule(tweets_dataset, rule_number, user_id):
    classification = 'human'
    df_csv = pandas.read_csv(tweets_dataset, index_col=4)
    #print(df_csv)
    try:
        tweets_user = df_csv.loc[int(user_id)]
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    except:
        print("no tweets for user")
        #everything is false by default
    else:
        if isinstance(tweets_user, pandas.Series):
            df_user = pandas.DataFrame(tweets_user).T
        else:
            df_user = tweets_user
        client_count = 0

        for _, tweet_row in df_user.iterrows():
            if rule_number == 3:
                text = tweet_row['text']
                in_reply_to_user_id = tweet_row['in_reply_to_user_id']
              
                

def socialbakers_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'classification'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    for _, row in df_csv.iterrows():
        #meaning of user fields
        #https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        user_already_classified = False
        user_id = row['id']
        dataset = row['dataset']
       
        with open(classification_file) as class_file:
            class_reader = csv.reader(class_file, delimiter=',')
            next(class_reader, None)
            for class_row in class_reader:
                class_user_id = class_row[0]
                if int(user_id) == int(class_user_id):
                    user_already_classified = True

        if not user_already_classified:
            classification = 'error'
            if rule_number == 1:
                followers_count = row['followers_count']
                friends_count = row['friends_count']
                if friends_count >= followers_count * 50:
                    classification = 'bot'
                else: 
                    classification = 'human'

            elif rule_number == 7:
                created_at = row['created_at']
                created_date = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')

                updated = row['updated']
                updated_date = datetime.strptime(updated,'%Y-%m-%d %H:%M:%S')
                timezone = pytz.timezone("Europe/Rome")
                crawled_date = timezone.localize(updated_date)

                difference = int((crawled_date - created_date).days)
                if difference > 62:
                    default_profile_image = row['default_profile_image']
                    if default_profile_image == 1.0:
                        classification = 'bot'
                    else:
                        classification = 'human'
                else:
                    classification = 'human'
            
            elif rule_number == 8:
                description = row['description']
                if isinstance(description,float) and math.isnan(description):
                    location = row['location']
                    if isinstance(location,float) and math.isnan(location): 
                        friends_count = int(row['friends_count'])
                        if friends_count > 100:
                            classification = 'bot'
                        else:
                            classification = 'human'
                    else:
                        classification = 'human'
                else:
                    classification = 'human'
                      

            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id, dataset, classification])


def main():
    rule_nr = sys.argv[1]
    dataset = home_directory + '/git/ICYBM121-p1/code/'
    classification_file = dataset + '/bas_classification_sb_r' + rule_nr + '.csv'
    users_dataset = dataset + '/bas_users.csv'
    tweets_dataset = dataset + '/bas_tweets.csv'
    #camisani_calzolari_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))
    #van_den_beld_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))
    socialbakers_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))


if __name__ == "__main__":
    main()
