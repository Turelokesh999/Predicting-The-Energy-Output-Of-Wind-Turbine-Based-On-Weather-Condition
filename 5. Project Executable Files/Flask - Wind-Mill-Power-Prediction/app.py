import numpy as np 
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mail import Mail, Message
import joblib
import requests
import windApp
import csv
import os
import random
import string
otp_code1 = [1]
app = Flask(__name__)

loaded_model = joblib.load('power_prediction.sav')
scale_model = joblib.load('scaler.pkl')

def format_to_two_decimals(value):
    return f"{value:.2f}"

if not os.path.isfile(r'Flask - Wind-Mill-Power-Prediction\login.csv'):
    with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Email', 'Password'])  # Add header if needed

# Configurations for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chat999ai@gmail.com'  # replace with your email
app.config['MAIL_PASSWORD'] = 'pdzy reju ltul qypd'

mail = Mail(app)

def generate_otp(length=6):
    """Generate a random OTP code"""
    characters = string.digits
    otp = ''.join(random.choice(characters) for i in range(length))
    return otp


@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    return render_template('index2.html')

@app.route('/predict/<city>')
def name(city):
    result = list(windApp.result(city))
    return jsonify(result)

@app.route('/predict_info/<theoretical>/<wind>')
def prediction(theoretical, wind):
    x_single = np.array([[theoretical, wind]])
    x_single = scale_model.transform(x_single)
    prediction = loaded_model.predict(x_single)
    print(prediction)

    prediction = float(format_to_two_decimals(prediction[0]))

    print(prediction)
    print(theoretical)
    print(wind)


    return jsonify({'prediction':prediction})



@app.route('/register', methods=['POST'])
def register():
    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    verification_code = request.form.get('verification_code')

    try:
        with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email:
                    return '<h1>Email already registered.</h1>'
    except FileNotFoundError:
        pass


    if otp_code1[0] == str(verification_code):
        # Save data to CSV
        with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password])

        msg = Message('Registration Successful', sender='projectbyme123@gmail.com', recipients=[email])
        msg.body = f'You have successfully registered.\n\nYour credentials:\nEmail: {email}\nPassword: {password}'
        mail.send(msg)

        # Redirect or render a success page
        return redirect(url_for('predict'))
    else:
        return '<h1>Verification failed. Please try again.</h1>'
    

@app.route('/send_code', methods=['POST'])
def send_code():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # For simplicity, we are not verifying the email and password in this example

    otp_code = generate_otp()
    otp_code1[0] = otp_code

    msg = Message('Your OTP Code', sender='projectbyme123@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is: {otp_code}'
    mail.send(msg)

    return jsonify({'message': 'OTP sent successfully'})


@app.route('/login', methods=['POST','GET'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    valid_credentials = False
    username = None

    with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email and row[2] == password:
                valid_credentials = True
                username = row[0]  # Assuming the username is in the first column
                break

    if valid_credentials:
        return jsonify({'success': True, 'username': username}), 200
    else:
        return jsonify({'success': False}), 401


@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    rows = []
    account_deleted = False

    with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email and row[2] == password:
                account_deleted = True
            else:
                rows.append(row)

    if account_deleted:
        with open(r'Flask - Wind-Mill-Power-Prediction\login.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 401


if __name__ == '__main__':
    app.run(debug=True)