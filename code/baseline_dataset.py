import random

home_directory = '/home/hanne'
size_fsf = 1169
size_int = 1337
size_twt = 845

def select_random_fake_accounts():
    
    total_size = size_fsf + size_int + size_twt
    selected_numbers = []
    for i in range(0,1950):
        number = random.randrange(1,total_size + 1)
        selected_numbers.append(number)
    return selected_numbers
    
    
def lookup_userids_of_selected_fake_accounts(selected_accounts):
    for number in selected numbers:
        if number <= 1169:
            lookup_userid(number,fsf_dataset)
        elif number > 1169 < 
    


def main():
    #table 6: results of running the algorithm over the complete dataset
    dataset = home_directory + '/git/ICYBM121-p1/database/E13/'
    users_dataset = dataset + 'users.csv'
    select_random_fake_accounts
    tweets_dataset = dataset + 'tweets.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset)


if __name__ == "__main__":
    main()
