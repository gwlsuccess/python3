from . import passport_blu
from flask import request,jsonify,current_app,make_response,session
#　导入自定义状态码
from info.utils.response_code import RET
from info.utils.captcha.captcha import captcha
from info import redis_store,constants,db
import re
from info.models import User
import random
from info.libs.yuntongxun import sms

@passport_blu.route('/image_code')
def image_code_id():
    # 创建图片验证码生成过程
    image_code_id = request.args.get('image_code_id')
    if not image_code_id:
        return jsonify(errno=RET.PARAMERR,errmsg='参数缺失')
    name,text,image = captcha.generate_captcha()
    print(text)
    try:
        #　保存图片验证码的内容　text 到 redis
        redis_store.setex('ImageCode_'+ image_code_id,
                          constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg = '保存图片验证码失败')
    else:
        # 将图片本身作为响应对象发送给客户端
        response = make_response(image)
        response.headers['Content-Type'] = 'image/jpg'
        return response

@passport_blu.route('/sms_code',methods=['POST'])

def send_sms_code():
    mobile = request.json.get('mobile')
    image_code = request.json.get('image_code')
    image_code_id = request.json.get('image_code_id')
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    if not re.match(r'^1[3456789]\d{9}$',mobile):
        return jsonify(errno=RET.PARAMERR,errmsg='手机号不符合格式')
    try:
        real_image_code = redis_store.get('ImageCode_'+ image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='获取图片验证码失败')
    if not real_image_code:
        return jsonify(errno=RET.NODATA,errmsg='图片验证码已过期')
    try:
        #　删除数据
        redis_store.delete('ImageCode_'+ image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    if real_image_code.lower() != image_code.lower():
        return  jsonify(errno=RET.DATAERR,errmsg='图片验证码不一致')
    # 查询 mysql 数据库，判断手机号是否已注册
    try:
       user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查询用户信息失败')
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST,errmsg='该手机号已注册')

        sms_code = '%06d'%random.randint(0,999999)
    try:
        redis_store.setex('SMSCode_' + mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存数据失败')
    # 调用云通讯
    try:
        ccp = sms.CCP()
        result = ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信异常')
    if result == 0:
        return jsonify(errno=RET.OK,errmsg='发送成功')
    else:
        return jsonify(errno=RET.THIRDERR, errmsg='发送失败')


#　用户注册视图接口
@passport_blu.route('/register',methods=['POST'])
def regsiter():
    # """
    # 用户注册
    # 1、获取参数，mobile/sms_code/password
    # 2、校验参数的完整性
    # 3、检查手机号的格式
    # 4、短信验证码进行比较
    # 5、尝试从redis数据库中获取真实的短信验证码
    # 6、判断获取结果是否有数据
    # 7、比较短信验证码是否正确
    # 8、如果短信验证码正确，删除redis中的短信验证码
    # 9、验证手机号是否注册
    # 10、构造模型类对象，准备存储用户信息
    # user = User()
    # user.mobile = mobile
    # user.nick_name = mobile
    # 11、需要对密码进行加密存储，
    # user.password = password
    # 12、保存数据到mysql数据库中
    # 13、把用户信息缓存到redis数据库中
    # session['user_id'] = user.id
    # 14、返回结果
    # :return:
    # """
      mobile = request.json.get('mobile')
      sms_code = request.json.get('sms_code')
      password = request.json.get('password')
      if not all([mobile,sms_code,password]):
          return jsonify(errno = RET.PARAMERR,errmsg ='输入的信息不完整')

      if not re.match(r'^1[3456789]\d{9}$', mobile):
          return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

      try:
          real_sms_code = redis_store.get('SMSCode_'+ mobile)
      except Exception as e:
          current_app.logger.error(e)
          return jsonify(errno=RET.DBERR, errmsg='短信验证码查询失败')
      if not real_sms_code:
          return jsonify(errno = RET.NODATA ,errmsg ='短信验证码已过期')
      if real_sms_code != sms_code:
          return jsonify(errno = RET.DATAERR ,errmsg ='短信验证码输入错误')
      # 短信验证码查询，验证成功之后删除
      try:
          redis_store.delete('SMSCode_' + mobile)
      except Exception as e:
          current_app.logger.error(e)
      # 验证用户的手机号是否已注册，根据手机号进行查询mysql数据库,
      try:
          user = User.query.filter_by(mobile = mobile).first()
      except Exception as e:
          current_app.logger.error(e)
          return jsonify(errno = RET.DBERR,errmsg ='查询用户信息失败')
      else:
          if user is None:
              return jsonify(errno = RET.DATAEXIST,errmsg ='该用户已存在')

      #  创建模型类，保存数据到mysql数据库
      user = User()
      # 对用户输入的密码进行加密保存，调用到models.py中的password属性方法进行密码加密
      user.password = password
      user.mobile = mobile
      user.nick_name = mobile
      # 提交用户数据到数据库中
      try:
          db.session.add(user)
          db.session.commit()
      except Exception as e:
          current_app.logger.error(e)
          # 提交数据发生异常时，需要进行回滚
          db.session.rollback()
          return jsonify(errno = RET.DBERR,errmsg ='数据保存失败')
      # 使用session缓存用户信息到redis数据库中
      session['user_id'] = user.id
      session['mobile'] = mobile
      session['nick_name'] = mobile
      return jsonify(errno = RET.OK,errmsg ='注册成功')

# # 登陆用户
# @passport_blu.route('/login',methods= ['POST'])
# def login():