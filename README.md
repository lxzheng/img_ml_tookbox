# 深度神经网络图像识别工具包img_ml_toolbox
## 为什么写这个工具包
img_ml_toolbox工具包是一个用Jupyter Notebook的交互控件ipywidgets写的机器学习工具包。它主要面向希望学习深度神经网络开发的初学者，体验深度神经网络，了解机器学习的基本步骤。由于Jupyter Notebook是深度学习较常用的一个工具，用它开发，也有助于初学者熟悉Jupyter Notebook的使用。img_ml_toolbox将机器学习的步骤与经过封装的少量的代码整合在一起，能够降低初学者的上手难度。

## 安装与使用
### docker（推荐）
下载docker 映像
```
docker pull lxzheng/img_ml_toolbox:1.0
```
启动docker容器
```
docker run --gpus all -it --rm -p 6006:6006 -p 8888:8888  lxzheng/img_ml_toolbox:1.0
```
在容器启动之后，打开浏览器输入地址
```
http://127.0.0.1:8888/
```
密码：xmu_atr

点击打开```image_recognition.ipynb```即可打开img_ml_toolbox，按照文档中的提示操作，体验机器学习的流程。
### 其他方式
安装相关依赖软件，启动jupyter notebook，打开```image_recognition.ipynb```

### 相关软件及版本
- ffmpeg
- python3
- tensorflow 2.6以上
- jupyter notebook
- 其他python模块参见requirements.txt

## License许可协议

项目使用[GNU General Public License v3.0](LICENSE)协议发布
