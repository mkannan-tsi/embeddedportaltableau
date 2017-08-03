from flask import Flask, render_template, request, json, session
from cryptography.fernet import Fernet
import tableauserverclient as TSC
import string
import random
from RestCalls import *

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))

key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def loginToServer():
	##########Storing credentials in an encrypted manner##########
	session['server'] = cipher_suite.encrypt(str(request.form['inputServer']))
	session['site'] = cipher_suite.encrypt(str(request.form ['inputSite']))
	session['username'] = cipher_suite.encrypt(str(request.form['inputName']))
	session['password'] = cipher_suite.encrypt(str(request.form['inputPassword']))
	
	##########Checking if user is authenticated##########
	server, isUserLoggedIn = loginUser()
	if isUserLoggedIn == True :
		project = showProjects(server, isUserLoggedIn)
		return render_template('projects.html', projects=project)
	else:
		state = "There is an error in logging in. Please re-try."
		return render_template('index.html', state = state)

@app.route('/project=<string:project>')
def workbook(project):
	url = request.path
	server, isUserLoggedIn = loginUser()
	workbooks = showWorkbooks(project, server, isUserLoggedIn)	
	return render_template('workbook.html', workbook=workbooks, url=url)

@app.route('/project=<string:project>&workbook=<string:workbook>')
def worksheet(project, workbook):
	url = request.path
	server, isUserLoggedIn = loginUser()
	worksheets = showWorksheets(project, workbook, server, isUserLoggedIn)
	return render_template('worksheet.html', worksheet=worksheets, url=url)

@app.route('/project=<string:project>&workbook=<string:workbook>&worksheet=<string:worksheet>')
def view(project, workbook, worksheet):
	worksheet = stripCharacter(worksheet)
	workbook = stripCharacter(workbook)
	details = extractUserDetails()
	return render_template('view.html', server = details[0], site = details[1], workbook = workbook, worksheet = worksheet)


def loginUser():
    isUserLoggedIn = False  
    #Taking in details from file
    details = extractUserDetails()
    #Initializing Server
    server = TSC.Server(details[0])
    tableau_auth = TSC.TableauAuth(details[2], details[3], details[1])
    #Logging into Server
    try :
    	server.auth.sign_in(tableau_auth)
        isUserLoggedIn = True
    except :
        pass
    return server, isUserLoggedIn

def extractUserDetails():
    details = []
    details.append (cipher_suite.decrypt(session['server']))
    details.append (cipher_suite.decrypt(session['site']))
    details.append (cipher_suite.decrypt(session['username']))
    details.append (cipher_suite.decrypt(session['password']))
    return details

if __name__ == "__main__":
	setDefaultEncoding ()
	app.run(host= '0.0.0.0', debug = True)


