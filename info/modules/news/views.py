from flask import session,render_template,current_app,jsonify,request,g
# 导入蓝图对象
from . import news_blue
# 导入模型类User 和 News
from info.models import User,News,Category
# 导入自定义状态码
from info.utils.response_code import RET
# 导入常量定义文件
from info import constants,db
# 导入自定义的登陆验证装饰器
from info.utils.commons import login_required
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

# 新闻列表数据的显示　
@news_blue.route('/news_list')

def get_news_list():
     cid = request.args.get('cid','1')
     page = request.args.get('page','1')
     per_page = request.args.get('per_page','10')
     try:
        cid,page,per_page  = int(cid),int(page),int(per_page)
     except Exception as e:
         current_app.logger.error(e)
         return jsonify(errno =RET.PARAMERR,errmsg ='参数格式错误')
     # 根据分类id查询数据库
     filters = []
     # 此处将查询到的所有数据显示在更新页面上，当id = 1
     # 当id > 1时，查询的是其他分类的内容
     if cid >1:
         filters.append(News.category_id == cid)
     try:
         # 默认按照新闻分类进行过滤，按照新闻发布时间倒序排序，分页每页10条
         paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,constants.HOME_PAGE_MAX_NEWS,False)
     except Exception as e:
         current_app.logger.error(e)
         return jsonify(errno =RET.DBERR,errmsg ='数据库访问失败')

     news_list = paginate.items
     total_page = paginate.pages
     current_page = paginate.page
     # 定义容器，遍历分页后的新闻对象，转成字典
     news_dict_list = []
     for news in news_list:
         news_dict_list.append(news.to_dict())
     data ={
         'news_dict_list':news_dict_list,
         'total_page':total_page,
         'current_page':current_page
     }
     # 返回结果
     return jsonify(errno =RET.OK,errmsg ='OK',data = data)

# 新闻页面详情加载，需要自定义一个装饰器
@news_blue.route('/<int:news_id>')
# 添加登陆验证装饰器
@login_required
def get_news_detail(news_id):
    # 使用g 对象保存程序运行过程中的临时数据
    user = g.user
    # 一般情况下，用户未登陆时，也是可以访问详细信息，收藏时，需要用户必须登陆
    if not user:
        return jsonify(errno =RET.SESSIONERR,errmsg ='用户未登陆')
    # 使用news_id 查询数据库
    try:
        news = News.query.get(news_id)
    except Exception as  e:
        current_app.logger.error(e)
        return jsonify(errno =RET.DBERR,errmsg ='新闻查询失败')
    if not news:
        return jsonify(errno =RET.NODATA,errmsg ='未查询到新闻的详细信息')
    # 新闻的点击量加　１
    news.clicks += 1
    try:
        # 新闻点击量保存到数据库中，可以设置自动提交
        db.session.add(news)
        db.session.commit()
    except  Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno =RET.DBERR,errmsg ='保存数据失败')
    data = {
        # 'user':user.to_dict() if user else None,
        'news':news.to_dict()
    }
    # 返回新闻的详细数据
    return render_template('news/detail.html',data = data)
# 加载项目小图标
@news_blue.route('/favicon.ico')
def favicon():
    # 静态路径访问的默认实现，send_static_file
    # 把静态文件发送给浏览器
    return current_app.send_static_file('news/favicon.ico')