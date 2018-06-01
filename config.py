class Config:
    DEBUG = True
    # 配置sqlalchemy连接mysql数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/flask_day08'
    # 配置数据库的动态追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS =False