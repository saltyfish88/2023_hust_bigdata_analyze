import csv
from collections import Counter
import itertools

# data
num = 9835
min_support = 0.005
min_confidence = 0.5

# 两者都为列表类型
all_item_sets = []  # set type
items = set()
# 创建一个空的 Counter 对象
result = Counter()
with open('Groceries.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)  # Skip the header row
    for row in reader:
        items_in_row = row[1][1:-1].split(',')
        item_set = set([item.strip() for item in items_in_row])
        all_item_sets.append(item_set)
        items |= item_set
# 购物车清单列表包含集合
# print(all_item_sets)
# 一阶频繁项集
first_order_counter = Counter()
# 遍历集合b_set中的每个集合，更新Counter对象
for my_set in all_item_sets:
    # 创建一个空的 Counter 对象，用于统计该集合中每个字符串的出现次数
    inner_counter = Counter()
    for string in my_set:
        inner_counter[string] += 1
    # 将内层 Counter 对象合并到外层 Counter 对象中
    result += inner_counter
# 输出结果
second_single_items = []
for string, count in result.items():
    if count > (num * min_support):
        first_order_counter[string] = count
        second_single_items.append(string)
        # 符合条件的一阶频繁项集
        # print(string, count)
# 将符合条件的string存入
# print(second_single_items)
# -----------------end of first_order_counter-----------------

# -----------------start of second_order_counter-----------------
two_sub_sets = set(itertools.combinations(second_single_items, 2))  # element tuple type
# 一阶频繁项集的集合 2 子集
second_item_dict = {}
prepare_three_items_sets = []
for two_sub_tuple in two_sub_sets:
    prepare_for_three_set = set(two_sub_tuple)
    two_set = frozenset(two_sub_tuple)
    second_item_dict[two_set] = 0
    for all_item_set in all_item_sets:
        if two_set.issubset(all_item_set):
            second_item_dict[two_set] += 1
    #  将符合support的二阶输出
    if second_item_dict[two_set] > (num * min_support):
        prepare_three_items_sets.append(prepare_for_three_set)
        #print('{} has count {}'.format(two_set, second_item_dict[two_set]))

# print(prepare_three_items_sets)
# 将符合条件的二维集合备份准备后续的三维阶段，
# 一维保存为second_single_items列表类型
# print(second_item_dict)
# -----------------end of second_order_sets-----------------

# -----------------start of third_order_sets-----------------
three_items_sets = []
for two_items_x in prepare_three_items_sets:
    for two_items_y in prepare_three_items_sets:
        if two_items_x != two_items_y and two_items_x & two_items_y:
            three_items_set = two_items_x | two_items_y
            three_items_sets.append(three_items_set)
# print(three_items_sets)得到三阶项集准备判断和上面相同啊
# print(type(three_items_sets)) list类型数据
third_item_dict = {}
for three_items_set in three_items_sets:
    three_set = frozenset(three_items_set)
    third_item_dict[three_set] = 0
    for all_item_set in all_item_sets:
        if three_set.issubset(all_item_set):
            third_item_dict[three_set] += 1
    # if third_item_dict[three_set] > (num * min_support):
    # print('{} has count {}'.format(three_set, third_item_dict[three_set]))

# print(len(third_item_dict))
# 12267组项集
# -----------------end of third_order_sets-----------------

# -----------------start of two_items_set_confidence-----------------
# 遍历包含两个元素的集合列表
for two_items_set in prepare_three_items_sets:
    f_two_set = frozenset(two_items_set)
    # 从字典中获取包含这两个元素的二阶分子计数器
    molecule = second_item_dict[f_two_set]
    for one_item in two_items_set:  # string in set
        # 获取这个元素的一阶分母计数器
        denominator = first_order_counter[one_item]
        # 创建只包含这一个元素的集合
        one_item_set = {one_item}
        other_item_set = two_items_set - one_item_set
        if molecule / denominator > min_confidence:
            print(" ")
            #print("{} has confidence to {}".format(one_item_set, other_item_set))
# -----------------end of two_items_set_confidence-----------------

# -----------------start of three_items_set_confidence-----------------
for three_items_set in three_items_sets:
    f_three_set = frozenset(three_items_set)
    three_support = third_item_dict[f_three_set]
    for one_item in three_items_set:
        one_item_set = {one_item}
        one_support = first_order_counter[one_item]
        other_items_set = frozenset(three_items_set - one_item_set)
        two_support = second_item_dict[other_items_set]
        if one_support != 0 and three_support / one_support > min_confidence:
            print(" ")
            #print("{} has confidence to {}".format(one_item, other_items_set))
        if two_support != 0 and three_support / two_support > min_confidence:
            print(" ")
            #print("{} has confidence to {}".format(other_items_set, one_item))
# -----------------end of three_items_set_confidence-----------------

# -----------------start of print-----------------
#print(all_item_sets)
#print(items)
print(first_order_counter)
#print(second_item_dict)
#print(third_item_dict)
#print(three_items_sets)



# -----------------start of debug-----------------
"""
for two_subset in two_sub_tuples:
    print(type(two_subset))
    break
for all_item_set in all_item_sets:
    print(type(all_item_set))
    break
print(type(second_single_items))
"""
