from flask import session,render_template,current_app,jsonify
# 导入蓝图对象
from . import news_blue
# 导入模型类User
from info.models import User
# 导入自定义状态码
from info.utils.response_code import RET

# 使用蓝图对象
@news_blue.route('/')
def index():
    # 检查用户登陆状态
    # 请求对象session
    # 展示用户的登陆信息　
    # 尝试从redis中获取用户信息
    # 根据　user_id查询mysql数据库
    # 判断查询结果
    user_id = session.get('user_id')
    # 如果注册user_id 存在，查询数据库
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno = RET.DBERR,errmsg = '数据查询失败')

    data = {
        'user_info':user.to_dict() if user else None
    }

    return render_template('news/index.html',data=data)

# 加载项目小图标
@news_blue.route('/favicon.ico')
def favicon():
    # 静态路径访问的默认实现，send_static_file
    # 把静态文件发送给浏览器
    return current_app.send_static_file('news/favicon.ico')