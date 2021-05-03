from UseSqlite import InsertQuery, RiskQuery
from src import bookmark_analysis


class Applicant:
    def __init__(self, scores, bookmark_file):
        self.scores = scores
        self.bookmark_file = bookmark_file


class MajorRecommender:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def recommend_for(self):
        pass

    def calc_user_sim(self, bookmark_file):
        rq = RiskQuery(self)
        rq.instructions('SELECT ID,bookmark_file FROM applicant WHERE bookmark_file IS NOT NULL')
        rq.do()
        applicant_result = rq.format_results()

        rq = RiskQuery(self)
        rq.instructions('SELECT applicantID,schoolId,majorId,bookmark_file '
                        'FROM admission '
                        'WHERE bookmark_file IS NOT NULL')
        rq.do()
        admission_result = rq.format_results()

        # 将字符串分割成元组，算出书签相似度后添加入元组，再将元组存入列表
        list_of_tuple = []
        for item in admission_result:
            result = tuple(item.split(','))
            # print(result)
            similarity = [str(bookmark_analysis.like_distance(str(result[3]), bookmark_file))]
            result += tuple(similarity)
            # print(result)
            list_of_tuple.append(result)
        # print(list_of_tuple)
        # 按相似度从大到小排序
        list_of_tuple.sort(key=lambda x: x[4], reverse=True)
        # print(list_of_tuple)
        print("{0:<25}{1:<10}{2:<10}{3:>10}".format('ID', 'schoolID', 'majorID', 'similarity'))
        for i in range(len(list_of_tuple)):
            admission_id, schoolID, majorID, bookmarkMD, user_sim = list_of_tuple[i]
            print("{0:<25}{1:<10}{2:<10}{3:>10}".format(admission_id, schoolID, majorID, user_sim))

        '''rq = RiskQuery(self)
        rq.instructions('SELECT applicantID,bookmark_file FROM admission WHERE bookmark_file IS NOT NULL')
        rq.do()
        admission_result = rq.format_results()

        # 将取出的用逗号隔开的字符串转化为字典格式
        dic = list_to_dic(admission_result)
        print(dic)
        # 将传入的书签和字典里的所有值进行计算得出相似度并重新赋给对应的键（id）
        for item in dic:
            print(item)
            print(dic[item])
            dic[item] = bookmark_analysis.like_distance(dic[item], bookmark_file)
        # 按相似度从大到小排序
        dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        print(dic)
        for i in range(len(dic)):
            admission_id, user_sim = dic[i]
            print("{0:<25}{1:>5}".format(admission_id, user_sim))
        print("{0:<25}{1:>5}".format('ID', 'similarity'))'''
        return True


def list_to_dic(results):
    list_of_result = []
    for result in results:
        # print(result)
        # print((result[0: result.rfind(',')], result[result.rfind(',') + 1:]))
        tuple_of_result = (result[0: result.rfind(',')], result[result.rfind(',') + 1:])
        list_of_result.append(tuple_of_result)
    # print(list_of_result)
    # print(dict(list_of_result))
    return dict(list_of_result)


if __name__ == '__main__':
    # read_browse_history()
    MajorRecommender.calc_user_sim('data.db', '../resource/书签/书签地球_1618830145650.md')
    # print(bookmark_analysis.like_distance('../resource/书签/书签地球_1618830145650.md','../resource/书签/书签地球_1618112020822.md'))
