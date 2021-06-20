# @Time  :2021/6/19 10:41
# @Author:Sleet
# @File  :operate_video.py


from . import api
from flask import request, g, jsonify
from lg_ffmpeg.response_code import RET
from lg_ffmpeg.models import User, Video
from lg_ffmpeg import db
from utils.common import login_required, create_filename
from utils.operate_video import Operation
from datetime import datetime
import logging
import os
from config import Config

video_op = None


@api.route('/video', methods=['POST'])
# @login_required
def make_video():
    """
    视频剪辑
    :return: 视频下载链接
    """
    # 获取参数
    user_id = request.form.get('user_id')
    video_file = request.files.get('video')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    new_name = request.form.get('new_name')
    video_format = request.form.get('format')

    # 校验参数
    if not all([video_file, start_time, end_time, new_name, video_format]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 上传视频
    video_name = video_file.filename
    prefix = video_name[:video_name.rfind(".")]
    suffix = video_name[video_name.rfind("."):]
    save_name = create_filename(prefix, suffix, user_id)
    video_url = os.path.join(Config.VIDEO_SAVE_URL, save_name)
    video_file.save(video_url)
    g.is_video = True   # 判断是否有视频

    # print(video_url)

    # 时间转化，计算剪辑时长
    start_time_tran = datetime.strptime(start_time, '%H:%M:%S')
    end_time = datetime.strptime(end_time, '%H:%M:%S')
    # print(start_time_tran, end_time)
    timescale = str((end_time - start_time_tran).seconds)
    # print(timescale)
    # print(type(timescale))

    # 剪辑
    global video_op
    video_op = Operation(video_url, start_time, timescale, new_name, video_format)
    url = video_op.clip_video(user_id)

    # 查询
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    # 保存
    video_info = Video(
        user_id=user_id,
        user_name=user.username,
        filename=video_name,
        timascale=timescale,
        downloadUrl=url
    )

    try:
        db.session.add(video_info)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    # 返回
    return jsonify(errno=RET.OK, errmsg='OK', data={'downloadUrl': url})


@api.route('/video_progress', methods=['GET'])
# @login_required
def video_progress():
    # 判断是否有视频在剪辑
    # is_video = g.is_video
    # if not is_video:
    #     return jsonify(errno=RET.OTHERERR, errmsg='没有视频在剪辑')

    global video_op
    try:
        progress = video_op.get_progress
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.SERVERERR, errmsg='无法获取进度')

    return jsonify(errno=RET.OK, errmsg='OK', data={'process': progress})
