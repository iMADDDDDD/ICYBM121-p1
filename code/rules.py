import math

def rules(ruleset, number, attribute):
    if ruleset == 'camisani_calzolari':
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
    return classification


def camisani_calzolari_rule_1(name):
    if name != '':
        classification = 'human'
    else:
        classification = 'bot'
    return classification


def camisani_calzolari_rule_2(default_profile_image):
    if isinstance(default_profile_image, float) and math.isnan(default_profile_image):
        classification = 'human'
    else:
        classification = 'bot'
    return classification

def camisani_calzolari_rule_3(location):
    if isinstance(location,float) and math.isnan(location):
        classification = 'bot'
    else:
        classification = 'human'
    return classification


def camisani_calzolari_rule_4(description):
    if isinstance(description,float) and math.isnan(description):
        classification = 'bot'
    else:
        classification = 'human'
    return classification


def camisani_calzolari_rule_5(followers_count):
    if int(followers_count) >= 30:
        classification = 'human
    else:
        classification = 'bot'
    return classification

def camisani_calzolari_rule_6(listed_count):
    if int(listed_count) > 0:
        classification = 'human'
    else:
        classification = 'bot'
    return classification


def camisani_calzolari_rule_7(statuses_count):
    if int(statuses_count) > 50:
        classification = 'human'
    else:
        classification = 'bot'
    return classification


def camisani_calzolari_rule_8(description):



