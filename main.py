from flask import Flask,render_template,request,session
import config
from models import User,Question
from exts import db
from sqlalchemy import and_,or_
from blueprints.myutils import utils_bp
from blueprints.forum import forum_bp
from blueprints.fm_options import dbOption_bp
from blueprints.agent_ops import ag_ops
import os
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
#注册蓝图
app.register_blueprint(utils_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(dbOption_bp)
app.register_blueprint(ag_ops)
app.config.from_object(config)
db.init_app(app)


@app.route('/', methods = ['GET', 'POST'])      #首页
@app.route('/index',methods = ['GET', 'POST'])
@app.route('/index/<int:page>',methods = ['GET', 'POST'])
def index(page=1):
    if request.method == 'GET':
        context = {
            'questions': Question.query.order_by(-Question.create_time).paginate(page,5,False) #当前页数，每页获取5条数据，是否打印错误信息
        }
        return render_template('forum/index.html',**context)
    else:
        words = request.form.get('words')  #获取搜素关键字
        questions = Question.query.filter(or_(Question.title.contains(words),Question.content.contains(words))).order_by(-Question.create_time)
        context = {
            'questions': questions.paginate(page, 5, False)
        }
        return render_template('forum/index.html', **context)

@app.context_processor
def my_content_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
