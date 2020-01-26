from bs4 import BeautifulSoup
import json
import os
import sys
import glob
import errno

CAPES_DATA_BLOB_PATH = './capes/*.html'
OUTPUT_PATH = './capes2.json'

def evaluateResponse(response):
    soupHTML = BeautifulSoup(response, 'html.parser')
    result = []
    for _, tr in enumerate(soupHTML.select('tr')):
        children = tr.findChildren('td', recursive=False)
        resultEntry = {}
        if len(children) > 0:
            resultEntry['instructor'] = children[0].text.strip()
            resultEntry['course'] = children[1].text.strip()
            resultEntry['term'] = children[2].text.strip()
            resultEntry['enrolled'] = children[3].text.strip()
            resultEntry['evalCount'] = children[4].text.strip()
            resultEntry['recommendedClass'] = children[5].text.strip()
            resultEntry['recommendedInstr'] = children[6].text.strip()
            resultEntry['StudyHrs/Week'] = children[7].text.strip()
            resultEntry['AvgGradeExpected'] = children[8].text.strip()
            resultEntry['AvgGradeReceived'] = children[9].text.strip()
            result.append(resultEntry)
    return result

contentResult = {}

# source: https://askubuntu.com/questions/352198/reading-all-files-from-a-directory
files = glob.glob(CAPES_DATA_BLOB_PATH)
for name in files:
    try:
        with open(name) as f:
            contentResult[os.path.basename(name)] = evaluateResponse(f.read())
    except IOError as err:
        if err.errno != errno.EISDIR:
            raise

output = json.dumps(contentResult, indent=4, sort_keys=True)
outputFile = open(OUTPUT_PATH, 'w')
outputFile.write(output)
outputFile.close()
