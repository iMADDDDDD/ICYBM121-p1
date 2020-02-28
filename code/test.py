import csv
import pandas

home_directory = '/home/hanne'

def main():
    dataset = home_directory + '/git/ICYBM121-p1/database/E13/'
    tweets_dataset = dataset + 'tweets.csv'
    tweets_utf8_dataset = dataset + 'tweets_utf-8.csv'
    csv_file = open(tweets_utf8_dataset, mode='w', encoding = 'utf-8')
    csv_writer = csv.writer(csv_file)
    with open(tweets_dataset, 'rb') as tweets_file:
        for line in tweets_file:
            #print(line)
            try:
                tweetrow = line.decode("utf-8")
            except:
                print("DECODE ERROR")
                print(line)
                tweet_line = input("Input the line: ")
            else:
                tweet_line = tweetrow   
            finally:
                tweet_line = tweet_line.replace('"', '')
                tweet_line = tweet_line.replace('\n', '')
                tweet_line = tweet_line.split(',')    
                print(tweet_line)
                csv_writer.writerow(tweet_line)
    csv_file.close()
            
            
def test():
    dataset = home_directory + '/git/ICYBM121-p1/database/E13/'
    tweets_dataset = dataset + 'tweets.csv'
    df_csv = pandas.read_csv(tweets_dataset, index_col=4)
    user_id = 3610511
    tweets_user = df_csv.loc[user_id]
    for _, row in tweets_user.iterrows():
        print(row)
        print('-------------------------')


if __name__ == "__main__":
    eliminate_null_values()
