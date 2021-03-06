from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from werkzeug.utils import secure_filename
from wtforms import BooleanField, StringField, PasswordField, SelectField, RadioField, SubmitField, IntegerField, TextAreaField, validators
from wtforms.validators import Length, DataRequired
from wtforms.fields.html5 import DateField
from flask_wtf import Form,FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_bootstrap import Bootstrap





import os
import pymssql
import sys_logger
import sys_util
import json
import collections
import time
import send_msg
import pandas as pd


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


class excelForm(FlaskForm):
    file = FileField('上传excel文件', validators=[FileRequired(), FileAllowed(['csv','CSV'], 'Excel ONLY!')])
    proto_name = SelectField(u'选择模板', coerce=int, validators=[DataRequired(message=u"模板名称不能为空")])
    excel_submit = SubmitField(u'立即发送')


class deleteForm(FlaskForm):
    delete_check = SubmitField(u'确认删除')


class historyForm(FlaskForm):
    his_tel = StringField(u'手机号')
    his_proto_id = SelectField(u'模板名称', coerce=int)
    his_date = DateField(u'上传时间')
    his_batches = StringField(u'当日批次')
    his_status = IntegerField(u'状态码')#可考虑增设table状态码制成下拉框
    his_submit = SubmitField(u'查询')



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


@app.route('/deleteChecked', methods=['POST'])
def deleteChecked():
    data = json.loads(request.get_data('data').decode('utf8'))
    checkedItem = data["checkedItem"]
    conn = link_sql()
    cursor4 = conn.cursor()
    sql4 = 'delete from [dbo].[prototype] where id in(' + str(checkedItem) + ')'
    cursor4.execute(sql4)
    conn.commit()
    conn.close()
    info = dict()
    info['checkedItem'] = checkedItem
    return jsonify(info)


@app.route("/msgGroup", methods=['POST','GET'])
def msgGroup():
    conn = link_sql()
    cur = conn.cursor()
    sql = "select id,name from [dbo].[prototype] order by id asc"
    cur.execute(sql)
    l = cur.fetchall()
    conn.close()
    #计算正在添加的文件的当日批次
    conn0 = link_sql()
    cur0 = conn0.cursor()
    sql0 = "select max(batches) from [dbo].[upload_details] where CONVERT(varchar,create_time,112)=CONVERT(varchar,GETDATE(),112)"
    cur0.execute(sql0)
    b = cur0.fetchall()
    conn0.close()
    if b[0][0] is not None:
        curr_batches = b[0][0] + 1
    else:
        curr_batches = 1
    form = excelForm()
    form.proto_name.choices = [(i[0],i[1]) for i in l]
    if request.method == 'POST':
        filename = form.file.data.filename
        print(filename)
        form.file.data.save('D:/msg_box/' + filename)
        conn1 = link_sql()
        cur1 = conn1.cursor()
        sql1 = "select content from [dbo].[prototype] where id=" + str(form.proto_name.data)
        cur1.execute(sql1)
        k = cur1.fetchall()
        conn1.close()
        #计算模板中的占位符个数
        proto_var_num = int(collections.Counter(k[0][0])['{'])
        proto_text = k[0][0]
        #pandas读取上传的文件
        time.sleep(20)
        df = pd.read_csv('D://msg_box/'+filename, encoding='gbk', header=None)
        #判断上传的文件中的变量个数是否等于模板中占位符个数
        if (df.shape[1]-1) == proto_var_num:
            #遍历dataframe，替换模板中占位符并发送短信
            for index,row in df.iterrows():
                curr_proto_text = proto_text
                for i in range(1, proto_var_num+1):
                    old = '{' + str(i) + '}'
                    curr_proto_text = curr_proto_text.replace(old, str(row[i]))
                print(curr_proto_text)
                status = send_msg.send_msg(content=curr_proto_text, mobile=str(int(row[0])))
                #向数据库中插值
                conn11 = link_sql()
                cur11 = conn11.cursor()
                sq = 'insert into [dbo].[upload_details] (tel,proto_id,batches,status'
                for j in range(1, proto_var_num + 1):
                    sq = sq + ',field' + str(j)
                sq = sq + ') values (' + to_standard((int(row[0]))) + ',' + str(form.proto_name.data) + ',' + str(curr_batches) + ',' + str(status)
                for j in range(1, proto_var_num + 1):
                    sq = sq + ',' + to_standard(row[j])
                sq = sq + ')'
                print(sq)
                cur11.execute(sq)
                conn11.commit()
                conn11.close()
            print("发送成功")
            return redirect('/history')
        else:
            print("模板不匹配！")
            return redirect('/msgGroup')
    return render_template('msgGroup.html', form=form, curr_batches=curr_batches)


@app.route("/history", methods=['POST','GET'])
def history():
    conn = link_sql()
    cur = conn.cursor()
    sql = "select id,name from [dbo].[prototype] order by id asc"
    cur.execute(sql)
    l = cur.fetchall()
    conn.close()
    tuple = (0, '不选择')
    l = [tuple] + l
    form = historyForm()
    form.his_proto_id.choices = [(i[0], i[1]) for i in l]
    #print(type(form.his_proto_id.choices[0]))
    if request.method == 'POST':
        if str(form.his_tel.data) == '':
            tel = 'None'
        else:
            tel = str(form.his_tel.data)
        if str(form.his_proto_id.data) == str(0):
            id = 'None'
        else:
            id = str(form.his_proto_id.data)
        if str(form.his_batches.data) == '':
            batches = 'None'
        else:
            batches = str(form.his_batches.data)
        date = str(form.his_date.data)
        status = str(form.his_status.data)
        url = '/his/'+ str(tel) + '/' + str(id) + '/' + str(date) + '/' + str(batches) + '/' + str(status)
        print(url)
        return redirect(url)
    return render_template('history.html', form=form)


@app.route('/his/<tel>/<id>/<date>/<batches>/<status>', methods=['GET','POST'])
def his(tel, id, date, batches, status):
    conn = link_sql()
    cur = conn.cursor()
    sql = "select tel,proto_id,create_time,batches,status from [dbo].[upload_details] where 1=1 "
    print()
    if tel == 'None':
        sql = sql
    else:
        sql = sql + 'and tel=' + to_standard(tel)
    if id == 'None':
        sql = sql
    else:
        sql = sql + 'and proto_id=' + str(id)
    if date == 'None':
        sql = sql
    else:
        sql = sql + 'and CONVERT(varchar(max),create_time,23)' + to_standard(date)
    if batches == 'None':
        sql = sql
    else:
        sql = sql + 'and batches=' + str(batches)
    if status == 'None':
        sql = sql
    else:
        sql = sql + 'and status=' + str(status)
    sql = sql + ' order by id desc'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('his.html', u=u)


@app.route("/content")
def content():
    return render_template('content.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('homePage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=9000)
