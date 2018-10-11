from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL

from flask import json
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

mysql = MySQL()

  # MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'crud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'crud'

# mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connect().cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()




    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connect().cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connect().commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connect().cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connect().commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connect().cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connect().commit()
        return redirect(url_for('Index'))









if __name__ == "__main__":
    app.run(debug=True)
