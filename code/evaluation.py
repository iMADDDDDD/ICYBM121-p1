import math
import csv
import sys
import pandas
import rules
from info_gain import info_gain


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
            classification = int(class_row[2])
            if classification == 0:
                if dataset == 'E13' or dataset == 'TFP':
                    true_negative += 1
                elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                    false_negative += 1
            elif classification == 1:
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
    total = true_negative + false_negative + true_positive + false_positive
    humans = true_negative + false_negative
    bots = true_positive + false_positive
    information_gain = 1 - ((humans/total)*((-(true_negative/humans)*math.log2(true_negative/humans)) - ((false_negative/humans)*math.log2(false_negative/humans))) + (bots/total)*((-(true_positive/bots)*math.log2(true_positive/bots)) - ((false_positive/bots)*math.log2(false_positive/bots))))
    return information_gain

def calculate_information_gain_star(dataset, classification_file, attribute, rule_set, rule_number):
    whole_total = 3900
    df_csv = pandas.read_csv(dataset)
    dict_entropy_classes = {}
    for _, row in df_csv.iterrows():
        attribute_value = row[attribute]
        if isinstance(attribute_value,float) and math.isnan(attribute_value):
            attribute_value = 'not available'
        elif not isinstance(attribute_value, str):
            attribute_value = str(attribute_value)   
        if attribute_value not in dict_entropy_classes:
            # {attribute_value : [TP, TN, FP, TP]}
            dict_entropy_classes[attribute_value] = [0,0,0,0]
        user_id = row['id']
        with open(classification_file) as class_file:
            class_reader = csv.reader(class_file, delimiter=',')
            next(class_reader, None)
            for class_row in class_reader:
                if int(user_id) == int(class_row[0]):
                    dataset = class_row[1]
                    classification = class_row[2]
                    if classification == 'human':
                        if dataset == 'E13' or dataset == 'TFP':
                            # TRUE NEGATIVE
                            dict_entropy_classes[attribute_value][1] += 1
                        elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                            # FALSE NEGATIVE
                            dict_entropy_classes[attribute_value][3] += 1
                    else:
                        if dataset == 'E13' or dataset == 'TFP':
                            # FALSE POSITIVE
                            dict_entropy_classes[attribute_value][2] += 1
                        elif dataset == 'FSF' or dataset == 'TWT' or dataset == 'INT':
                            # TRUE POSITIVE
                            dict_entropy_classes[attribute_value][0] += 1
                        
    information_gain_star = 1
    for value in dict_entropy_classes:
        tp = dict_entropy_classes[value][0]
        tn = dict_entropy_classes[value][1]
        fp = dict_entropy_classes[value][2]
        fn = dict_entropy_classes[value][3]
        humans = tn + fn
        bots = tp + fp
        total = humans + bots
        print(value)
        print(tp)
        print(tn)
        print(fn)
        print(fp)
        print(humans)
        print(bots)
        print(total)
        if value == 'not available':
            attribute_value = math.nan
        else:
            attribute_value = value
        classification = rules.rules(rule_set, rule_number, attribute_value)
        if classification == 'human':
            attribute_value_entropy = 0
            if fn != 0 and tn != 0:
                attribute_value_entropy = ((humans/whole_total)*((-(tn/humans)*math.log2(tn/humans)) - ((fn/humans)*math.log2(fn/humans))))
             
        else:
            attribute_value_entropy = (bots/whole_total)*((-(tp/bots)*math.log2(tp/bots)) - ((fp/bots)*math.log2(fp/bots)))
        information_gain_star -= attribute_value_entropy
        
    return information_gain_star

def calculate_pearson_correlation_coefficient(classification_file):
    df_csv = pandas.read_csv(classification_file)
    df_rule_class = df_csv.filter(['output','class'], axis=1)
    pearson_correlation_coefficient = df_rule_class.corr(method='pearson')
    return pearson_correlation_coefficient

def calculate_pearson_correlation_coefficient_star(bas_dataset, classification_file, rule_set, rule_number):
    attribute = rules.attributes(rule_set, rule_number)
    df_dataset = pandas.read_csv(bas_dataset)
    df_attribute = df_dataset[attribute]
    df_numerical_attribute = df_attribute.fillna(0)
    #df_numerical_attribute = df_numerical_attribute.astype(int)
    df_classification = pandas.read_csv(classification_file)
    df_class = df_classification['class']
    df_pcc_star = pandas.concat([df_numerical_attribute, df_class], axis=1)
    pearson_correlation_coefficient_star = df_pcc_star.corr(method='pearson')
    return pearson_correlation_coefficient_star

def main():
    dataset = home_directory + '/git/ICYBM121-p1/code'
    file_name = sys.argv[1]
    kind_dataset = sys.argv[2]
    #attribute = sys.argv[3]
    if 'cc' in file_name:
        rule_set = 'camisani_calzolari'
    rule_number = int(file_name[-5])
    print(rule_number)
    if kind_dataset == 'u':
        bas_dataset = dataset + '/' + 'bas_users.csv'
    elif kind_dataset == 't':
        bas_dataset = dataset + '/' + 'bas_tweets.csv'
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
    #information_gain_star = calculate_information_gain_star(bas_dataset, classification_file, attribute, rule_set, rule_number)
    #print("INFORMATION GAIN STAR")
    #print(information_gain_star)
    pearson_correlation_coefficient = calculate_pearson_correlation_coefficient(classification_file)
    print("PEARSON CORRELATION COEFFICIENT")
    print(pearson_correlation_coefficient)
    pearson_correlation_coefficient_star = calculate_pearson_correlation_coefficient_star(bas_dataset, classification_file, rule_set, rule_number)
    print("PEARSON CORRELATION COEFFICIENT STAR")
    print(pearson_correlation_coefficient_star)
    
    


if __name__ == "__main__":
    main()
