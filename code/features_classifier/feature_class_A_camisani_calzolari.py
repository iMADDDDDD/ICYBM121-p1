import csv
import pandas
import math
import os

home_directory = '/home/hanne'

def generate_class_A(classification_file, users_dataset):
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['index','name','image','address','biography', 'followers', 'list', 'tweets', 'URL', 'followers_friends_ratio'])
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
            name = row['name']
            if isinstance(name,float) and math.isnan(name):
                f_name = 0
            else:
                f_name = 1
            
            default_profile_image = row['default_profile_image']
            if isinstance(default_profile_image,float) and math.isnan(default_profile_image):
                f_image = 1
            elif default_profile_image == 1.0:
                f_image = 0

            location = row['location']
            if isinstance(location,float) and math.isnan(location):
                f_address = 0 
            else:
                f_address = 1


            description = row['description']
            if isinstance(description,float) and math.isnan(description):
                f_biography = 0
            else:
                f_biography = 1

            followers_count = row['followers_count']
            if followers_count >= 30:
                f_followers = 1
            else:
                f_followers = 0

            
            listed_count = row['listed_count']
            if listed_count > 0:
                f_list = 1
            else:
                f_list = 0

            statuses_count = row['statuses_count']
            if statuses_count > 50:
                f_tweets = 1
            else:
                f_tweets = 0


            url = row['url']
            if isinstance(url,float) and math.isnan(url):
                f_url = 0
            else:
                f_url = 1


            followers_count = row['followers_count']
            friends_count = row['friends_count']
            if (2*followers_count) >= (friends_count):
                f_followers_friends = 1
            else:
                f_followers_friends = 0
            
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id, f_name, f_image, f_address, f_biography, f_followers, f_list, f_tweets, f_url, f_followers_friends])


def main():
    classification_file = 'camisani_calzolari_classificationFinal.csv'
    users_dataset = home_directory + '/git/ICYBM121-p1/code/bas_users.csv'
    generate_class_A(classification_file, users_dataset)


if __name__ == "__main__":
    main()
