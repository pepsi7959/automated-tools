'''
Project		: G-Survey
File name	: clnt_gen_report 
Version		: 1.0.0
Create Date	: 2018/10/26
Create by	: Narongsak Mala<narongsak.mala@dga.or.th>
Email		: narongsak.mala@dga.or.th
Description	: Client script for generating report
'''
import datetime
import requests 
import json

# mock report 
# reportId_str = '{"reportIds": [1,2,3,4]}';

# URL
allReportIdsURL = "http://localhost:8000/gsurvey/admin/apis/allreports"
genReportURL = "http://localhost:8000/gsurvey/admin/apis/genReportAsExcel"

# Queries all report 
r = requests.get(allReportIdsURL);
print(r.json)

# Parses to json format
#reportIds = json.loads(reportId_str); 
reportIds = r.json()
print(reportIds["reportIds"]);

success_cnt = 0;
total_cnt = 0;
# Call each of reports
for reportId in reportIds["reportIds"] :
	total_cnt += 1 
	print("report ID: "+reportId)
	url = genReportURL + "/" + str(reportId) + "/" + datetime.datetime.today().strftime('%Y%m%d_0020')
	print("calling " + url)
	r = requests.get(url) 
	print("status: " + str(r.status_code))
	
	# Verify status
	if r.status_code == 200 :
		success_cnt += 1
		print("generate report ID " + str(reportId) + " success")
	else:
		print("generate report ID " + str(reportId) + " failed")

print("success: " + str(success_cnt) + " failed: " + str(total_cnt-success_cnt))
