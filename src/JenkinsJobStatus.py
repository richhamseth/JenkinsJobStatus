from oauth2client.client import SignedJwtAssertionCredentials
import requests
import json
import gspread
import datetime
import datetime

import urllib3
urllib3.disable_warnings()

url = 'https://sukulab.co/jenkins/api/json'
auth = ('cr_reviewer','rgdfm419@')
now = datetime.datetime.now()

def gspreedauthorized():
    json_key = json.load(open('creds.json'))
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    file = gspread.authorize(credentials)
    sheet = file.open("Jenkins Status").sheet1
    return sheet

sheet = gspreedauthorized()
var = sheet.row_values(1)
var = [x for x in var if x != '']
del var[0]

def buildId(job, Id, first, second):
	sheet = gspreedauthorized()
	success = []
	failure = []

	for i in range(Id):
		build_no_url = 'https://sukulab.co/jenkins/job/'+str(job)+'/'+str(i+1)+'/api/json'
		build_no_res = requests.get(build_no_url, auth=auth)
		
		print (str(build_no_res.json()["result"]))
		if str(build_no_res.json()["result"])=="SUCCESS":
			success.append("SUCCESS")
		else:
			failure.append("FAILURE")

	print (len(success))
	print (len(failure))
	sheet.update_cell(first, len(sheet.row_values(first))+1, len(success))
	sheet.update_cell(first, len(sheet.row_values(first))+1, len(failure))

def jobslist(arr):
	res = requests.get(url, auth=auth)
	for i in range(len(res.json()["jobs"])):
		if str(res.json()["jobs"][i]["name"])=="sandbox":
			print ("testing")
		else:
			arr.append(str(res.json()["jobs"][i]["name"]))
	return arr

def fetchjobstatus(var, first, second):
	for i in var:
		Job_url = 'https://sukulab.co/jenkins/job/'+str(i)+'/api/json'
		job_res = requests.get(Job_url, auth=auth)
		buildId(i, len(job_res.json()["builds"]), first, second)

def join_additional_jobs(additionaljob, first, second):
	for i in additionaljob:
		sheet.update_cell(1, len(sheet.row_values(1))+2, i)
		sheet.update_cell(2, len(sheet.row_values(1))+1, "Success")
		sheet.update_cell(2, len(sheet.row_values(1))+1, "Failure")
		Job_url = 'https://sukulab.co/jenkins/job/'+str(i)+'/api/json'
		job_res = requests.get(Job_url, auth=auth)
		buildId(i, len(job_res.json()["builds"]), first, second)

def getjobsname():
	sheet = gspreedauthorized()
	sheet.update_cell(len(sheet.col_values(1))+1, 1, now.strftime("%Y-%m-%d"))
	first = len(sheet.col_values(2))+1
	second = len(sheet.col_values(2))+1
	res = requests.get(url, auth=auth)
	arr = []
	for i in range(len(res.json()["jobs"])):
		print (res.json()["jobs"][i]["name"])
		if str(res.json()["jobs"][i]["name"])=="sandbox":
			print ("testing")
		else:
			Job_url = 'https://sukulab.co/jenkins/job/'+str(res.json()["jobs"][i]["name"])+'/api/json'
			job_res = requests.get(Job_url, auth=auth)
			arr.append(res.json()["jobs"][i]["name"])

	if len(arr) != len(var):
		additionaljob = list(set(arr).difference(set(var)))

	fetchjobstatus(var, first, second)

	if additionaljob != []:
		print (additionaljob)
		join_additional_jobs(additionaljob, first, second)
getjobsname()
