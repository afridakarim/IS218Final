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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)