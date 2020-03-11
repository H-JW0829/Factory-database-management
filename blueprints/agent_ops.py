from flask import Blueprint
from decorators import login_required
from models import User,Question,Answer,Worker,Cooperation,Workshop,Product,Warehouse,Produce,Order,Attendance,Performance,Store,Order_product
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,json,Response
from exts import db
from sqlalchemy import and_,or_
from myutils import *
ag_ops = Blueprint('ag_ops',__name__) #url_prefix url前缀 template_folder static_folder


@ag_ops.route('/agent_management/', methods=['GET', 'POST'])
@login_required
def agent_management():
        select = request.args.get("select")
        user_id = int(session['user_id'])
        worker = Worker.query.filter(Worker.worker_id == user_id).first()
        if select == '1':
            if not (worker.work_type == "车间主任") :
                return render_template('agent/agent_management.html', warning=True,msg="您没有操作的权力~")
            else:
                worker = Worker.query.filter(Worker.worker_id == user_id).first()
                workshop_id = worker.workshop_id
                workshop = Workshop.query.filter(Workshop.workshop_id==workshop_id).first()
                context = {
                    'workshop': workshop
                }
                return render_template('agent/agent_select.html',**context)

        elif select == '2':
            if not (worker.work_type == "车间主任"):
                return render_template('agent/agent_management.html', warning=True,msg="您没有操作的权力~")
            else:
                return render_template('agent/agent_update.html')

        elif select == '3':
            if not (worker.work_type == "车间主任"):
                return render_template('agent/agent_management.html', warning=True,msg="您没有操作的权力~")
            else:
                return render_template('agent/agent_add.html')


        else:
            return render_template('agent/agent_management.html', warning=False)


@ag_ops.route('/update_worker/', methods=['POST'])
def update_worker():
    id = request.form.get('worker_id')
    if id:
        id = int(id)
        user_id = session['user_id']
        agent = Worker.query.filter(Worker.worker_id == user_id).first()
        workshop_id = agent.workshop_id
        workshop = Workshop.query.filter(Workshop.workshop_id == workshop_id).first()
        workers_id = [x.worker_id for x in workshop.workers]
        if id not in workers_id:
            return render_template('agent/agent_update.html', success=False,msg="您不能更新不属于本车间的员工的信息~")
    else:
        return render_template('agent/agent_update.html', success=False,msg="请输入员工编号~")
    try:
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
        return render_template('agent/agent_update.html', success=True,msg="更新成功~")
    except:
        db.session.rollback()
        return render_template('agent/agent_update.html', success=False,msg="更新信息出错，请确保输入无误~")

@ag_ops.route('/add_woker/', methods=['POST'])
def add_worker():
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
        user_id = session['user_id']
        agent = Worker.query.filter(Worker.worker_id == user_id).first()
        workshop_id = agent.workshop_id
        worker = Worker(worker_id=id, name=name, id_card_NO=id_card, age=age, sex=sex, contart_info=tel,
                        address=address,
                        salary=salary, work_type=type, workshop_id=workshop_id)
        db.session.add(worker)
        db.session.commit()
        return render_template('agent/agent_add.html', success=True,msg="添加成功~")
    except:
        db.session.rollback()
        return render_template('agent/agent_add.html', success=False,msg="添加失败，请确保输入信息无误~")



@ag_ops.route('/warehouse',methods = ['GET', 'POST'])
@login_required
def warehouse_show():
        return render_template('warehouse_management.html', show=False)

@ag_ops.route('/delete_store',methods=['GET'])
def delete_store():
    productID = request.args.get('productID')
    warehouseID = request.args.get('warehouseID')
    if productID:
        productID = int(productID)
    if warehouseID:
        warehouseID = int(warehouseID)
    try:
        store = Store.query.filter(and_(Store.product_id==productID,Store.warehouse_id==warehouseID)).first()
        db.session.delete(store)
        db.session.commit()
        return jsonify({'status': '200', 'msg': '删除成功！'})
    except:
         db.session.rollback()
         return jsonify({'status': '400', 'msg': '删除出错，请稍后尝试或者联系管理员！'})


@ag_ops.route('/getstore', methods=['GET', 'POST'])
def getstore():
    print("来了老弟")
    user_id = session['user_id']
    print(type(user_id))
    try:
        warehouses = Warehouse.query.filter(Warehouse.worker_id == user_id)
        stores = Store.query.filter(Store.warehouse_id == warehouses[0].warehouse_id)
        worker = Worker.query.filter(Worker.worker_id == warehouses[0].worker_id)
        worker = to_json(worker)
        warehouses = to_json(warehouses)
        stores = to_json(stores)
        temp = warehouses[0]
        temp["name"] = worker[0]["name"]
        data = []
        data.append({'status': '200'})
        for i in range(len(stores)):
            productId = stores[i]["product_id"]
            product = Product.query.filter(Product.product_id == productId)
            product = to_json(product)
            temp["product_name"] = product[0]['product_name']
            data.append(dict(stores[i],**temp))
        print(data)
        return Response(json.dumps(data),mimetype='application/json')
        #products = Product.query.filter(Product.product_id == stores.product_id)
        #products = to_json(products)
    except:
    #      print("except")
          return jsonify([{'status': '400', 'msg': '您没有查看的权力！'}])
    # if request.method == 'GET':
    #     if id == '1':
    #         global stores
    #         if go_on_select == '1':
    #             user_id = session['user id']
    #             warehouse = Warehouse.query.filter(Warehouse.worker_id == user_id).first()
    #             try:
    #                 stores = Store.query.filter(Store.warehouse_id == warehouse.warehouse_id)
    #                 context = {
    #                     'stores': stores.paginate(page, 10, False)
    #                 }
    #                 return render_template('warehouse_management.html', **context, show=True, show_no=1)
    #             except:
    #                 return '您没有查看权利！'
    #         else:
    #             context = {
    #                 'stores': stores.paginate(page, 10, False)
    #             }
    #             return render_template('warehouse_management.html', **context, show=True, show_no=1)
    #
    #     if id == '2':
    #         global products
    #         if go_on_select == '1':
    #             user_id = session['user id']
    #             warehouse = Warehouse.query.filter(Warehouse.worker_id == user_id).first()
    #             try:
    #                 stores = Store.query.filter(and_(Store.warehouse_id == warehouse.warehouse_id,Store.quantity<=3))
    #                 context = {
    #                     'stores': stores.paginate(page, 10, False)
    #                 }
    #                 return render_template('warehouse_management.html', **context, show=True, show_no=2)
    #             except:
    #                 return '您没有查看权利！'
    #         else:
    #             context = {
    #                 'stores': stores.paginate(page, 10, False)
    #             }
    #             return render_template('warehouse_management.html', **context, show=True, show_no=2)

@ag_ops.route('/delete_woker/', methods=['POST'])
def delete_worker():
    id = ''
    id = request.form.get('worker_id')
    if id:
        id = int(id)
    user_id = session['user_id']
    agent = Worker.query.filter(Worker.worker_id == user_id).first()
    workshop_id = agent.workshop_id
    workshop = Workshop.query.filter(Workshop.workshop_id == workshop_id).first()
    workers_id = [x.worker_id for x in workshop.workers]
    if id not in workers_id:
        return render_template('agent/agent_delete.html', update=False)
    worker = Worker.query.filter(Worker.worker_id == id).first()
    try:
        db.session.delete(worker)
        db.session.commit()
        return render_template('BOSS/delete.html', success=True)
    except:
        db.session.rollback()
        return render_template('BOSS/delete.html', delete=False)

@ag_ops.route('/search_1',methods=['POST','GET'])
def search():
    search = request.args.get('search')
    print("----------")
    print(search)
    print("----------")
    user_id = session['user_id']
    agent = Worker.query.filter(Worker.worker_id == user_id).first()
    workshop_id = agent.workshop_id
    if search == "all":
        workers = Worker.query.filter(Worker.workshop_id == workshop_id)
        workers = to_json(workers)
        return Response(json.dumps(workers),mimetype='application/json')
    else:
        q = request.args.get('name')
        target =  Worker.query.filter(and_(Worker.name.contains(q),Worker.workshop_id==workshop_id)).all()
        target = to_json(target)
        print(target)
        return Response(json.dumps(target),mimetype='application/json')

@ag_ops.route('/agentdelete',methods=['POST','GET'])
def agentDelete():
    workerID = request.args.get('workerID')
    try:
        if workerID:
            workerID = int(workerID)
        worker = Worker.query.filter(Worker.worker_id == workerID).first()
        db.session.delete(worker)
        db.session.commit()
        return jsonify({'status': '200', 'msg': '删除员工成功！'})
    except:
        db.session.rollback()