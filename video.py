import io
import cv2
import numpy as np
import os
import base64
from PIL import Image


class VideoCamera(object):
    def __init__(self, video_path):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


# def get_frame(self):
#     self.video = cv2.VideoCapture("C:\\Users\\K\\Desktop\\dangmianmngyue.mp4")
#     # -img是返回的捕捉到的帧，如果没有帧被捕获，该值为空
#     # -retval表示捕获是否成功，如果成功则该值为True，不成功则为False
#     retval, img = self.video.read


def video_to_image(video_dir, save_dir):
    cap = cv2.VideoCapture(video_dir)  # 生成读取视频对象
    n = 1  # 计数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    print(fps)
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
    # 定义视频输出
    # writer = cv2.VideoWriter("teswellvideo_02_result.mp4", fourcc, fps, (width, height))
    i = 0
    timeF = int(fps)  # 视频帧计数间隔频率
    while cap.isOpened():
        ret, frame = cap.read()  # 按帧读取视频
        # 到视频结尾时终止
        if ret is False:
            break
        # 每隔timeF帧进行存储操作
        if (n % timeF == 0):
            i += 1
            print('保存第 %s 张图像' % i)
            save_image_dir = os.path.join(save_dir, '%s.png' % i)
            print('save_image_dir: ', save_image_dir)
            cv2.imwrite(save_image_dir, frame)  # 保存视频帧图像
        n = n + 1
        # cv2.waitKey(1) #延时1ms
    cap.release()  # 释放视频对象


# 有没有办法不保存 图片就直接 转码
def pict_to_byte():
    with open(r'C:\Users\K\Desktop\video2image\1.png', 'rb') as f:
        a = f.read()
    print(f'a:{a}')
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    print(f'img_stream:{img_stream}')
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(imgByteArr)
    return img_stream


if __name__ == '__main__':
    # video_to_image(r'C:\Users\K\Desktop\dangmianmngyue.mp4', r'C:\Users\K\Desktop\video2image')
    pict_to_byte()
    # for info in os.listdir(r'C:\Users\K\Desktop\video2image'):
    #     domain = os.path.abspath(r'C:\Users\K\Desktop\video2image')  # 获取路径
    #     # print(f'domain:{domain}')
    #     path = os.path.join(domain, info)  # 拼接路径
    #     print(path)
    #
    #     with open(path, 'rb') as f:
    #         a = f.read()
    #     print(f'a:{a}')
    #     '''对读取的图片进行处理'''
    #     img_stream = io.BytesIO(a)
    #     print(f'img_stream:{img_stream}')
    #     img = Image.open(img_stream)
    #     imgByteArr = io.BytesIO()
    #     img.save(imgByteArr, format='PNG')
    #     imgByteArr = imgByteArr.getvalue()
