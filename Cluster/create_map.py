"""
还需要根据分类，给不同类的点进行不同颜色的标注，并且还要展示三个聚类的中心点
"""

import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('result.csv')

# 提取需要的两列数据
x = df.iloc[:, 8]
y = df.iloc[:, 6]
colors = ['blue' if c == 0 else 'red' if c == 1 else 'yellow' for c in df.iloc[:, 13]]

# 绘制点图
plt.scatter(x, y, color=colors)
plt.show()
plt.savefig('output3.png')
