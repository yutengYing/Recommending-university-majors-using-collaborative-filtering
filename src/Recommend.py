# Copyright (C) 2021 Yuteng Ying
from UseSqlite import RiskQuery
import bookmark_analysis


class Applicant:
    def __init__(self, scores, bookmark_file):
        self.scores = scores
        self.bookmark_file = bookmark_file


class MajorRecommender:
    def __init__(self):
        self.db_filename = 'static/data.db'

    def recommend_for(self, applicant=Applicant):
        scores = applicant.scores
        bookmark_file = applicant.bookmark_file

        rq = RiskQuery(self.db_filename)
        rq.instructions('SELECT appraiserID,school.ID,school.name,major.ID,major.name,'
                        'minimum_requirement,bookmark_file,appraisalForMajor.star '
                        'FROM major,appraisalForMajor,applicant,school '
                        'WHERE major.ID = appraisalForMajor.majorID '
                        'AND major.school_ID = appraisalForMajor.schoolID '
                        'AND appraisalForMajor.schoolID = school.ID '
                        'AND appraiserID = applicant.ID '
                        'AND bookmark_file IS NOT NULL ')
        rq.do()
        appraisal_result = rq.format_results()

        # 将字符串分割成元组，算出书签相似度后添加入元组，再将元组存入列表
        list_of_tuple = []
        for item in appraisal_result:
            result = tuple(item.split(','))
            # print(result)
            if result[5] > scores:
                continue
            else:
                # 计算相似度
                similarity = bookmark_analysis.like_distance(str(result[6]), bookmark_file)
                # 计算推荐度即相似度和评价的积
                tendency = [str(round(similarity * int(result[7]), 2))]
                result += tuple(tendency)
                list_of_tuple.append(result)

        # 按相似度从大到小排序
        list_of_tuple.sort(key=lambda x: x[8], reverse=True)
        # print(list_of_tuple)
        print("{0:<20}{1:<15}{2:<10}".format('School Name', 'Major Name', 'Recommendation Level'))
        for i in range(len(list_of_tuple)):
            appraiserID, schoolID, schoolName, majorID, majorName, minimumRequirement, bookmarkFile, star, tendency = list_of_tuple[i]
            print("{0:<20}{1:<15}{2:<10}".format(schoolName, majorName, tendency))
        return list_of_tuple


if __name__ == '__main__':
    applicant = Applicant('650', 'static/bookmark/书签地球_1618832316906.md')
    mr = MajorRecommender()
    mr.recommend_for(applicant)
    # print(bookmark_analysis.like_distance('static/bookmark/书签地球_1618830145650.md','static/bookmark/书签地球_1618112020822.md'))

