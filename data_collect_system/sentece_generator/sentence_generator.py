import numpy
import extract_attr
# main_attr: 重要的、有区分度的维度。
# other_attr: 不重要的维度，所有都是一样的维度。
# value_name: 变量的名字：如GDP的值。


def get_range_sentence(important_statistic, cat0_diff, cat1_diff):
    # print(important_statistic)
    value_name = "GDP"
    cat0_name = ["Africa","Banama","China","Dutch","England","France","Ganna","Holand","Ireland","Russia"]
    name = extract_attr.get_all_name(cat0_name, important_statistic["category0"])
    sentence = "the {} of {} ranges from {} to {}".format(value_name, name, important_statistic["quantity0"]["min"][0],important_statistic["quantity0"]["max"][0])
    return sentence


def get_maximum_sentence(important_statistic, cat0_diff, cat1_diff):
    value_name = "GDP"
    cat0_name = ["Africa","Banama","China","Dutch","England","France","Ganna","Holand","Ireland","Russia"]
    name = extract_attr.get_all_name(cat0_name, important_statistic["category0"])
    sentence = "the max {} of {} is {} billion from {}".format(value_name, name,important_statistic["quantity0"]["max"][0], cat0_name[important_statistic["quantity0"]["max"][1]])
    return sentence

def get_minimum_sentence(important_statistic, cat0_diff, cat1_diff):
    value_name = "GDP"
    cat0_name = ["Africa","Banama","China","Dutch","England","France","Ganna","Holand","Ireland","Russia"]
    name = extract_attr.get_all_name(cat0_name, important_statistic["category0"])
    sentence = "the min {} of {} is {} billion from {}".format(value_name, name,important_statistic["quantity0"]["min"][0], cat0_name[important_statistic["quantity0"]["min"][1]])
    return sentence

def get_compare_sentence(focal_statistic, compare_statistic, cat0_diff, cat1_diff):
    value_name = "GDP"
    cat0_name = ["Africa","Banama","China","Dutch","England","France","Ganna","Holand","Ireland","Russia"]
    name_focal = extract_attr.get_all_name(cat0_name, focal_statistic["category0"])
    name_compare = extract_attr.get_all_name(cat0_name, compare_statistic["category0"])
    focal_quantity = focal_statistic["quantity0"]
    compare_quantity = focal_statistic["quantity0"]
    sentence = []

    if (focal_quantity["min"][0] > compare_quantity["max"][0]):
        sentence.append("the GDP of {} is higher than that of {}".format(name_focal, name_compare))
    if (focal_quantity["max"][0] < compare_quantity['min'][0]):
        sentence.append("the GDP of {} is lower than that of {}".format(name_focal, name_compare))

    return sentence

def generate_sentence(focal_element, compare_element, important_element):
    focal_statistic = extract_attr.cal_attribute(focal_element)
    compare_statistic = extract_attr.cal_attribute(compare_element)
    important_statistic = extract_attr.cal_attribute(important_element)
    cat0_diff, cat1_diff = extract_attr.judge_diff_cat(focal_statistic, compare_statistic)
    print(get_range_sentence(important_statistic, cat0_diff, cat1_diff))
    print(get_maximum_sentence(important_statistic, cat0_diff, cat1_diff))
    print(get_minimum_sentence(important_statistic, cat0_diff, cat1_diff))
    compare_sentences = get_compare_sentence(focal_statistic, compare_statistic, cat0_diff, cat1_diff)

    for sentence in compare_sentences:
        print(sentence)
    # get_range_sentence(foca

def get_element_set():
    element_set = numpy.load("../spider/focal/0021.npy")
    element_full_information = numpy.load("../spider/svg_npy/0021.npy")
    # numbers =
    # print(element_set.shape)
    # print(element_full_information.shape)
    focal_element, compare_element, important_element = extract_attr.get_focal_compare_from_numpy(element_set, element_full_information)

    generate_sentence(focal_element, compare_element, important_element)
    # return focal_statistic, compare_statistic


# get_fake_data()
get_element_set()
