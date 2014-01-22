import logging
import json
import glob
import re
from datetime import datetime
from string import Template

""" Variables """
logging.basicConfig(filename='../../../transformer_game_stats.log', level=logging.DEBUG)
tableTemplate=Template('$gameID\x01$gameDate\x01$gameStatus\x01$gameSeason\x01$gameSequence\x01$gameAttendance\x01$teamHomeID\x01$teamVisitID\n')
filenamePattern = re.compile(".*(\d{10})_.*$")
inputDir = "../../../output/"
outputDirPrefix = "../../../"
filesProcessed = 0
exceptionsThrown = 0

print 'Starting Transforming'
logging.info('Staring Transforming')

gamePlayerFileName = "%sgame_stats.hive" % outputDirPrefix
with open(gamePlayerFileName, 'a+') as outfile:
    for f in glob.glob(inputDir + "*_gamestats.json"):
        try:
            d = open(f, 'r')
            gameID = filenamePattern.match(f).group(1)
            content = json.load(d, encoding='utf-8')
            gameDate=content['resultSets'][0]['rowSet'][0][0]
            gameDate=datetime.strptime(gameDate, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            gameStatus=content['resultSets'][0]['rowSet'][0][4]
            teamHomeID=content['resultSets'][0]['rowSet'][0][6]
            teamVisitID=content['resultSets'][0]['rowSet'][0][7]
            gameSeason=content['resultSets'][0]['rowSet'][0][8]
            gameSequence=content['resultSets'][1]['rowSet'][0][1]
            gameAttendance=content['resultSets'][8]['rowSet'][0][1]

            outfile.write(tableTemplate.substitute(gameID=gameID, gameDate=gameDate,gameStatus=gameStatus,gameSeason=gameSeason,gameSequence=gameSequence,gameAttendance=gameAttendance,teamHomeID=teamHomeID,teamVisitID=teamVisitID))
           
            d.close()
            filesProcessed += 1
        except Exception as e:
            logging.exception("Error in transforming file: %s" % f)
            exceptionsThrown += 1
            continue
outfile.close()

print '\nStopping Transforming\n-- Files Processed: %s\n-- Exceptions Caught: %s' %(filesProcessed, exceptionsThrown)
logging.info('Stopping Transforming\n-- Files Processed: %s\n-- Exceptions Caught: %s' %(filesProcessed, exceptionsThrown))