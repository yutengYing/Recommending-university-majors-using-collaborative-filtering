# coding = utf-8

# 基于项目的协同过滤推荐算法实现
import random

import math
from operator import itemgetter


class ItemBasedCF():
    # 初始化参数
    def __init__(self):
        # 找到相似的20个用户，为目标用户推荐10个专业
        self.n_sim_major = 20
        self.n_rec_major = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.major_sim_matrix = {}
        self.major_popular = {}
        self.major_count = 0

        print('Similar major number = %d' % self.n_sim_major)
        print('Recommneded major number = %d' % self.n_rec_major)

    # 读文件得到“用户-专业”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, info1, info2, rating, major = line.split(',')
            if (random.random() < pivot):
                self.trainSet.setdefault(user, {})
                self.trainSet[user][major] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][major] = rating
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 计算专业之间的相似度
    def calc_major_sim(self):
        for user, majors in self.trainSet.items():
            for major in majors:
                if major not in self.major_popular:
                    self.major_popular[major] = 0
                self.major_popular[major] += 1

        self.major_count = len(self.major_popular)
        print("Total major number = %d" % self.major_count)

        for user, majors in self.trainSet.items():
            for m1 in majors:
                for m2 in majors:
                    if m1 == m2:
                        continue
                    self.major_sim_matrix.setdefault(m1, {})
                    self.major_sim_matrix[m1].setdefault(m2, 0)
                    self.major_sim_matrix[m1][m2] += 1
        print("Build co-rated users matrix success!")

        # 计算专业之间的相似性
        print("Calculating major similarity matrix ...")
        for m1, related_majors in self.major_sim_matrix.items():
            for m2, count in related_majors.items():
                if self.major_popular[m1] == 0 or self.major_popular[m2] == 0:
                    self.major_sim_matrix[m1][m2] = 0
                else:
                    self.major_sim_matrix[m1][m2] = count / math.sqrt(self.major_popular[m1] * self.major_popular[m2])
        print('Calculate major similarity matrix success!')

    # 针对目标用户U，找到K个相似的专业，并推荐其N个专业
    def recommend(self, user):
        K = self.n_sim_major
        N = self.n_rec_major
        rank = {}
        watched_majors = self.trainSet[user]

        for major, rating in watched_majors.items():
            for related_major, w in sorted(self.major_sim_matrix[major].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_major in watched_majors:
                    continue
                rank.setdefault(related_major, 0)
                rank[related_major] += w * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print('Evaluating start ...')
        N = self.n_rec_major
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_majors = set()

        for i, user in enumerate(self.trainSet):
            test_moives = self.testSet.get(user, {})
            rec_majors = self.recommend(user)
            for major, w in rec_majors:
                if major in test_moives:
                    hit += 1
                all_rec_majors.add(major)
            rec_count += N
            test_count += len(test_moives)

        print('产生推荐的物品id', rec_majors)


if __name__ == '__main__':
    rating_file = 'C:\\Users\\朝潮厨\\Desktop\\ratings2.csv'
    itemCF = ItemBasedCF()
    itemCF.get_dataset(rating_file)
    itemCF.calc_major_sim()
    itemCF.evaluate()
