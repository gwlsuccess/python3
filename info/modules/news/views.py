from flask import session
# 导入蓝图对象
from . import news_blue
# 使用蓝图对象
@news_blue.route('/')
def index():
    # 请求对象session
    session['name']=2018
    return 'index'