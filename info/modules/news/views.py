from flask import session,render_template,current_app,jsonify
# 导入蓝图对象
from . import news_blue
# 导入模型类User 和 News
from info.models import User,News,Category
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
            # return jsonify(errno = RET.DBERR,errmsg = '数据查询失败')

    # 2018/6/6 --1 项目首页的点击排行：默认按照点击次数进行排序，limit 6条
    try:
        # 访问得到的数据为对象
        news_list = News.query.order_by(News.clicks.desc()).limit(6)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =RET.DBERR,errmsg ='数据查询失败')
    if not news_list:
        return jsonify(errno =RET.NODATA,errmsg ='没有新闻数据')

    # 遍历对象之后，然后在列表中以字典形式保存 news.to_dict()
    news_dict_list = []
    for news in news_list:
        news_dict_list.append(news.to_dict())

    # 2018/6/6 --2 首页新闻数据的分类展示
    try:
        categories = Category.query.all()
    except Exception  as e:
        current_app.logger.error(e)
        return jsonify(errno =RET.DBERR,errmsg ='分类新闻查询失败')
    if not categories:
        return jsonify(errno =RET.NODATA ,errmsg ='无新闻分类信息')
    # 定义一个容器，保存查询的数据
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())


    data = {
        'user_info':user.to_dict() if user else None,
        'news_dict_list':news_dict_list,
        'category_list':category_list
    }

    return render_template('news/index.html',data=data)

# 加载项目小图标
@news_blue.route('/favicon.ico')
def favicon():
    # 静态路径访问的默认实现，send_static_file
    # 把静态文件发送给浏览器
    return current_app.send_static_file('news/favicon.ico')