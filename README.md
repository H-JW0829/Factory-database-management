# Factory-database-management
实现了一个基于python的flask框架设计的前后端不分离的工厂数据库管理系统，前端部分用到了js、vue、jq的相关知识，后端用flask蓝图管理视图函数，数据库采用MySQL，用到了Bootstrap美化界面<br/>
主要实现的功能：<br/>
1.工厂内的所有人都可以注册一个账号，实现登录、个人中心的功能，在个人中心可以修改个人的基本信息，查看个人绩效和考勤情况，非登录状态下只能浏览首页，无法查看详情和发布问答<br/>
2.实现了一个工厂论坛，可以在上面发表问题和添加评论，导航栏有搜索框，可以根据关键字找到相应的问题<br/> 
3.厂长可以对工厂的员工、订单、顾客、产品、车间产品等信息进行查询、删除、更新、添加的功能<br/>
4.车间主任可以对本车间的员工进行查询、删除、添加、更新的功能  5.仓库管理员可以对本仓库的产品进行查询，同时可以查看库存不足的产品<br/>

文件结构：<br/>
1.blueprints文件夹：蓝图管理，存放视图函数<br/>
2.migrations文件夹：数据库迁移<br/>
3.static文件夹：存放静态文件<br/>
4.templates文件夹：存放html模板<br/>
5.config文件：连接数据库，配置基本信息<br/>
6.decorators文件：存装饰器（主要实现的是查看详情前要登录）<br/>
7.exts：数据库初始化<br/>
8.main：主app文件<br/>
9.manage：数据库迁移管理<br/>
10.models：创建数据库表<br/>
11.myutils：一些有用的函数<br/>


部分效果截图<br/>
①登录注册界面：
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/1.png)
②首页
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/2.png)
③问答详情页，可以添加评论
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/3.png)
④可以发布问题
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/6.png)
⑤个人中心可以查看个人基本信息、考勤、绩效，双击个人基本信息可以修改
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/4.png)
⑥可以在管理界面按信息查找
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/5.png)
⑦对查找的信息可以进行操作
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/7.png)
⑧可以添加信息（这个功能实现的说实话还不是很方便）
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/8.png)
⑨车间主任可以按姓名精确查找
![image](https://github.com/H-JW0829/Factory-database-management/blob/master/images/9.png)

