# Copyright (c) ATR Lab,XMU.
# Distributed under the terms of the Modified BSD License.

# tensorflow docker 


FROM tensorflow/tensorflow:2.6.0-gpu-jupyter


MAINTAINER Lingxiang Zheng <lxzheng@xmu.edu.cn>

USER root


RUN apt-get clean && \
          apt-get update && \
          apt-get -y install software-properties-common --fix-missing &&\
	  apt-get -yq upgrade && \
 	  apt-get -y install libsm6 libxrender1 libxext6 graphviz ffmpeg && \  
	  apt-get clean && \
          rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install \
    	pandas \
	Pillow \
	opencv-python\
	lxml\
	tqdm\
	pydot\
	graphviz\
	bs4 \
	requests \
	selenium \
	piexif	\
	ffmpeg-python	\
	scipy	\
	tensorflow_hub	\
	wget	\
	-i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	--trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/

RUN pip3 --no-cache-dir install \
	sklearn \
	-i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	--trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/
#error if not uninstall enum34
RUN pip3 uninstall -y enum34
RUN pip3 --no-cache-dir install \
	numpy-quaternion \
	-i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	--trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/
	
RUN pip3 --no-cache-dir install \
	jupyter-tensorboard\
	-i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	--trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/
RUN jupyter tensorboard enable --user
RUN rm -rf /tf
COPY src /tf
#RUN echo "c.NotebookApp.password = u'argon2:$argon2id$v=19$m=10240,t=10,p=8$PCGJeCeDz3Q5jB4HgrGo/w$7lqhswj8Ttvb2jdXMcFYUw'" >/root/.jupyter/jupyter_notebook_config.py
RUN python -c "from notebook.auth import passwd;print('c.NotebookApp.password = u'+'\''+passwd('xmu_atr')+'\'')"  >/root/.jupyter/jupyter_notebook_config.py