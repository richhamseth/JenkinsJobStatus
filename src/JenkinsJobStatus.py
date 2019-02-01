import json
import gspread
import requests
from oauth2client.client import SignedJwtAssertionCredentials
import dateutil.parser as dp
import datetime as DT
import datetime
import urllib3
urllib3.disable_warnings()

url = 'http://192.168.1.44:5000/taskDetails'
today = datetime.datetime.now().strftime("%Y-%m-%d")

def gspreedauthorized():
    json_key = json.load(open('creds.json'))
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    file = gspread.authorize(credentials)
    sheet = file.open("Members details").sheet1
    return sheet

sheet = gspreedauthorized()

def updatetask(data):
	col = len(sheet.col_values(1))
	sheet.update_acell('A'+str(col+1), data['employeeID'])
	sheet.update_acell('B'+str(col+1), today)
	sheet.update_acell('C'+str(col+1), data['WorkId'])
	sheet.update_acell('D'+str(col+1), data['ActivityId'])
	sheet.update_acell('E'+str(col+1), data['ExtRefId'])
	sheet.update_acell('F'+str(col+1), data['Hrs'])
	sheet.update_acell('G'+str(col+1), data['Mins'])
	sheet.update_acell('H'+str(col+1), data['TaskDetails'])

def employeeupdate(sheet):
    headers = {"Content-Type":"application/json", "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXBsb3llZUlEIjoiZW1wbG95ZWVJRCIsImlhdCI6MTU0NDg1NDA0OX0.BS1S0kOZd3Rvd8DgANpWTnMdQHgeFirlmgGSqjNqAWk"}
    empreq = requests.get(url, headers=headers)
    #print (empreq.content)

    for j in range(len(empreq.json()['data'])):
    	#date = datetime.datetime.strptime(empreq.json()['data'][j]['Date'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
    	#print (date)

    	t = datetime.datetime.today().isoformat()
    	parsed_t = dp.parse(empreq.json()['data'][j]['Date'])
    	t_in_seconds = parsed_t.strftime('%s')
    	since = DT.datetime.utcfromtimestamp(int(t_in_seconds)+86400).isoformat()

    	date = datetime.datetime.strptime(since, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    	if str(date) == str(today):
    		print (date)
    		updatetask(empreq.json()['data'][j])

employeeupdate(sheet)
