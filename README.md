# 手势识别远程控制树莓派点亮LED灯
## 原理
在电脑端运行yolov7识别手势，识别到开或关的手势后通过socket向树莓派发送指令，树莓派接收到后通过GPIO点亮LED灯
## 使用方法
先修改control_light.py和raspi/server.py里边的IP为树莓派的IP地址  
参考yolo_my.py文件中的注释修改其中的配置，主要注意model_path、classes_path和cuda  
在树莓派端运行raspi路径下的server.py文件，再在电脑端运行control_light.py文件  
开灯为五指张开，关灯为握拳
## 模型和数据集
模型使用来自bubbliiiing的yolov7
```
https://github.com/bubbliiiing/yolov7-pytorch
```
数据集来源于以下链接，包含model_data/my_classes.txt中的10个动作
```
https://download.csdn.net/download/ECHOSON/83460039
```
在logs路径下有已经训练好的模型，可以直接使用

若要训练自己的数据集，请参考bubbliiiing的yolov7-pytorch，训练好后在yolo_my中修改model_path的路径指向训练好的模型，修改classes_path指向自己的classes文件，里边写自己的分类（参考model_data下的classes文件）  
## 致谢
感谢bubbliiiing大佬的yolov7模型，本代码大部分基于他的模型制作