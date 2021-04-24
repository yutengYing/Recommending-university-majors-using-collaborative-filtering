# coding = utf-8

# 基于用户的协同过滤推荐算法实现
import random

import math
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的20个用户，为其推荐10个专业
        self.n_sim_user = 20
        self.n_rec_major = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.major_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommnededmajor number = %d' % self.n_rec_major)

    # 读文件得到“用户-专业”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, info1, info2, rating, major = line.split(',')
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][major] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][major] = rating
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“专业-用户”倒排索引
        print('Building major-user table ...')
        major_user = {}
        for user, majors in self.trainSet.items():
            for major in majors:
                if major not in major_user:
                    major_user[major] = set()
                major_user[major].add(user)
        print('Build major-user table success!')

        self.major_count = len(major_user)
        print('Total major number = %d' % self.major_count)

        print('Build user co-rated majors matrix ...')
        for major, users in major_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated majors matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')

    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_major
        rank = {}
        watched_majors = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for major in self.trainSet[v]:
                if major in watched_majors:
                    continue
                rank.setdefault(major, 0)
                rank[major] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_major
        hit = 0
        rec_count = 0
        test_count = 0
        all_rec_majors = set()

        for i, user, in enumerate(self.trainSet):
            test_majors = self.testSet.get(user, {})
            rec_majors = self.recommend(user)
            for major, w in rec_majors:
                if major in test_majors:
                    hit += 1
                all_rec_majors.add(major)
            rec_count += N
            test_count += len(test_majors)

        print('推荐的学校专业及推荐度', rec_majors)


if __name__ == '__main__':
    rating_file = 'C:\\Users\\朝潮厨\\Desktop\\ratings.csv'
    userCF = UserBasedCF()
    userCF.get_dataset(rating_file)
    userCF.calc_user_sim()
    userCF.evaluate()
