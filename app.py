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
    add_name = StringField(u'*模板名称',validators = [DataRequired()])
    add_type = StringField(u'*模板主题', validators=[DataRequired()])
    add_content = TextAreaField(u'*模板内容', validators=[DataRequired()])
    add_comment = TextAreaField	(u'备注')
    add_submit = SubmitField(u'提交')


class editForm(FlaskForm):
    edit_name = StringField(u'*模板名称', validators=[DataRequired()])
    edit_type = StringField(u'*模板主题', validators=[DataRequired()])
    edit_content = TextAreaField(u'*模板内容', validators=[DataRequired()])
    edit_comment = TextAreaField	(u'备注')
    edit_submit = SubmitField(u'提交')


class deleteForm(FlaskForm):
    delete_check = SubmitField(u'确认删除')


def link_sql():
    c = sys_util.get_sql_config("config/SQLConfig.config")
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
    sql = "select * from [dbo].[prototype] order by id asc"
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
        sql1 = 'insert into [dbo].[prototype] (name,content,comment) values(' + to_standard(form.add_name.data) + ',' + to_standard(form.add_content.data) + ',' + to_standard(form.add_comment.data) + ')'
        cursor1.execute(sql1)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/prototypeEditor')
    return render_template('addProto.html', form=form)


@app.route('/editProto/<id>', methods=['GET','POST'])
def editProto(id):
    conn = link_sql()
    cur = conn.cursor()
    sql = "select * from [dbo].[prototype] where id=" + to_standard(id)
    cur.execute(sql)
    l = cur.fetchall()
    conn.close()
    CSRF_ENABLED = True
    app.config["SECRET_KEY"] = "87654321"
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        curr_name = form.edit_name.data
        curr_type = form.edit_type.data
        curr_content = form.edit_content.data
        curr_comment = form.edit_comment.data
        conn = link_sql()
        cursor2 = conn.cursor()
        sql2 = 'update [dbo].[prototype] set name=' + to_standard(curr_name) + ',content=' + to_standard(curr_content) + ',comment=' + to_standard(curr_comment) + 'where id = ' + to_standard(id)
        cursor2.execute(sql2)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/prototypeEditor')
    form.edit_name.data = l[0][1]
    form.edit_type.data =l[0][2]
    form.edit_content.data = l[0][3]
    form.edit_comment.data = l[0][4]
    return render_template('editProto.html', form=form, id=id)


@app.route('/deleteProto/<id>', methods=['GET','POST'])
def deleteProto(id):
    CSRF_ENABLED = True
    app.config["SECRET_KEY"] = "123456"
    form = deleteForm(request.form)
    if request.method == 'POST' and form.validate():
        conn = link_sql()
        cursor3 = conn.cursor()
        sql3 = 'delete from [dbo].[prototype] where id = ' + to_standard(id)
        cursor3.execute(sql3)
        conn.commit()
        conn.close()
        return redirect('http://localhost:9000/prototypeEditor')
    return render_template('deleteProto.html', form=form, id=id)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('homePage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=9000)
