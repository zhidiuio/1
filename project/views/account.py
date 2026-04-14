
from flask import Blueprint, request, redirect, render_template, session
from ublit import db

ac = Blueprint('ac', __name__)


@ac.route('/account/login', methods=['GET', 'POST'])
def login():
    # GET请求：显示登录页面
    if request.method == 'GET':
        return render_template("login.html")

    # POST请求：处理登录或注册
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证必填字段
        if not username or not password:
            return render_template('login.html', tis='账号和密码不能为空')

        # ========== 注册 ==========
        if action == '1':
            # 1. 检查用户是否已存在
            existing = db.fetch_one(
                'SELECT id FROM yonghu WHERE usrname = %s',
                [username]
            )
            if existing:
                return render_template('login.html', tis='用户名已存在，请直接登录')

            # 2. 插入新用户
            db.mysql_caozuo(
                'INSERT INTO yonghu (usrname, password) VALUES (%s, %s)',
                [username, password]
            )
            return render_template('login.html', tis='注册成功，请登录')

        # ========== 登录 ==========
        elif action == '2':
            # 1. 查询用户
            data = db.fetch_one(
                'SELECT usrname, password FROM yonghu WHERE usrname = %s AND password = %s',
                [username, password]
            )

            if data:
                # 2. 登录成功，保存session
                session['cookie'] = {
                    'user': data['usrname'],
                    'password': data['password'],
                }
                return redirect('/worker')
            else:
                return render_template('login.html', tis='账号或密码错误')

        else:
            return render_template('login.html', tis='无效的操作类型')



