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

	query = ("select ft.user_id, ft.sfdc_trial_id as 'record id', u.fname as 'first name', u.lname as 'last name' from free_trial ft inner join users u on u.id = ft.user_id inner join user_campaign_info uci on uci.user_id = ft.user_id left join( select ft.user_id, case when subContacts.contacts is null then 0 else subContacts.contacts end as 'contacts' from free_trial ft left join ( select user_id, count(*) as 'contacts' from contact c where user_id in (select distinct user_id from free_trial) and c.email not in (select email from users u where u.id in (select distinct user_id from free_trial)) and c.email not in (select email from user_campaign_info uci where uci.user_id in (select distinct user_id from free_trial))) subContacts on subContacts.user_id = ft.user_id) sub1Contacts on sub1Contacts.user_id = ft.user_id left join ( select u.id \"user_id\", case when u.vertical_id = 1 and custom_link_1_link is not null and custom_link_2_link is not null then 'good' when u.vertical_id = 1 and custom_link_1_link = '' and custom_link_2_link = '' then 'bad' when u.vertical_id != 1 then 'good' else null end \"is_good_trec\" from free_trial ft inner join users u on u.id = ft.user_id inner join user_microsite_info umi on umi.user_id = ft.user_id ) sub2 on sub2.user_id = ft.user_id where is_active = 1 and is_internal = 0 and email_validated_on is not null and uci.full_name is not null and uci.email is not null and uci.address1 is not null and uci.city is not null and uci.state is not null and uci.zip is not null and uci.logo_img_id is not null and uci.headshot_img_id is not null and sub1Contacts.contacts > 9 and sub2.is_good_trec = 'good' and u.is_onhold = 1")

	cursor.execute(query)

	rows = cursor.fetchall()

	cursor.close()
	cnx.close()


with open('take_off_hold.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(title)
    for row in rows: 
		  wr.writerow(row)

print "take_off_hold done"

