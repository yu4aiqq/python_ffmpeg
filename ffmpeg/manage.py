# @Time  :2021/6/10 20:19
# @Author:Sleet
# @File  :manage.py

from lg_ffmpeg import create_app, db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 实例化
app = create_app('Dev')
# 让其可以通过命令行传参
manage = Manager(app)
# 迁移
Migrate(app, db)
# 添加命令
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()
