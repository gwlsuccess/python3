from flask import Blueprint
# 定义蓝图对象
profile_blu  = Blueprint('profile_blu',__name__,url_prefix='/user')
# 导入使用蓝图对象的文件
from . import views