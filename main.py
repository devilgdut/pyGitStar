from flask import Flask, render_template, redirect, request,url_for
import oauth
import urllib  
import json
import urllib 
from models import Project

app = Flask(__name__)
tokenurl = "https://github.com/login/oauth/access_token?client_id=%s&client_secret=%s&code=%s"
# 用Python处理Cookie http://blog.csdn.net/ericzhong83/article/details/7576371
# http://flask.pocoo.org/snippets


with open('client_secrets.json') as data_file:    
	data = json.load(data_file)

client_id = data["client_id"]
client_secret = data["client_secret"]

@app.route("/")
def home():
	return render_template("home.html",clientid=client_id)

@app.route("/authorizationcallback")
def authorizationcallback():
	code = request.args.get("code")
	req = urllib.request.Request(tokenurl %(client_id,client_secret,code)) 
	req.add_header("Accept","application/json")
	f = urllib.request.urlopen(req)
	print(80*"*")
	print('Status:', f.status, f.reason)
	#for k, v in f.getheaders():
	#	print('%s: %s' % (k, v))
	jstr = f.read().decode('utf-8')
	#print("type",type(jstr))
	#jdata = json.dumps(jstr)
	decode_json = json.loads(jstr)
	print('Data:', jstr)
	access_token = decode_json["access_token"]
	print('access_token:', access_token)
	
	print(80*"*")
	f.close();
	ujs = urllib.request.urlopen("https://api.github.com/user?access_token=%s" %access_token) 
	myuserstr = ujs.read().decode('utf-8')
	myuser = json.loads(myuserstr)
	usersname = myuser["login"]
	resprojects = urllib.request.urlopen("https://api.github.com/users/%s/starred?access_token=%s&page=1&per_page=100" %(usersname,access_token)) 
	projectsstr =  resprojects.read().decode('utf-8')
	pyprojectss = json.loads(projectsstr)
	print("projects:",len(pyprojectss))
	Projectsr = [] 
	for pp in pyprojectss:
		Projectsr.append(Project(pp["id"],pp["name"],pp["description"]))
	#return projectsstr
	return render_template("projects.html",projects=Projectsr)


if __name__ == "__main__":

    app.run(debug=True,port=80)
