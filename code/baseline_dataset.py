import random
import csv

home_directory = '/home/hanne'
size_fsf = 1169
size_int = 1337
size_twt = 845


def select_random_fake_accounts(number_to_select):
    total_size = size_fsf + size_int + size_twt
    selected_numbers = []
    while len(selected_numbers) != number_to_select:
        number = random.randrange(1,total_size + 1)
        if number not in selected_numbers:
            selected_numbers.append(number)
    return selected_numbers
    
    
def look_up_user_ids_of_selected_fake_accounts(selected_numbers, fsf_dataset, int_dataset, twt_dataset, user_id_file):
    user_ids = []
    for number in selected_numbers:
        if number <= size_fsf:
            user_id = look_up_user_id(number,fsf_dataset)
        elif number > size_fsf and number <= (size_fsf + size_int):
            select_number = number - size_fsf
            user_id = look_up_user_id(select_number,int_dataset)
        else:
            select_number = number - size_fsf - size_int
            user_id = look_up_user_id(select_number,twt_dataset)
        user_ids.append(user_id)
    with open(user_id_file, mode = 'w') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['id'])
            for user_id in user_ids:
                output_writer.writerow([user_id])
    

def look_up_user_id(select_number,dataset):
    with open(dataset) as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        i = 1
        for row in users_reader:
            if i == select_number:
                user_id = row[0]
            i += 1
    return user_id
           

def main():
    fsf_dataset = home_directory + '/git/ICYBM121-p1/database/FSF/users.csv'
    int_dataset = home_directory + '/git/ICYBM121-p1/database/INT/users.csv'
    twt_dataset = home_directory + '/git/ICYBM121-p1/database/TWT/users.csv'
    user_id_file = home_directory + '/git/ICYBM121-p1/code/FAK_user_ids.csv'
    number_to_select = 1950
    selected_numbers = select_random_fake_accounts(number_to_select)
    look_up_user_ids_of_selected_fake_accounts(selected_numbers, fsf_dataset, int_dataset, twt_dataset, user_id_file)


if __name__ == "__main__":
    main()
