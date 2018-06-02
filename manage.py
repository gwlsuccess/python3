from flask import session
# 导入　flask_scrip　管理器，在终端执行程序
from flask_script import Manager
# 导入迁移扩展包和迁移命令
from flask_migrate import Migrate,MigrateCommand

# 导入info模块创建实例对象app
from info import create_app,db
app = create_app('development')

# 实例化管理器对象
manager = Manager(app)
# 使用迁移框架
Migrate(app,db)
# 通过管理器对象集成迁移命令
manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    # 请求对象session
    session['name']=2018
    return 'index'

if __name__ == '__main__':
    # app.run(debug=True)
    # 必须配置项目参数　runserver
    manager.run()