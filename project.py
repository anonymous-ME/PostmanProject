import mysql.connector
import re
import requests
import json

slack_url = "https://hooks.slack.com/services/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"
WarningThreshold=90

mydb = mysql.connector.connect(
  host="localhost",
  database = "project",
  user="root",
  passwd="password"
)
Limits={'tinyint':127,'tinyint unsigned':255,'smallint':32767,'smallint unsigned':65535,'mediumint':8388607,'mediumint unsigned':16777215,'int':2147483647,'int unsigned':4294967295,'bigint':9223372036854775807,'bigint unsigned':18446744073709551615}
mycursor = mydb.cursor()

mycursor.execute("show tables")
myresult = mycursor.fetchall()

for x in myresult:
    mycursor.execute('show columns from '+str(x[0])+' where Extra="auto_increment"')
    res = mycursor.fetchall()
    mycursor.execute('select Max('+res[0][0]+') as Max from '+str(x[0]))
    curr_val = mycursor.fetchall()
    data_type = (re.sub(r'\(.*\)', '', res[0][1]))
    max_val = Limits[str(data_type)]

    percent_full = (int(curr_val[0][0])/int(max_val))*100
    
    if percent_full >= WarningThreshold:
        msg = {"text":"**WARNING** \n Auto Increment LIMIT APPROACHING for "+str(x[0])+" table."}
        requests.post(slack_url,data=json.dumps(msg))
