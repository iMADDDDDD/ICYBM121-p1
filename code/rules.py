import math

#Classification equals 0 (human) or 1 (bot)

def rules(rule_set, number, attribute):
    if rule_set == 'camisani_calzolari':
        if number == 1:
            classification = camisani_calzolari_rule_1(attribute)
        elif number == 2:
            classification = camisani_calzolari_rule_2(attribute)
        elif number == 3:
            classification = camisani_calzolari_rule_3(attribute)
        elif number == 4:
            classification = camisani_calzolari_rule_4(attribute)
        elif number == 5:
            classification = camisani_calzolari_rule_5(attribute)
        elif number == 6:
            classification = camisani_calzolari_rule_6(attribute)
        elif number == 7:
            classification = camisani_calzolari_rule_7(attribute)
        elif number == 8:
            classification = camisani_calzolari_rule_8(attribute)
        elif number == 9:
            classification = camisani_calzolari_rule_9(attribute)
        elif number == 10:
            classification = camisani_calzolari_rule_10(attribute)
        elif number == 11:
            classification = camisani_calzolari_rule_11(attribute)
        elif number == 12:
            classification = camisani_calzolari_rule_12(attribute)
        elif number == 13:
            classification = camisani_calzolari_rule_13(attribute)
        elif number == 14:
            classification = camisani_calzolari_rule_14(attribute)
        elif number == 15:
            classification = camisani_calzolari_rule_15(attribute)
        elif number == 16:
            classification = camisani_calzolari_rule_16(attribute)
        elif number == 17:
            classification = camisani_calzolari_rule_17(attribute)
        elif number == 18:
            classification = camisani_calzolari_rule_18(attribute)
        elif number == 19:
            classification = camisani_calzolari_rule_19(attribute[0], attribute[1])
        elif number == 20:
            classification = camisani_calzolari_rule_20(attribute)
        elif number == 21:
            classification = camisani_calzolari_rule_21(attribute)
        elif number == 22:
            classification = camisani_calzolari_rule_22(attribute)
    return classification


def attributes(rule_set, rule_number):
    if rule_set == 'camisani_calzolari':
        if rule_number == 1:
            attribute = 'name'
        elif rule_number == 2:
            attribute = 'default_profile_image'
        elif rule_number == 3:
            attribute = 'location'
    return attribute


#rule 1. the profile contains a name
def camisani_calzolari_rule_1(name):
    if name != '':
        classification = 0
    else:
        classification = 1
    return classification


#rule 2. the profile contains an image
# default_profile_image is a Boolean
# * true if default image is used
# * false if user has uploaded its own image
def camisani_calzolari_rule_2(default_profile_image):
    if isinstance(default_profile_image, float) and math.isnan(default_profile_image):
        classification = 0
    elif default_profile_image == 1.0:
        classification = 1
    else:
        classification = 0
    return classification


#rule 3. the profile contains a physical address
def camisani_calzolari_rule_3(location):
    if isinstance(location,float) and math.isnan(location):
        classification = 1
    else:
        classification = 0
    return classification


#rule 4. the profile contains a biography
def camisani_calzolari_rule_4(description):
    if isinstance(description,float) and math.isnan(description):
        classification = 1
    else:
        classification = 0
    return classification


#rule 5. the account has at least 30 followers
def camisani_calzolari_rule_5(followers_count):
    if int(followers_count) >= 30:
        classification = 0
    else:
        classification = 1
    return classification


#rule 6. it has been inserted in a list by other Twitter users
# listed_count = number of public lists that this user is a member of
def camisani_calzolari_rule_6(listed_count):
    if int(listed_count) > 0:
        classification = 0
    else:
        classification = 1
    return classification


#rule 7. it has written at least 50 tweets
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
def camisani_calzolari_rule_7(statuses_count):
    if int(statuses_count) > 50:
        classification = 0
    else:
        classification = 1
    return classification


#rule 8. the account has been geo-localized
def camisani_calzolari_rule_8(geo):
    if isinstance(geo,float) and math.isnan(geo):
        classification = 1
    else:
        classification = 0
    return classification


#rule 9. the profile contains a URL
def camisani_calzolari_rule_9(url):
    if isinstance(url,float) and math.isnan(url):
        classification = 1
    else:
        classification = 0
    return classification


#rule 10. it has been includes in another user's favorites
def camisani_calzolari_rule_10(favorite_count):
    if not isinstance(favorite_count, float) and not math.isnan(favorite_count):
        if int(favorite_count) > 0:
            classification = 0
        else:
            classification = 1
    else:
        classification = 1
    return classification


#rule 11. it writes tweets that have punctuation
# in one text
# three punctuation marks that are appropriate for use as sentence endings
def camisani_calzolari_rule_11(text):
    if not isinstance(text, float):
        if '.' in text or '?' in text or '!' in text:
            classification = 0
        else:
            classification = 1
    else:
        classification = 1
    return classification


#rule 12. it has used a hashtag in at least one tweet
def camisani_calzolari_rule_12(num_hashtags):
    if int(num_hashtags) > 0:
        classification = 0
    else:
        classification = 1
    return classification


#rule 13. it has logged into Twitter using an iPhone
def camisani_calzolari_rule_13(source):
    if 'Twitter for iPhone' in source:
        classification = 0
    else:
        classification = 1
    return classification


#rule 14. it has logged into Twitter using an Android device
def camisani_calzolari_rule_14(source):
    if 'Twitter for Android' in source:
        classification = 0
    else:
        classification = 1
    return classification


#rule 15. it is connected with Foursquare
def camisani_calzolari_rule_15(source):
    if 'foursquare' in source:
        classification = 0
    else:
        classification = 1
    return classification


#rule 16. it is connected with Instagram
def camisani_calzolari_rule_16(source):
    if 'Instagram' in source:
        classification = 0
    else:
        classification = 1
    return classification


#rule 17. it has logged into twitter.com website
def camisani_calzolari_rule_17(source):
    if source == 'web':
        classification = 0
    else:
        classification = 1
    return classification


#rule 18. it has written the userID of another user in at least one tweet, that is it posted a @reply or a mention
def camisani_calzolari_rule_18(in_reply_to_user_id):
    if in_reply_to_user_id != 0:
        classification = 0
    else:
        classification = 1
    return classification


#rule 19. (2*number followers) >= (number of friends)
def camisani_calzolari_rule_19(followers_count, friends_count):
    if (2*followers_count) >= (friends_count):
        classification = 0
    else:
        classification = 1
    return classification


#rule 20. it publishes content which does not just contain URLs
def camisani_calzolari_rule_20(text):
    if not isinstance(text, float):
    #source: https://www.geeksforgeeks.org/python-check-url-string/
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
        text_without_url = ''
        for u in url:
            text_without_url = text.replace(u,'')
            text = text_without_url
            if text_without_url != '':
                classification = 0
            else:
                classification = 1
    else:
        classification = 1
    return classification 


#rule 21. at least one of its tweets has been retweeted by other accounts          
def camisani_calzolari_rule_21(retweet_count):
    if int(retweet_count) > 0:
        classification = 0
    else:
        classification = 1
    return classification


#rule 22. it has logged into Twitter through different clients
def camisani_calzolari_rule_22(df_sources):
    if len(df_sources.unique()) > 1:
        classification = 0
    else:
        classification = 1
    return classification
    

