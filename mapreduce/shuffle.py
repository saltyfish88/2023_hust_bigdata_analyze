"""
第二步处理
Shuffle（分组）操作是指在 Map 阶段之后，将 Map 输出的键值对（key-value pairs）根据 Key 进行分组，
将相同 Key 的所有键值对分配到同一个 Reduce Task 中进行归约处理的过程。

对map01~09的文件每个readline，将键值对中的key进行hash（）然后%3再+1可以得出它应该啊被分配到的reduce结点序号
例如：apple,1
file_number = hash(apple) % 3 + 1
将apple,1写入shuffle_file_number文件中
output_filename = "source{:02d}".format(file_number)
"""
import os
import time

# 当需要同时写入大量数据时，频繁地打开和关闭文件会降低程序效率。
# 可以将所有的文件操作放到一个上下文管理器中，
# 同时将每个文件的输出流缓存起来，统一处理写入操作。改进速度很快！

time_start = time.time()

# 清除上一次运行后的结果以免和a模式打开文件出现冲突
delete_filenames = {"shuffle01", "shuffle02", "shuffle03"}
for delete_filename in delete_filenames:
    if os.path.exists(delete_filename):
        os.remove(delete_filename)

# 打开输入文件
combine_files = {"combine01", "combine02", "combine03", "combine04", "combine05", "combine06", "combine07", "combine08",
                 "combine09"}

# 打开输出文件，并将所有输出流缓存起来
output_files = {}
for i in range(1, 4):
    output_filename = "shuffle{:02d}".format(i)
    output_files[i] = open(output_filename, "a")

# 遍历所有输入文件
for combine_file in combine_files:
    with open(combine_file, "r") as f:
        # 遍历每一行
        for line in f:
            # 将每一行按照','分割成键值对
            word, count = line.strip().split(',')
            count = int(count)
            # 计算键的哈希值并分配到对应的文件
            file_idx = hash(word) % 3 + 1
            # 写入到对应的文件流缓存中
            output_files[file_idx].write(f"{word},{count}\n")

# 关闭所有输出流
for output_file in output_files.values():
    output_file.close()

time_end = time.time()
time_sum = time_end - time_start
print("shuffle.py运行时间为" + str(time_sum) + "s")
