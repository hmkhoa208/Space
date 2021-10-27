from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# Lay BeautifulSoup cua website
def getSoup(site):
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(site)
	time.sleep(5)
	soup = BeautifulSoup(driver.page_source,'lxml')
	driver.quit()
	return soup

class Lauch:
	def __init__(self, id, date, payload, lauchVehicle, site, remark):
		self.id = id
		self.date = date
		self.payload = payload
		self.lauchVehicle = lauchVehicle
		self.site = site
		self.remark = remark

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4, ensure_ascii=False)

	def print(self):
		print(self.id)
		print(self.date)
		print(self.payload)
		print(self.lauchVehicle)
		print(self.site)
		print(self.remark)

def getLauchData():
	soup = getSoup('https://space.skyrocket.de/doc_chr/lau2021.htm')
	rowArr = soup.find(id = 'chronlist').tbody.find_all('tr')

	# jsonStr = '{\n'
	launchArr = []
	for tr in rowArr:
		all_td = tr.find_all('td')
		if len(all_td) == 6:

			if all_td[2].text != '':
				payloadArr = all_td[2].text.split("\n")
			else:
				payloadArr = []

			status = 'success'
			if all_td[5].text == 'failed':
				status = 'failed'

			remark = {"id": all_td[0].text, "status": status}
			
			launch = Lauch(all_td[0].text, all_td[1].text, payloadArr, all_td[3].text, all_td[4].text, remark)
			# if launch.remark == '':
			# 	launch.remark = 'success'
			launchArr.append(launch)
			# jsonStr += ('"' + launch.id + '": ' + launch.toJSON() + ',\n')

	# jsonStr += '}'
	return launchArr



#----------------------------------------
#main code

launchArr = getLauchData()
jsonStr = ''
filename = 'space.json'

# 2. Update json object
for entry in launchArr:
	jsonStr += ('"' + entry.id + '": ' + entry.toJSON() + ',\n')

jsonStr = jsonStr[:-2]

# 3. Write json file
with open(filename, "w") as file:
    file.write(jsonStr)

