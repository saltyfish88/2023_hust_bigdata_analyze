from PIL import Image
import numpy as np


def compare_point_clouds(image_path1, image_path2, color_similarity_threshold=100):
    """
    比较两个二维点云的相似度
    :param image_path1: 第一张图片的文件名
    :param image_path2: 第二张图片的文件名
    :param color_similarity_threshold: 颜色相似度阈值，默认为 30（范围是0-255）
    :return: 返回两个点云的相似度
    """
    img1 = Image.open(image_path1).convert('RGB')
    img2 = Image.open(image_path2).convert('RGB')
    # 如果图片大小不同，调整图片大小为相同
    size = (max(img1.width, img2.width), max(img1.height, img2.height))
    img1 = img1.resize(size)
    img2 = img2.resize(size)
    pixels1 = np.array(img1.getdata())
    pixels2 = np.array(img2.getdata())
    # 计算两张图片中不同像素点之间的颜色差异
    color_diff = np.sum(np.abs(pixels1 - pixels2), axis=1)
    # 如果颜色差异值小于阈值，则认为它们是相同的点。否则它们代表的是不同的点。
    similarity = np.sum(color_diff < color_similarity_threshold) / color_diff.size
    return similarity


similarity = compare_point_clouds('answer1.png', 'answer2.png')
print('图片相似度为：', similarity)
