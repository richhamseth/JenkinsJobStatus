from oauth2client.client import SignedJwtAssertionCredentials
import requests
import json
#import pandas
import gspread
import datetime
import datetime

import urllib3
urllib3.disable_warnings()

url = 'https://sukulab.co/jenkins/api/json'
auth = ('cr_reviewer','rgdfm419@')
now = datetime.datetime.now()
#now = "2019-12-24"

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
#var.remove('')
var = [x for x in var if x != '']
del var[0]

#sheet.merge_cells(start_row=4, start_column=1, end_row=4, end_column=2)

def buildId(job, Id, first, second):
	sheet = gspreedauthorized()
	success = []
	failure = []

	for i in range(Id):
		build_no_url = 'https://sukulab.co/jenkins/job/'+str(job)+'/'+str(i+1)+'/api/json'
		build_no_res = requests.get(build_no_url, auth=auth)
		
		#result_ms=pandas.to_datetime(str(build_no_res.json()["timestamp"]),unit='ms')
		#temp = result_ms.strftime('%Y-%m-%d')

		#if str(now.strftime("%Y-%m-%d"))==str(temp):
		#if str(now)==str(temp):
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
	#sheet.update_cell(len(sheet.col_values(2))+1, 2, "SUCCESS")
	second = len(sheet.col_values(2))+1
	#sheet.update_cell(len(sheet.col_values(2))+1, 2, "FAILURE")
	res = requests.get(url, auth=auth)
	arr = []
	#jobslist = jobslist(arr)
	#if len(jobslist)==
	for i in range(len(res.json()["jobs"])):
		print (res.json()["jobs"][i]["name"])
		if str(res.json()["jobs"][i]["name"])=="sandbox":
			print ("testing")
		else:
			Job_url = 'https://sukulab.co/jenkins/job/'+str(res.json()["jobs"][i]["name"])+'/api/json'
			job_res = requests.get(Job_url, auth=auth)
			#print (res.json()["jobs"][i]["name"])
			#print (len(job_res.json()["builds"]))
			#print (len(sheet.row_values(1)))
			#sheet.update_cell(1, len(sheet.row_values(1))+1, str(res.json()["jobs"][i]["name"]))
			arr.append(res.json()["jobs"][i]["name"])
			#buildId(res.json()["jobs"][i]["name"], len(job_res.json()["builds"]), first, second)

	#print (arr)
	additionaljob = []
	if len(arr) != len(var):
		for i in arr:
			for j in var:
				if i != j:
					additionaljob.append(i)

	fetchjobstatus(var, first, second)

	if additionaljob != []:
		join_additional_jobs(additionaljob, first, second)

getjobsname()
