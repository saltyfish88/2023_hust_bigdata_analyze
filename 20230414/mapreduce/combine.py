"""
第三步处理

Combine步骤可以用来减少中间键值对的数量。它在Map节点上对Map函数的输出进行本地聚合，
将相同键的值相加，然后将聚合后的结果输出到Reducer。
这样，可以减少网络传输和Reducer的负担，提高程序的性能。
"""
import time

time_start = time.time()
map_filenames = {"map01", "map02", "map03", "map04", "map05", "map06", "map07", "map08", "map09"}

for map_filename in map_filenames:
    words = {}
    with open(map_filename, "r") as f:
        for line in f:
            word, count = line.strip().split(',')
            count = int(count)
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
    output_file = map_filename.replace("map", "combine")

    with open(output_file, "w") as op:
        for word, words[word] in words.items():
            # 将键和计数值格式化为一个字符串，并写入文件
            op.write('{0},{1}\n'.format(word, words[word]))

time_end = time.time()
time_sum = time_end - time_start
print("combine.py文件运行时间为" + str(time_sum) + "s")