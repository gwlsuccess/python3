from flask import Blueprint
# 添加前缀，划分不同的实现模块　url_prefix=
passport_blu = Blueprint('passport_blu',__name__,url_prefix='/passport')

from . import views