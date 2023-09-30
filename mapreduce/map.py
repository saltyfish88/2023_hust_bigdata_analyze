"""
第一步处理
将每个source文件中单词拆分成key,value的键值对，且只是拆分步骤，不进行统计，
例如: apple,banana,apple
apple,1
banana,1
apple,1
拆分处理后，存入文件map01~09.txt
"""
import time
import threading


def map_file(inputfile, outputfile):
    with open(inputfile, "r") as f1, open(outputfile, "w") as f2:
        for line in f1:
            words = line.strip().split(",")
            for word in words:
                f2.write(word.strip() + ",1\n")


time_start = time.time()

# 多线程处理
threads = []
for i in range(1, 10):
    input_filename = "source{:02d}".format(i)
    output_filename = "map{:02d}".format(i)
    t = threading.Thread(target=map_file, args=(input_filename, output_filename))
    threads.append(t)
    t.start()

# 判断是否结束
for t in threads:
    t.join()

time_end = time.time()
time_sum = time_end - time_start
print("map.py执行时间为" + str(time_sum) + "s")


