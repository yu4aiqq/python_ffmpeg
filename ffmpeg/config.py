# @Time  :2021/6/12 10:09
# @Author:Sleet
# @File  :config.py

import redis
import os


class Config(object):
    """数据库配置"""
    HOSTNAME = '127.0.0.1'
    DATABASE = 'ffmpeg'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = 'root'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """redis配置"""
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    """配置session"""
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    SECRET_KEY = os.urandom(12)
    PERMANENT_SESSION_LIFETIME = 60*60

    """视频保存地址"""
    VIDEO_SAVE_URL = os.getcwd() + r'\video'
    NEW_VIDEO_SAVE_URL = os.getcwd() + r'\new_video'


class DevConfig(Config):
    """Development Environment"""
    Debug = True


class ProConfig(Config):
    """Production Environment"""


config_map = {
    'Dev': DevConfig,
    'Pro': ProConfig
}
