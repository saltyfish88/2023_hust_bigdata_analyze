"""
完成这些后，即可由寄件人和收件人为节点构造有向图，
不考虑重复边，编写pagerank算法的代码，
根据每个节点的入度计算其pagerank值，迭代直到误差小于10-8
"""

import csv  # 用于读写csv文件
import numpy as np
import networkx as nx  # 用于构建图可以方便处理复杂的图网络结构

# 读取csv文件，每一行有三个数字，第一行表头不读取
# 第一个数字为序号，第二个数字为发送邮件的id，第三个数字为接收邮件的id
with open('sent_receive.csv', 'r') as file:
    reader = csv.reader(file)
    # 跳过文件头
    next(reader)
    # 只保留第二列和第三列，作为有向图的边
    edges = [(int(row[1]), int(row[2])) for row in reader]
# 构建有向图
graph = nx.DiGraph()  # 创建有向图
graph.add_edges_from(edges)  # 将边添加到有向图中

# print(len(graph))

alpha = 0.85

# 构建邻接矩阵
number = len(graph)  # 结点数目
adj_mtx = nx.adjacency_matrix(graph).todense()  # 转换为密集矩阵
neigh_matrix = np.asarray(adj_mtx)  # numpy数组方便处理
print(neigh_matrix)
print("\n\n\n\n\n")
# 统计每列的1的数量
col_sum = np.sum(neigh_matrix, axis=0)
m_matrix = np.divide(neigh_matrix, col_sum, where=col_sum != 0)
# 初始化r0
initial_matrix_r0 = np.full((number, 1), 1 / number)
compare_matrix_r = initial_matrix_r0
while True:
    cal_matrix_r = alpha * np.dot(m_matrix, compare_matrix_r) + (1 - alpha) * initial_matrix_r0
    if abs(np.linalg.norm(cal_matrix_r) - np.linalg.norm(compare_matrix_r)) < alpha:
        break
    compare_matrix_r = cal_matrix_r
print(cal_matrix_r)
print("\n\n\n\n\n")
sorted_indices = np.argsort(cal_matrix_r.flatten())[::-1]
# 按照排序结果输出 ID 和对应的矩阵中的数
for i in sorted_indices:
    page_id = i + 1  # 矩阵中的索引从 0 开始，而 ID 从 1 开始
    page_rank = cal_matrix_r[i]
    print(f"ID: {page_id}, PageRank: {page_rank}")
