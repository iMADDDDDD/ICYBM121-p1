import csv
import os.path

home_directory = '/home/hanne'

def create_csv(e13_dataset, ftp_dataset, fsf_dataset, int_dataset, twt_dataset, fak_users_file, bas_users_dataset, user_id_index):
    copy_whole_content_of_csv(e13_dataset, bas_users_dataset)
    copy_whole_content_of_csv(ftp_dataset, bas_users_dataset)
    with open(fak_users_file, 'r') as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
           user_id = row[0]
           dataset = row[1]
           if dataset == 'fsf':
              copy_part_of_csv(fsf_dataset, bas_users_dataset, user_id, user_id_index)
           elif dataset == 'int':
              copy_part_of_csv(int_dataset, bas_users_dataset, user_id, user_id_index)
           elif dataset == 'twt': 
              copy_part_of_csv(twt_dataset, bas_users_dataset, user_id, user_id_index)


def copy_whole_content_of_csv(dataset1, dataset2):
    header_present = True
    if not os.path.isfile(dataset2):
       header_present = False
    output_file = open(dataset2, 'a', encoding = 'utf-8')
    csv_writer = csv.writer(output_file)
    with open(dataset1, 'r') as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        if not header_present:
            for row in users_reader:
                csv_writer.writerow(row)
        else:
            next(users_reader, None)
            for row in users_reader:
                csv_writer.writerow(row)
    output_file.close()


def copy_part_of_csv(dataset1, dataset2, user_id, user_id_index):
    output_file = open(dataset2, 'a', encoding = 'utf-8')
    csv_writer = csv.writer(output_file)
    with open(dataset1, 'r') as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
            if user_id == row[index]:
                csv_writer.writerow(row)
    output_file.close()
        
    
    
def main():
    bas_users_dataset = home_directory + '/git/ICYBM121-p1/code/bas_users.csv'
    e13_users_dataset =  home_directory + '/git/ICYBM121-p1/database/E13/users.csv'
    ftp_users_dataset =  home_directory + '/git/ICYBM121-p1/database/FTP/users.csv'
    fsf_users_dataset =  home_directory + '/git/ICYBM121-p1/database/FSF/users.csv'
    int_users_dataset =  home_directory + '/git/ICYBM121-p1/database/INT/users.csv'
    twt_users_dataset =  home_directory + '/git/ICYBM121-p1/database/TWT/users.csv'
    fak_users_file = home_directory + '/git/ICYBM121-p1/code/FAK_user_ids.csv'
    user_id_index_users = 0
    create_csv(e13_users_dataset, ftp_users_dataset, fsf_users_dataset, int_users_dataset, twt_users_dataset, fak_users_file, bas_users_dataset, user_id_index_users)
    bas_tweets_dataset = home_directory + '/git/ICYBM121-p1/code/bas_tweets.csv'
    e13_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/E13/tweets.csv'
    ftp_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/FTP/tweets.csv'
    fsf_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/FSF/tweets.csv'
    int_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/INT/tweets.csv'
    twt_tweets_dataset =  home_directory + '/git/ICYBM121-p1/database/TWT/tweets.csv'
    user_id_index_tweets = 4
    create_csv(e13_tweets_dataset, ftp_tweets_dataset, fsf_tweets_dataset, int_tweets_dataset, twt_tweets_dataset, fak_users_file, bas_tweets_dataset, user_id_index_tweets)


if __name__ == "__main__":
    main()


