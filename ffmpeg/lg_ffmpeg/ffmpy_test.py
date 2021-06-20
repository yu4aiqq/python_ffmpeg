# @Time  :2021/6/16 10:19
# @Author:Sleet
# @File  :ffmpy_test.py


from ffmpy import FFmpeg


ff = FFmpeg(
    executable=r'D:\ffmpeg\ffmpeg-N-102753-gfcb80aa289-win64-gpl\ffmpeg-N-102753-gfcb80aa289-win64-gpl\bin\ffmpeg.exe',
    inputs={'test_mp4.mp4': ['-ss', '00:00:00', '-t', '20']},
    outputs={'part1_mp4.mp4': ['-acodec', 'copy', '-vcodec', 'copy']}
)

print(ff.cmd)
ff.run()
