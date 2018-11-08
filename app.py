from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import BooleanField, StringField, PasswordField, SelectField, RadioField, SubmitField, IntegerField, TextAreaField, validators
from wtforms.validators import Length, DataRequired
from flask_wtf import Form,FlaskForm
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_admin.form import widgets

import os
import pymssql
import sys_logger


class addForm(Form):
    add_num = IntegerField(u'*模板编号',validators = [DataRequired()])
    add_theme = StringField(u'*模板主题',validators = [DataRequired()])
    add_contains = StringField(u'*模板内容', validators=[DataRequired()])
    add_details = StringField(u'备注')
    add_submit = SubmitField(u'提交')


def link_sql():
    host = 'LAPTOP-GPKFSA00'
    user = 'sa'
    password = 'xyt555'
    database = 'msg'
    conn = pymssql.connect(host, user, password, database, charset='cp936')
    return conn


def to_standard(var):
	standard_var = "'"+str(var)+"'"
	return standard_var





app = Flask(__name__)
logger = sys_logger.get_logger(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    logger.debug("Index page.")
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/menuBar', methods=['GET', 'POST'])
def menu_bar():
    return render_template('menuBar.html')


@app.route('/prototypeEditor', methods=['GET', 'POST'])
def prototype_editor():
    conn = link_sql()
    cur = conn.cursor()
    sql = "select * from [dbo].[prototype]"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('prototypeEditor.html', u=u)


@app.route('/addProto', methods=['GET', 'POST'])
def add_prototype():
    form = addForm(request.form)
    if request.method == 'POST' and form.validate():
        conn = link_sql()
        cursor1 = conn.cursor()
        sql1 = 'insert into [dbo].[prototype] values(' + form.add_num.data + ',' + to_standard(form.add_theme.data) + ',' + to_standard(form.add_contains.data) + ',' + to_standard(form.add_details.data) + ')'
        cursor1.execute(sql1)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/logout')
    return render_template('addProto.html', form=form)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('homePage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=9000)
