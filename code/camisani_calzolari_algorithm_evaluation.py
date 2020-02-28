import math
from camisani_calzolari_algorithm import camisani_calzolari_algorithm

home_directory = '/home/hanne'

def calculate_accuracy(true_positive, true_negative, false_positive, false_negative):
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    return accuracy

def calculate_precision(true_positive, false_positive):
    precision = true_positive / (true_positive + false_positive)
    return precision

def calculate_recall(true_positive, false_negative):
    recall = true_positive / (true_positive + false_negative)
    return recall

def calculate_f_measure(precision, recall):
    f_measure = (2 * precision * recall) / (precision + recall)
    return f_measure

def calculate_MCC(true_positive, true_negative, false_positive, false_negative):
    MCC = ((true_positive * true_negative) - (false_positive * false_negative)) / math.sqrt((true_positive + false_negative) * (true_positive + false_positive) * (true_negative + false_positive) * (true_negative + false_negative))
    return MCC


def main():
    fak_dataset = home_directory + '/git/ICYBM121-p1/database/'
    users_dataset = dataset + 'users.csv'
    tweets_dataset = dataset + 'tweets.csv'
    camisani_calzolari_algorithm(users_dataset, tweets_dataset)


if __name__ == "__main__":
    main()
