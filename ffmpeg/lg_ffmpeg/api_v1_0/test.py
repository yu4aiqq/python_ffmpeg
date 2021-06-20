# @Time  :2021/6/18 12:56
# @Author:Sleet
# @File  :test.py

from . import api


@api.route('/test', methods=['GET'])
def test():
    return 'hello'
