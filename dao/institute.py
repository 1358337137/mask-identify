from dao.base import *

engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db", isolation_level="READ UNCOMMITTED")
session = sessionmaker(engine)()  # 实例化session


# 查询所有学院信息
def showAllInstitute():
    session.commit()
    res = session.query(Institute).all()
    result = []
    for item in res:
        result.append(item.to_json())
    session.close()
    return result


# 根据id查询
def queryInstituteInfo(institute_id):
    session.commit()
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    res = session.query(Institute).filter(Institute.institute_id == institute_id).one()
    result = res.to_json()
    session.close()
    return result


# 传的student_id 必须是int，不然在下面在修改貌似会报错
# 只更改名称与简介
def updateInstituteInfo(institute_id, info):
    # 查询Student dao.base.Student
    print(institute_id)
    print(f'info:{info}')

    res = session.query(Institute).filter(Institute.institute_id == institute_id).update(
        {
            "institute_name": info.get('institute_name'),
            'profile': info.get('profile'),
        })
    print(f'res:{res}')
    session.commit()
    session.close()


# 更新查询的另一种方法，在原有的基础上更新数据
def updateInstituteMajorNum(institute_id, flag):
    '''
    add 与delete专业  ，更新num
    :param institute_id:
    :param flag: True 增加 Flase 减少
    :return:
    '''
    print(institute_id)
    if flag:
        session.query(Institute).filter(Institute.institute_id == institute_id).update({
            'major_num': (Institute.major_num + 1)
        })
        print('专业增加，所属学院的专业个数也发生变化！')
    else:
        session.query(Institute).filter(Institute.institute_id == institute_id).update({
            'major_num': (Institute.major_num - 1)
        })
        print('专业减少，所属学院的专业个数也发生变化！')
    session.commit()

    session.close()


def deleteInstituteInfo(institute_id):
    session.commit()
    session.query(Institute).filter(Institute.institute_id == institute_id).delete()
    session.commit()
    session.close()


# info ：json字符串信息
def addInstituteInfo(info):
    session.commit()
    # 添加学院默认为 0
    # major_num = queryMajorById()
    major_num = 0
    institute = Institute(
        institute_name=info.get('institute_name'),
        profile=info.get('profile'),
        major_num=major_num,
    )
    session.add(institute)
    session.commit()
    session.close()


if __name__ == '__main__':
    updateInstituteMajorNum(1)
