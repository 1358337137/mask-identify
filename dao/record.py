import os.path

from dao.base import *
from dao.student import queryStudentID
from dao.units import upload, getTime

engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db", isolation_level="READ UNCOMMITTED")
session = sessionmaker(engine)()  # 实例化session

# 查询所有student
def showAllRecord():
    session.commit()
    res = session.query(Record).all()
    result = []
    for item in res:
        result.append(item.to_json())
    print('record----')
    print(result)

    session.close()
    print('commt之后----')
    print(result)
    return result

# 根据id查询
def queryRecord(record_id):
    session.commit()
    # filter(Student.student_id==student_id).all() 返回的是list
    # one 返回的是字典
    res = session.query(Record).filter(Record.record_id == record_id).one()
    result = res.to_json()
    session.close()
    return result


# 添加记录信息
# param ：stuent_name 学生名字 ，local_file :图片的本地路径
# eg: stuent_name="肖森"   local_file= "C:\Users\K\Desktop\video2image\2.png"
def addRecordInfo(stuent_name, local_file):
    # 把本地图片上传到云服务器
    upload(local_file)

    try:
        student_all_info = queryStudentID(stuent_name)  # 查找学生信息
        print('在数据库中找到该学生信息')
        student_id = student_all_info['student_id']
        name = student_all_info['name']
        student_number = student_all_info['student_number']
    except Exception as e:
        student_id = 999
        name = "佚名"
        student_number = "99999"
        print('没有在数据库中找到学生信息，默认学生信息')

    record = Record(
        student_number=student_number,
        name=name,
        student_id=student_id,
        image_url='http://43.138.26.63/mask/'+os.path.basename(local_file),     # os.path.basename 获取路径最后的文件名
        create_time=getTime()
    )
    session.add(record)
    session.commit()
    session.close()

# 删除记录信息
def deleteRecordInfo(record_id):
    session.commit()
    print(f'即将要删除的记录id：{record_id}')
    # 这会把所在的student_id 都删去
    session.query(Record).filter(Record.record_id == record_id).delete()
    # student = session.query(Student).filter(student_id == student_id).first()
    # session.delete(student)
    session.commit()
    session.close()


if __name__ =='__main__':
    # addRecordInfo('肖森','ccc')
    # addRecordInfo('肖森', r"C:\Users\K\Desktop\video2image\5.png")
    # print(res)
    showAllRecord()