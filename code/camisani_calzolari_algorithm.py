import csv



def camisani_calzolari_algorithm(users_dataset, tweets_dataset):
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
            
            favorites_count = row[6]
            listed_count = row[7]
            url = row[9]
            
            
            
            user_id = row[0]

            human_points = calculate_human_points(rules_dict)
            bot_points = calculate_bot_points(rules_dict)


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
def check_rule_6(listed_count):
    if listed_count != '':
        rule_6 = True
    else: 
        rule_6 = False
    return rule_6

#7. it has written at least 50 tweets
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
# subtract the number of retweets? 
# there is no number of retweets per user account
def check_rule_7(statuses_count):
    if statuses_count != '':
        rule_7 = True
    else: 
        rule_7 = False
    return rule_7

#8. the account has been geo-localized
def check_rule_8(geo):
    if geo != '':
        rule_8 = True
    else: 
        rule_8 = False
    return rule_8

#9. the profile contains a URL
def check_rule_9(url):
    if url != '':
        rule_9 = True
    else: 
        rule_9 = False
    return rule_9

#10. it has been includes in another user's favorites
def check_rule_10(favorites_count):
    if favorites_count != '':
        rule_10 = True
    else: 
        rule_10 = False
    return rule_10

#11. it writes tweets that have punctuation
def check_rule_11(favorites_count):
    if favorites_count != '':
        rule_11 = True
    else: 
        rule_11 = False
    return rule_11

#12. it has used a hashtag in at least one tweet
def check_rule_12(favorites_count):
    if favorites_count != '':
        rule_12 = True
    else: 
        rule_12 = False
    return rule_12

#13. it has logged into Twitter using an iPhone
def check_rule_13(favorites_count):
    if favorites_count != '':
        rule_13 = True
    else: 
        rule_13 = False
    return rule_13

#14. it has logged into Twitter using an Android device
def check_rule_14(favorites_count):
    if favorites_count != '':
        rule_14 = True
    else: 
        rule_14 = False
    return rule_14

#15. it is connected with Foursquare
def check_rule_15(favorites_count):
    if favorites_count != '':
        rule_15 = True
    else: 
        rule_15 = False
    return rule_15

#16. it is connected with Instagram
def check_rule_16(favorites_count):
    if favorites_count != '':
        rule_16 = True
    else: 
        rule_16 = False
    return rule_16

#17. it has logged into twitter.com website
def check_rule_17(favorites_count):
    if favorites_count != '':
        rule_17 = True
    else: 
        rule_17 = False
    return rule_17

#18. it has written the userID of another user in at least one tweet, that is it posted a @reply or a mention
def check_rule_18(favorites_count):
    if favorites_count != '':
        rule_18 = True
    else: 
        rule_18 = False
    return rule_18

#19. (2*number followers) >= (number of friends)
def check_rule_19(favorites_count):
    if favorites_count != '':
        rule_19 = True
    else: 
        rule_19 = False
    return rule_19

#20. it publishes content which does not just contain URLs
def check_rule_20(favorites_count):
    if favorites_count != '':
        rule_20 = True
    else: 
        rule_20 = False
    return rule_20

#21. at least one of its tweets has been retwitted by other accounts
def check_rule_21(favorites_count):
    if favorites_count != '':
        rule_21 = True
    else: 
        rule_21 = False
    return rule_21

#22. it has logged into Twitter through different clients
def check_rule_22(favorites_count):
    if favorites_count != '':
        rule_22 = True
    else: 
        rule_22 = False
    return rule_22

#TODO
def calculate_human_points(rules_dict):
    human_points = 0
    return human_points

#TODO
def calculate_bot_points(rules_dict):
    bot_points = 0
    return bot_points


def points_found_in_tweets(tweets_dataset, user_id):
    with open(tweets_dataset) as tweets_file:
        tweets_reader = csv.reader(tweets_file, delimiter=',')
        next(tweets_reader, None)
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
