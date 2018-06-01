# 导入redis 数据库模块
from redis import StrictRedis

class Config:
    DEBUG = True
    # 设置密钥
    SECRET_KEY='LPyirIeIv0lJVsLrUl2QLA=='
    # 配置sqlalchemy连接mysql数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/flask_day08'
    # 配置数据库的动态追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    # 配置redis的主机和端口
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 使用redis 用于保存session数据
    SESSION_TYPE ='redis'
    # 对象session信息进行签名
    SESSION_USE_SIGNER =  True
    # 存储session的redis实例
    SESSION_REDIS= StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 指定session的过期时间1天
    PERMANENT_SESSION_LIFETIME = 86400