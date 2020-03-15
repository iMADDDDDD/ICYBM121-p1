import csv
import re
import pandas
import math
import os
import rules
import time

home_directory = '/home/hanne'

def camisani_calzolari_algorithm(users_dataset, tweets_dataset, classification_file):
    rule_set = 'camisani_calzolari'
    human = 0
    bot = 0
    neutral = 0
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id','dataset', 'classification'])
    df_users = pandas.read_csv(users_dataset, sep=',')
    df_tweets = pandas.read_csv(tweets_dataset, index_col=4)
  
    for _, row in df_users.iterrows():
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
            rules_dict = initialize_rules_dictionary()
        
            # check rules related to users dataset
            for number in [1,2,3,4,5,6,7,9,19]:
                rules_dict = check_rule(rule_set, number, rules_dict, row)
            
            # check rules related to tweets dataset
            for number in [8,10,11,12,13,14,15,16,17,18,20,21,22]:
                rules_dict = check_rules_related_to_tweets(df_tweets, user_id, rules_dict, number, rule_set)

            
            dataset = row['dataset']
            #calculate the final classification of user
            classification = end_result(rules_dict)
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


def check_rules_related_to_tweets(df_tweets, user_id, rules_dict, number, rule_set):
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
            rules_dict = check_rule(rule_set, number, rules_dict, df_user)
        else:
            for _, tweet_row in df_user.iterrows():
                rules_dict = check_rule(rule_set, number, rules_dict, tweet_row)
    return rules_dict

          
def check_rule(rule_set, number, rules_dict, row): 
    attribute = rules.attributes(rule_set, number)
    if isinstance(attribute, list):
       attribute_value = []
       for attr in attribute:
           attribute_value.append(row[attr])
    else:
       attribute_value = row[attribute]    
    rule_output = rules.rules(rule_set, number, attribute_value)
    if rule_output == 1:
        rule_index = 'rule_' + str(number)
        rules_dict[rule_index] = True
    return rules_dict
            
def end_result(rules_dict):
    human_points = calculate_human_points(rules_dict)
    bot_points = calculate_bot_points(rules_dict)
    result = human_points - bot_points
    if result > 0 :
        classification = 'human'
    elif result < -4:
        classification = 'bot'
    else:
        classification = 'neutral'
    return classification


def initialize_rules_dictionary():
    rules_dict = {}
    rules_dict['rule_1'] = False
    rules_dict['rule_2'] = False
    rules_dict['rule_3'] = False
    rules_dict['rule_4'] = False
    rules_dict['rule_5'] = False
    rules_dict['rule_6'] = False
    rules_dict['rule_7'] = False
    rules_dict['rule_8'] = False
    rules_dict['rule_9'] = False
    rules_dict['rule_10'] = False
    rules_dict['rule_11'] = False
    rules_dict['rule_12'] = False
    rules_dict['rule_13'] = False
    rules_dict['rule_14'] = False
    rules_dict['rule_15'] = False
    rules_dict['rule_16'] = False
    rules_dict['rule_17'] = False
    rules_dict['rule_18'] = False
    rules_dict['rule_19'] = False
    rules_dict['rule_20'] = False
    rules_dict['rule_21'] = False
    rules_dict['rule_22'] = False
    return rules_dict

def calculate_human_points(rules_dict):
    human_points = 0
    if rules_dict['rule_1']:
        human_points += 1
    if rules_dict['rule_2']:
        human_points += 1
    if rules_dict['rule_3']:
        human_points += 1
    if rules_dict['rule_4']:
        human_points += 1
    if rules_dict['rule_5']:
        human_points += 1
    if rules_dict['rule_6']:
        human_points += 1
    if rules_dict['rule_7']:
        human_points += 1
    if rules_dict['rule_8']:
        human_points += 1
    if rules_dict['rule_9']:
        human_points += 1
    if rules_dict['rule_10']:
        human_points += 1
    if rules_dict['rule_11']:
        human_points += 1
    if rules_dict['rule_12']:
        human_points += 1
    if rules_dict['rule_13']:
        human_points += 1
    if rules_dict['rule_14']:
        human_points += 1
    if rules_dict['rule_15']:
        human_points += 1
    if rules_dict['rule_16']:
        human_points += 1
    if rules_dict['rule_17']:
        human_points += 1
    if rules_dict['rule_18']:
        human_points += 1
    if rules_dict['rule_19']:
        human_points += 1
    if rules_dict['rule_20']:
        human_points += 1
    if rules_dict['rule_21']:
        human_points += 2
    if rules_dict['rule_22']:
        human_points += 3
    return human_points

def calculate_bot_points(rules_dict):
    bot_points = 0
    if not rules_dict['rule_1']:
        bot_points += 1
    if not rules_dict['rule_2']:
        bot_points += 1
    if not rules_dict['rule_3']:
        bot_points += 1
    if not rules_dict['rule_4']:
        bot_points += 1
    if not rules_dict['rule_5']:
        bot_points += 1
    if not rules_dict['rule_6']:
        bot_points += 1
    if not rules_dict['rule_7']:
        bot_points += 1
    if not rules_dict['rule_8']:
        bot_points += 0
    if not rules_dict['rule_9']:
        bot_points += 1
    if not rules_dict['rule_10']:
        bot_points += 1
    if not rules_dict['rule_11']:
        bot_points += 1
    if not rules_dict['rule_12']:
        bot_points += 1
    if not rules_dict['rule_13']:
        bot_points += 0
    if not rules_dict['rule_14']:
        bot_points += 0
    if not rules_dict['rule_15']:
        bot_points += 0
    if not rules_dict['rule_16']:
        bot_points += 0
    if not rules_dict['rule_17']:
        bot_points += 0
    if not rules_dict['rule_18']:
        bot_points += 1
    if not rules_dict['rule_19']:
        bot_points += 1
    if not rules_dict['rule_20']:
        bot_points += 1
    if not rules_dict['rule_21']:
        bot_points += 2
    if not rules_dict['rule_22']:
        bot_points += 1
    # 2 bot points if it only uses APIs
    if not rules_dict['rule_17']:
        bot_points += 2
    return bot_points


def main():
    database = 'TWT'
    dataset = home_directory + '/git/ICYBM121-p1/database/' + database + '/'
    users_dataset = dataset + 'users.csv'
    tweets_dataset = dataset + 'tweets.csv'
    classification_file = dataset + database +'_classification.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset, classification_file)


if __name__ == "__main__":
    main()
