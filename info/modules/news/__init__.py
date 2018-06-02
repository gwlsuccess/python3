# 导入蓝图
from flask import Blueprint
# 1---创建蓝图对象
news_blue =Blueprint('news_blue',__name__)

# 把使用蓝图对象的模块导入创建蓝图对象的下面
from . import views