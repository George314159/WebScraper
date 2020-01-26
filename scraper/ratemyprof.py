from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

MAX_NUMBER_OF_PROFS = 2747
OUTPUT_PATH = 'ratemyprof.json'

def fetchContentFromURL(url):
    try:
        with closing(get(url, stream=True)) as response:
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

COUNT = str(MAX_NUMBER_OF_PROFS)
URL = 'https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=' + COUNT + '&wt=json&json.wrf=noCB&callback=noCB&q=*%3A*+AND+schoolid_s%3A1079&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=' + COUNT + '&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='
rawContent = fetchContentFromURL(URL)
stringContent = str(rawContent)[7:-2].replace('\\', '')
output = json.loads(stringContent)
output = json.dumps(output, indent=4, sort_keys=True)

#soupHTML = BeautifulSoup(rawHTML, 'html.parser')
#for i, li in enumerate(soupHTML.select('li')):
#    print(i, li.text)

outputFile = open(OUTPUT_PATH, 'w')
#outputFile.write(soupHTML.prettify())
outputFile.write(str(output))
outputFile.close()