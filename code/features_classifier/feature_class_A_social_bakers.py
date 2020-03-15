import csv
import pandas
import math
import os
from datetime import datetime
import pytz

home_directory = '/home/hanne'

def generate_class_A(classification_file, users_dataset):
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['index','followers_friends_ratio','default_image','no biography','no location', 'friends', 'no tweets', ])
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
            followers_count = row['followers_count']
            friends_count = row['friends_count']
            if friends_count >= followers_count * 50:
                f_followers_friends = 1
            else: 
                f_followers_friends = 0

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
                    f_image = 1
                else:
                    f_image = 0
            else:
                f_image = 0

            description = row['description']
            if isinstance(description,float) and math.isnan(description):
                f_biography = 1
            else:
                f_biography = 0

            location = row['location']
            if isinstance(location,float) and math.isnan(location): 
                f_location = 1
            else:
                f_location = 0

            friends_count = int(row['friends_count'])
            if friends_count > 100:
                f_friends = 1
            else:
                f_friends = 0

            statuses_count = int(row['statuses_count'])
            #print(statuses_count)
            if statuses_count == 0:
                f_tweets = 1
            else:
                f_tweets = 0            
            
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id, f_followers_friends, f_image, f_biography, f_location, f_friends, f_tweets ])


def main():
    classification_file = 'social_bakers_classificationFinal.csv'
    users_dataset = home_directory + '/git/ICYBM121-p1/code/bas_users.csv'
    generate_class_A(classification_file, users_dataset)


if __name__ == "__main__":
    main()
