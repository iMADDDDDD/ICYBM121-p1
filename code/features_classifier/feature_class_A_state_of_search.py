import csv
import pandas
import math
import os

home_directory = '/home/hanne'

def generate_class_A(classification_file, users_dataset):
    if not os.path.isfile(classification_file):
        with open(classification_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['index','bot_biography','followers_friends_ratio', 'duplicate_images'])
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
            description = row['description']
            if not isinstance(description,float):
                if 'bot' in description:
                    f_biography = 1
                else: 
                    f_biography = 0

            followers_count = row['followers_count']
            friends_count = row['friends_count']
            if friends_count >= followers_count * 100:
                f_followers_friends = 1
            else: 
                f_followers_friends = 0

            user_profile_image_url = row['profile_image_url']
            number_same_images = df_csv.loc[df_csv.profile_image_url == user_profile_image_url, 'profile_image_url'].count()
            if number_same_images > 1:
                f_image = 1     
            else:
                f_image = 0            
            
            with open(classification_file, mode = 'a') as output:
                output_writer = csv.writer(output)
                output_writer.writerow([user_id, f_biography, f_followers_friends, f_image])


def main():
    classification_file = 'state_of_search_classificationFinal.csv'
    users_dataset = home_directory + '/git/ICYBM121-p1/code/bas_users.csv'
    generate_class_A(classification_file, users_dataset)


if __name__ == "__main__":
    main()
