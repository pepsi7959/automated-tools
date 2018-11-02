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
import sys

class ClientGenerator:

	# mock report 
	# reportId_str = '{"reportIds": [1,2,3,4]}';

	# URL
	allReportIdsURL = "http://localhost:8000/gsurvey/admin/apis/allreports"
	genReportURL = "http://localhost:8000/gsurvey/admin/apis/genReportAsExcel"

	def genReports(self, postfix, allReportIdsURL, genReportURL):
	
		try:
			# Queries all report 
			r = requests.get(allReportIdsURL);
			print(r.json)
			
			# Parses to json format
			#reportIds = json.loads(reportId_str); 
			reportIds = r.json()
			print(reportIds["results"]);
			success_cnt = 0;
			total_cnt = 0;
		
			# Call each of reports
			for report in reportIds["results"] :
				total_cnt += 1 
				reportId = report['GenerateID']
				reportName = report['GenerateName']
				reportIdName = "Report ID: " + str(reportId) + " Name: " + reportName
				url = genReportURL + "/" + str(reportId) + "/" + datetime.datetime.today().strftime('%Y%m%d') + postfix
				print(reportIdName + " calling " + url)
				r = requests.get(url) 
				print("status: " + str(r.status_code))
	
				# Verify status
				if r.status_code == 200 :
					response = r.json()
					if response["data"]["status"] != 0 : 
						print(reportIdName + " failed: " + response["data"]["message"])
					else :
						success_cnt += 1
						print(reportIdName + " success")
				else:
					print(reportIdName + " failed")
			print("success: " + str(success_cnt) + " failed: " + str(total_cnt-success_cnt))
			return 0
		except Exception as e:
			print(str(e))
			return 1


	def help(self) :
		print "Example command:" 
		print "python ./clnt_gen_report.py _0200 http://localhost:8000/gsurvey/admin/apis/allreports http://localhost:8000/gsurvey/admin/apis/genReportAsExcel" 
		 

# Create Client Generator 
clntGen = ClientGenerator()
retry = 0
maxRetry = 3
if len(sys.argv) > 3 :
	while retry < maxRetry :
		if clntGen.genReports(sys.argv[1], sys.argv[2], sys.argv[3]) == 0 :
			break	
		else:
			retry += 1
			print("Retry :" + str(retry))
			continue
else:
	clntGen.help()
