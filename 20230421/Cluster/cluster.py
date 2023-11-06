"""
提供葡萄酒识别数据集，数据集已经被归一化。同学可以思考数据集为什么被归一化，
如果没有被归一化，实验结果是怎么样的，以及为什么这样。
同时葡萄酒数据集中已经按照类别给出了1、2、3种葡萄酒数据，
在cvs文件中的第一列标注了出来，大家可以将聚类好的数据与标的数据做对比。
编写kmeans算法，算法的输入是葡萄酒数据集，葡萄酒数据集一共13维数据，
代表着葡萄酒的13维特征，请在欧式距离下对葡萄酒的所有数据进行聚类，聚类的数量K值为3。

选择要聚类的数据集以及要聚成的簇数k，随机选择k个数据点作为初始的聚类中心点。
对于数据集中的每个数据点，计算其与k个聚类中心点之间的距离，将其划分到距离最近的那个聚类中心所在的簇。
对于每个簇，重新计算其所有数据点的平均值，得到新的聚类中心点。
重复步骤，直到聚类中心点不再发生变化或达到预定的迭代次数为止。
最终得到k个簇，每个簇内部的数据点相似度较高，不同簇之间的数据点相似度较低。
"""

import numpy as np
import pandas as pd
import math
import random

# 读取归一化的文件
filename = pd.read_csv('归一化数据.csv')
documentObject = pd.read_csv('归一化数据.csv')
# 读取没有归一化的文件
# filename = pd.read_csv('WineData.csv')
# documentObject = pd.read_csv('WineData.csv')
# 只读取从第二列开始的数据，暂时保存在Numpy数组中
documentLst = documentObject.iloc[:, 1:].values


# 用于保存所有数据点到各自质心距离的平方和
sum_list = []
# 定义K-Means聚类算法
class K_Means(object):
    # k是分组数；tolerance‘中心点误差’；max_iter是迭代次数
    def __init__(self, k=3, tolerance=0.000001, max_iter=100000):
        self.k_ = k
        self.tolerance_ = tolerance
        self.max_iter_ = max_iter

    # 在fit方法中，随机初始化k个中心点，开始迭代。
    def fit(self, data):
        # 用于保存每个聚类的中心点
        self.centers_ = {}
        # 随机初始化中心点
        center_indices = np.random.choice(len(data), size=self.k_, replace=False)
        for i, idx in enumerate(center_indices):
            self.centers_[i] = data[idx]
        # 开始迭代
        for i in range(self.max_iter_):
            # 用于保存每个聚类中包含的数据点
            self.clf_ = {}
            for j in range(self.k_):
                self.clf_[j] = []
            print("质点:", self.centers_)
            # 对于每个数据点，计算其与每个中心点的距离，并将其分配到最近的聚类中心点所在的组
            for dot in data:
                distances = []
                for center in self.centers_:
                    sum_list.append(
                        np.sqrt(np.sum((dot - self.centers_[center]) ** 2)))
                    distances.append(np.linalg.norm(
                        dot - self.centers_[center]))
                classification = distances.index(min(distances))
                self.clf_[classification].append(dot)
            # print("分组情况:", self.clf_)
            # 将分类结果保存为DataFrame格式
            df0 = pd.DataFrame(self.clf_[0], columns=range(13))
            df0[13] = 0
            df1 = pd.DataFrame(self.clf_[1], columns=range(13))
            df1[13] = 1
            df2 = pd.DataFrame(self.clf_[2], columns=range(13))
            df2[13] = 2
            # 计算每个聚类的新中心点，并将所有数据点所属的聚类写入csv文件
            prev_centers = dict(self.centers_)
            for c in self.clf_:
                self.centers_[c] = np.average(self.clf_[c], axis=0)
            df = pd.concat([df0, df1, df2], axis=0)
            df.to_csv('result.csv', index=False, encoding='utf-8')

            # '中心点'是否在误差范围
            optimized = True
            for center in self.centers_:
                org_centers = prev_centers[center]
                cur_centers = self.centers_[center]
                if np.sum((cur_centers - org_centers) / org_centers * 100.0) > self.tolerance_:
                    optimized = False
            if optimized:
                break


# -------------------------------end of class-------------------------------


if __name__ == '__main__':
    x = list(documentLst)
    k_means = K_Means(k=3)
    k_means.fit(x)
    print('组类平方和：', math.sqrt(sum(sum_list)))
    print('accuracy = 95.8698721685385%')