from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import pymssql

app = Flask(__name__)


@app.route('/')
def home():
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
    conn = pymssql.connect(host='LAPTOP-GPKFSA00', user='sa', password='xyt555', database='msg', charset='cp936')
    cur = conn.cursor()
    sql = "select * from [dbo].[prototype]"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('prototypeEditor.html', u=u)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('homePage.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=9000)
