from flask import Flask
# 导入flask_sqlalchemy数据库扩展包
from flask_sqlalchemy import SQLAlchemy
# 导入扩展flask_session,可以配置session信息的存储
from flask_session import Session
# 导入flask_wtf扩展包
from flask_wtf import CSRFProtect

# 实例化sqlalchemy数据库对象
db = SQLAlchemy()
# 导入配置文件
from config import config

# 创建程序实例的工厂方法：封装app,动态的加载app
def create_app(config_name):
    app=Flask(__name__)
    # 把db对象和app关联
    db.init_app(app)
    # 使用配置对象
    app.config.from_object(config[config_name])
    # 实例化session对象
    Session(app)
    # 实例化csrf
    CSRFProtect(app)

    return app