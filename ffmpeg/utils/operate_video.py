# @Time  :2021/6/19 11:30
# @Author:Sleet
# @File  :operate_video.py

from config import Config
import os
import random
import re
import subprocess


class Operation(object):

    def __init__(self, video_url=None, start_time=None, timescale=None, new_name=None, video_format=None):
        self.video_url = video_url
        self.start_time = start_time
        self.timescale = timescale
        self.new_name = new_name
        self.video_format = video_format
        self.user_id = None
        self._process = None
        self._time = None
        self._new_file_url = None
        self._result = None

    # 将日志输出的时间类型转换成秒
    @staticmethod
    def get_seconds(time=None):
        h = int(time[0:2])
        # print("时：" + str(h))
        m = int(time[3:5])
        # print("分：" + str(m))
        s = int(time[6:8])
        # print("秒：" + str(s))
        ms = int(time[9:12])
        # print("毫秒：" + str(ms))
        ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
        return ts

    # size=   25189kB time=00:04:28.67 bitrate= 768.0kbits/s speed= 748x
    # video:0kB audio:25189kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000302%
    # cmd = ['ffmpeg.exe', '-i', 'E:\\ffmpeg\\lg_ffmpeg\\test_mp4.mp4', '-ar', '48000', '-ac',
    #        '1', '-acodec', 'pcm_s16le', '-hide_banner', 'E:\\ffmpeg\\lg_ffmpeg\\out.avi']

    def clip_video(self, user_id):
        # 新文件名
        num = random.randint(10, 99)
        new_file = f'{self.new_name}-{num}_{user_id}.{self.video_format}'
        self._new_file_url = os.path.join(Config.NEW_VIDEO_SAVE_URL, new_file)

        # 时间格式转换
        self._time = float(self.timescale)

        cmd = f"ffmpeg.exe -ss {self.start_time} -t {self.timescale} -i {self.video_url} -ar 48000 -ac 1 -acodec pcm_s16le -vcodec copy -hide_banner {self._new_file_url}"
        self._process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True)

        return self._new_file_url

    @property
    def get_progress(self):
        for line in self._process.stdout:
            # print(line)

            # duration_res = re.search(r'\sDuration: (?P<duration>\S+)', line)
            # if duration_res is not None:
            #     duration = duration_res.groupdict()['duration']
            #     duration = re.sub(r',', '', duration)

            result = re.search(r'\stime=(?P<time>\S+)', line)
            if result is not None:
                elapsed_time = result.groupdict()['time']
                # 此处可能会出现进度超过100%，未对数值进行纠正
                progress = (self.get_seconds(elapsed_time) / self._time) * 100
                print('------')
                print(self._time)
                print('------')
                print(elapsed_time)
                print(progress)
                print("进度:%3.2f" % progress + "%")
                self._result = "进度:%3.2f" % progress + "%"
        self._process.wait()
        if self._process.poll() == 0:
            print("success:", self._process)
            self._result = "进度:%3.2f" % 100 + "%"
        else:
            print("error:", self._process)
            self._result = "fail"

        return self._result
    # def clip_video(video_url, start_time, timescale, new_name, video_format, user_id):
    #     """
    #     视频剪辑
    #     :param video_url: 待剪辑的视频地址
    #     :param start_time: 剪辑开始时间
    #     :param timescale: 剪辑时长
    #     :param new_name: 新文件名
    #     :param video_format: 新文件格式
    #     :param user_id: 用户id
    #     :return:
    #     """
    #     # 新文件名
    #     num = random.randint(10, 99)
    #     new_file = f'{new_name}-{num}_{user_id}.{video_format}'
    #     new_file_url = os.path.join(Config.NEW_VIDEO_SAVE_URL, new_file)
    #
    #     # 调用FFmpeg
    #     ff = FFmpeg(
    #         executable=r'D:\ffmpeg\ffmpeg-N-102753-gfcb80aa289-win64-gpl\ffmpeg-N-102753-gfcb80aa289-win64-gpl\bin\ffmpeg.exe',
    #         inputs={video_url: ['-ss', start_time, '-t', timescale]},
    #         outputs={new_file_url: ['-acodec', 'copy', '-vcodec', 'copy']}
    #     )
    #
    #     return ff.cmd
