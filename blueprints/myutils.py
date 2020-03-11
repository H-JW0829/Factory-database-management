from flask import Blueprint
from decorators import login_required
from models import User,Question,Answer,Worker,Cooperation,Workshop,Product,Warehouse,Produce,Order,Attendance,Performance,Store,Order_product
from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from exts import db
utils_bp = Blueprint('utils',__name__) #url_prefix url前缀 template_folder static_folder

@utils_bp.route('/usercenter/<user_id>/<tag>')
@login_required
def usercenter(user_id,tag='1'):
    user = Worker.query.filter(Worker.worker_id == user_id).first()
    context = {
        'user': user
    }
    # if request.method == 'GET':
    print(user.attendances)
    if tag == '1':
        return render_template('utils/user_center.html', **context)
    elif tag == '2':
        return render_template('utils/user_center.html', **context)
    else:
        return render_template('utils/user_center.html', **context)


@utils_bp.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('utils/login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            #cookic保存用户信息
            session['user_id'] = user.id
            #在规定天数内都不需要再登录 31天
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('utils/login.html',success=False,msg="您输入的密码不正确，请重新输入~")

@utils_bp.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('utils/regist.html')
    else:
        user_name = request.form.get('username')
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        #手机号码验证，看是否注册过了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return render_template('utils/regist.html',regist_success=False,msg="该手机号码已经注册过了，直接登录吧~")
        else:
            #看密码和确认密码是否相等
            if password != re_password:
                return render_template('utils/regist.html', regist_success=False, msg="两次输入密码不相同，请重新输入~")
            else:
                user = User(telephone=telephone,user_name=user_name,password=re_password)
                db.session.add(user)
                db.session.commit()
                #注册成功 跳转到登录页面
                return redirect(url_for('utils.login'))

#注销
@utils_bp.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('utils.login'))

@utils_bp.route('/updateuser')
def updateUserInfo():
    userid = session.get('user_id')
    name = request.args.get('name')
    idCardNo = request.args.get('idCardNo')
    age = request.args.get('age')
    contartInfo = request.args.get('contartInfo')
    address = request.args.get('address')
    sex = request.args.get('sex')
    worker = Worker.query.filter(Worker.worker_id == userid).first()
    worker.age = age
    worker.name = name
    worker.id_card_NO = idCardNo
    worker.sex = sex
    worker.contart_info = contartInfo
    worker.address = address
    try:
        db.session.commit()
        return jsonify({"status": "200", "msg": "修改信息成功！"})
    except:
        db.session.rollback()
        return jsonify({"status": "200", "msg": "修改信息失败，请确认输入数据无误"})
