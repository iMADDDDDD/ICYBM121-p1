import math
import csv
import sys


home_directory = '/home/hanne'

def determine_positive_and_negative(classification_file):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    with open(classification_file) as class_file:
        class_reader = csv.reader(class_file, delimiter=',')
        next(class_reader, None)
        for class_row in class_reader:
            dataset = class_row[1]
            classification = class_row[2]
            if classification == 'human':
                if dataset == 'E13' or dataset == 'TFP':
                    true_negative += 1
                elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                    false_negative += 1
            elif classification == 'bot':
                if dataset == 'E13' or dataset == 'TFP':
                    false_positive += 1
                elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                    true_positive += 1
    return true_positive, true_negative, false_positive, false_negative

def calculate_accuracy(true_positive, true_negative, false_positive, false_negative):
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    return accuracy

def calculate_precision(true_positive, false_positive):
    if (true_positive == 0 and false_positive == 0):
        return 0
    else:
        precision = true_positive / (true_positive + false_positive)
        return precision

def calculate_recall(true_positive, false_negative):
    if (true_positive == 0 and false_negative == 0):
        return 0
    else:
        recall = true_positive / (true_positive + false_negative)
        return recall

def calculate_f_measure(precision, recall):
    if (precision == 0 and recall == 0):
        return 0
    else:
        f_measure = (2 * precision * recall) / (precision + recall)
        return f_measure

def calculate_MCC(true_positive, true_negative, false_positive, false_negative):
    if (true_positive == 0 and false_negative == 0):
        return 0
    elif (true_positive == 0 and false_positive == 0):
        return 0
    elif (true_negative == 0 and false_positive == 0):
        return 0
    elif (true_negative == 0 and false_negative == 0):
        return 0
    else:
        MCC = ((true_positive * true_negative) - (false_positive * false_negative)) / math.sqrt((true_positive + false_negative) * (true_positive + false_positive) * (true_negative + false_positive) * (true_negative + false_negative))
        return MCC

def calculate_information_gain(true_positive, true_negative, false_positive, false_negative):
    print(true_negative)
    print(false_negative)
    print(true_positive)
    print(false_positive)
    total = true_negative + false_negative + true_positive + false_positive
    humans = true_negative + false_negative
    bots = true_positive + false_positive
    information_gain = 1 - ((humans/total)*((-(true_negative/humans)*math.log2(true_negative/humans)) - ((false_negative/humans)*math.log2(false_negative/humans))) + (bots/total)*((-(true_positive/bots)*math.log2(true_positive/bots)) - ((false_positive/bots)*math.log2(false_positive/bots))))
    return information_gain


def main():
    file_name = sys.argv[1]
    dataset = home_directory + '/git/ICYBM121-p1/code/'
    classification_file = dataset + '/' + file_name
    tp, tn, fp, fn = determine_positive_and_negative(classification_file)
    accuracy = calculate_accuracy(tp, tn, fp, fn)
    print("ACCURACY")
    print(accuracy)
    precision = calculate_precision(tp, fp)
    print("PRECISION")
    print(precision)
    recall = calculate_recall(tp, fn)
    print("RECALL")
    print(recall)
    f_measure = calculate_f_measure(precision, recall)
    print("F MEASURE")
    print(f_measure)
    mcc = calculate_MCC(tp, tn, fp, fn)
    print("MCC")
    print(mcc)
    information_gain = calculate_information_gain(tp, tn, fp, fn)
    print("INFORMATION GAIN")
    print(information_gain)
    


if __name__ == "__main__":
    main()
