from flask import Blueprint
from decorators import login_required
from models import User,Question,Answer,Worker,Cooperation,Workshop,Product,Warehouse,Produce,Order,Attendance,Performance,Store,Order_product
from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from exts import db
from sqlalchemy import and_,or_
forum_bp = Blueprint('forum',__name__) #url_prefix url前缀 template_folder static_folder

@forum_bp.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('forum/question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@forum_bp.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content = content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id==question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('forum.detail',question_id=question_id))


#详情页面
@forum_bp.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    length = len(question_model.answers)
    return render_template('forum/detail.html',question=question_model,length=length)


