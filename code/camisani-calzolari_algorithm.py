import csv



def camisani_calzolari_algorithm(users_dataset, tweets_dataset):
    with open(users_dataset) as users_file:
        users_reader = csv.reader(users_file, delimiter=',')
        next(users_reader, None)
        for row in users_reader:
            name = row[1]
            followers_count = row[4]
            favorites_count = row[6]
            listed_count = row[7]
            url = row[9]
            location = row[12]
            profile_image_url = row[16]
           
    


def main():
    #table 6: results of running the algorithm over the complete dataset
    dataset = '~/git/ICYBM121-p1/databases/E13/'
    users_dataset = dataset + 'users.csv'
    camisani_calzolari_algorithm(dataset)


if __name__ == "__main__":
    main()
