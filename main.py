from flask import Flask, render_template, request
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
app = Flask('app')
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
global sentMessages 
sentMessages = 0
@app.route('/')
def main():
  global sentMessages
  return render_template('index.html', sentMessages=sentMessages)
@app.route('/mail', methods=["GET", "POST"])
def send_mail():
  if request.method == 'POST':
    reciver = request.form['reciver']
    message = request.form['message']
    name = request.form['name']
    
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
 
    with open('users.txt', 'a') as f:
      f.write(f'{name}, {IPAddr}, {hostname} \n')
    subject = request.form['subject']
    email = request.form['email']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'EmailService@fastmailexpressemails.com'
    msg['To'] = reciver
    
    s = smtplib.SMTP('smtp-relay.brevo.com', 587)
    s.starttls()
    s.login('EmailService@fastmailexpressemails.com', os.environ['SMTP_KEY'])
    msghtml = f"""\
<html>
  <head></head>
  <body>
    <center>
    <h2> {message} </h2>
    <br>
    <br>
    <p style='color:aqua;'>From: {name} <br>Sent By: FASTMAIL EXPRESS EMAIL SERVICE</p>
    <p>Need Support? support@fastmailexpressemails.com</p>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <p>RESPOND-TO: {email} </p>
    <p>*ALL RESPONCES TO THIS EMAIL WILL BE DELETED</p>
    </center>
  </body>
</html>
"""
    msg.attach(MIMEText(msghtml, 'html'))
    try:
      s.sendmail('coder7898@gmail.com', reciver, msg.as_string())
      s.quit()
      global sentMessages
      sentMessages += 1
      return render_template('sent.html')
    except:
      return 'ERROR SENDING EMAIL'
  elif request.method == 'GET':
    return 'No Information Avalible'
  else:
    return 'ERROR'

app.run(host='0.0.0.0', port=8080, debug="true")
