# 导入蓝图对象
from . import profile_blu
# 导入用户验证自定义装饰器
from info.utils.commons import login_required
from flask import g,jsonify,redirect,render_template
# 导入常量文件
from info.utils.response_code import RET
# 使用蓝图对象
@profile_blu.route('/info')
@login_required
def user_info():
    """
    用户信息页面
    1、尝试获取用户信息
    2、判断用户如果没有登录，重定向到项目首页
    3、默认加载模板页面

    :return:
    """
    user = g.user
    # 用户未登陆时，重定向到首页
    if not user:
        return redirect('/')
    # 调用模型类中的方法，获取用户的基本信息
    data = {
        'user':user.to_dict()
    }
    # 默认加载模板页面
    return render_template('news/user.html',data=data)
