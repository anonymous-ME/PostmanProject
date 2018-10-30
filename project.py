import mysql.connector
import re
import requests
import json
import ConfigParser

#Retrieving Values From Configuration File
config = ConfigParser.ConfigParser()
config.readfp(open(r'auto_increment_check.config'))
user_name = config.get('MySQL', 'user_name')
password = config.get('MySQL', 'password')
host = config.get('MySQL', 'host')
database = config.get('MySQL', 'database')
slack_url = config.get('Slack', 'msg_url')
WarningThreshold = config.get('Param', 'Warning_Threshold')

#Connect to server and select database
mydb = mysql.connector.connect(
  host= host,
  database = database,
  user = user_name,
  passwd = password
)

#Max Limit For Different Data Types In MySQL
Limits={'tinyint':127,'tinyint unsigned':255,'smallint':32767,'smallint unsigned':65535,'mediumint':8388607,'mediumint unsigned':16777215,'int':2147483647,'int unsigned':4294967295,'bigint':9223372036854775807,'bigint unsigned':18446744073709551615}

#Initializing Cursor
mycursor = mydb.cursor()

#Retrieving All Tables In The Database
mycursor.execute("show tables")
myresult = mycursor.fetchall()

#Iterating Over All The Tables In The Database
for x in myresult:
    #Fetching Column With auto_increment
    mycursor.execute('show columns from '+str(x[0])+' where Extra="auto_increment"')
    res = mycursor.fetchall()
    #Checking If Table has auto_increment
    if len(res) > 0:
        #Retrieving Current Value For auto_increment
        mycursor.execute('select Max('+res[0][0]+') as Max from '+str(x[0]))
        curr_val = mycursor.fetchall()
        #Retrieving Data Type
        data_type = (re.sub(r'\(.*\)', '', res[0][1]))
        #Retrieving Max Value For The Data Type
        max_val = Limits[str(data_type)]
        #Calculating Percentage Full
        percent_full = (int(curr_val[0][0])/int(max_val))*100
        #Checking If Crossed Our Set Threshold Value
        if int(percent_full) >= int(WarningThreshold):
            #Sending Warning Message On Slack
            msg = {"text":"**WARNING** \n Auto Increment LIMIT APPROACHING for "+str(x[0])+" table."}
            requests.post(slack_url,data=json.dumps(msg))
