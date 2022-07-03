import pymysql
from sqlalchemy import create_engine  # sqlalchemy的引擎
from sqlalchemy.orm import sessionmaker  # 预配置范围的会话(session),代替connect执行数据库操作

from dao.base import *
from dao.major import updateMajorStuentnum

db = pymysql.connect(host="43.138.26.63", user='root', password='Key1999...', database='flask_db', port=3306,
                     cursorclass=pymysql.cursors.DictCursor, autocommit=True)
cursor = db.cursor()

engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db", isolation_level="READ UNCOMMITTED")
session = sessionmaker(engine)()  # 实例化session

# 查询所有student
def showAllStudent():
    session.commit()
    sql = 'SELECT * FROM student  LEFT JOIN major\
        on student.major_id=major.major_id\
        LEFT JOIN institute\
        on major.institute_id=institute.institute_id;'
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    print(len(result))
    # res = session.query(Student).all()
    # result = []
    # for item in res:
    #     result.append(item.to_json())
    # session.close()
    return result


# 根据id查询
def queryStudent(student_id):
    session.commit()
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    res = session.query(Student).filter(Student.student_id == student_id).one()
    result = res.to_json()
    print(result)

    session.close()
    return result


# 根据学生详细信息
def queryStudentDetail(student_id):
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    # res = session.query(Student).filter(Student.student_id == student_id).one()
    # result = res.to_json()
    # session.close()

    sql = 'SELECT * FROM student  LEFT JOIN major\
           on student.major_id=major.major_id\
           LEFT JOIN institute\
           on major.institute_id=institute.institute_id\
           WHERE student.student_id=' + str(student_id) + ';'
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    return result


# 根据学生姓名查询学生所有信息
def queryStudentID(name):
    session.commit()
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    res = session.query(Student).filter(Student.name == name).one()

    session.close()
    result = res.to_json()  # 转成字典形式
    return result


def queryStuentNum_by_majorid(major_id):
    session.commit()
    # 返回list ,注意测试 如果没有该id 返回什么
    res = session.query(Student).filter(Student.major_id == major_id).all()

    session.close()
    return len(res)


# 传的student_id 必须是int，不然在下面在修改貌似会报错
def updateStudentInfo(student_id, info):
    session.commit()
    # 查询Student dao.base.Student
    print(student_id)
    print(f'info:{info}')

    res = session.query(Student).filter(Student.student_id == student_id).update(
        {
            "name": info.get('name'),
            'student_number': info.get('student_number'),
            'student_phone': info.get('student_phone'),
            'teacher': info.get('teacher'),
            'teacher_phone': info.get('teacher_phone')
        })
    print(f'res:{res}')
    session.commit()
    session.close()


# info ：json字符串信息
def addStudentInfo(info):
    # try:
    #     institute_id = queryMajorInfo(major_id)['institute_id']
    # except Exception as e:
    #     print(e)
    student = Student(
        name=info.get('name'),
        student_number=info.get('student_number'),
        student_phone=info.get('student_phone'),
        teacher=info.get('teacher'),
        teacher_phone=info.get('teacher_phone'),
        major_id=info.get('major_id'),
        institute_id=info.get('institute_id')
    )
    session.add(student)
    session.commit()
    session.close()
    # 更新专业中学生人数
    updateMajorStuentnum(info.get('major_id'), True)


def deleteStudentInfo(student_id):
    session.commit()
    student_info = queryStudent(student_id)
    print(f'即将要删除的student_id：{student_id}')
    # 这会把所在的student_id 都删去
    session.query(Student).filter(Student.student_id == student_id).delete()
    session.commit()
    session.close()
    updateMajorStuentnum(student_info.get('major_id'), False)


# 根据id查询
def queryjoin_student_(student_id):
    session.commit()
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    res = session.query(Student).filter(Student.student_id == student_id).one()
    result = res.to_json()
    session.close()
    return result


if __name__ == "__main__":
    queryStudentDetail(1)
    pass
