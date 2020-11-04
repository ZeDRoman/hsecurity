from flask import *
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__)
mysql = MySQL(app)


def create_table(rv):
    df = pd.DataFrame(list(rv), columns=['id', 'login', 'money_amount', 'card_number', 'status'])
    df = df.set_index(['id'])
    return render_template('view.html',tables=[df.to_html(classes='data')],
                           titles = ['na', 'Users data'])


def perform_sql(sql_req):
    cur = mysql.connection.cursor()
    cur.execute(sql_req)
    rv = cur.fetchall()
    return create_table(rv)

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/users')
def users():
    sql_req = '''SELECT * FROM tmp.users where status = 1'''
    return perform_sql(sql_req)


@app.route('/by-login')
def user_by_login():
    login =request.args.get('login')
    sql_req = '''SELECT * FROM tmp.users where login = '{}' '''.format(login)
    return perform_sql(sql_req)


@app.route('/by-id')
def user_by_id():
    id_ =request.args.get('id')
    sql_req = '''SELECT * FROM tmp.users where id = {}'''.format(id_)
    return perform_sql(sql_req)

@app.route('/all', methods = ['POST'])
def redirect_all():
    return redirect('/users')


@app.route('/id', methods = ['POST'])
def redirect_id():
    id_ = request.form.get('id')
    return redirect('/by-id?id={}'.format(id_))


@app.route('/login', methods = ['POST'])
def redirect_login():
    login = request.form.get('login')
    return redirect('/by-login?login={}'.format(login))


if __name__ == '__main__':
    app.run(debug=True)

