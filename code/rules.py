import math

#Classification equals 0 (human) or 1 (bot)

def rules(rule_set, number, attribute):
    if rule_set == 'camisani_calzolari':
        if number == 1:
            classification = camisani_calzolari_rule_1(attribute)
        elif number == 2:
            classification = camisani_calzolari_rule_2(attribute)
        elif number == 3:
            classification = camisani_calzolari_rule_3(attribute)
        elif number == 4:
            classification = camisani_calzolari_rule_4(attribute)
        elif number == 5:
            classification = camisani_calzolari_rule_5(attribute)
        elif number == 6:
            classification = camisani_calzolari_rule_6(attribute)
        elif number == 7:
            classification = camisani_calzolari_rule_7(attribute)
        elif number == 9:
            classification = camisani_calzolari_rule_9(attribute)
        elif number == 19:
            classification = camisani_calzolari_rule_19(attribute[0], attribute[1])
    return classification

def attributes(rule_set, rule_number):
    if rule_set == 'camisani_calzolari':
        if rule_number == 1:
            attribute = 'name'
        elif rule_number == 2:
            attribute = 'default_profile_image'
        elif rule_number == 3:
            attribute = 'location'
    return attribute

def camisani_calzolari_rule_1(name):
    if name != '':
        classification = 0
    else:
        classification = 1
    return classification


def camisani_calzolari_rule_2(default_profile_image):
    if isinstance(default_profile_image, float) and math.isnan(default_profile_image):
        classification = 0
    else:
        classification = 1
    return classification

def camisani_calzolari_rule_3(location):
    if isinstance(location,float) and math.isnan(location):
        classification = 1
    else:
        classification = 0
    return classification


def camisani_calzolari_rule_4(description):
    if isinstance(description,float) and math.isnan(description):
        classification = 1
    else:
        classification = 0
    return classification


def camisani_calzolari_rule_5(followers_count):
    if int(followers_count) >= 30:
        classification = 0
    else:
        classification = 1
    return classification

def camisani_calzolari_rule_6(listed_count):
    if int(listed_count) > 0:
        classification = 0
    else:
        classification = 1
    return classification


def camisani_calzolari_rule_7(statuses_count):
    if int(statuses_count) > 50:
        classification = 0
    else:
        classification = 1
    return classification

def camisani_calzolari_rule_8(geo):
    if isinstance(geo,float) and math.isnan(geo):
        classification = 1
    else:
        classification = 0
    return classification

def camisani_calzolari_rule_9(url):
    if isinstance(url,float) and math.isnan(url):
        classification = 1
    else:
        classification = 0
    return classification


def camisani_calzolari_rule_19(followers_count, friends_count):
    if (2*followers_count) >= (friends_count):
        classification = 0
    else:
        classification = 1
    return classification
            


