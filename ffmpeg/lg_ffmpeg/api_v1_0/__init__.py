# @Time  :2021/6/18 11:34
# @Author:Sleet
# @File  :__init__.py.py

from flask import Blueprint
api = Blueprint('api_1_0' ,__name__, url_prefix='/api/v1.0')
from . import test, regist, login, video_record, make_video
