from flask import Flask
# 导入flask_sqlalchemy数据库扩展包/home/python/flask_day08
from flask_sqlalchemy import SQLAlchemy
# 导入扩展flask_session,可以配置session信息的存储0.
from flask_session import Session
# 导入flask_wtf扩展包
from flask_wtf import CSRFProtect
# 导入配置文件
from config import config,Config
# 导入日志模块 pycharm中的模块
import logging
# 导入日志模块文件处理
from logging.handlers import RotatingFileHandler
# 导入redis数据库
from redis import StrictRedis
from flask_wtf import csrf
# 需要指定host port,此处可以使用配置文件中的变量,用来缓存和业务逻辑相关的数据
redis_store = StrictRedis(Config.REDIS_HOST,Config.REDIS_PORT,decode_responses=True)
# 实例化sqlalchemy数据库对象
db = SQLAlchemy()

# 集成项目日志（不需要自己写）
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG) # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)

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

    # 使用请求钩子，在每次请求后执行设置csrf_token
    @app.after_request
    def after_request(response):
        # 调用扩展生成csrf_token口令，
        # csrf.generate_csrf()　含有一个secret_key，不需要指定，已在config中设置过
        csrf_token = csrf.generate_csrf()
        # 把csrf_token 写入到客户端浏览器cookie中
        response.set_cookie('csrf_token',csrf_token)
        return response
    # 导入蓝图对象
    from info.modules.news import news_blue
    # 注册蓝图对象
    app.register_blueprint(news_blue)
    # 注册蓝图对象，图片验证码的视图图片
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app