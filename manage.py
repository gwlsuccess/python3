from flask import Flask
from flask_script import Manager
from config import Config
app=Flask(__name__)

app.config.from_object(Config)

manager = Manager(app)

@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    # app.run(debug=True)
    # 必须配置项目参数　runserver
    manager.run()