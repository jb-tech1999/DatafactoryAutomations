import pyodbc
import time
import datetime

server = 'servername'
database = 'database name'
username = 'username'
password = 'password'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = conn.cursor()

#get all stored procedures from the database
cursor.execute("SELECT name FROM sys.procedures")
procedures = cursor.fetchall()

for proc in procedures:
    if 'UPD' in proc[0].upper():
        template = '''
                {
                "name": "%s",
                "type": "SqlServerStoredProcedure",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false,
                    "secureInput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "storedProcedureName": "[schemaname].[%s]"
                },
                "linkedServiceName": {
                    "referenceName": "linked service name",
                    "type": "LinkedServiceReference"
                }
            },
            
'''%(proc[0], proc[0])
        #append to file
        with open('procs.json', 'a') as f:
           f.write(template)
    #print(template)
