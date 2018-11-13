'''
Project		: G-Survey
File name	: clnt_gen_report 
Version		: 1.0.1
Create Date	: 2018/11/13
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

	ALL_REPORTS = "admin/apis/allreports"
	GEN_REPORT_AS_EXCEL = "admin/apis/genReportAsExcel"
	
	def genReports(self, postfix, baseUrl):
	
		try:
			# Queries all report 
			r = requests.get(baseUrl + "/" + self.ALL_REPORTS);
			strResponse = r.text.encode('utf-8') 
			print(strResponse)
			
			# Parses to json format
			reportIds = json.loads(strResponse); 
			print(reportIds["results"]);
			success_cnt = 0;
			total_cnt = 0;
		
			# Call each of reports
			for report in reportIds["results"] :
				total_cnt += 1 
				reportId = report['GenerateID']
				reportName = report['GenerateName']
				reportIdName = str(total_cnt) +") "+ "Report ID: " + str(reportId) + " Name: " + reportName
				url = baseUrl + "/" + self.GEN_REPORT_AS_EXCEL + "/" + str(reportId) + "/" + datetime.datetime.today().strftime('%Y%m%d') + postfix
				print(reportIdName + " calling " + url)
				r = requests.get(url) 
				print("status: " + str(r.status_code))
				strResponse = r.text.encode('utf-8') 
				print("response: " + str(strResponse))	
				# Verify status
				if r.status_code == 200 :
					
					#response = json.load(strResponse)
					response = r.json() 
					if response is None :
						print("Error: Cannot parse json") 
						continue;	
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
			print("fatal: " + str(e))
			return 1


	def help(self) :
		print "Example command:" 
		print "python ./clnt_gen_report.py <postfix> <base url>" 
		print "python ./clnt_gen_report.py _0200 http://localhost:8000/gsurvey" 
		 

# Create Client Generator 
clntGen = ClientGenerator()
retry = 0
maxRetry = 3
if len(sys.argv) > 2 :
	while retry < maxRetry :
		if clntGen.genReports(sys.argv[1], sys.argv[2]) == 0 :
			break	
		else:
			retry += 1
			print("Retry :" + str(retry))
			continue
else:
	clntGen.help()
