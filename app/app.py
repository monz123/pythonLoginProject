from flask import Flask, render_template, request, session, logging, url_for, redirect
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import json
import os
import quickemailverification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'infoDB'
mysql.init_app(app)

QUICK_MAIL_VERIFICATION_API_KEY = '26817cd745243111bbd23dc7d4c4d9a61a809e49a881aaf02ad47cccd157'
SEND_GRID_API_KEY = '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'


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        ##to get the registration data
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        ##to avoid duplicate emails registered
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT email FROM information where email=%s', email)
        checkIfemailExists = cursor.fetchall()
        if checkIfemailExists:
            return render_template("register.html",
                                   msg="Sorry, the email is already taken! Please use a different email")
        ##to verify the email
        client = quickemailverification.Client(QUICK_MAIL_VERIFICATION_API_KEY)
        quickemailverification = client.quickemailverification()
        response = quickemailverification.verify(email)
        for i in response:
            if i['result'] == 'valid':
                inputData = (fname, lname, address, email, password)
                sql_insert_query = """INSERT INTO information(firstName, lastName, address, email,password) VALUES (%s, %s,%s, %s,%s) """
                cursor.execute(sql_insert_query, inputData)
                mysql.get_db().commit()
                return redirect("home.html", code=302)
            else:
                return render_template("register.html",
                                       msg="Sorry, this is a invalid email, Please try with a valid mail")

    if request.method == "GET":
        return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT email,password FROM information where email=%s and password =%s', (email, password))
        result = cursor.fetchall()
        json_result = json.dumps(result)
        print(result)
        print(json_result)
        if (result):
            return render_template("homepageAfterLogin.html", msg="Logged In Successfully!!!")
        else:
            return render_template("login.html", msg="Incorret Login ID/Password !")

    if request.method == "GET":
        return render_template("login.html")


@app.route("/sendMail", methods=['POST'])
def sendmail():
    ## first- get the data from the page
    toemail = request.form.get("email")
    sub = request.form.get("subject")
    content = request.form.get("myTextArea")
    message = Mail(
        from_email='monishaa138@gmail.com',
        to_emails=toemail,
        subject=sub,
        html_content=content)

    try:
        sg = SendGridAPIClient(SEND_GRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e.message)
    return render_template("homepageAfterLogin.html", msg="Message Sent")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
