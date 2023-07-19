import re

import requests

url = "https://gw-mg-test.61info.cn/hll-leads-manager-provider/o/experience/student/specialCourse"
payload = {
    "studentId": 22624518,
    "language": 1
}
header = {
    "authorization": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoickYrMW9oSEFPb2pkN0UzTnpMN3lndzFyS0ViU3RIUXRZZjc5QWVUZUtMcXY5Y2pjWTFJUnpSbTRHd1c2SmZycWE1TEJxUFNNV1graUxPSGtCclhqUmdORG5yZmpyeTl1M1BnZHFQS2xDNDM2YjFwSDRLUnRycGlPaFlMbWN1anB1anptTmxROUt6Q3FMQVJqVThteDQxVHZRVWFaSWY1dzIrYWtiTHFKQzIxMnVUR0tIOTdlWnQrTGxNdDNpQ3R1c2d1dmFmc3VMemE4aUxUTXpTNW5XT2h0cEZKNGV3eW9UajJLYkpDRlhSdHUydGhqcUxOakpIYkowcGFUUnBOcUhiVUpjaDRwVkozaVhYSm1lODEySEE9PSIsImV4cCI6MTcwNTMxMDgyMn0.Z-JrzP57DSmSbgKdn9sQC9hEtj8AdL3RhkRRoMyxzVc"
}
response = requests.post(url=url,data=payload,headers=header)
print(response.json())
ids = re.findall(r"'id': (\d+)", str(response.json()))
names = re.findall(r"'name': (.+?),", str(response.json()))
strips = [i.strip("'") for i in names]
dict_course = dict(zip(ids,strips))
print(dict_course)