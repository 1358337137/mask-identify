import datetime
import random
from datetime import datetime, timedelta
import os
from dao.base import *
import paramiko
from sqlalchemy import create_engine  # sqlalchemy的引擎
from sqlalchemy.orm import sessionmaker  # 预配置范围的会话(session),代替connect执行数据库操作

from dao.base import User

import pymysql

db = pymysql.connect(host="43.138.26.63", user='root', password='Key1999...', database='flask_db', port=3306,
                     cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

# 防止长时间 数据库池丢失链接
engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db", pool_recycle=3600,
                       pool_pre_ping=True, isolation_level="READ UNCOMMITTED")
session = sessionmaker(engine)()  # 实例化session


# ############# 执行ORM操作 #############
# 用户注册
def addUser(username, password):
    obj1 = User(username=username, password=password)
    session.add(obj1)
    # 提交事务
    session.commit()
    session.close()


# 登录验证
def login_validate(username, password):
    try:
        res = session.query(User).filter(User.username == username).one()
        result = res.to_json()
        # {'username': 'admin', 'password': '123456', 'id': 1}
        true_password = result.get('password')
        if true_password == password:
            return 1
        else:
            print("密码错误")
            return -1
    except Exception as e:
        print(e)
        return 0


def getTime():
    # 获取当前时间 ，类型为 datatime 2022-06-01 17:47:53.347511
    t1 = datetime.now()
    time1 = t1.strftime('%Y-%m-%d %H:%M:%S')  # 只取年月日，时分秒 ，转为 str
    return time1


# local_file是要上传的本地文件路径  eg:C:\Users\K\Desktop\video2image\2.png
# file_name 图片名称  eg: 2.png
# remote_path是要上传到服务器上指定文件的路径  需要加文件名
def upload(local_file):
    hostname = '43.138.26.63'
    username = 'root'
    password = 'Xs1358337137'
    port = 22  # 配置信息可以写到配置文件中
    remote_root = '/usr/local/nginx/html/mask/'  # 云服务器上的文件路径

    # file_name = time.time()
    # print(f'时间戳={file_name}')
    # os.path.basename 获取路径下的最后文件名
    remote_path = remote_root + os.path.basename(local_file)
    # remote_path = remote_root +str(file_name)+".png"
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('开始上传图片%s ' % datetime.now())

        try:
            sftp.put(local_file, remote_path)
        except Exception as e:
            sftp.mkdir(os.path.split(remote_path)[0])
            sftp.put(local_file, remote_path)
            print("从本地： %s 上传到： %s" % (local_file, remote_path))

        print('文件上传成功 %s ' % datetime.now())
        t.close()
    except Exception as e:
        print(repr(e))


# -------------------- mock 数据------------------------#
def fake_institute_data():
    # mysql 查询近7天的数据
    # sql = "select * from record  where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(create_time)"
    # try:
    #     cursor.execute(sql)
    #     list_res = cursor.fetchall()
    #     print(list_res)
    #     print(type(list_res))
    # except Exception as e:
    #     print(e)
    #     db.rollback()

    #     sqlAlchemy 查询方式
    # NOW = datetime.utcnow()
    # res = session.query(Record).filter(Record.create_time >= NOW - timedelta(days=7)).all()
    # list_res = []
    # for item in res:
    #     list_res.append(item.to_json())
    # print(list_res)
    # print(len(list_res))

    # 筛选日期，记录每天的次数
    # data_date = [0, 0, 0, 0, 0, 0, 0]
    # for item in list_res:
    #     t = item.get('create_time')
    #     today = datetime.strptime(t, "%Y-%m-%d %H:%M:%S").weekday()    # 根据时间，返回星期几，周一=0 周日=6 ，
    #     print(t)
    #     print(today)
    #     data_date[today] += 1
    # print(data_date)
    # data_date.append(data_date[0])  # 整体左移一个
    # data_date.pop(0)    # pop 默认出最后一个，param：index
    dict_data = {}
    list_name = ['计算机科学与技术学院', '海洋与空间信息学院', '石油工程学院', '化学化工学院', '石大新能源学院', '经济管理学院']
    for j in range(0, 6):

        list_num = []
        for i in range(0, 7):
            i = random.randint(100, 200)
            list_num.append(i)
        dict_data[list_name[j]] = list_num
    return dict_data


if __name__ == "__main__":
    # path2 = "D:\data\Beijing.png"
    # c = os.path.basename(path2)
    # print(c)
    # print(getTime())
    fake_institute_data()

    pass
