"""
最后一步
将combine01~03统计好的3个文件，采用多线程处理
最后将结果统计到reduce文件中
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def reduce(key_value_list):
    word_counts = key_value_list
    return sum(key_value_list)


def process_file(filename):
    with open(filename, "r") as fo:
        lines = fo.readlines()
    word_counts = {}
    for line in lines:
        keyword, word_value = line.strip().split(",")
        if keyword in word_counts:
            word_counts[keyword] += int(word_value)
        else:
            word_counts[keyword] = int(word_value)
    return word_counts


time_start = time.time()

input_filenames = {"combine01", "combine02", "combine03"}
output_filename = "reduceResult"
threads_number = 3

with ThreadPoolExecutor(max_workers=threads_number) as executor:
    tasks = []
    for input_filename in input_filenames:
        tasks.append(executor.submit(process_file, input_filename))
    results = []
    for future in as_completed(tasks):
        results.append(future.result())
    grouped_results = {}
    for result in results:
        for key, value in result.items():
            if key in grouped_results:
                grouped_results[key].append(value)
            else:
                grouped_results[key] = [value]

    # print(grouped_results)

    reduced_results = {}
    for key, value_list in grouped_results.items():
        reduced_results[key] = reduce(value_list)

    with open(output_filename, "w") as f:
        for key, value in reduced_results.items():
            f.write(f"{key},{value}\n")

time_end = time.time()
time_sum = time_end - time_start
print("reduce.py运行时间为" + str(time_sum) + "s")