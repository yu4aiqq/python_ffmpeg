# @Time  :2021/6/18 13:22
# @Author:Sleet
# @File  :regist.py


from . import api
from flask import request, jsonify
from lg_ffmpeg.response_code import RET
from lg_ffmpeg.models import User
from lg_ffmpeg import db
import logging
import re


@api.route('/regist', methods=['POST'])
def regist():
    """
    用户注册
    :return: 注册状态
    """
    # 获取参数
    try:
        regist_dict = request.get_json()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    username = regist_dict.get('username')
    phone = regist_dict.get('phone')
    passwd = regist_dict.get('passwd')
    passwd_confirm = regist_dict.get('passwd_confirm')

    # 校验参数
    if not all([username, phone, passwd, passwd_confirm]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'1[345789]\d{9}', phone):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号不合法')

    # 保存
    user_info = User(
        username=username,
        phone=phone,
        passwd=passwd
    )
    try:
        db.session.add(user_info)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    # 返回状态

    return jsonify(errno=RET.OK, errmsg='注册成功')
