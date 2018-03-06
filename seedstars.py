import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import sqlite3
import getpass
import time
import datetime

username = raw_input("Username: ")
password = getpass.getpass("Password: ")
try:
    J = Jenkins('http://localhost:8080',username,password)
except:
    print("Error logging in")

db = sqlite3.connect('jenkinsdb')

cursor = db.cursor()

null = "NULL" #Jobs don't have to have a description, this will be used in such cases
jobs = []
cursor.execute('CREATE table IF NOT exists Jobs (name TEXT, description TEXT, lastBuild INTEGER, buildStatus TEXT, dateChecked TEXT)')

print "Getting jobs..."
for job_name, job_instance in J.get_jobs():
    if not job_instance.is_queued_or_running():
        print "Getting information on job " + job_name
        last_build = job_instance.get_last_build()
        last_build_status = last_build.get_status()
        if job_instance.get_description() is None:
            cursor.execute('INSERT INTO Jobs (name,null,lastBuild,buildStatus,dateChecked) values (?,?,?,?,?)', (job_name, null, str(last_build), str(last_build_status), str(datetime.datetime.now())))
        else:
            description = job_instance.get_description()
            cursor.execute('INSERT INTO Jobs (name,description,lastBuild,buildStatus,dateChecked) values (?,?,?,?,?)', (job_name, description, str(last_build), str(last_build_status), str(datetime.datetime.now())))
        db.commit()

cursor.execute('SELECT * FROM Jobs')
result = cursor.fetchall()
for res in result:
    print res