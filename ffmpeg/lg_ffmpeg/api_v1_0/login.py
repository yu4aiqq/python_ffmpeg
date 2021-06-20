# @Time  :2021/6/18 12:20
# @Author:Sleet
# @File  :login.py


from . import api
from flask import request, jsonify, session
from lg_ffmpeg.response_code import RET
from lg_ffmpeg.models import User
import logging


@api.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: 用户登录状态
    """
    # 获取参数
    try:
        user_dict = request.get_json()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    phone = user_dict.get('phone')
    passed = user_dict.get('passwd')

    # 校验参数
    if not all([phone, passed]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 判断
    try:
        user = User.query.filter(User.phone == phone, User.passwd == passed).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='账号或密码不正确')

    # 状态保持
    session['user_id'] = user.id
    session['user_name'] = user.username
    session['user_phone'] = user.phone

    return jsonify(errno=RET.OK, errmsg='登录成功')