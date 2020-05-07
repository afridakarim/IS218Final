from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'addressData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Afrida'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblAddresses')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, address=result)


@app.route('/view/<int:addr_id>', methods=['GET'])
def record_view(addr_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblAddresses WHERE id=%s', addr_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', addr=result[0])


@app.route('/edit/<int:addr_id>', methods=['GET'])
def form_edit_get(addr_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblAddresses WHERE id=%s', addr_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', addr=result[0])


@app.route('/edit/<int:addr_id>', methods=['POST'])
def form_update_post(addr_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first'), request.form.get('last'), request.form.get('Address'),
                 request.form.get('City'), request.form.get('State'),
                 request.form.get('zip'), addr_id)
    sql_update_query = """UPDATE tblAddresses t SET t.first = %s, t.last = %s, t.Address = %s, t.City = 
    %s, t.State = %s, t.zip = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/address/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Address Form')


@app.route('/address/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first'), request.form.get('last'), request.form.get('Address'),
                 request.form.get('City'), request.form.get('State'),
                 request.form.get('zip'))
    sql_insert_query = """INSERT INTO tblAddresses (first ,last ,Address,City,State,zip) VALUES (%s,%s,%s,%s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:addr_id>', methods=['POST'])
def form_delete_post(addr_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblAddresses WHERE id = %s """
    cursor.execute(sql_delete_query, addr_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
