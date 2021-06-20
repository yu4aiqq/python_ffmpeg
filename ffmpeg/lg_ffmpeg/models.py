# @Time  :2021/6/16 11:53
# @Author:Sleet
# @File  :models.py

from . import db
from datetime import datetime


class BaseModel(object):
    """模型基类，为欸个模型增加记录创建时间和更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseModel, db.Model):
    """User表"""

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 用户id
    username = db.Column(db.String(32), unique=True, nullable=False)    # 用户名
    phone = db.Column(db.String(11), unique=True, nullable=False)   # 用户手机号
    passwd = db.Column(db.String(12), nullable=False)   # 用户密码
    video = db.relationship('Video', backref='user')


class Video(BaseModel, db.Model):
    """Video表"""

    __tablename__ = 'video_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # video id
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)  # 用户id
    user_name = db.Column(db.String(32), nullable=False)    # 用户名
    filename = db.Column(db.String(128), nullable=False)    # 文件名
    timascale = db.Column(db.String(128), nullable=False)   # 时长
    downloadUrl = db.Column(db.String(128), nullable=False)  # 下载地址

    def to_dict(self):
        """将基本信息弄成字典格式"""
        video_dict = {
            'create_time': self.create_time,
            'filename': self.filename,
            'timescale': self.timascale + '秒',
            'url': self.downloadUrl
        }

        return video_dict
