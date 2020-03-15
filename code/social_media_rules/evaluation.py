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
            classification = int(class_row[3])
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

#Function that calculates the accuracy of a feature
def calculate_accuracy(true_positive, true_negative, false_positive, false_negative):
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    return accuracy

#Function that calculates the precision of a feature
def calculate_precision(true_positive, false_positive):
    if (true_positive == 0 and false_positive == 0):
        return 0
    else:
        precision = true_positive / (true_positive + false_positive)
        return precision

#Function that calculates the recall of a feature
def calculate_recall(true_positive, false_negative):
    if (true_positive == 0 and false_negative == 0):
        return 0
    else:
        recall = true_positive / (true_positive + false_negative)
        return recall

#Function that calculates the F-measure of a feature
def calculate_f_measure(precision, recall):
    if (precision == 0 and recall == 0):
        return 0
    else:
        f_measure = (2 * precision * recall) / (precision + recall)
        return f_measure

#Function that calculates the MCC of a feature
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

#Function that calculates the information gain of a feature.
def calculate_information_gain_manual(true_positive, true_negative, false_positive, false_negative):
    total = true_negative + false_negative + true_positive + false_positive
    humans = true_negative + false_negative
    bots = true_positive + false_positive
    try:
        information_gain = 1 - ((humans/total)*((-(true_negative/humans)*math.log2(true_negative/humans)) - ((false_negative/humans)*math.log2(false_negative/humans))) + (bots/total)*((-(true_positive/bots)*math.log2(true_positive/bots)) - ((false_positive/bots)*math.log2(false_positive/bots))))
    except ZeroDivisionError:
        information_gain = 0
    return information_gain

#Function that uses info_gain to calculate the information gain of a feature
def calculate_information_gain(classification_file, rule_set,rule_number):
    df_classification = pandas.read_csv(classification_file)
    output_list = df_classification['output'].values
    classification_list = df_classification['class'].values
    information_gain = info_gain.info_gain(classification_list, output_list)
    return information_gain

#Function that uses info_gain to calculate the information gain * of a feature
def calculate_information_gain_star(dataset, classification_file, rule_set, rule_number):
    if 'users' in dataset:
        df_dataset = pandas.read_csv(dataset)
        attribute = rules.attributes(rule_set,rule_number)
        #if isinstance(attribute,list):
        attribute_list = []
        attrs = df_dataset[attribute].values
        for attr in attrs:
            rule_output = rules.rules(rule_set, rule_number, attr)
            if rule_output == 1:
                number_satisfied = 1
            else:
                number_satisfied = 0
            attribute_list.append(number_satisfied)
            
        #else:
         #   attribute_list = df_dataset[attribute].values
        df_classification = pandas.read_csv(classification_file)
        classification_list = df_classification['class'].values
        print(classification_list)
        print(attribute_list)
        information_gain_star = info_gain.info_gain(classification_list, attribute_list)
    else:
        attribute = rules.attributes(rule_set, rule_number)
        df_dataset = pandas.read_csv(dataset)
        user_id_list = list(set(df_dataset['user_id'].values))
        df_classification = pandas.read_csv(classification_file)
        attr_values = []
        real_classes = []
        for user_id in user_id_list:
            df_user = df_dataset.loc[df_dataset['user_id'] == user_id]
            attribute_list = df_user[attribute].values
            attribute_value = attribute_list[0]
            number_satisfied = 0
            if rule_number == 22:
                number_satisfied = len(df_user[attribute].unique())
            elif rule_number == 3 and rule_set == 'social_bakers':
                number_satisfied = df_user[attribute].value_counts().max()
            else:
                for attr in attribute_list:
                    rule_output = rules.rules(rule_set, rule_number, attr)
                    if rule_output == 1:
                        number_satisfied += 1
            attr_values.append(number_satisfied)
            df_class = df_classification.loc[df_classification['id'] == user_id]
            real_class = df_class['class'].values[0]
            real_classes.append(real_class)
        information_gain_star = info_gain.info_gain(real_classes, attr_values)
        
    return information_gain_star

#Function that uses corr of pandas DataFrame to calculate the pearson correlation coefficient
def calculate_pearson_correlation_coefficient(classification_file):
    df_csv = pandas.read_csv(classification_file)
    df_rule_class = df_csv.filter(['output','class'], axis=1)
    pearson_correlation_coefficient = df_rule_class.corr(method='pearson')
    return pearson_correlation_coefficient

#Function that uses corr of pandas DataFrame to calculate the pearson correlation coefficient *
def calculate_pearson_correlation_coefficient_star(bas_dataset, classification_file, rule_set, rule_number):
    if 'users' in bas_dataset and ((rule_number in [2,3,4,9] and rule_set == 'camsani_calzolari') or (rule_number in [1,4] and rule_set == 'van_den_beld')):
        #print('IF')
        attribute = rules.attributes(rule_set, rule_number)
        df_dataset = pandas.read_csv(bas_dataset)
        attribute_list = df_dataset[attribute].values
        attr_values = []
        for attr in attribute_list:
            if rule_number == 4:
                rule_output = rules.rules(rule_set, rule_number, [attr, df_dataset[attribute]])
            else:
                rule_output = rules.rules(rule_set, rule_number, attr)
            if rule_output == 1:
                number_satisfied = 1
            else:
                number_satisfied = 0
            attr_values.append(number_satisfied) 
        df_attr = pandas.DataFrame(attr_values, columns =[attribute])
        df_classification = pandas.read_csv(classification_file)
        df_class = df_classification['class']
        df_pcc_star = pandas.concat([df_attr, df_class], axis=1)
        pearson_correlation_coefficient_star = df_pcc_star.corr(method='pearson')
    elif 'users' in bas_dataset:
        attribute = rules.attributes(rule_set, rule_number)
        df_dataset = pandas.read_csv(bas_dataset)
        df_attribute = df_dataset[attribute]
        #print(df_attribute)
        df_numerical_attribute = df_attribute.fillna(0)
        #df_numerical_attribute = df_numerical_attribute.astype(int)
        df_classification = pandas.read_csv(classification_file)
        df_class = df_classification['class']
        df_pcc_star = pandas.concat([df_numerical_attribute, df_class], axis=1)
        pearson_correlation_coefficient_star = df_pcc_star.corr(method='pearson')
    
        
    else:
        print(rule_set)
        print(rule_number)
        attribute = rules.attributes(rule_set, rule_number)
        df_dataset = pandas.read_csv(bas_dataset)
        user_id_list = list(set(df_dataset['user_id'].values))
        df_classification = pandas.read_csv(classification_file)
        attr_values = []
        real_classes = []
        for user_id in user_id_list:
            df_user = df_dataset.loc[df_dataset['user_id'] == user_id]
            attribute_list = df_user[attribute].values
            attribute_value = attribute_list[0]
            number_satisfied = 0
            if rule_number == 22:
                number_satisfied = len(df_user[attribute].unique())
            elif rule_number == 3 and rule_set == 'social_bakers':
                number_satisfied = df_user[attribute].value_counts().max()
            else:
                for attr in attribute_list:
                    rule_output = rules.rules(rule_set, rule_number, attr)
                    if rule_output == 1:
                        number_satisfied += 1
            attr_values.append(number_satisfied) 
            df_class = df_classification.loc[df_classification['id'] == user_id]
            real_class = df_class['class'].values
            real_classes.append(real_class)
                
        df_attr = pandas.DataFrame(attr_values, columns =[attribute])
        df_cl = pandas.DataFrame(real_classes, columns =['class'])
        df_pcc_star = pandas.concat([df_attr, df_cl], axis=1)
        pearson_correlation_coefficient_star = df_pcc_star.corr(method='pearson')
            
    return pearson_correlation_coefficient_star


def main():
    dataset = home_directory + '/git/ICYBM121-p1/code'
    file_name = sys.argv[1]
    kind_dataset = sys.argv[2]
    rule_number = int(sys.argv[3])
    rule_set = sys.argv[4]
    if 'cc' in rule_set:
        rule_set = 'camisani_calzolari'
    elif 'sb' in rule_set:
        rule_set = 'social_bakers'
    elif 'vdb' in rule_set:
        rule_set = 'van_den_beld'
    print(rule_number)
    if kind_dataset == 'u':
        bas_dataset = dataset + '/' + 'bas_users.csv'
    elif kind_dataset == 't':
        bas_dataset = dataset + '/' + 'bas_tweets.csv'
    classification_file = home_directory + '/git/ICYBM121-p1/social_media_results/' + file_name
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
    information_gain_manual = calculate_information_gain_manual(tp, tn, fp, fn)
    print("INFORMATION GAIN MANUAL")
    print(information_gain_manual)
    information_gain = calculate_information_gain(classification_file, rule_set, rule_number)
    print("INFORMATION GAIN")
    print(information_gain)
    information_gain_star = calculate_information_gain_star(bas_dataset, classification_file, rule_set, rule_number)
    print("INFORMATION GAIN STAR")
    print(information_gain_star)
    pearson_correlation_coefficient = calculate_pearson_correlation_coefficient(classification_file)
    print("PEARSON CORRELATION COEFFICIENT")
    print(pearson_correlation_coefficient)
    pearson_correlation_coefficient_star = calculate_pearson_correlation_coefficient_star(bas_dataset, classification_file, rule_set, rule_number)
    print("PEARSON CORRELATION COEFFICIENT STAR")
    print(pearson_correlation_coefficient_star)
    
    


if __name__ == "__main__":
    main()
