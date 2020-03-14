import os
import csv
import pandas
import math
import sys
from datetime import datetime
import pytz
import time
import re
import rules


home_directory = "/home/hanne"

def camisani_calzolari_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    rule_set = 'camisani_calzolari'
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'output', 'class'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    df_tweets = pandas.read_csv(tweets_dataset, index_col=4)
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
            rule_satisfied = 0

            if rule_number in [1,2,3,4,5,6,7,9,19]:
                rule_satisfied = check_rule(rule_set, rule_number, row)

            # needs to be checked in tweets
            elif rule_number in [8,10,11,12,13,14,15,16,17,18,20,21,22]:
                rule_satisfied = check_rules_related_to_tweets(df_tweets, user_id, rule_number, rule_set)
                
            dataset = row['dataset']
            if dataset == 'E13' or dataset == 'TFP':
                class_user = 0
            elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                class_user = 1
            # RULE IS NOT SATISFIED
            if rule_satisfied == 0:
                # USER IS BOT
                bot += 1

            # RULE IS SATISFIED
            elif rule_satisfied == 1:
                # USER IS HUMAN
                human += 1

            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id,dataset,rule_satisfied,class_user])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('----------------------------------------') 


def check_rules_related_to_tweets(df_tweets, user_id, number, rule_set):
    rule_satisfied = 0
    try:
        tweets_user = df_tweets.loc[int(user_id)]
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    except:
        print("no tweets for user")
        #everything is false by default
    else:
        if isinstance(tweets_user, pandas.Series):
            df_user = pandas.DataFrame(tweets_user).T
        else:
            df_user = tweets_user
        if number == 22:
            rule_satisfied = check_rule(rule_set, number, df_user)
        else:
            for _, tweet_row in df_user.iterrows():
                rule_satisfied = check_rule(rule_set, number, tweet_row)
    return rule_satisfied


def check_rule(rule_set, number, row): 
    rule_satisfied = 0
    attribute = rules.attributes(rule_set, number)
    if isinstance(attribute, list):
       attribute_value = []
       for attr in attribute:
           attribute_value.append(row[attr])
    else:
       attribute_value = row[attribute]    
    rule_output = rules.rules(rule_set, number, attribute_value)
    if rule_output == 1:
        rule_satisfied = 1
    return rule_satisfied



def van_den_beld_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    rule_set = 'van_den_beld'
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'output', 'class'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    df_tweets = pandas.read_csv(tweets_dataset, index_col=4)
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
            if rule_number in [1,2,4]:
                rule_output =  check_vdb_rule(rule_set, number, row, df_csv) 
            elif rule_number == 3 or rule_number == 5:
                rule_output = check_vdb_tweet_rule(df_tweets, rule_number, user_id)

            dataset = row['dataset']
            if dataset == 'E13' or dataset == 'TFP':
                class_user = 0
            elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                class_user = 1
            if rule_output == 0:
                human += 1
            elif rule_output == 1:
                bot += 1
            
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id,dataset,rule_output,class_user])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('----------------------------------------') 

def check_vdb_tweet_rule(df_csv, rule_number, user_id):
    classification = 0
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
        for _, tweet_row in df_user.iterrows():

            if rule_number == 5:
                source = tweet_row['source']
                if source != 'web':
                    classification = 1

        if rule_number == 3:
            df_user['created_at'] = pandas.to_datetime(df_user['created_at'])
            created_date = df_user.sort_values(by=['created_at'], ascending=False)
            df_last_tweets = created_date.head(20)
            dict_same_tweets = {}
            for _, row in df_last_tweets.iterrows():
                text = row['text']
                in_reply_to_user_id = int(row['in_reply_to_user_id'])
                if text not in dict_same_tweets:
                    dict_same_tweets[text] = []
                if in_reply_to_user_id not in dict_same_tweets[text]:
                    dict_same_tweets[text].append(in_reply_to_user_id)
            for tweet in dict_same_tweets:
                if len(dict_same_tweets[tweet]) > 1:
                    classification = 1 
             
                

           

    return classification

def check_vdb_rule(rule_set, number, row, df_row): 
    rule_satisfied = 0
    attribute = rules.attributes(rule_set, number)
    if number == 4:
        attribute_value = []
        attribute_value.append(row[attr])
        attribute_value.append(df_row[attr])
    else: 
        if isinstance(attribute, list):
           attribute_value = []
           for attr in attribute:
               attribute_value.append(row[attr])
        else:
           attribute_value = row[attribute] 
    
    rule_output = rules.rules(rule_set, number, attribute_value)
    if rule_output == 1:
        rule_satisfied = 1
    return rule_satisfied

def socialbakers_rules(classification_file, users_dataset, tweets_dataset, rule_number):
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'output', 'class'])
    df_csv = pandas.read_csv(users_dataset, sep=',')
    df_tweets = pandas.read_csv(tweets_dataset, index_col=4)
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
                    classification = 1
                else: 
                    classification = 0

            elif rule_number == 6:
                statuses_count = int(row['statuses_count'])
                if statuses_count == 0:
                    classification = 1
                else:
                    classification = 0
 
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
                        classification = 1
                    else:
                        classification = 0
                else:
                    classification = 0
            
            elif rule_number == 8:
                description = row['description']
                if isinstance(description,float) and math.isnan(description):
                    location = row['location']
                    if isinstance(location,float) and math.isnan(location): 
                        friends_count = int(row['friends_count'])
                        if friends_count > 100:
                            classification = 1
                        else:
                            classification = 0
                    else:
                        classification = 0
                else:
                    classification = 0
            
            elif rule_number == 2 or rule_number == 3 or rule_number == 4 or rule_number == 5:
                classification = check_sb_tweet_rule(df_tweets, rule_number, user_id)    
            if dataset == 'E13' or dataset == 'TFP':
                class_user = 0
            elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                class_user = 1          
            if classification == 0:
                human += 1
            elif classification == 1:
                bot += 1
            elif classification == 'neutral':
                neutral += 1
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id, dataset, classification, class_user])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('NEUTRAL')
            print(neutral)  
            print('----------------------------------------') 


def check_sb_tweet_rule(df_csv, rule_number, user_id):
    classification = 0
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
        count_spam_tweets = 0
        count_retweets = 0
        count_links = 0
        number_tweets = 0
        
        for _, tweet_row in df_user.iterrows():
            number_tweets += 1

            if rule_number == 2:   
                text = tweet_row['text']
                if not isinstance(text, float):
                    if 'diet' in text or 'make money' in text or 'work from home' in text or 'dieta' in text or 'fare soldi' in text or 'lavoro da casa' in text:
                        count_spam_tweets += 1
             
            elif rule_number == 4:
                retweeted_status_id = tweet_row['retweeted_status_id']
                if not math.isnan(retweeted_status_id): 
                    count_retweets += 1

            elif rule_number == 5:
                text = tweet_row['text']
                if not isinstance(text, float):
                #source: https://www.geeksforgeeks.org/python-check-url-string/
                    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
                    text_without_url = ''
                    for u in url:
                        text_without_url = text.replace(u,'')
                        text = text_without_url
                    if text_without_url == '':
                        count_links += 1
                 
                 
        if rule_number == 2: 
            percentage = count_spam_tweets / number_tweets
            if percentage > 30.00:
                classification = 1  
             
        elif rule_number == 3:
            max_frequency = df_user['text'].value_counts().max()
            if max_frequency > 3:
                classification = 1

        elif rule_number == 4:
            percentage = count_retweets / number_tweets
            if percentage > 90.00:
                classification = 1  
                
        elif rule_number == 5:
            percentage = count_links / number_tweets
            if percentage > 90.00:
                classification = 1  
            
    return classification



def main():
    rule_nr = sys.argv[1]
    rule_set = sys.argv[2]
    dataset = home_directory + '/git/ICYBM121-p1/code'
    users_dataset = dataset + '/bas_users.csv'
    tweets_dataset = dataset + '/bas_tweets.csv'

    if rule_set == 'cc':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        camisani_calzolari_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))
    elif rule_set == 'vdb':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        van_den_beld_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))
    elif rule_set == 'sb':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        socialbakers_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr))


if __name__ == "__main__":
    main()
