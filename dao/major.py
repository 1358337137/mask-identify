from dao.base import *
from dao.institute import updateInstituteMajorNum

engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db", isolation_level="READ UNCOMMITTED")
session = sessionmaker(engine)()  # 实例化session


# 查询所有 Major,
def showAllMajor():
    session.commit()
    res = session.query(Major).all()
    result = []
    for item in res:
        result.append(item.to_json())
    session.close()
    return result


# 根据id查询专业信息
def queryMajorInfo(major_id):
    session.commit()
    res = session.query(Major).filter(Major.major_id == major_id).one()
    result = res.to_json()

    session.close()
    return result


# 根据专业查询 学院信息
def queryInstituteInfo_by_majorid(major_id):
    session.commit()

    try:
        majorInfo = queryMajorInfo(major_id)
        Institute_id = majorInfo['Institute_id']
    except Exception as e:
        print(e)
        print('没有查找到学院id')
    res = session.query(Major).filter(Major.major_id == major_id).one()
    result = res.to_json()
    session.close()
    return result


# 当学生增加或者删除时，更新Major_student_id
def updateMajorStuentnum(major_id, flag):
    '''
    :param major_id: 专业id
    :param flag: True：增加学生 ；False：删除学生
    :return: 更新专业学生人数
    '''
    session.commit()
    if flag:
        print('增加major_num')
        session.query(Major).filter(Major.major_id == major_id).update(
            {
                "student_num": (Major.student_num + 1),
            })
    else:
        print('减少major_num')
        session.query(Major).filter(Major.major_id == major_id).update(
            {
                "student_num": (Major.student_num - 1),
            })
    session.commit()
    session.close()


# 传的student_id 必须是int，不然在下面在修改貌似会报错
def updateMajorInfo(major_id, info):
    # 查询Student dao.base.Student
    print(f'info:{info}')

    res = session.query(Major).filter(Major.major_id == major_id).update(
        {
            "major_name": info.get('major_name'),
            'profile': info.get('profile'),
        })
    print(f'res:{res}')
    session.commit()
    session.close()




def addMajorInfo(info):
    student_num = 0  # 添加默认学生个数为0
    major = Major(
        major_name=info.get('major_name'),
        profile=info.get('profile'),
        institute_id=info.get('institute_id'),
        student_num=student_num
    )
    session.add(major)
    session.commit()
    session.close()

    # info['institute_id']
    updateInstituteMajorNum(info.get('institute_id'), True)


def deleteMajorInfo(major_id):
    session.commit()
    # 检查是否有该专业有学生，如果有，则返回
    # try:
    #     flag = session.query(Student).filter(Student.major_id == major_id).one()
    #     raise Exception
    # except Exception as e:
    #
    # print(f'flag={flag}')
    # print(type(flag))
    # print('继续执行')
    major_info = queryMajorInfo(major_id)

    print(major_info)
    session.query(Major).filter(Major.major_id == major_id).delete()
    session.commit()
    session.close()

    Institute_id=major_info.get('institute_id')
    # print(type(Institute_id))
    updateInstituteMajorNum(Institute_id, False)




if __name__ == "__main__":
    # deleteMajorInfo(11)
    showAllMajor()
    pass
