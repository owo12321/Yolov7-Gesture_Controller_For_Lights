from os import stat
import time
import cv2
import numpy as np
from PIL import Image
from yolo_my import YOLO
from socket import *


# 配置opencv视频流
# 视频源路径和保存路径
video_path = 0 # 0为摄像头
video_save_path="" # 如果是""则不保存

# 配置socket
IP = '192.168.0.107'
SERVER_PORT = 50001
BUFLEN = 1024





# 实例化一个socket用于通信
dataSocket = socket(AF_INET, SOCK_STREAM)
# 连接到服务器
dataSocket.connect((IP, SERVER_PORT))
print('已与树莓派成功建立连接')



# 向树莓派发送控制灯的指令
on_num=0
off_num=0
state = 'off'
def control_light(flag:str):
    global on_num, off_num, state
    global off_num
    global dataSocket

    # 计数
    if flag=='on':
        on_num+=1
        off_num=0
    elif flag=='off':
        off_num+=1
        on_num=0
    else:
        off_num=0
        on_num=0
    # print(off_num, on_num)

    # 积累10次(大概半秒)才发送指令，不然太频繁了，如果本来就是on也不会重复发
    # 开
    if on_num==10 and state=='off':
        on_num=0
        off_num=0
        print('send on')
        dataSocket.send(b'on')
        recved = dataSocket.recv(BUFLEN)
        if not recved:
            print('对方已断开连接')
            return False
        # 打印回传的信息
        print('pi: ' + recved.decode() + '\n')
        state = 'on'
    # 关
    if off_num==10 and state=='on':
        on_num=0
        off_num=0
        print('send off')
        dataSocket.send(b'off')
        recved = dataSocket.recv(BUFLEN)
        if not recved:
            print('对方已断开连接')
            return False
        # 打印回传的信息
        print('pi: ' + recved.decode() + '\n')
        state='off'
    
    return True
        
    


# 初始化yolo
yolo = YOLO()

# 视频输入流
capture = cv2.VideoCapture(video_path)
ref, frame = capture.read()
if not ref:
    raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")
# 视频输出流
if video_save_path!="":
    fourcc  = cv2.VideoWriter_fourcc(*'XVID')
    size    = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out     = cv2.VideoWriter(video_save_path, fourcc, 30, size)

fps = 0.0
while(True):
    t1 = time.time()
    # 读取某一帧
    ref, frame = capture.read()
    if not ref:
        break
    # 格式转变，BGRtoRGB
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # 转变成Image
    frame = Image.fromarray(np.uint8(frame))
    # 进行检测
    frame, label_list = yolo.detect_image(frame)
    frame = np.array(frame)
    # RGBtoBGR满足opencv显示格式
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    # 控制树莓派的灯
    # label_list = [['label1', conf_rate1], ['label2', conf_rate2], ...]
    flag = 'nothing'
    for item in label_list:
        if item[0] == 'number 5':
            flag = 'on'
        elif item[0] == 'A':
            flag = 'off'
    control_light(flag)
    
    # 计算fps
    fps  = ( fps + (1./(time.time()-t1)) ) / 2
    # print(f"fps={fps:.2f}, flag={flag}, label_list={label_list}")

    frame = cv2.putText(frame, f"fps={fps:.2f}, flag={flag}, label_list={label_list}", (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("video",frame)
    c= cv2.waitKey(1) & 0xff 

    if video_save_path!="":
        out.write(frame)

    if c==27:
        capture.release()
        break
    

    
print("Video Detection Done!")
capture.release()
if video_save_path!="":
    print("Save processed video to the path :" + video_save_path)
    out.release()
cv2.destroyAllWindows()