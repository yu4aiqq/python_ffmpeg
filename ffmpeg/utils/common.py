# @Time  :2021/6/18 12:23
# @Author:Sleet
# @File  :common.py

import functools
from flask import session, g, jsonify
from lg_ffmpeg.response_code import RET
from ffmpy import FFmpeg
import random


def login_required(view_func):
    """
    用户登录检测
    :param view_func:
    :return:
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户是否登录了
        user_id = session.get('user_id')
        if user_id is not None:
            g.user_id = user_id
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper


def create_filename(prefix, suffix, user_id):
    """
    生成新的文件名
    :param prefix: 文件名前缀
    :param suffix: 文件名后缀
    :param user_id: 用户id
    :return: 新的文件名
    """
    num = random.randint(10, 99)
    new_filename = f'{prefix}-{num}_{user_id}{suffix}'

    return new_filename
