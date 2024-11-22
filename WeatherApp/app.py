from flask import Flask, make_response, jsonify, request,render_template, redirect, url_for, session
from weather import getWeather
from flask_mysqldb import MySQL
from functools import wraps
import requests
import os
# from Advisor.model import tierOneModel
import config as cfg

config = cfg.get_config()
app = Flask(__name__)
app.secret_key = os.urandom(64)

# Setting Up MySQL 
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '' #Make sure to add password before running app to connect to DB
app.config['MYSQL_DB']= 'WeatherApp'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(app)

#Ensuring unauthenticated user will always be redirected to login page
# In real world scenario, this will need for be more sophisticated for better
#   security of the information. This is mainly for functioning to assist in
#   automations of CI/CD. Main focus is DevOps set up over WebDevelopment or this
#   project.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#simple logout 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#performing queries grabbing list of all users and information
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users")
    users = cur.fetchall()
    cur.close()
    return str(users)

def get_recommendation (context):
    url = config['recommendation_app']
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'context': context
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['answer']

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        birth_date= request.form['birthday']
        email = request.form['email']
        state = request.form['state']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users (username, password, email, birth_date, state) VALUES (%s,%s,%s,%s,%s)",
                    (username, password, email, birth_date, state))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE username = %s",[username])
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == password:
            session['user'] = username
            return redirect(url_for('main'))
        else:
            return 'Login Failed'

    return render_template('login.html')

@app.route('/health', methods=['GET'])
def health_check():
    return make_response(jsonify({'status': 'Health in Good Status'}), 200)

@app.route('/', methods=['GET'])
@login_required
def main():
    return app.send_static_file('main.html')

@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)

@app.route('/get_weather', methods=['GET'])
@login_required
def get_weather():
    zip= request.args.get('zip')
    weather = getWeather(zip)
    context = weather.verbal_weather()
    # model = tierOneModel()
    # answer = get_recommendation(context) //we are not using model yet
    answer = 'model is down at this time'
    report = weather.weather_report()
    report['suggestion'] = answer
    return jsonify(report)


@app.route('/getWeather/<zip>', methods=['GET'])
def get_weather_url(zip):
    weather = getWeather(zip)
    context = weather.verbal_weather()
    # model = tierOneModel()
    # answer = get_recommendation(context) //we are not using model yet 
    answer = 'model is down at this time'
    report = weather.weather_report()
    report['suggestion'] = answer
    return jsonify(report)


app.run(debug=True, host="0.0.0.0", port="8080")