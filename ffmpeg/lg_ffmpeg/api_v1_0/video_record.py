# @Time  :2021/6/18 15:59
# @Author:Sleet
# @File  :video_record.py


from . import api
from utils.common import login_required
from flask import request, g, jsonify
from lg_ffmpeg.response_code import RET
from lg_ffmpeg.models import Video
import logging


@api.route('/video_record', methods=['GET'])
# @login_required
def get_record():
    """
    返回用户剪辑记录
    :return: 返回用户剪辑过的视频名称，时长，剪辑时间，下载链接
    """
    # 获取参数
    # user_id = g.user_id
    user_id = request.get_json()['user_id']

    # 查询记录
    try:
        video_info = Video.query.filter_by(user_id=user_id).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    username = video_info[0].user_name
    video_list = [video.to_dict() for video in video_info]
    # print(video_list)

    # 返回记录
    return jsonify(errno=RET.OK, errmsg='OK', data={'username': username, 'video_record': video_list})
