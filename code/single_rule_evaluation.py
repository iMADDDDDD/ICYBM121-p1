import os
import csv
import pandas

home_directory = "/home/hanne"

def camisani_calzolari_rule_1(classification_file, users_dataset):
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
            name = row['name']
            if name != '':
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
    dataset = home_directory + '/git/ICYBM121-p1/code/'
    classification_file = dataset + '/bas_classification_cc_r1.csv'
    users_dataset = dataset + '/bas_users.csv'
    camisani_calzolari_rule_1(classification_file, users_dataset)


if __name__ == "__main__":
    main()
