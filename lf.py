from flask import Flask
from flask import render_template,redirect,request,url_for
from flask import request
import firebase_admin
from firebase_admin import credentials,db,auth
import socket   
import smtplib
app = Flask(__name__)

@app.route('/favicon.ico/')
def favi():
	return 'hi'

@app.route('/sendmessage/',methods=["GET", "POST"])
def sendmessage():
	if request.method == 'GET':
		fromname = request.values.get('name')
		emailid = request.values.get('email')
		message = request.values.get('message')
		s=smtplib.SMTP('smtp.gmail.com:587')
		s.ehlo()
		s.starttls()
		s.login('lostandfoundwebportal@gmail.com','lostandfound')
		message='Subject:Message from '+fromname+'\n\n'+'from: '+emailid+'\n'+message
		s.sendmail('lostandfoundwebportal@gmail.com','lostandfoundwebporta@gmail.com',message)
		s.quit()
		return render_template('homepage.html')

@app.route('/sendclaimmail/<fromemail>/<touid>/<object1>')
def sendclaimmail(fromemail,touid,object1):
	toemail=(auth.get_user(touid).email)
	fromuid=auth.get_user_by_email(fromemail).uid
	fromname=db.reference('/users/'+fromuid+'/Name').get()
	print(fromname)
	s=smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()
	s.login('lostandfoundwebportal@gmail.com','lostandfound')
	message='Subject:'+fromname+' just claimed an Object\n\n'+'from: '+fromemail+'\n'+fromname+' just claimed \"'+object1+'\" as his/her.\nPlease review at 127.0.0.1:5001/user_acc'
	s.sendmail('lostandfoundwebportal@gmail.com',toemail,message)
	s.quit()
	return render_template('listing.html')

@app.route('/<filename>/')
def home(filename):
	return render_template(filename+'.html')


if __name__ == '__main__':
	print(" * Starting to connect to database")
	cred = credentials.Certificate('./cred.json')
	default_app = firebase_admin.initialize_app(cred,{
		'databaseURL': 'https://lostandfound-5d806.firebaseio.com/'
		})
	print(" * Database connected successfully")
	app.debug = True
	app.run(host='127.0.0.1',port=5001)