import math
import re

#Output equals 0 (false) or 1 (true)

def rules(rule_set, number, attribute):
    if rule_set == 'camisani_calzolari':
        if number == 1:
            output = camisani_calzolari_rule_1(attribute)
        elif number == 2:
            output = camisani_calzolari_rule_2(attribute)
        elif number == 3:
            output = camisani_calzolari_rule_3(attribute)
        elif number == 4:
            output = camisani_calzolari_rule_4(attribute)
        elif number == 5:
            output = camisani_calzolari_rule_5(attribute)
        elif number == 6:
            output = camisani_calzolari_rule_6(attribute)
        elif number == 7:
            output = camisani_calzolari_rule_7(attribute)
        elif number == 8:
            output = camisani_calzolari_rule_8(attribute)
        elif number == 9:
            output = camisani_calzolari_rule_9(attribute)
        elif number == 10:
            output = camisani_calzolari_rule_10(attribute)
        elif number == 11:
            output = camisani_calzolari_rule_11(attribute)
        elif number == 12:
            output = camisani_calzolari_rule_12(attribute)
        elif number == 13:
            output = camisani_calzolari_rule_13(attribute)
        elif number == 14:
            output = camisani_calzolari_rule_14(attribute)
        elif number == 15:
            output = camisani_calzolari_rule_15(attribute)
        elif number == 16:
            output = camisani_calzolari_rule_16(attribute)
        elif number == 17:
            output = camisani_calzolari_rule_17(attribute)
        elif number == 18:
            output = camisani_calzolari_rule_18(attribute)
        elif number == 19:
            output = camisani_calzolari_rule_19(attribute[0], attribute[1])
        elif number == 20:
            output = camisani_calzolari_rule_20(attribute)
        elif number == 21:
            output = camisani_calzolari_rule_21(attribute)
        elif number == 22:
            output = camisani_calzolari_rule_22(attribute)
    elif rule_set == 'van_den_beld':
        if number == 1:
            output = van_den_beld_rule_1(attribute)
        elif number == 2:
            output = van_den_beld_rule_2(attribute[0], attribute[1])
        elif number == 3:
            output = van_den_beld_rule_3(attribute)
        elif number == 4:
            output = van_den_beld_rule_4(attribute[0], attribute[1])
        elif number == 5:
            output = van_den_beld_rule_5(attribute)
    elif rule_set == 'social_bakers':
        if number == 1:
            output = social_bakers_rule_1(attribute[0], attribute[1])
        elif number == 2:
            output = social_bakers_rule_2(attribute)
        elif number == 3:
            output = social_bakers_rule_3(attribute)
        elif number == 4:
            output = social_bakers_rule_4(attribute)
        elif number == 5:
            output = social_bakers_rule_5(attribute)
        elif number == 6:
            output = social_bakers_rule_6(attribute)
        elif number == 7:
            output = social_bakers_rule_7(attribute[0], attribute[1], attribute[2])
        elif number == 8:
            output = social_bakers_rule_8(attribute[0], attribute[1], attribute[2])
    
    return output


def attributes(rule_set, rule_number):
    if rule_set == 'camisani_calzolari':
        if rule_number == 1:
            attribute = 'name'
        elif rule_number == 2:
            attribute = 'profile_image_url'
        elif rule_number == 3:
            attribute = 'location'
        elif rule_number == 4:
            attribute = 'description'
        elif rule_number == 5:
            attribute = 'followers_count'
        elif rule_number == 6:
            attribute = 'listed_count'
        elif rule_number == 7:
            attribute = 'statuses_count'
        elif rule_number == 8:
            attribute = 'geo'
        elif rule_number == 9:
            attribute = 'url'
        elif rule_number == 10:
            attribute = 'favorite_count'
        elif rule_number == 11 or rule_number == 20:
            attribute = 'text'
        elif rule_number == 12:
            attribute = 'num_hashtags'
        elif rule_number == 13 or rule_number == 14 or rule_number == 15 or rule_number == 16 or rule_number == 17 or rule_number == 22:
            attribute = 'source'
        elif rule_number == 18:
            attribute = 'in_reply_to_user_id'
        elif rule_number == 19:
            attribute = ['followers_count', 'friends_count']
        elif rule_number == 21:
            attribute = 'retweet_count'
    elif rule_set == 'van_den_beld':
        if rule_number == 1:
            attribute = 'description'
        elif rule_number == 2:
            attribute = ['followers_count', 'friends_count']
        elif rule_number == 3:
            attribute = ''
        elif rule_number == 4:
            attribute = 'profile_image_url'
        elif rule_number == 5:
            attribute = 'source'
    elif rule_set == 'social_bakers':
        if rule_number == 1:
            attribute = ['followers_count', 'friends_count']
        elif rule_number in [2, 3, 5]:
            attribute = 'text'
        elif rule_number == 4:
            attribute = 'retweeted_status_id'
        elif rule_number == 6:
            attribute = 'statuses_count'
        elif rule_number == 7:
            attribute = ['created_at', 'updated', 'profile_image_url']
        elif rule_number == 8: 
            attribute = ['description', 'location', 'friends_count']
    return attribute


#rule 1. the profile contains a name
def camisani_calzolari_rule_1(name):
    if isinstance(name, str):
        output = 1
    else:
        output = 0
    return output


#rule 2. the profile contains an image
# default_profile_image is a Boolean
# * true if default image is used
# * false if user has uploaded its own image
def camisani_calzolari_rule_2(profile_image_url):
    if 'default' not in profile_image_url:
        output = 1
    else:
        output = 0
    return output


#rule 3. the profile contains a physical address
def camisani_calzolari_rule_3(location):
    if isinstance(location,float) and math.isnan(location):
        output = 0
    else:
        output = 1
    return output


#rule 4. the profile contains a biography
def camisani_calzolari_rule_4(description):
    if isinstance(description,float) and math.isnan(description):
        output = 0
    else:
        output = 1
    return output


#rule 5. the account has at least 30 followers
def camisani_calzolari_rule_5(followers_count):
    if int(followers_count) >= 30:
        output = 1
    else:
        output = 0
    return output


#rule 6. it has been inserted in a list by other Twitter users
# listed_count = number of public lists that this user is a member of
def camisani_calzolari_rule_6(listed_count):
    if int(listed_count) > 0:
        output = 1
    else:
        output = 0
    return output


#rule 7. it has written at least 50 tweets
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
def camisani_calzolari_rule_7(statuses_count):
    if int(statuses_count) > 50:
        output = 1
    else:
        output = 0
    return output


#rule 8. the account has been geo-localized
def camisani_calzolari_rule_8(geo):
    if isinstance(geo,float) and math.isnan(geo):
        output = 0
    else:
        output = 1
    return output


#rule 9. the profile contains a URL
def camisani_calzolari_rule_9(url):
    if isinstance(url,float) and math.isnan(url):
        output = 0
    else:
        output = 1
    return output


#rule 10. it has been includes in another user's favorites
def camisani_calzolari_rule_10(favorite_count):
    if not isinstance(favorite_count, float) and not math.isnan(favorite_count):
        if int(favorite_count) > 0:
            output = 1
        else:
            output = 0
    else:
        output = 0
    return output


#rule 11. it writes tweets that have punctuation
# in one text
# three punctuation marks that are appropriate for use as sentence endings
def camisani_calzolari_rule_11(text):
    if not isinstance(text, float):
        if '.' in text or '?' in text or '!' in text:
            output = 1
        else:
            output = 0
    else:
        output = 0
    return output


#rule 12. it has used a hashtag in at least one tweet
def camisani_calzolari_rule_12(num_hashtags):
    if int(num_hashtags) > 0:
        output = 1
    else:
        output = 0
    return output


#rule 13. it has logged into Twitter using an iPhone
def camisani_calzolari_rule_13(source):
    if 'Twitter for iPhone' in source:
        output = 1
    else:
        output = 0
    return output


#rule 14. it has logged into Twitter using an Android device
def camisani_calzolari_rule_14(source):
    if 'Twitter for Android' in source:
        output = 1
    else:
        output = 0
    return output


#rule 15. it is connected with Foursquare
def camisani_calzolari_rule_15(source):
    if 'foursquare' in source:
        output = 1
    else:
        output = 0
    return output


#rule 16. it is connected with Instagram
def camisani_calzolari_rule_16(source):
    if 'Instagram' in source:
        output = 1
    else:
        output = 0
    return output


#rule 17. it has logged into twitter.com website
def camisani_calzolari_rule_17(source):
    if source == 'web':
        output = 1
    else:
        output = 0
    return output


#rule 18. it has written the userID of another user in at least one tweet, that is it posted a @reply or a mention
def camisani_calzolari_rule_18(in_reply_to_user_id):
    if in_reply_to_user_id != 0:
        output = 1
    else:
        output = 0
    return output


#rule 19. (2*number followers) >= (number of friends)
def camisani_calzolari_rule_19(followers_count, friends_count):
    if (2*followers_count) >= (friends_count):
        output = 1
    else:
        output = 0
    return output


#rule 20. it publishes content which does not just contain URLs
def camisani_calzolari_rule_20(text):
    output = 0
    if not isinstance(text, float):
    #source: https://www.geeksforgeeks.org/python-check-url-string/
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
        text_without_url = ''
        for u in url:
            text_without_url = text.replace(u,'')
            text = text_without_url
            if text_without_url != '':
                output = 1
            else:
                output = 0
    else:
        output = 0
    return output 


#rule 21. at least one of its tweets has been retweeted by other accounts          
def camisani_calzolari_rule_21(retweet_count):
    if int(retweet_count) > 0:
        output = 1
    else:
        output = 0
    return output


#rule 22. it has logged into Twitter through different clients
def camisani_calzolari_rule_22(df_sources):
    if len(df_sources.unique()) > 1:
        output = 1
    else:
        output = 0
    return output

#rule 1. bot in biography
def van_den_beld_rule_1(description):
    if not isinstance(description,float):
        if 'bot' in description:
            output = 1
        else: 
            output = 0
    else:
        output = 0
    return output

#rule 2. following:followers = 100:1
def van_den_beld_rule_2(followers_count, friends_count):
    if friends_count >= followers_count * 100:
        output = 1
    else: 
        output = 0
    return output

#rule 3.
def van_den_beld_rule_3(df_tweets):
   output = 0
   df_tweets['created_at'] = pandas.to_datetime(df_tweets['created_at'])
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
           output = 1
   return output   

#rule 4. duplicate_profile_pictures
def van_den_beld_rule_4(profile_image_url, df_profile_image_url):
    number_same_images = (df_profile_image_url == profile_image_url).sum()
    if number_same_images > 1:
        output = 1
    else:
        output = 0
    return output

#rule 5. tweet from API 
def van_den_beld_rule_5(source):
    if source != 'web':
        output = 1
    else: 
        output = 0
    return output


#rule 1. friends:followers >= 50:1
def social_bakers_rule_1(followers_count, friends_count):
    if friends_count >= followers_count * 50:
        output = 1
    else: 
        output = 0
    return output


#rule 2. tweets spam phrases
def social_bakers_rule_2(df_text):
    count_spam_tweets = 0
    number_tweets = 0
    for _, text in df_text.iterrows():
        number_tweets += 1
        if not isinstance(text, float):
            if 'diet' in text or 'make money' in text or 'work from home' in text or 'dieta' in text or 'fare soldi' in text or 'lavoro da casa' in text:
                count_spam_tweets += 1

    percentage = count_spam_tweets / number_tweets
    if percentage > 30.00:
        output = 1 
    else:
        output = 0
    return output


#rule 3. same tweet >= 3
def social_bakers_rule_3(df_text):
    max_frequency = df_text.value_counts().max()
    if max_frequency >= 3:
        output = 1
    else:
        output = 0
    return output


#rule 4. retweets >= 90%
def social_bakers_rule_4(df_retweeted_status_id):
    count_spam_tweets = 0
    number_tweets = 0
    for _, retweeted_status_id in df_retweeted_status_id.iterrows():
        number_tweets += 1
        if not math.isnan(retweeted_status_id): 
            count_retweets += 1

    percentage = count_retweets / number_tweets
    if percentage > 90.00:
        output = 1  
    else:
        output = 0
    return output


#rule 5. tweet-links >= 90%
def social_bakers_rule_5(df_text):
    count_links = 0
    number_tweets = 0
    for _, text in df_text.iterrows():
        number_tweets += 1
        if not isinstance(text, float):
        #source: https://www.geeksforgeeks.org/python-check-url-string/
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
            text_without_url = ''
            for u in url:
                text_without_url = text.replace(u,'')
                text = text_without_url
                if text_without_url == '':
                    count_links += 1

    percentage = count_links / number_tweets
    if percentage > 90.00:
        output = 1  
    else:
        output = 0
    return output


#rule 6. 0 tweets
def social_bakers_rule_6(statuses_count):
    if statuses_count == 0:
        output = 1
    else:
        output = 0
    return output


#rule 7. default image after 2 months
def social_bakers_rule_7(created_at, updated_date, profile_image_url):
    created_date = datetime.strptime(created_at,'%a %b %d %H:%M:%S %z %Y')
    updated_date = datetime.strptime(updated,'%Y-%m-%d %H:%M:%S')
    timezone = pytz.timezone("Europe/Rome")
    crawled_date = timezone.localize(updated_date)

    difference = int((crawled_date - created_date).days)
    if difference > 62:
        if 'default' in profile_image_url:
            output = 1
        else:
            output = 0
    else:
        output = 0
    return output


#rule 8. no bio, no location, friends >= 100
def social_bakers_rule_8(description, location, friends_count):
    if isinstance(description,float) and math.isnan(description):
        if isinstance(location,float) and math.isnan(location): 
            if int(friends_count) > 100:
                output = 1
            else:
                output = 0
        else:
            output = 0
    else:
        output = 0
    return output
    
   


    
    

