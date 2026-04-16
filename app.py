import warnings
warnings.filterwarnings('ignore')
from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib
import sqlite3

import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home1')
def home1():
    return render_template('home1.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/about1')
def about1():
    return render_template('about1.html')

@app.route('/about2')
def about2():
    return render_template('about2.html')


@app.route('/logon')
def logon():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('signin.html')



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get('user','')
        name = request.form.get('name','')
        email = request.form.get('email','')
        number = request.form.get('mobile','')
        password = request.form.get('password','')
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("SELECT 1 FROM info WHERE user = ?", (username,))
        if cur.fetchone():
            con.close()
            return render_template("signup.html", message="Username already exists. Please choose another.")
        cur.execute("insert into `info` (`user`,`name`, `email`,`mobile`,`password`) VALUES (?, ?, ?, ?, ?)",(username,name,email,number,password))
        con.commit()
        con.close()
        return redirect(url_for('login'))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        mail1 = request.form.get('user','')
        password1 = request.form.get('password','')
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
        data = cur.fetchone()

        if data == None:
            return render_template("signin.html", message="Invalid username or password.")    

        elif mail1 == 'admin' and password1 == 'admin':
            return render_template("home1.html")

        elif mail1 == str(data[0]) and password1 == str(data[1]):
            return render_template("home1.html")
        else:
            return render_template("signin.html", message="Invalid username or password.")


@app.route('/predict1', methods=['POST'])
def predict1():

    int_features = [float(x) for x in request.form.values()]
    final4 = [np.array(int_features)]

    model = joblib.load('model/eng_5_vc1.sav')
    prediction = int(model.predict(final4))
    
    if prediction == 0:  # Insomnia
        context = {
            "disorder_name": "Insomnia",
            "title_message": "About Insomnia",
            "disorder_info": "Insomnia is a common sleep disorder that can make it hard to fall asleep, hard to stay asleep, or cause you to wake up too early and not be able to get back to sleep.",
            "recommendations": [
                "Stick to a regular sleep schedule.",
                "Avoid caffeine and nicotine, especially before bed.",
                "Create a restful environment.",
                "Limit daytime naps."
            ],
            "border_color": "#dc3545",
            "header_bg_class": "bg-danger",
            "icon_class": "bx-alarm-exclamation"
        }
        return render_template('result1.html', **context)
    
    elif prediction == 1:  # No disorder
        context = {
            "disorder_name": "No Disorder Detected",
            "title_message": "Great News!",
            "disorder_info": "Based on the provided data, our AI model did not detect any signs of common sleep disorders. Your sleep patterns appear to be healthy.",
            "recommendations": [
                "Maintain a consistent sleep schedule, even on weekends.",
                "Create a relaxing bedtime routine to help you unwind.",
                "Ensure your bedroom is dark, quiet, and cool.",
                "Limit exposure to screens (phones, TVs) before bed."
            ],
            "border_color": "#28a745",
            "header_bg_class": "bg-success",
            "icon_class": "bx-check-circle"
        }
        return render_template('result1.html', **context)

    elif prediction == 2:  # Sleep Apnea
        context = {
            "disorder_name": "Sleep Apnea",
            "title_message": "About Sleep Apnea",
            "disorder_info": "Sleep apnea is a potentially serious sleep disorder in which breathing repeatedly stops and starts. If you snore loudly and feel tired even after a full night's sleep, you might have sleep apnea.",
            "recommendations": [
                "Maintain a healthy weight.",
                "Avoid alcohol and sleeping pills.",
                "Sleep on your side or stomach rather than your back.",
                "Use a continuous positive airway pressure (CPAP) device if prescribed."
            ],
            "border_color": "#dc3545",
            "header_bg_class": "bg-danger",
            "icon_class": "bx-alarm-exclamation"
        }
        return render_template('result1.html', **context)

   
@app.route('/predict2', methods=['POST'])
def predict2():

    int_features = [float(x) for x in request.form.values()]
    final4 = [np.array(int_features)]

    model = joblib.load('model/eng_2_vc1.sav')
    prediction = int(model.predict(final4))
    
    if prediction == 0:  # Insomnia
        context = {
            "disorder_name": "Insomnia",
            "title_message": "About Insomnia",
            "disorder_info": "Insomnia is a common sleep disorder that can make it hard to fall asleep, hard to stay asleep, or cause you to wake up too early and not be able to get back to sleep.",
            "recommendations": [
                "Stick to a regular sleep schedule.",
                "Avoid caffeine and nicotine, especially before bed.",
                "Create a restful environment.",
                "Limit daytime naps."
            ],
            "border_color": "#dc3545",
            "header_bg_class": "bg-danger",
            "icon_class": "bx-alarm-exclamation"
        }
        return render_template('result2.html', **context)
    
    elif prediction == 1:  # No disorder
        context = {
            "disorder_name": "No Disorder Detected",
            "title_message": "Great News!",
            "disorder_info": "Based on the provided data, our AI model did not detect any signs of common sleep disorders. Your sleep patterns appear to be healthy.",
            "recommendations": [
                "Maintain a consistent sleep schedule, even on weekends.",
                "Create a relaxing bedtime routine to help you unwind.",
                "Ensure your bedroom is dark, quiet, and cool.",
                "Limit exposure to screens (phones, TVs) before bed."
            ],
            "border_color": "#28a745",
            "header_bg_class": "bg-success",
            "icon_class": "bx-check-circle"
        }
        return render_template('result2.html', **context)

    elif prediction == 2:  # Sleep Apnea
        context = {
            "disorder_name": "Sleep Apnea",
            "title_message": "About Sleep Apnea",
            "disorder_info": "Sleep apnea is a potentially serious sleep disorder in which breathing repeatedly stops and starts. If you snore loudly and feel tired even after a full night's sleep, you might have sleep apnea.",
            "recommendations": [
                "Maintain a healthy weight.",
                "Avoid alcohol and sleeping pills.",
                "Sleep on your side or stomach rather than your back.",
                "Use a continuous positive airway pressure (CPAP) device if prescribed."
            ],
            "border_color": "#dc3545",
            "header_bg_class": "bg-danger",
            "icon_class": "bx-alarm-exclamation"
        }
        return render_template('result2.html', **context)

   

@app.errorhandler(404)
def not_found(e):
    return render_template('notfound.html'), 404


if __name__ == "__main__":
    app.run(debug=False)
