from flask import Blueprint
from decorators import login_required
from models import User,Question,Answer,Worker,Cooperation,Workshop,Product,Warehouse,Produce,Order,Attendance,Performance,Store,Order_product
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,json,Response
from exts import db
from sqlalchemy import and_,or_
from myutils import *
dbOption_bp = Blueprint('db_options',__name__) #url_prefix url前缀 template_folder static_folder

@dbOption_bp.route('/management',methods=['GET','POST'])
@login_required
def factory_management():
        select = request.args.get("select")
        if select == '1':
            user_id = session['user_id']
            if not user_id == 99999:
                return render_template('BOSS/factory_management.html', warning=True,msg="对不起，您没有操作权力~")
            else:
                return render_template('BOSS/select.html')

        elif select == '2':
            user_id = session['user_id']
            if not user_id == 99999:
                return render_template('BOSS/factory_management.html',warning=True,msg="对不起，您没有操作权力~")
            else:
                return render_template('BOSS/update.html')

        elif select == '3':
            user_id = session['user_id']
            if not user_id == 99999:
                return render_template('BOSS/factory_management.html', warning=True,msg="对不起，您没有操作权力~")
            else:
                return render_template('BOSS/insert.html')

        else:
            return render_template('BOSS/factory_management.html', warning=False)


@dbOption_bp.route('/delete',methods=['GET','POST'])
def deleteItem():
    deleteOption = request.form["type"]
    if deleteOption == "worker":
        workerID = request.form["workerID"]
        try:
            if workerID:
                workerID = int(workerID)
            worker = Worker.query.filter(Worker.worker_id == workerID).first()
            db.session.delete(worker)
            db.session.commit()
            return jsonify({'status':'200','msg':'删除员工成功！'})
        except:
            db.session.rollback()
            return jsonify({'status':'400','msg':'删除员工失败，请重新尝试或和管理员咨询！'})
    elif deleteOption == "order":
        orderNum = request.form['orderNum']
        if orderNum:
            orderNum = int(orderNum)
        order = Order.query.filter(Order.order_num == orderNum).first()
        try:
            db.session.delete(order)
            db.session.commit()
            return jsonify({"status": "200", "msg": "删除订单成功！"})
        except:
            db.session.rollback()
            return jsonify({"status": "400", "msg": "删除订单失败，请重新尝试或和管理员咨询！"})
    elif deleteOption == "cooperation":
        name = ''
        name = request.form["companyName"]
        print(name)
        cooperation = Cooperation.query.filter(Cooperation.company == name).first()
        try:
            db.session.delete(cooperation)
            db.session.commit()
            return jsonify({"status": "200", "msg": "删除顾客成功！"})
        except:
            db.session.rollback()
            return jsonify({"status": "400", "msg": "删除顾客失败，请重新尝试或和管理员咨询！"})
    elif deleteOption == "product":
        product_id = request.form["productId"]
        print(product_id)
        product = Product.query.filter(Product.product_id == product_id).first()
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"status": "200", "msg": "删除产品成功！"})
        except:
            db.session.rollback()
            return jsonify({"status": "400", "msg": "删除产品失败，请重新尝试或和管理员咨询！"})




@dbOption_bp.route('/select',methods=['GET','POST'])
def select_in_db():
    select = request.form["select"]
    print(select)
    if select == "worker":
        worker_type = request.form["staff_type"]
        if worker_type=="":
            jsonify({"status": "400", "msg": "员工编号是必填选项！"})
        worker_age = request.form["staff_age"]
        if worker_age:
            worker_age = int(worker_age)
        worker_workshop = request.form["staff_car_room"]
        if worker_workshop:
            worker_workshop = int(worker_workshop)
        if worker_age and worker_workshop:
            print(1)
            staffs = Worker.query.filter(Worker.work_type == worker_type, Worker.age == worker_age,
                                         Worker.workshop_id == worker_workshop)
        elif worker_age:
            print(2)
            staffs = Worker.query.filter(Worker.work_type == worker_type, Worker.age == worker_age)
        elif worker_workshop:
            print(3)
            staffs = Worker.query.filter(Worker.work_type == worker_type, Worker.workshop_id == worker_workshop)
        else:
            print(4)
            staffs = Worker.query.filter(Worker.work_type == worker_type)
        staffs = to_json(staffs)
        return Response(json.dumps(staffs),mimetype='application/json')

    if select == 'order':
        time = request.form["time"]
        customer = request.form["customer"]
        if time and customer:
            orders = Order.query.filter(Order.order_data == time, Order.company == customer)
        elif time:
            orders = Order.query.filter(Order.order_data == time)
        else:
            orders = Order.query.filter(Order.company == customer)
        orders = to_json(orders)
        return jsonify(orders)

    if select == 'workshop':
        workshop_id = request.form["workshopID"]
        if workshop_id:
            workshop_id = int(workshop_id)
        workshops = Workshop.query.filter(Workshop.workshop_id == workshop_id)
        workshops = to_json(workshops)
        return  Response(json.dumps(workshops),mimetype='application/json')

    if select == 'cooperation':
        company = request.form["companyName"]
        cooperations = Cooperation.query.filter(Cooperation.company == company)
        cooperations = to_json(cooperations)
        return Response(json.dumps(cooperations), mimetype='application/json')

    if select == 'product':
        product_id = request.form["product_id"]
        if product_id:
            product_id = int(product_id)
        products = Product.query.filter(Product.product_id == product_id)
        products = to_json(products)
        return Response(json.dumps(products), mimetype='application/json')

    if select == 'produce':
        workshop_id = request.form["workShopID"]
        if workshop_id:
            workshop_id = int(workshop_id)
        produces = Produce.query.filter(Produce.workshop_id == workshop_id)
        produces = to_json(produces)
        all_products = []
        for produce in produces:
            productId = int(produce['product_id'])
            products = Product.query.filter(Product.product_id == productId)
            products = to_json(products)
            all_products.extend(products)
        return Response(json.dumps(all_products), mimetype='application/json')

    if select == 'orderProduct':
        order_id = request.form["orderNum"]
        if order_id:
            order_id = int(order_id)
        order_products = Order_product.query.filter(Order_product.order_id == order_id)
        order_products = to_json(order_products)
        all_products = []
        for orderProduct in order_products:
            productId = int(orderProduct['product_id'])
            products = Product.query.filter(Product.product_id == productId)
            products = to_json(products)
            all_products.extend(products)
        return Response(json.dumps(all_products), mimetype='application/json')


@dbOption_bp.route('/insert/<insert_id>/',methods=['GET','POST'])
def insert_in_db(insert_id):
    if request.method == 'POST':
        if insert_id == '1':
            try:
                id = int(request.form.get('worker_id'))
                name = request.form.get('worker_name')
                id_card = request.form.get('id_card_no')
                age = int(request.form.get('age'))
                sex = request.form.get('sex')
                tel = request.form.get('telephone')
                address = request.form.get('address')
                salary = int(request.form.get('salary'))
                type = request.form.get('worker_type')
                workshop_id = int(request.form.get('workshop_id'))
                worker = Worker(worker_id=id, name=name, id_card_NO=id_card, age=age, sex=sex, contart_info=tel,
                                address=address, salary=salary, work_type=type, workshop_id=workshop_id)
                db.session.add(worker)
                db.session.commit()
                return render_template('BOSS/insert.html',success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html', success=False,msg="输入有误，添加失败~")
        elif insert_id == '2':
            try:
                id = int(request.form.get('order-num'))
                company = request.form.get('company')
                date = request.form.get('order_data')
                delivery_date = request.form.get('delivery_date')
                order_state = request.form.get('order_state')
                order = Order(order_num=id, company=company, order_date=date, delivery_data=delivery_date,
                              delivery_state=order_state)
                db.session.add(order)
                db.session.commit()
                return render_template('BOSS/insert.html',success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html', success=False,msg="输入有误，添加失败~")
        elif insert_id == '3':
            try:
                workshop_id = int(request.form.get('workshop_id'))
                director_id = int(request.form.get('director_id'))
                tel = request.form.get('telephone')
                workshop = Workshop(workshop_id=workshop_id, director_id=director_id, telephone=tel)
                db.session.add(workshop)
                db.session.commit()
                return render_template('BOSS/insert.html',success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html', success=False,msg="输入有误，添加失败~")
        elif insert_id == '4':
            try:
                company_name = request.form.get('company-name')
                name = request.form.get('name')
                tel = request.form.get('telephone')
                address = request.form.get('address')
                cooperation = Cooperation(company=company_name, contact_info=tel, name=name, address=address)
                db.session.add(cooperation)
                db.session.commit()
                return render_template('BOSS/insert.html', success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html', success=False,msg="输入有误，添加失败~")

        elif insert_id == '5':
            try:
                product_id = int(request.form.get('product-id'))
                product_name = request.form.get('product-name')
                price = int(request.form.get('price'))
                reward = int(request.form.get('reward'))
                output = int(request.form.get('output'))
                product = Cooperation(product_id=product_id,product_name=product_name,
                                      price=price,reward=reward,output=output)
                db.session.add(product)
                db.session.commit()
                return render_template('BOSS/insert.html', success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html',success=False,msg="输入有误，添加失败~")

        elif insert_id == '6':
            try:
                warehouse_id = int(request.form.get('warehouse-id'))
                worker_id = int(request.form.get('worker-id'))
                tel = request.form.get('telephone')
                warehouse = Warehouse(warehouse_id=warehouse_id,worker_id=worker_id,
                                      telephone=tel)
                db.session.add(warehouse)
                db.session.commit()
                return render_template('BOSS/insert.html', success=True,msg="添加成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/insert.html', success=False,msg="输入有误，添加失败~")
    else:
        pass



@dbOption_bp.route('/update/<update_id>/',methods=['GET','POST'])
def update_in_db(update_id):
    if request.method == 'POST':
        if update_id == '1':
            try:
                id = request.form.get('worker_id')
                if id:
                    id = int(id)
                else:
                    return render_template('BOSS/update.html', success=False, msg="请输入员工编号~")
                new_age = request.form.get('new_age')
                new_tel = request.form.get('new_tel')
                new_addr = request.form.get('new_addr')
                new_salary = request.form.get('new_salary')
                new_type = request.form.get('new_type')
                workshop_id = request.form.get('new_workshop')
                worker = Worker.query.filter(Worker.worker_id == id).first()
                if new_age:
                    worker.age = int(new_age)
                if new_tel:
                    worker.contart_info = new_tel
                if new_addr:
                    worker.address = new_addr
                if new_salary:
                    worker.salary = int(new_salary)
                if new_type:
                    worker.work_type = new_type
                if workshop_id:
                    worker.workshop_id = int(workshop_id)
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新数据成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入信息有误，更新数据失败~")

        elif update_id == '2':
            try:
                workshop_id = request.form.get('workshop_id')
                if workshop_id:
                    workshop_id = int(workshop_id)
                else:
                    return render_template('BOSS/update.html', success=False, msg="请输入车间号~")
                new_dir = request.form.get('new_dir')
                new_tel = request.form.get('new_tel')
                workshop = Workshop.query.filter(Workshop.workshop_id == workshop_id).first()
                pre_dir = int(workshop.director_id)
                if new_dir:
                    workshop.director_id = int(new_dir)
                    worker1 = Worker.query.filter(Worker.worker_id == pre_dir).first()
                    worker1.work_type = "员工"
                    worker2 = Worker.query.filter(Worker.worker_id == int(new_dir)).first()
                    worker2.work_type = "车间主任"
                if new_tel:
                    workshop.telephone = new_tel
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新信息成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入有误，更新失败~")

        elif update_id == '3':
            try:
                company = request.form.get('company')
                new_tel = request.form.get('new_tel')
                new_name = request.form.get('new_name')
                new_addr = request.form.get('new_addr')
                cooperation = Cooperation.query.filter(Cooperation.company == company).first()
                if new_tel:
                    cooperation.contact_info = new_tel
                if new_name:
                    cooperation.name = new_name
                if new_addr:
                    cooperation.address = new_addr
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新信息成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入有误，更新失败~")

        elif update_id == '4':
            try:
                product_id = request.form.get('product_id')
                if product_id:
                    product_id = int(product_id)
                else:
                    return render_template('BOSS/update.html', success=False, msg="请输入产品编号~")
                product_name = request.form.get('product_name')
                price = request.form.get('price')
                reward = request.form.get('reward')
                output = request.form.get('output')
                product = Product.query.filter(Product.product_id == product_id).first()
                if product_name:
                    product.product_name = product_name
                if price:
                    product.price = int(price)
                if reward:
                    product.reward = int(reward)
                if output:
                    product.output = int(output)
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新信息成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入有误，更新失败~")

        elif update_id == '5':
            try:
                order_num = request.form.get('order_num')
                if order_num:
                    order_num = int(order_num)
                else:
                    return render_template('BOSS/update.html', success=False, msg="请输入订单编号~")
                order_date = request.form.get('order_date')
                delivery_date = request.form.get('delivery_date')
                order_state = request.form.get('order_state')
                order = Order.query.filter(Order.order_num == order_num).first()
                if order_date:
                    order.order_data = order_date
                if delivery_date:
                    order.delivery_data = delivery_date
                if order_state:
                    order.delievry_state = order_state
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新信息成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入有误，更新失败~")

        elif update_id == '6':
            try:
                warehouse_id = request.form.get('warehouse_id')
                if warehouse_id:
                    warehouse_id = int(warehouse_id)
                else:
                    return render_template('BOSS/update.html', success=False, msg="输入有误，更新失败~")
                worker_id = request.form.get('worker_id')
                telephone = request.form.get('tel')
                warehouse = Warehouse.query.filter(Warehouse.warehouse_id == warehouse_id).first()
                pre_id = warehouse.worker_id
                if worker_id:
                    warehouse.worker_id = worker_id
                    worker1 = Worker.query.filter(Worker.worker_id == pre_id).first()
                    worker1.work_type = "员工"
                    worker2 = Worker.query.filter(Worker.worker_id == int(worker_id)).first()
                    worker2.work_type = "仓库管理员"
                if telephone:
                    warehouse.telephone = telephone
                db.session.commit()
                return render_template('BOSS/update.html', success=True,msg="更新信息成功~")
            except:
                db.session.rollback()
                return render_template('BOSS/update.html', success=False,msg="输入有误，更新失败~")

    else:
        pass

