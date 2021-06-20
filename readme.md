# 准备



### 环境安装

- Python库

安装第三方库

```
pip install -r requirements,txt
```

- MySQL
  - 官网下载
  - 小皮面板



# 说明



### 实现的功能

- 用户的注册和登录
- 利用ffmpeg剪辑视频
- 显示剪辑进度
- 提供剪辑后的视频下载链接



### 文档说明（此处只说明必要的文件）

- lg_ffmpeg：存放项目所有逻辑文件
  - api_v1_0：存放蓝图文件
    - __init__.py：蓝图初始化文件
    - login.py：用户登录接口
    - make_video.py：视频剪辑，显示剪辑进度接口
    - regist.py：用户注册接口
    - video_record.py：查询用户提交记录接口
  - __init__.py：项目初始文件，包括flask的实例化函数
  - models.py：数据库模型文件
  - response_code.py：全局错误码
- logs：错误日志
- new_video：用来存储剪辑后的视频，上线时可采用对象存储代替
- utils：自定义文件
  - common.py：登录检测函数和生成文件名函数
  - operate_video.py：定义了一个类用以操作视频，包括视频剪辑，和显示进度等类方法
- config.py：项目配置文件
- manage.py：项目入口文件





# 运行



### 迁移数据库



cmd进入manage.py所在目录

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```



### 运行manage.py

**注意：**此项目包含redis，如果不需要可以注释



### 接口测试

由于本项目未写前端，因此需要用postman做测试



# 存在的问题



- 进度条的显示和视频剪辑需要异步进行（进度能够打印，但返回前端我一直测试不成功）
