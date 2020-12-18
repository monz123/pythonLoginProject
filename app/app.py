from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)



@app.route("/",methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)