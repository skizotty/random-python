import mysql.connector
from mysql.connector import errorcode
import sys
import csv
title = [('user_id'),('record id'),('first name'),('last name')]

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

	query = ("select * from xyz")

	cursor.execute(query)

	rows = cursor.fetchall()

	cursor.close()
	cnx.close()


with open('trial_expired.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(title)
    for row in rows: 
		  wr.writerow(row)


print "trial_expired done"
