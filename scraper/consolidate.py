import sys
import glob
import errno
import json

RATE_MY_PROF_DATA_FILE_PATH = './ratemyprof.json'
CAPES_DATA_FILE_PATH = './capes2.json'
OUTPUT_PATH = './cleandata.json'

def loadJSONFile(filepath):
    contentString = ''
    try:
        with open(filepath) as f:
            contentString = f.read()
    except IOError as err:
        if err.errno != errno.EISDIR:
            raise
    return json.loads(contentString)

rateData = loadJSONFile(RATE_MY_PROF_DATA_FILE_PATH)
capeData = loadJSONFile(CAPES_DATA_FILE_PATH)
cleanData = {}
capeAverageData = {}

# Get relevant capes data...
for key in capeData:
    for value in capeData[key]:
        if not value['instructor']:
            print('Skipped \'' + str(value) + '\'...')
            continue

        fullName = value['instructor'].upper()
        lastName = fullName[:fullName.index(',')]
        
        # Create the data entry if it doesn't exist...
        dataEntry = None
        if lastName in capeAverageData:
            dataEntry = capeAverageData[lastName]
        else:
            dataEntry = capeAverageData[lastName] = {
                "name": fullName,
                "value": 0,
                "count": 0,
                "average": 0,
            }

        # Removes any profs with duplicate last names
        if dataEntry['name'] != fullName:
            del capeAverageData[lastName]
        else:
            # Save the data for average func later
            recommendValue = float(value['recommendedInstr'][:-1].strip())
            recommendCount = int(value['evalCount'])
            capeAverageData[lastName]['value'] += recommendValue * recommendCount
            capeAverageData[lastName]['count'] += recommendCount

# Compute average for that data...
for _, value in capeAverageData.items():
    value['average'] = float(value['value']) / float(value['count'])

# Compute for RateMyProf...

# Set it to the output data...
cleanData = capeAverageData

# Write data to output
output = json.dumps(cleanData, indent=4, sort_keys=True)
outputFile = open(OUTPUT_PATH, 'w')
outputFile.write(output)
outputFile.close()
