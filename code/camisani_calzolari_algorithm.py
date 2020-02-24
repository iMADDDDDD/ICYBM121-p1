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
          
            #check other rules related to tweets:
            user_id = row[0]

            human_points = calculate_human_points(rules_dict)
            bot_points = calculate_bot_points(rules_dict)


def check_rules_related_to_tweets(tweets_dataset, user_id, rules_dict):
    with open(tweets_dataset) as tweets_file:
        tweets_reader = csv.reader(tweets_file, delimiter=',')
        next(tweets_reader, None)
        for tweet_row in tweets_reader:
            # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
            user_id_tweet = tweet_row[4]
            if user_id == user_id_tweet:

                #check rule 8: check if account has been geo-localized
                geo = tweet_row[8]
                rules_dict = check_rule_8(rules_dict, geo)

                #check rule 10: check if it has been included in another user's favorites
                favorite_count = int(tweet_row[14])
                rules_dict = check_rule_10(rules_dict, favorite_count)

                #check rule 11: check if it writes tweets that have punctuation
                text = tweet_row[2]
                rules_dict = check_rule_11(rules_dict, text)
             
                #check rule 12: check if it has used a hashtag in at least one tweet
                num_hashtags = int(tweet_row[15])
                rules_dict = check_rule_12(rules_dict, num_hashtags)

                #check rule 13: check if it has logged into Twitter using an iPhone
                source = tweet_row[3]
                rules_dict = check_rule_13(rules_dict, source)

                #check rule 14: check if it has logged into Twitter using an Android device
                rules_dict = check_rule_14(rules_dict, source)

                #check rule 15: check if it is connected with foursquare
                rules_dict = check_rule_15(rules_dict, source)
                
                retweet_count = tweet_row[12]
                
 

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
    if geo != '':
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
def check_rule_11(rules_dict, text):
    if '.' in text or '?' in text or '!' in text:
        rules_dict['rule_11'] = True
    return rules_dict

#12. it has used a hashtag in at least one tweet
def check_rule_12(rules_dict, num_hashtags):
    if num_hashtags > 0:
        rules_dict['rule_12'] = True
    return rules_dict

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
def check_rule_19(rules_dict, followers_count, friends_count):
    if (2*followers_count) >= (friends_count):
         rules_dict['rule_19'] = True
    return rules_dict


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



            
           
    


def main():
    #table 6: results of running the algorithm over the complete dataset
    dataset = '~/git/ICYBM121-p1/databases/E13/'
    users_dataset = dataset + 'users.csv'
    tweets_dataset = dataset + 'tweets.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset)


if __name__ == "__main__":
    main()
