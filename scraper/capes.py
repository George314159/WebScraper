from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

def fetchContentFromURL(url, data):
    try:
        with closing(post(url, data=data, stream=True)) as response:
            if isValidResponse(response):
                return response.content
            else:
                return None
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))

def isValidResponse(response):
    contentType = response.headers['Content-Type'].lower()
    return (response.status_code == 200
        and contentType is not None)

COUNT = str(2747)
URL = 'https://cape.ucsd.edu/responses/Results.aspx'
DATA = {
    'ctl00%24ContentPlaceHolder1%24btnSubmit': 'Search',
    'ctl00%24ContentPlaceHolder1%24ddlDepartments': 'ANTH',
    '__ASYNCPOST': 'true',
}
rawContent = fetchContentFromURL(URL, DATA)
stringContent = str(rawContent)
output = stringContent

#soupHTML = BeautifulSoup(rawHTML, 'html.parser')
#for i, li in enumerate(soupHTML.select('li')):
#    print(i, li.text)

outputFile = open('output.txt', 'w')
#outputFile.write(soupHTML.prettify())
outputFile.write(str(output))
outputFile.close()