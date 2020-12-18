from flask import Flask, render_template, request, session, logging, url_for, redirect
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'infoDatabase'
mysql.init_app(app)


@app.route("/",methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = mysql.get_db().cursor()
        inputData = (fname,lname, address,email, password)
        sql_insert_query = """INSERT INTO information(firstName, lastName, address, email,password) VALUES (%s, %s,%s, %s,%s) """
        cursor.execute(sql_insert_query, inputData)
        mysql.get_db().commit()
        return redirect("home.html", code=302)

    if request.method == "GET":
        return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT email,password FROM information where email=%s and password =%s',( email,password))
        account=cursor.fetchall
        if(email== account['email'] & password == account['password']):
            return redirect("home.html")

    if request.method == "GET":
        return render_template("login.html")



if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)