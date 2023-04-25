
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request,render_template,redirect,url_for,flash

# from flask_sqlalchemy import SQLAlchemy



	
import mysql.connector
# import pymysql 
# pymysql.install_as_MySQLdb()
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Gk270911'
app.config['MYSQL_DB']='FLASKDEMO'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "abc" 

mysql = MySQL(app)


@app.route('/')
def home():
	message=None
	message1=None
	cur=mysql.connection.cursor()
	cur.execute("select count(id) As donars from donars")
	result=cur.fetchone()
	message=result
	cur.execute("select count(id) As needers from need_blood")
	result1=cur.fetchone()
	message1=result1
	return render_template('home.html',message=message,message1=message1)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        userDetails = request.form
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        if result is not None:
            flash("You already have an account!!!") 
        else:
            number = request.form['number']
            dob = request.form['dob']
            bloodgroup = request.form['bloodgroup']
            address = request.form['address']
            password = request.form['password']
            gender = request.form['gender']
            confirmpwd = request.form['confirmpwd']
            if(password == confirmpwd):
                cur.execute("INSERT INTO users (name, password, email, number, dob, gender, bloodgroup, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, password, email, number, dob, gender, bloodgroup, address))
                mysql.connection.commit()
                results = cur.fetchall()
                user_id = cur.lastrowid  
                return f"""<script>alert("Success! Your user ID is {user_id}"); window.location.href = '{url_for('login')}'</script>"""
            else:
                error = "Confirm password does not match!"
            cur.close()
    return render_template('signup.html', error=error)


@app.route('/login', methods =["GET","POST"])
def login():
	if request.method=="POST":
		email=request.form['email']
		password=request.form['password']
		id=request.form['id']
		cur=mysql.connection.cursor()
		cur.execute("select id from users where id=%s AND password=%s AND email=%s",(id,password,email))
		result=cur.fetchone()
		if not result:
			flash("Entered Email or Password or ID is incorrect !")
			return redirect(url_for('login'))
		else:
			return redirect(url_for('middle'))
		
	return render_template("login.html")

@app.route('/middle', methods =["GET","POST"])
def middle():
	return render_template('middle.html')

@app.route('/needblood', methods =["GET","POST"])
def needblood():
	message = None
	error=None
	if request.method=="POST":
		userdetails=request.form
		name=userdetails['name']
		age=userdetails['age']
		bloodgroup=userdetails['bloodgroup']
		id=userdetails['id']
		reason=userdetails['reason']
		cur=mysql.connection.cursor()
		cur.execute("SELECT id FROM users WHERE id = %s", (id,))
		result = cur.fetchone()
		if not result:
			error="Your id doesn't exist!"
		else:
				cur.execute("INSERT INTO need_blood(name,id,bloodgroup,age,reason) VALUES(%s,%s,%s,%s,%s)",(name,id,bloodgroup,age,reason))
				mysql.connection.commit()
				cur.execute("SELECT * FROM users WHERE bloodgroup = %s", (bloodgroup))
				mysql.connection.commit()
				results=cur.fetchall()
				if not results:
					message= f"{bloodgroup} Blood Group not Available SORRY:("
				else:
					message = f"{bloodgroup} Available!! Thank You visit again :)"
		cur.close()
	return render_template('needblood.html', message=message,error=error)



@app.route('/donate', methods =["GET","POST"])
def donate():
	error=None
	error1=None
	message=None
	if request.method == "POST":
		userDetails=request.form
		name=userDetails['name']
		age=int(userDetails['age'])
		id=userDetails['id']
		bloodgroup=userDetails['bloodgroup']
		disease=userDetails['disease']
		cur=mysql.connection.cursor()
		cur.execute("SELECT id FROM users WHERE id = %s", (id,))
		result = cur.fetchone()
		if age<18 and not result:
			error="You cannot donate at a age less than 18"
			error1="Your id doesn't exist!"
		elif not result:
			error1="Your id doesn't exist!"
		elif age<18:
			error="You cannot donate at a age less than 18"
		else:
				message= " Thank you for donating blood:)"
				cur.execute("INSERT INTO donars(id,name,bloodgroup,age,disease) VALUES(%s,%s,%s,%s,%s)",(id,name,bloodgroup,age,disease))
				mysql.connection.commit()
		cur.close()
	return render_template('donate.html',error=error,error1=error1,message=message)

@app.route('/wwdb', methods =["GET","POST"])
def wwdb():
	return render_template('wwdb.html')

if __name__ == '_main_':
	app.run(debug=True)
