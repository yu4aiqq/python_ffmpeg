# @Time  :2021/6/12 10:09
# @Author:Sleet
# @File  :__init__.py.py

from flask import Flask
from config import config_map
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
redis_store = None


def setup_log():
    # 设置日志的的登记  DEBUG调试级别
    logging.basicConfig(level=logging.DEBUG)
    # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=100)
    # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
    # 为日志记录器设置记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaks app使用的）加载日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    setup_log()
    # 实例化
    app = Flask(__name__)
    # 配置
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 绑定Session
    Session(app)
    # 绑定数据库操作对象db
    db.init_app(app)
    # 绑定redis对象
    global redis_store
    redis_store = redis.Redis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 注册蓝图
    from lg_ffmpeg.api_v1_0 import api
    app.register_blueprint(api)

    return app
