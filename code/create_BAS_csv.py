import csv
import os
import pandas

home_directory = "/home/hanne"

def create_csv(e13_dataset, tfp_dataset, fsf_dataset, int_dataset, twt_dataset, fak_users_file, bas_users_dataset, user_id_index, header,kind):
    key_error = 0
    copy_whole_content_of_csv(e13_dataset, bas_users_dataset, header, user_id_index)
    copy_whole_content_of_csv(tfp_dataset, bas_users_dataset, header, user_id_index)
    with open(fak_users_file, 'r', encoding = 'utf-8') as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
           user_id = row[0]
           dataset = row[1]
           if dataset == 'fsf':
              key_error = copy_part_of_csv(fsf_dataset, bas_users_dataset, user_id, user_id_index, kind,key_error)
           elif dataset == 'int':
              key_error = copy_part_of_csv(int_dataset, bas_users_dataset, user_id, user_id_index, kind,key_error)
           elif dataset == 'twt': 
              key_error = copy_part_of_csv(twt_dataset, bas_users_dataset, user_id, user_id_index, kind, key_error)
    print("users not found:")
    print(key_error)


def copy_whole_content_of_csv(dataset1, dataset2,header_csv,user_id_index):
    df_csv = pandas.read_csv(dataset1, index_col=int(user_id_index))
    if not os.path.isfile(dataset2):
        output_file = open(dataset2, 'w', encoding = 'utf-8')
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(header_csv)
    df_csv.to_csv(dataset2, mode='a', header=False)
    


def copy_part_of_csv(dataset1, dataset2, user_id, user_id_index, kind,key_error):
    if kind == 'users':
        df_csv = pandas.read_csv(dataset1, index_col=int(user_id_index))
        rows_user = df_csv.loc[int(user_id)]
        df_user = pandas.DataFrame(rows_user).T
        df_user.insert(loc=0, column = 'user_id', value = int(user_id))
        df_user.to_csv(dataset2, index = False, mode='a', header=False)
    elif kind == 'tweets':
        df_csv = pandas.read_csv(dataset1, index_col=int(user_id_index))
        try:
            rows_user = df_csv.loc[int(user_id)]
        except: 
            key_error += 1
        else:
            if isinstance(rows_user, pandas.Series):
                df_user = pandas.DataFrame(rows_user).T
                df_user.insert(loc=0, column = 'user_id', value = int(user_id))
                df_user.to_csv(dataset2, index = False, mode='a', header=False)
            elif isinstance(rows_user, pandas.DataFrame):
                for _, tweet_row in rows_user.iterrows():
                    df_tweet_row = pandas.DataFrame(tweet_row).T
                    df_tweet_row.insert(loc=0, column = 'user_id', value = int(user_id))
                    df_tweet_row.to_csv(dataset2, mode='a', header=False)
            else:
                print("ERROR")
    return key_error      
        
    
    
def main():
    bas_users_dataset = home_directory + '/git/ICYBM121-p1/code/bas_users.csv'
    e13_users_dataset =  home_directory + '/git/ICYBM121-p1/database/E13/users.csv'
    tfp_users_dataset =  home_directory + '/git/ICYBM121-p1/database/TFP/users.csv'
    fsf_users_dataset =  home_directory + '/git/ICYBM121-p1/database/FSF/users.csv'
    int_users_dataset =  home_directory + '/git/ICYBM121-p1/database/INT/users.csv'
    twt_users_dataset =  home_directory + '/git/ICYBM121-p1/database/TWT/users.csv'
    fak_users_file = home_directory + '/git/ICYBM121-p1/code/FAK_user_ids.csv'
    user_id_index_users = 0
    header_users = ["id","name","screen_name","statuses_count","followers_count","friends_count","favourites_count","listed_count","created_at","url","lang",
"time_zone","location","default_profile","default_profile_image","geo_enabled","profile_image_url","profile_banner_url","profile_use_background_image",
"profile_background_image_url_https","profile_text_color","profile_image_url_https","profile_sidebar_border_color","profile_background_tile","profile_sidebar_fill_color",
"profile_background_image_url","profile_background_color","profile_link_color","utc_offset","protected","verified","description","updated","dataset"]
    create_csv(e13_users_dataset, tfp_users_dataset, fsf_users_dataset, int_users_dataset, twt_users_dataset, fak_users_file, bas_users_dataset, user_id_index_users, header_users, 'users')
    bas_tweets_dataset = home_directory + '/git/ICYBM121-p1/code/bas_tweets.csv'
    e13_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/E13/tweets.csv'
    tfp_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/TFP/tweets.csv'
    fsf_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/FSF/tweets.csv'
    int_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/INT/tweets.csv'
    twt_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/TWT/tweets.csv'
    user_id_index_tweets = 4
    header_tweets = ["created_at","id","text","source","user_id","truncated","in_reply_to_status_id","in_reply_to_user_id","in_reply_to_screen_name",
"retweeted_status_id","geo","place","retweet_count","reply_count","favorite_count","num_hashtags","num_urls","num_mentions","timestamp"]
    create_csv(e13_tweets_dataset, tfp_tweets_dataset, fsf_tweets_dataset, int_tweets_dataset, twt_tweets_dataset, fak_users_file, bas_tweets_dataset, user_id_index_tweets, header_tweets, 'tweets')
    


if __name__ == "__main__":
    main()


