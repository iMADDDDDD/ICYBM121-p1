import csv
import re
import pandas
import math

home_directory = '/home/hanne'

def camisani_calzolari_algorithm(users_dataset, tweets_dataset):
    human = 0
    bot = 0
    neutral = 0
    with open(users_dataset) as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
            #meaning of user fields
            #https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
            rules_dict = initialize_rules_dictionary()
            
            #check rule 1: check if profile contains a name
            name = row[1]
            rules_dict = check_rule_1(rules_dict, name)

            #check rule 2: check if profile contains an image
            default_profile_image = row[14]
            rules_dict = check_rule_2(rules_dict, default_profile_image)

            #check rule 3: check if profile contains a physical address
            location = row[12]
            rules_dict = check_rule_3(rules_dict, location)

            #check rule 4: check if profile contains a biography
            description = row[31]
            rules_dict = check_rule_4(rules_dict, description)

            #check rule 5: check if the account has at least 30 followers
            followers_count = int(row[4])
            rules_dict = check_rule_5(rules_dict, followers_count)
            
            #check rule 6: check if it has been inserted in a list by other Twitter users
            listed_count = int(row[7])
            rules_dict = check_rule_6(rules_dict, listed_count)

            #check rule 7: check if it has written at least 50 tweets
            statuses_count = int(row[3])
            rules_dict = check_rule_7(rules_dict, statuses_count)
            
            #check rule 9: check if the profile contains a URL
            url = row[9]
            rules_dict = check_rule_9(rules_dict, url)

            #check rule 11: check if it writes tweets that have punctuation
            rules_dict = check_rule_11(rules_dict, description)
            
            #check rule 19: check if the equation for number of followers and friends is satisfies
            friends_count = int(row[5])
            rules_dict = check_rule_19(rules_dict, followers_count, friends_count)
          
            #check other rules related to tweets
            user_id = row[0]
            rules_dict = check_rules_related_to_tweets(tweets_dataset, user_id, rules_dict)

            #calculate the final classification of user
            classification = end_result(rules_dict)
            print(classification)
            if classification == 'human':
               human += 1
            elif classification == 'bot':
               bot += 1
            elif classification == 'neutral':
               neutral += 1

            print('HUMAN')
            print(human)
            print('BOT')
            print(bot)
            print('NEUTRAL')
            print(neutral)  
            print('----------------------------------------')       


def check_rules_related_to_tweets(tweets_dataset, user_id, rules_dict):
    df_csv = pandas.read_csv(tweets_dataset, index_col=4)
    tweets_user = df_csv.loc[int(user_id)]
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    for _, tweet_row in tweets_user.iterrows():
        #check rule 8: check if account has been geo-localized
        geo = tweet_row['geo']
        rules_dict = check_rule_8(rules_dict, geo)

        #check rule 10: check if it has been included in another user's favorites
        favorite_count = int(tweet_row['favorite_count'])
        rules_dict = check_rule_10(rules_dict, favorite_count)

        #check rule 11: check if it writes tweets that have punctuation
        text = tweet_row['text']
        rules_dict = check_rule_11(rules_dict, text)
             
        #check rule 12: check if it has used a hashtag in at least one tweet
        num_hashtags = int(tweet_row['num_hashtags'])
        rules_dict = check_rule_12(rules_dict, num_hashtags)

        #check rule 13: check if it has logged into Twitter using an iPhone
        source = tweet_row['source']
        rules_dict = check_rule_13(rules_dict, source)

        #check rule 14: check if it has logged into Twitter using an Android device
        rules_dict = check_rule_14(rules_dict, source)

        #check rule 15: check if it is connected with foursquare
        rules_dict = check_rule_15(rules_dict, source)

        #check rule 16: check if it is connected with instagram
        rules_dict = check_rule_16(rules_dict, source)

        #check rule 17: check if it has logged into twitter.com website
        rules_dict = check_rule_17(rules_dict, source)

        #check rule 18: check if it has written the userID of another user in at least one tweet, that is it posted an @reply or a mention         
        in_reply_to_user_id = tweet_row['in_reply_to_user_id']
        rules_dict = check_rule_18(rules_dict, in_reply_to_user_id)
                      
        #check rule 20: check if it publishes content which does not just contain URLs
        rules_dict = check_rule_20(rules_dict, text)

        #check rule 21: check if at least one of its tweets has been retwitted by other accounts
        retweet_count = int(tweet_row['retweet_count'])
        rules_dict = check_rule_21(rules_dict, retweet_count)

    #check rule 22: check if it has logged into Twitter
    rules_dict = check_rule_22(rules_dict)
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

    
#1. the profile contains a name
def check_rule_1(rules_dict, name):
    if name != '':
        rules_dict['rule_1'] = True
    return rules_dict

   
#2. the profile contains an image
# default_profile_image is a Boolean
# * true if default image is used
# * false if user has uploaded its own image
def check_rule_2(rules_dict, default_profile_image):
    if default_profile_image != 'true':
        rules_dict['rule_2'] = True
    return rules_dict


#3. the profile contains a physical address
def check_rule_3(rules_dict, location):
    if location != '':
        rules_dict['rule_3'] = True
    return rules_dict


#4. the profile contains a biography
def check_rule_4(rules_dict, description):
    if description != '':
        rules_dict['rule_4'] = True
    return rules_dict


#5. the account has at least 30 followers
def check_rule_5(rules_dict, followers_count):
    if followers_count >= 30:
        rules_dict['rule_5'] = True
    return rules_dict

#6. it has been inserted in a list by other Twitter users
# listed_count = number of public lists that this user is a member of
def check_rule_6(rules_dict, listed_count):
    if listed_count > 0:
        rules_dict['rule_6'] = True
    return rules_dict

#7. it has written at least 50 tweets
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
# subtract the number of retweets? 
# there is no number of retweets per user account
def check_rule_7(rules_dict, statuses_count):
    if statuses_count > 0:
        rules_dict['rule_7'] = True
    return rules_dict

#8. the account has been geo-localized
def check_rule_8(rules_dict, geo):
    if not math.isnan(geo):
        print('TRUE')
        rules_dict['rule_8'] = True
    return rules_dict


#9. the profile contains a URL
def check_rule_9(rules_dict, url):
    if url != '':
        rules_dict['rule_9'] = True
    return rules_dict


#10. it has been includes in another user's favorites
def check_rule_10(rules_dict, favorite_count):
    if favorite_count >= 0:
        rules_dict['rule_10'] = True
    return rules_dict


#11. it writes tweets that have punctuation
# in one text or in all? #TODO
# three punctuation marks that are appropriate for use as sentence endings
def check_rule_11(rules_dict, text):
    if not isinstance(text, float):
        if '.' in text or '?' in text or '!' in text:
            rules_dict['rule_11'] = True
    return rules_dict

#12. it has used a hashtag in at least one tweet
def check_rule_12(rules_dict, num_hashtags):
    if num_hashtags > 0:
        rules_dict['rule_12'] = True
    return rules_dict

#13. it has logged into Twitter using an iPhone
def check_rule_13(rules_dict, source):
    if source == 'iphone':
        rules_dict['rule_13'] = True
    return rules_dict


#14. it has logged into Twitter using an Android device
def check_rule_14(rules_dict, source):
    if source == 'android':
        rules_dict['rule_14'] = True
    return rules_dict

#15. it is connected with Foursquare
def check_rule_15(rules_dict, source):
    if source == 'foursquare':
        rules_dict['rule_15'] = True
    return rules_dict

#16. it is connected with Instagram
def check_rule_16(rules_dict, source):
    if source == 'instagram':
        rules_dict['rule_16'] = True
    return rules_dict

#17. it has logged into twitter.com website
def check_rule_17(rules_dict, source):
    if source == 'web':
        rules_dict['rule_17'] = True
    return rules_dict

#18. it has written the userID of another user in at least one tweet, that is it posted a @reply or a mention
def check_rule_18(rules_dict, in_reply_to_user_id):
    if in_reply_to_user_id != '':
        rules_dict['rule_18'] = True
    return rules_dict

#19. (2*number followers) >= (number of friends)
def check_rule_19(rules_dict, followers_count, friends_count):
    if (2*followers_count) >= (friends_count):
         rules_dict['rule_19'] = True
    return rules_dict


#20. it publishes content which does not just contain URLs
def check_rule_20(rules_dict, text):
    if not isinstance(text, float):
        #source: https://www.geeksforgeeks.org/python-check-url-string/
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
        text_without_url = ''
        for u in url:
            text_without_url = text.replace(u,'')
            text = text_without_url
        if text_without_url != '':
            rules_dict['rule_20'] = True
    return rules_dict

#21. at least one of its tweets has been retwitted by other accounts
def check_rule_21(rules_dict, retweet_count):
    if retweet_count > 0:
        rules_dict['rule_21'] = True
    return rules_dict

#22. it has logged into Twitter through different clients
def check_rule_22(rules_dict):
    client_count = 0
    if rules_dict['rule_13']:
       client_count += 1
    if rules_dict['rule_14']:
       client_count += 1
    if rules_dict['rule_15']:
       client_count += 1
    if rules_dict['rule_16']:
       client_count += 1
    if rules_dict['rule_17']:
       client_count += 1
    if client_count > 1:
       rules_dict['rule_22'] = True
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

#TODO
# 2 bot points if it only uses APIs
# at which rule do we have to look for this
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
    return bot_points


def main():
    #table 6: results of running the algorithm over the complete dataset
    dataset = home_directory + '/git/ICYBM121-p1/database/E13/'
    users_dataset = dataset + 'users.csv'
    tweets_dataset = dataset + 'tweets.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset)


if __name__ == "__main__":
    main()
