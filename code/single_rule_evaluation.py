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

def single_rule(classification_file, users_dataset, tweets_dataset, rule_number, rule_set):
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
            if rule_set == 'camisani_calzolari':
                if rule_number in [1,2,3,4,5,6,7,9,19]:
                    rule_satisfied = check_rule(rule_set, rule_number, row)

            # needs to be checked in tweets
                elif rule_number in [8,10,11,12,13,14,15,16,17,18,20,21,22]:
                    rule_satisfied = check_cc_tweet_rule(df_tweets, user_id, rule_number, rule_set)
                # RULE IS NOT SATISFIED
                if rule_satisfied == 0:
                 # USER IS BOT
                   bot += 1

                # RULE IS SATISFIED
                elif rule_satisfied == 1:
                # USER IS HUMAN
                   human += 1

            elif rule_set == 'van_den_beld':
                if rule_number in [1,2,4]:
                    rule_output =  check_vdb_rule(rule_set, number, row, df_csv) 
                elif rule_number in [3,5]:
                    rule_output = check_vdb_tweet_rule(df_tweets, rule_number, user_id)

            elif rule_set == 'social_bakers':
                if rule_number in [1, 6, 7, 8]:
                    rule_output = check_rule(rule_set, number, row)
                
                elif rule_number in [2, 3, 4, 5]:
                    rule_output = check_sb_tweet_rule(df_tweets, rule_number, user_id)
                
            dataset = row['dataset']
            if dataset == 'E13' or dataset == 'TFP':
                class_user = 0
            elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                class_user = 1
            

            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id,dataset,rule_output,class_user])
            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('----------------------------------------') 


def check_cc_tweet_rule(df_tweets, user_id, number, rule_set):
    rule_output = 0
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
            rule_output = check_rule(rule_set, number, df_user)
        else:
            for _, tweet_row in df_user.iterrows():
                rule_output = check_rule(rule_set, number, tweet_row)
    return rule_output


def check_rule(rule_set, number, row): 
    attribute = rules.attributes(rule_set, number)
    if isinstance(attribute, list):
       attribute_value = []
       for attr in attribute:
           attribute_value.append(row[attr])
    else:
       attribute_value = row[attribute]    
    rule_output = rules.rules(rule_set, number, attribute_value)
    return rule_output


def check_vdb_tweet_rule(df_csv, rule_number, user_id):
    rule_output = 0
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
               rule_output = check_vdb_rule(rule_set, number, tweet_row, df_user)

        if rule_number == 3:
            rule_output = check_vdb_rule(rule_set, number, [], df_user)

    return rule_output

def check_vdb_rule(rule_set, number, row, df_row): 
    rule_satisfied = 0
    attribute = rules.attributes(rule_set, number)
    if number == 4:
        attribute_value = []
        attribute_value.append(row[attribute])
        attribute_value.append(df_row[attribute])
    elif number == 3:
        attribute_value = df_row
    else: 
        if isinstance(attribute, list):
           attribute_value = []
           for attr in attribute:
               attribute_value.append(row[attr])
        else:
           attribute_value = row[attribute] 
    
    rule_output = rules.rules(rule_set, number, attribute_value)
    return rule_output


def check_sb_tweet_rule(df_tweets, user_id, number, rule_set):
    classification = 0
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
        rule_output = check_rule(rule_set, number, df_user)
     
    return rule_output



def main():
    rule_nr = sys.argv[1]
    rule_set = sys.argv[2]
    dataset = home_directory + '/git/ICYBM121-p1/code'
    users_dataset = dataset + '/bas_users.csv'
    tweets_dataset = dataset + '/bas_tweets.csv'

    if rule_set == 'cc':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        single_rule(classification_file, users_dataset, tweets_dataset, int(rule_nr), 'camisani_calzolari')
    elif rule_set == 'vdb':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        van_den_beld_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr), 'van_den_beld')
    elif rule_set == 'sb':
        classification_file = dataset + '/bas_classification_' + rule_set + '_r' + rule_nr + '.csv'
        socialbakers_rules(classification_file, users_dataset, tweets_dataset, int(rule_nr), 'social_bakers')


if __name__ == "__main__":
    main()
