'''
Project		: G-Survey
File name	: clnt_gen_report 
Version		: 1.0.0
Create Date	: 2018/10/26
Create by	: Narongsak Mala<narongsak.mala@dga.or.th>
Email		: narongsak.mala@dga.or.th
Description	: Client script for generating report
'''

import requests 
import json

# mock report 
# reportId_str = '{"reportIds": [1,2,3,4]}';

# URL
allReportIdsURL = "http://localhost:8000/gsurvey/apis/allreports"
genReportURL = "http://localhost:8000/gsurvey/apis/genreport/"

# Queries all report 
r = requests.get(allReportIdsURL);
print(r.json)

# Parses to json format
#reportIds = json.loads(reportId_str); 
reportIds = r.json()
print(reportIds["reportIds"]);

# Call each of reports
for reportId in reportIds["reportIds"] :
	print("report ID: "+reportId)
	url = genReportURL + str(reportId)
	print("calling " + url)
	r = requests.get(url) 
	print("status: " + str(r.status_code))
	
	# Verify status
	if r.status_code == 200 :
		print("generate report ID " + str(reportId) + " success")
	else:
		print("generate report ID " + str(reportId) + " failed")
