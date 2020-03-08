# Essential imports
import pandas as pd
import random
from multiprocessing.pool import ThreadPool as Pool

# Declaring global dataset paths
E13 = '../datasets/E13/users.csv'  # Human
TFP = '../datasets/TFP/users.csv'  # Human
FSF = '../datasets/FSF/users.csv'  # Fake
INT = '../datasets/INT/users.csv'  # Fake
TWT = '../datasets/TWT/users.csv'  # Fake


# Creates human dataset
def human_dataset():
    HUM = pd.concat([pd.read_csv(E13), pd.read_csv(TFP)])
    HUM.to_csv('../datasets/HUM/users.csv', index=False, encoding='utf-8-sig')
    pass


# Creates fake dataset
def fake_dataset():
    fsf_data = pd.read_csv(FSF)
    int_data = pd.read_csv(INT)
    twt_data = pd.read_csv(TWT)

    full_fake = pd.concat([fsf_data, int_data, twt_data])
    selected = []

    FAK = pd.DataFrame(
        columns=["id", "name", "screen_name", "statuses_count", "followers_count", "friends_count", "favourites_count",
                 "listed_count", "created_at", "url", "lang", "time_zone", "location", "default_profile",
                 "default_profile_image", "geo_enabled", "profile_image_url", "profile_banner_url",
                 "profile_use_background_image", "profile_background_image_url_https", "profile_text_color",
                 "profile_image_url_https", "profile_sidebar_border_color", "profile_background_tile",
                 "profile_sidebar_fill_color", "profile_background_image_url", "profile_background_color",
                 "profile_link_color", "utc_offset", "protected", "verified", "description", "updated", "dataset"
                 ])

    while len(selected) != 1950:
        rand_id = random.randrange(0, full_fake.shape[0])
        if rand_id not in selected:
            FAK = FAK.append(full_fake.iloc[rand_id].copy(), ignore_index=True)
            selected.append(rand_id)

    FAK.to_csv('../datasets/FAK/users.csv', index=False, encoding='utf-8-sig')
    pass


# Creates baseline dataset
def baseline_dataset():
    HUM = '../datasets/HUM/users.csv'
    FAK = '../datasets/FAK/users.csv'

    BAS = pd.concat([pd.read_csv(HUM), pd.read_csv(FAK)])
    BAS.to_csv('../datasets/BAS/users.csv', index=False, encoding='utf-8-sig')
    pass


# Creates baseline dataset tweets
def baseline_tweets():
    BAS = '../datasets/BAS/users.csv'
    bas_dataset = pd.read_csv(BAS)

    BAS_TWEETS = pd.DataFrame(
        columns=["created_at", "id", "text", "source", "truncated", "in_reply_to_status_id",
                 "in_reply_to_user_id", "in_reply_to_screen_name", "retweeted_status_id", "geo", "place",
                 "retweet_count", "reply_count", "favorite_count", "num_hashtags", "num_urls", "num_mentions",
                 "timestamp"
                 ])

    user_ids = bas_dataset['id'].values
    datasets = bas_dataset['dataset'].values

    print("READING ALL TWEETS DATASETS...")

    e13_tweets = pd.read_csv('../datasets/E13/tweets.csv')
    e13_tweets.set_index('user_id', inplace=True)
    tfp_tweets = pd.read_csv('../datasets/TFP/tweets.csv')
    tfp_tweets.set_index('user_id', inplace=True)
    fsf_tweets = pd.read_csv('../datasets/FSF/tweets.csv')
    fsf_tweets.set_index('user_id', inplace=True)
    int_tweets = pd.read_csv('../datasets/INT/tweets.csv')
    int_tweets.set_index('user_id', inplace=True)
    twt_tweets = pd.read_csv('../datasets/TWT/tweets.csv')
    twt_tweets.set_index('user_id', inplace=True)

    print("DONE!")

    for i in range(0, len(user_ids)):
        try:
            if datasets[i] == 'E13':
                BAS_TWEETS = BAS_TWEETS.append(e13_tweets.loc[user_ids[i]])
            elif datasets[i] == 'TFP':
                BAS_TWEETS = BAS_TWEETS.append(tfp_tweets.loc[user_ids[i]])
            elif datasets[i] == 'FSF':
                BAS_TWEETS = BAS_TWEETS.append(fsf_tweets.loc[user_ids[i]])
            elif datasets[i] == 'INT':
                BAS_TWEETS = BAS_TWEETS.append(int_tweets.loc[user_ids[i]])
            elif datasets[i] == 'TWT':
                BAS_TWEETS = BAS_TWEETS.append(twt_tweets.loc[user_ids[i]])
        except:
            pass

    BAS_TWEETS.to_csv('../datasets/BAS/baseline_tweets.csv', index=True, encoding='utf-8-sig')


if __name__ == '__main__':
    print("[*] Generating human dataset...")
    human_dataset()
    print("[!] DONE!")
    print("[*] Generating fake dataset...")
    fake_dataset()
    print("[!] DONE!")
    print("[*] Generating baseline dataset...")
    baseline_dataset()
    print("[*] Generating baseline tweets dataset...")
    baseline_tweets()
    print("[!] DONE!")
