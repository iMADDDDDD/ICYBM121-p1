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
    bas_tweets_dataset = home_directory + '/git/ICYBM121-p1/code/bas_tweets.csv'
    e13_users_dataset = 
    create_csv(e13_dataset, ftp_dataset, fsf_dataset, int_dataset, twt_dataset, fak_users_file, bas_users_dataset, user_id_index)


if __name__ == "__main__":
    main()


