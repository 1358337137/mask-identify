import datetime
import os
import random

import paramiko


# db = pymysql.connect('43.138.26.63', 'root', 'Key1999...', 'flask_db')
# cursor = db.cursor()


# local_file是要上传的本地文件路径  eg:C:\Users\K\Desktop\video2image\2.png
# remote_path是要上传到服务器上指定文件的路径  需要加文件名 ，可
def upload(local_file):
    hostname = '43.138.26.63'
    username = 'root'
    password = 'Xs1358337137'
    port = 22  # 配置信息可以写到配置文件中
    remote_root = '/usr/local/nginx/html/mask/'  # 云服务器上的文件路径

    file_name = local_file.split('/')[-1]  # 获取路径下的文件名
    remote_path = remote_root + file_name  # 文件路径+ 文件名

    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('开始上传文件%s ' % datetime.datetime.now())

        try:
            sftp.put(local_file, remote_path)
        except Exception as e:
            sftp.mkdir(os.path.split(remote_path)[0])
            sftp.put(local_file, remote_path)
            print("从本地： %s 上传到： %s" % (local_file, remote_path))

        print('文件上传成功 %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    # local_file = r'C:\Users\K\Desktop\video2image\2.png'
    # remote_path = os.path.join('/usr/local/nginx/html/mask/', "2.png")
    # remote_path= '/usr/local/nginx/html/mask/'
    #   print(remote_path)
    #   # upload(local_file, remote_path)
    dlist = []
    for i in range(0, 7):
        dig = random.randint(100, 200)
        dlist.append(dig)
    print(dlist)