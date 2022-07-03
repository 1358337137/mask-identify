from flask import Flask, request, jsonify, json, Response
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy

import config
from dao.institute import *
from dao.major import *
from dao.student import *
from dao.record import *
from dao.units import *
from video import VideoCamera

app = Flask(__name__)

CORS(app, supports_credentials=True)  # 解决跨域问题
app.debug = True

app.config.from_object(config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)
session = sessionmaker(engine)()


# 定义路由，vue中的访问地址要和这里保持一致，设置访问方式
@app.route('/login', methods=['POST'])
def returns():
    print('后端收到登录验证请求')
    if request.method == 'POST':  # 判断访问方式，
        data = request.get_json(silent=True)
        print(data)
        username = data['username']
        password = data['password']
        res = login_validate(username, password)
        if res > 0:
            datas = {'username': username, 'password': password, 'msg': 1}  # 构造返回数据
            return jsonify(datas)
        else:
            datas = {'username': username, 'password': password, 'msg': 0}  # 构造返回数据
            return jsonify(datas)


# -------------------- 学生 --------------------

# 查询所有学生信息
@app.route('/show/student', methods=['GET'])
def showStudent():
    res_list = showAllStudent()
    return jsonify({'tableData': res_list})


@app.route('/query/student/<string:student_id>', methods=['GET'])
def queryStudentBy_id(student_id):
    '''
    返回student 的详细信息，包括专业与学院信息
    :param student_id:
    :return:
    '''
    # 如何进行异常处理
    try:
        result = queryStudentDetail(student_id)
        return jsonify({'data': result, "status": 200})
    except Exception as e:
        return jsonify({"data": e, "status": 400})


@app.route('/add/student', methods=['POST'])
def addStudent():
    # print(request)
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(data)
    try:
        addStudentInfo(data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/update/student/<string:student_id>', methods=['PUT'])
def updateStudent(student_id):
    print(request)
    print(student_id)
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(data)
    print(type(data))
    print(f'student_id的type{type(student_id)}')
    try:
        updateStudentInfo(int(student_id), data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/delete/student/<string:student_id>', methods=['DELETE'])
def deleteStudent(student_id):
    try:
        deleteStudentInfo(int(student_id))
        return jsonify({'msg': '删除成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


# -------------------- 违规记录 --------------------

# 查询所有违规记录
@app.route('/show/record', methods=['GET'])
def showRecord():
    res_list = showAllRecord()
    return jsonify({'tableData': res_list})


@app.route('/query/student/<string:record_id>', methods=['GET'])
def query_record_byid(record_id):
    # 如何进行异常处理
    try:
        result = queryRecord(record_id)
        return jsonify({'data': result, "status": 200})
    except Exception as e:
        return jsonify({"data": e, "status": 400})


@app.route('/delete/record/<string:record_id>', methods=['DELETE'])
def deleteRecord(record_id):
    try:
        deleteRecordInfo(int(record_id))
        return jsonify({'msg': '删除成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


# -------------------- 专业 --------------------#

@app.route('/show/major', methods=['GET'])
def showMajor():
    '''
    : 进行多表查询，遗留问题！！返回Institution 的名称
    :return:
    '''
    res_list = showAllMajor()
    return jsonify({'tableData': res_list})


@app.route('/add/major', methods=['POST'])
def addMajor():
    # print(request)
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(data)
    try:
        addMajorInfo(data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/query/major/<string:major_id>', methods=['GET'])
def queryMajor(major_id):
    # 如何进行异常处理
    try:
        result = queryMajorInfo(major_id)
        return jsonify({'data': result, "status": 200})
    except Exception as e:
        return jsonify({"data": e, "status": 400})


@app.route('/update/major/<string:major_id>', methods=['PUT'])
def updateMajor(major_id):
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(f'要更新的专业信息：{data}')
    try:
        updateMajorInfo(int(major_id), data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/delete/major/<string:major_id>', methods=['DELETE'])
def deleteMajor(major_id):
    print(f'要删除的major_Id{major_id}')
    try:
        deleteMajorInfo(int(major_id))
        return jsonify({'msg': '删除成功', 'status': 200})
    except Exception as e:
        print(e)
        return jsonify({'msg': e})


# -------------------- 学院--------------------#

@app.route('/show/institute', methods=['GET'])
def showInstitute():
    res_list = showAllInstitute()
    print(res_list)
    return jsonify({'tableData': res_list})


@app.route('/add/institute', methods=['POST'])
def addInstitute():
    # print(request)
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(data)
    try:
        addInstituteInfo(data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/query/institute/<string:institute_id>', methods=['GET'])
def queryInstitute(institute_id):
    # 如何进行异常处理
    try:
        result = queryInstituteInfo(institute_id)
        return jsonify({'data': result, "status": 200})
    except Exception as e:
        return jsonify({"data": e, "status": 400})


@app.route('/update/institute/<string:institute_id>', methods=['PUT'])
def updateInstitute(institute_id):
    # 将json格式转为字典
    data = json.loads(request.get_data())
    print(f'要更新的学院信息：{data}')
    try:
        updateInstituteInfo(int(institute_id), data)
        return jsonify({'msg': '更新成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})


@app.route('/delete/institute/<string:institute_id>', methods=['DELETE'])
def deleteInstitute(institute_id):
    try:
        deleteInstituteInfo(int(institute_id))
        return jsonify({'msg': '删除成功', 'status': 200})
    except Exception as e:
        return jsonify({'msg': e})




# ---------------Mock数据-------------------
@app.route('/mock/institute', methods=['GET'])
def mock_institute_data():
    result = fake_institute_data()
    return jsonify({'dict_data': result, "status": 200})




# -------------------- 其他--------------------#
# 实时请求1s
@app.route('/getprecision', methods=['GET'])
def getPrecisionInfo():
    return jsonify({'info': '没带口罩'})


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        # print(b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/acquirepicture', methods=['GET'])  # 这个地址返回视频流响应
def video_feed():
    # print('睡10s')
    # time.sleep(10)
    # print('睡眠结束')
    # 这里，“x-”表示属于实验类型。“replace”表示每一个新数据块都会代替前一个数据块
    # 新数据不是附加到旧数据之后，而是替代它。
    return Response(gen(VideoCamera("C:\\Users\\K\\Desktop\\dangmianmngyue.mp4")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # 172.24.247.8

    app.run(host='172.24.247.8', port=5000)
