import math

def rules(ruleset, number, attribute):
    if ruleset == 'camisani_calzolari':
        if number == 1:
            camisani_calzolari_rule_1(attribute)
        elif number == 2:
            classification = camisani_calzolari_rule_2(attribute)
        elif number == 3:
            classification = camisani_calzolari_rule_3(attribute)
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


