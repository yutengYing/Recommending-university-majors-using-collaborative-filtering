from UseSqlite import InsertQuery, RiskQuery
import random
from random import choice, sample

FIXED_STAR_DICT = {'上海大学': 3, '北京师范大学': 4, '西南大学': 3, '西华大学': 2, '贵州大学': 3}
FIXED_SCORE_DICT = {'上海大学': 610, '西南大学': 630, '北京师范大学': 670, '贵州大学': 630}
FIXED_SALARY_DICT = {'上海大学': 5000, '北京师范大学': 6000, '西南大学': 5000, '西华大学': 4000, '贵州大学': 4000}


def get_star(s):
    if s in FIXED_STAR_DICT:
        return FIXED_STAR_DICT[s]

    if len(s) == 4 and '大学' in s:
        return 5

    return random.randint(1, 5)


# 最低分数线
def get_score(s):
    if s in FIXED_SCORE_DICT:
        return FIXED_SCORE_DICT[s]

    if len(s) == 4 and '大学' in s:
        return 700

    return random.randint(520, 730)


# 毕业平均薪资
def get_salary(s):
    if s in FIXED_SALARY_DICT:
        return FIXED_SALARY_DICT[s]

    if len(s) == 4 and '大学' in s:
        return 9000

    return random.randint(3000, 8000)


# 经纬度 https://blog.csdn.net/cold_long/article/details/102966505
def get_longitude_and_latitude(school_name):
    longitude = round(random.uniform(20, 46), 6)
    latitude = round(random.uniform(80, 130), 6)

    return longitude, latitude


# 产生申请者模拟考试数据
def get_test_info(applicant_id):
    list = ['高三语文模拟考', '高三数学模拟考', '高三英语模拟考', '高二语文模拟考', '高二数学模拟考', '高二英语模拟考']
    test = random.choice(list)

    return test


# 获取省份
def get_province_info(applicant_name):
    list = ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省',
            '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省']
    province = random.choice(list)

    return province


# 获取专业
def get_major_info(school_name):
    list = ['0101', '0201', '0301', '0401', '0702', '0809']
    major = random.choice(list)

    return major


# 生成浏览历史
def get_applicant_browse_history():
    lists = ['科幻=' + str(random.randint(1, 5)) + ' ' + '文学=' + str(random.randint(1, 5)) + ' ' + '游戏=' + str(
        random.randint(1, 5))]
    history = random.choice(lists)

    return history


# 生成入学时间
def get_addmission_date():
    date = random.randint(2014, 2018)

    return date


'''
#写入school表
f = open('university.txt', encoding='utf8')
lines = f.readlines()
count = 0
for line in lines:
  line = line.strip()
  if line.startswith('1'):
      school_lst = line.split('\t')
      for school in school_lst:
          school_id = school[0:5]
          school_name = school[5:]
        
            # insert into database
          iq = InsertQuery('data.db')
          sql_stmt = 'REPLACE INTO school Values (\'%s\', \'%s\', \'%s\', \'%s\', \'%d\')' % \
                     (school_id, school_name, get_longitude_and_latitude(school_name), 'None', get_star(school_name))
          #print(sql_stmt)
          iq.instructions(sql_stmt)
          iq.do()
          #print('%s\t%s' % (school_id, school_name))
          count += 1
'''

'''
#写入major表
f = open('university.txt', encoding='utf8')
lines_1 = f.readlines()
count = 0
for line_1 in lines_1:
    line_1 = line_1.strip()
    if line_1.startswith('1'):
        school_lst = line_1.split('\t')
        for school in school_lst:
            school_id = school[0:5]
            school_name = school[5:]
            fp = open('major_info.txt', encoding='utf8')
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('0'):
                    major_lst = line.split('\t')
                    for major in major_lst:
                        major_id = major[0:4]
                        major_name = major[4:]
                        
                        iq = InsertQuery('data.db')
                        sql_stmt = 'REPLACE INTO major VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                                   (major_id, major_name, school_id, get_star(school_name), get_score(school_name),
                                    'None', 'None', 'None', get_salary(school_name))
                        print(sql_stmt)
                        iq.instructions(sql_stmt)
                        iq.do()
                        fp.close()

    f.close()
'''

'''
#写入test表
f = open('applicant_info.txt', encoding='utf8')
lines = f.readlines()

for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
        test_score = get_test_info(applicant_id)
             # insert into database
        iq = InsertQuery('data.db')
        sql_stmt = 'INSERT INTO test Values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                       (applicant_id,applicant_name, test_score, test_score[4:], applicant_id[7:15],random.randint(80,150),'none')
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()

'''
'''
f = open('admission_applicant_info.txt', encoding='utf8')
lines = f.readlines()
for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
        test_score = get_test_info(applicant_id)
             # insert into database

        iq = InsertQuery('data.db')
        sql_stmt = 'INSERT INTO test Values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                       (applicant_id,applicant_name, test_score, test_score[4:], applicant_id[7:15],random.randint(80,150),'none')
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()
'''
# 写入考生信息
'''
f = open('applicant_info.txt', encoding='utf8')
lines = f.readlines()

for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
        gender = random.choice(['男性','女性'])
             # insert into database
        iq = InsertQuery('data.db')
        sql_stmt = 'REPLACE INTO applicant Values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                       (applicant_id,applicant_name, applicant_id[7:15], gender,get_longitude_and_latitude(applicant_name),get_province_info(applicant_name),'none','none','none','none',get_applicant_browse_history())
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()
        f.close
'''
'''
f = open('admission_applicant_info.txt', encoding='utf8')
lines = f.readlines()
for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
        gender = random.choice(['男性', '女性'])
             # insert into database

        iq = InsertQuery('data.db')
        sql_stmt = 'REPLACE INTO applicant Values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                   (applicant_id, applicant_name, applicant_id[7:15], gender, get_longitude_and_latitude(applicant_name),get_province_info(applicant_name), 'none', 'none', 'none', 'none', get_applicant_browse_history())
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()
 '''
# 写入录取者信息
'''
f = open('admission_applicant_info.txt', encoding='utf8')
lines = f.readlines()
for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
             # insert into database

        iq = InsertQuery('data.db')
        sql_stmt = 'REPLACE INTO admission Values (\'%s\',\'%s\',\'%s\',\'%s\')' % \
                       (applicant_id,'','',get_addmission_date())
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()
'''

# 写入评价者信息
'''
f = open('admission_applicant_info.txt', encoding='utf8')
lines = f.readlines()
for line in lines:
    line = line.strip()
    applicant_lst = line.split('\t')
    for applicant in applicant_lst:
        applicant_name = applicant[0:3]
        applicant_id = applicant[3:]
        list = ['北京大学在读', '浙江大学在读', '清华大学在读', '北京师范大学在读', '浙江师范大学在读', '复旦大学在读']
        describtion=random.choice(list)
             # insert into database
        iq = InsertQuery('data.db')
        sql_stmt = 'REPLACE INTO appraiser Values (\'%s\',\'%s\',\'%s\')' % \
                   (applicant_id, applicant_name, describtion)
        print(sql_stmt)
        iq.instructions(sql_stmt)
        iq.do()
'''
# 写入评价人对考生评价
'''
iq = InsertQuery('data.db')

sql_stmt1 = 'INSERT INTO appraisalForApplicant(applicantID) SELECT ID from applicant '
#print(sql_stmt)
iq.instructions(sql_stmt1)
iq.do()
'''
'''
iq = InsertQuery('data.db')

sql_stmt1 = 'INSERT INTO appraisalForApplicant(appraiserID) SELECT ID from appraiser where appraiser is not null '
#print(sql_stmt)
iq.instructions(sql_stmt1)
iq.do()


sql_stmt2 = 'UPDATE appraisalForApplicant set star=abs(random()%5 ) +1 WHERE star is not NULL '
iq.instructions(sql_stmt2)
iq.do()
'''

# 评价人对专业评价
'''
iq = InsertQuery('data.db')
sql_stmt1='INSERT INTO appraisalForMajor(appraiserID) select ID from appraiser'
print(sql_stmt)
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'REPLACE INTO appraisalForMajor(schoolID) select ID from school order by random() limit 48 '
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'REPLACE INTO appraisalForMajor(majorID) select ID from major order by random() limit 48 '
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'UPDATE appraisalForMajor set star=abs(random()%5 ) +1 WHERE star is  NULL'
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'UPDATE appraisalForMajor set star=abs(random()%5 )  WHERE star is not  null '
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'delete from appraisalForMajor where star = 1'
iq.instructions(sql_stmt)
iq.do()
'''

# 计算所有数据的，生成rating
'''
iq = InsertQuery('data.db')
sql_stmt = 'INSERT INTO ratings(applicantID) select ID from applicant'
iq.instructions(sql_stmt)
iq.do()
'''
'''
iq = InsertQuery('data.db')
sql_stmt = 'INSERT INTO ratings(applicantID,schoolID,majorID) select a.ID,b.schoolID,c.majorID from applicant as a,school as b,ceshi as c'
iq.instructions(sql_stmt)
iq.do()
'''
iq = InsertQuery('data.db')
sql_stmt = 'update ratings set schoolIDandmajorID=schoolid||majorID'
iq.instructions(sql_stmt)
iq.do()
print('写入数据库完成')
