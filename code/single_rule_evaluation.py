import os
import csv
import pandas
import math
import sys

home_directory = "/home/hanne"

def camisani_calzolari_rules(classification_file, users_dataset, rule_number):
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
                print('RULE 7')
                statuses_count = row['statuses_count']
                print(statuses_count)
                if statuses_count > 50:
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 8:
                geo = row['geo']
                if not math.isnan(geo):
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 9:
                url = row['url']
                if url != '':
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 10:
                favorite_count = row['favorite_count']
                if favorite_count >= 0:
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 11:
                text = row['text']
                if not isinstance(text, float):
                    if '.' in text or '?' in text or '!' in text:
                        classification = 'human'
                else:
                    classification = 'bot'
            
            elif rule_number == 12:
                num_hashtags = row['num_hashtags']
                if num_hashtags > 0:
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 13:
                source = row['source']
                if source == 'iphone':
                    classification = 'human'
                else:
                    classification = 'bot'
            
            elif rule_number == 14:
                source = row['source']
                if source == 'android':
                    classification = 'human'
                else:
                    classification = 'bot'  
            
            elif rule_number == 15:
                source = row['source']
                if source == 'foursquare':
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 16:
                source = row['source']
                if source == 'instagram':
                    classification = 'human'
                else:
                    classification = 'bot' 

            elif rule_number == 17:
                source = row['source']
                if source == 'web':
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 18:
                in_reply_to_user_id = row['in_reply_to_user_id']
                if in_reply_to_user_id != '':
                    classification = 'human'
                else:
                    classification = 'bot'

            elif rule_number == 19:
                followers_count = row['followers_count']
                friends_count = row['friends_count']
                if (2*followers_count) >= (friends_count):
                    classification = 'human'
                else:
                    classification = 'bot'
            
            elif rule_number == 20:
                if not isinstance(text, float):
                #source: https://www.geeksforgeeks.org/python-check-url-string/
                    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) 
                    text_without_url = ''
                    for u in url:
                        text_without_url = text.replace(u,'')
                        text = text_without_url
                    if text_without_url != '':
                        classification = 'human'
                    else:
                        classification = 'bot'

            elif rule_number == 21:
                retweet_count = row['retweet_count']
                if retweet_count > 0:
                    classification = 'human'
                else:
                    classification = 'bot'
            
                
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



def main():
    rule_nr = sys.argv[1]
    dataset = home_directory + '/git/ICYBM121-p1/code/'
    classification_file = dataset + '/bas_classification_cc_r' + rule_nr + '.csv'
    users_dataset = dataset + '/bas_users.csv'
    camisani_calzolari_rules(classification_file, users_dataset, int(rule_nr))


if __name__ == "__main__":
    main()
