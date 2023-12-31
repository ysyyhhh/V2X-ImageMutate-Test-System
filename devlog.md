# 开发日志

## Week 1

### 进度安排

- 确定项目需求和目标
- 搭建项目的开发环境和版本控制系统

### 任务分配

- 陆润风：
  - 设计项目的基本结构和架构
  - 确定项目所需的前后端技术栈和开发工具
- 彭坤：
  - 负责编写变异算子配置模块
  - 进行相关技术调研，确定最佳的变异算法和实现方式
- 吴德盛：
  - 负责编写模型测试管理模块
  - 研究相关领域的车联网协同感知技术，了解模型测试的方法和评估指标
- 肖琛：
  - 负责编写测试报告生成模块
  - 研究报告生成的相关技术和工具，了解如何提取测试结果并生成可视化报告

## Week 2

### 进度安排

- 完成各个模块的基本功能实现
- 进行单元测试和集成测试，确保各个模块的正确性和合理性
- 完善项目的文档和注释

### 任务分配

- 陆润风：
  - 实现基本的前后端代码框架，确保能够正常运行
- 彭坤：
  - 编写变异算子配置模块的核心代码，并进行单元测试
- 吴德盛：
  - 编写模型测试模块，确保能够根据变异前后的图像数据进行模型测试
- 肖琛：
  - 设计测试报告生成模块的数据结构和算法
  - 编写测试报告生成模块的核心代码，并进行单元测试

## Week 3

### 进度安排

- 进行系统测试和实验评估
- 根据测试结果进行必要的调整和优化
- 完善项目的文档，包括README和devlog

### 任务分配

- 陆润风：
  - 进行系统测试，并修复前端的bug
- 彭坤：
  - 编写项目的devlog，整理项目的开发日志
- 吴德盛：
  - 完成模型测试模块，增加模型测试的评估指标生成
  - 进行docker打包和部署配置
- 肖琛：
  - 编写README文档，描述项目的设计方案和使用方法

### 碰到的难题和解决的过程

#### 开发时间紧张，前端开发工作量大，如果使用vue或react很可能无法完成

调研并学习使用了amis作为前端框架,进行开发. 使用amis可以快速搭建前端页面

#### 待测试模型的各个使用方法不同，对每个模型难以进行统一的接口整合和测试

最终仅选择了一个CoBEVT网络模型进行测试。

#### 测试结果可视化

- 在测试报告生成模块的开发过程中，我们遇到了如何提取测试结果并生成可视化报告的挑战。我们通过学习数据分析和可视化工具，掌握了相关技术，并成功地将测试结果转化为直观清晰的报告。

#### 部署的困难

##### 将amis部署在docker中

amis在开发时是直接使用node server.js, 并没有打包成静态文件.

如果直接使用node server.js, 需要在docker中安装node环境, 并且需要在docker中安装npm包, 会导致docker镜像过大.

解决方法: 针对amis已有的index.html, 使用nginx进行部署, 并且将amis的静态文件打包成静态文件.

##### 后端要使用opencood, 需要配置特定的python版本环境

在docker中使用conda安装python环境

```dockerfile
# 安装conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# 创建conda环境并安装python
RUN /opt/conda/bin/conda create -n py37 python=3.7.16
ENV PATH /opt/conda/envs/py37/bin:$PATH
```

##### 需要在docker中使用GPU，而GPU并不是像CPU一样是docker的基本组件，需要额外安装并在外部配置. dockerfile编写起来也比较麻

比如，直接使用nvidia/cuda:11.0-base镜像，时会报错

[Updating the CUDA Linux GPG Repository Key](https://developer.nvidia.com/blog/updating-the-cuda-linux-gpg-repository-key/)
需要在dockerfile中添加

```dockerfile
RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub
```

docker中使用宿主机的GPU,需要在docker-compose中添加

```yml
deploy:
  resources:
    reservations:
      devices:
        - driver: "nvidia"
          count: "all"
          capabilities: [ "gpu" ]
```

- 在架构设计阶段，我们遇到了如何将各个模块有机地组织起来的问题。经过团队讨论和分析，我们决定采用模块化的设计，每个模块负责特定的功能，并通过接口进行交互。这样可以提高代码的可维护性和可扩展性。
