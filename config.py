# 导入redis 数据库模块
from redis import StrictRedis

class Config:
    # 开启调试模式
    DEBUG = None
    # 设置密钥
    SECRET_KEY = 'heyKyqaUgg8jAJJvjwxy3bUCkBFBX5ao3kK0HLptbW8='

    # 配置sqlalchemy连接mysql数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/flask_day08'
    # 配置数据库的动态追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis的主机和端口
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 使用redis来保存session信息
    SESSION_TYPE = 'redis'
    # 对象session信息进行签名
    SESSION_USE_SIGNER = True
    # 存储session的redis实例
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 指定session的过期时间1天
    PERMANENT_SESSION_LIFETIME = 86400
# 开发模式
class developmentConfig(Config):
    DEBUG = True
# 生产模式
class productionConfig(Config):
    DEBUG = False

# 把我们的配置对象实现字典映射(导入文件是用次即可)
config ={
    'development':developmentConfig,
    'production':productionConfig
}