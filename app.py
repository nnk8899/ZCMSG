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
import sys_util


class addForm(FlaskForm):
    add_num = IntegerField(u'*模板编号',validators = [DataRequired()])
    add_theme = StringField(u'*模板主题',validators = [DataRequired()])
    add_contains = TextAreaField(u'*模板内容', validators=[DataRequired()])
    add_details = TextAreaField	(u'备注')
    add_submit = SubmitField(u'提交')


class editForm(FlaskForm):
    edit_theme = StringField(u'*模板主题',validators = [DataRequired()], default="XX")
    edit_contains = TextAreaField(u'*模板内容', validators=[DataRequired()])
    edit_details = TextAreaField	(u'备注')
    edit_submit = SubmitField(u'提交')


def link_sql():
    c = sys_util.get_sql_config()
    # database, _host, _port, _user, _pwd
    host = c[1]
    user = c[3]
    password = c[4]
    database = c[0]
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
    sql = "select * from [dbo].[prototype] order by num asc"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('prototypeEditor.html', u=u)


@app.route('/addProto', methods=['GET', 'POST'])
def add_prototype():
    CSRF_ENABLED = True
    app.config["SECRET_KEY"] = "12345678"
    form = addForm(request.form)
    if request.method == 'POST' and form.validate():
        conn = link_sql()
        cursor1 = conn.cursor()
        sql1 = 'insert into [dbo].[prototype] values(' + to_standard(form.add_num.data) + ',' + to_standard(form.add_theme.data) + ',' + to_standard(form.add_contains.data) + ',' + to_standard(form.add_details.data) + ')'
        cursor1.execute(sql1)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/prototypeEditor')
    return render_template('addProto.html', form=form)


@app.route('/editProto/<id>', methods=['GET','POST'])
def editProto(id):
    conn = link_sql()
    cur = conn.cursor()
    sql = "select * from [dbo].[prototype] where num=" + to_standard(id)
    cur.execute(sql)
    l = cur.fetchall()
    conn.close()
    CSRF_ENABLED = True
    app.config["SECRET_KEY"] = "87654321"
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        curr_theme = form.edit_theme.data
        curr_contains = form.edit_contains.data
        curr_details = form.edit_details.data
        conn = link_sql()
        cursor2 = conn.cursor()
        sql2 = 'update [dbo].[prototype] set theme=' + to_standard(curr_theme) + ',contain=' + to_standard(curr_contains) + ',details=' + to_standard(curr_details) + 'where num = ' + to_standard(id)
        cursor2.execute(sql2)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/prototypeEditor')
    form.edit_theme.data = l[0][1]
    form.edit_contains.data = l[0][2]
    form.edit_details.data = l[0][3]
    return render_template('editProto.html', form=form, id=id)



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('homePage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=9000)
