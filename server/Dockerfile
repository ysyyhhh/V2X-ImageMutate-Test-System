# python 3.7.16 nvidia/cuda:11.7-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# 设置apt的源为tsinghua镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y curl wget

# 安装conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# 创建conda环境并安装python
RUN /opt/conda/bin/conda create -n py37 python=3.7.16
ENV PATH /opt/conda/envs/py37/bin:$PATH

#WORKDIR /app
WORKDIR /app

# pip 使用tsinghua镜像源
RUN mkdir -p /root/.pip
RUN echo "[global]" > /root/.pip/pip.conf
RUN echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> /root/.pip/pip.conf

# 更新pip
RUN pip install --upgrade pip

# fix ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update

COPY requirements.txt .

RUN pip install -r requirements.txt --no-deps

# 其他配置

RUN apt install libgl1-mesa-glx -y

ENV TZ=Asia/Shanghai


# RUN apt-get install libglib2.0-dev -y
# 由于安装libglib2.0-dev的时候，bash会有交互操作叫你选择对应的时区，在docker build的时候没有交互的，所以需要加上DEBIAN_FRONTEND="noninteractive"
RUN DEBIAN_FRONTEND="noninteractive" apt -y install libglib2.0-dev libmagickwand-dev
# 拷贝项目代码
COPY . .


# RUN rm -rf migrations/ __pycache__/

# RUN python manage.py makemigrations

# RUN python manage.py migrate

# RUN rm -rf /app/static/static/3

# RUN rm db.sqlite3

# RUN python manage.py makemigrations
# # 
# RUN python manage.py migrate

ENV DJANGO_SETTINGS_MODULE=TestSystemServer.settings
ENV DJANGO_ALLOWED_HOSTS=*
# 启动django

CMD [ "python", "manage.py", "runserver","0.0.0.0:8000"]

