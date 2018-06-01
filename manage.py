from flask import Flask
# 导入　flask_scrip　管理器，在终端执行程序
from flask_script import Manager
# 导入迁移扩展包和迁移命令
from flask_migrate import Migrate,MigrateCommand
# 导入flask_sqlalchemy数据库扩展包
from flask_sqlalchemy import SQLAlchemy
# 导入配置文件
from config import Config

app=Flask(__name__)
# 实例化数据库对象
db = SQLAlchemy(app)
# 使用配置对象
app.config.from_object(Config)
# 实例化管理器对象
manager = Manager(app)
# 使用迁移框架
Migrate(app,db)
# 通过管理器对象集成迁移命令
manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    # app.run(debug=True)
    # 必须配置项目参数　runserver
    manager.run()