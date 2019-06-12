import mysql.connector
from mysql.connector import errorcode
import sys
import os

try:
  cnx = mysql.connector.connect(user='XXX', password='XXX',
                              host='XXX',
                              database='XXX')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
	cursor = cnx.cursor()

	query = ("select id,name,html_content from template_store where html_tpl_file is null and html_content is not null and name is not null")

	cursor.execute(query)

	rows = cursor.fetchall()

	cursor.close()
	cnx.close()


for row in rows: 
  splitString = row[1].split('/')
  listLength = len(splitString)-1
  fileId = row[0]
  fileName = splitString[listLength].replace('.html','')+"_"+str(fileId) + '.html'
  with open('/tmp/path/to/thing/'+fileName, "w") as file:
    file.write(row[2])
  print fileName + ' is migrated.'
