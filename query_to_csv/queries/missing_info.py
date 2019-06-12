import mysql.connector
from mysql.connector import errorcode
import sys
import csv
title = [('user_id'),('first name'),('last name'),('record id'),('Days since signup'),('email_validated'),('full_name'),('email'),('address'),('city'),('zip'),('state'),('logo'),('headshot'),('contacts'),('TREC')]


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

	query = ("select u.id, u.fname as 'first name', u.lname as 'last name', ft.sfdc_trial_id as 'record id', DATEDIFF(CURRENT_DATE,u.created_on) as \"Days since signup\", case when email_validated_on is null then 'false' else 'true' end as 'email_validated', case when uci.full_name is null then 'false' else 'true' end as 'full_name', case when uci.email is null then 'false' else 'true' end as 'email', case when uci.address1 is null then 'false' else 'true' end as 'address', case when uci.city is null then 'false' else 'true' end as 'city', case when uci.zip is null then 'false' else 'true' end as 'zip', case when uci.state is null then 'false' else 'true' end as 'state', case when uci.logo_img_id is null then 'false' else 'true' end 'logo', case when uci.headshot_img_id is null then 'false' else 'true' end as 'headshot', case when sub1.contacts < 10 then 'false' else 'true' end as 'contacts', case when sub2.is_good_trec != 'good' then 'false' else 'true' end as \"TREC\" from users u inner join user_campaign_info uci on uci.user_id = u.id inner join free_trial ft on ft.user_id = u.id left join( select ft.user_id, case when subContacts.contacts is null then 0 else subContacts.contacts end as 'contacts' from free_trial ft left join (select user_id,count(*) as 'contacts' from contact c where user_id in (select distinct user_id from free_trial) and c.email not in (select email from users u where u.id in (select distinct user_id from free_trial)) and c.email not in (select email from user_campaign_info u where u.id in (select distinct user_id from free_trial))) subContacts on subContacts.user_id = ft.user_id) sub1 on sub1.user_id = u.id left join ( select u.id \"user_id\", case when u.vertical_id = 1 and custom_link_1_link != '' and custom_link_2_link != '' then 'good' when u.vertical_id = 1 and custom_link_1_link = '' and custom_link_2_link = '' then 'bad' when u.vertical_id != 1 then 'good' else null end \"is_good_trec\" from free_trial ft inner join users u on u.id = ft.user_id inner join user_microsite_info umi on umi.user_id = ft.user_id ) sub2 on sub2.user_id = u.id where u.id not in ( select ft.user_id from free_trial ft inner join users u on u.id = ft.user_id inner join user_campaign_info uci on uci.user_id = ft.user_id left join ( select ft.user_id,count(c.id) from free_trial ft left join contact c on c.user_id = ft.user_id where is_active = 1 and contact_status_id in (1,2) and is_active_global = 1 and is_deleted = 0 and c.user_id in (select distinct user_id from free_trial) and c.email not in (select email from users u where id in (select distinct user_id from free_trial)) and c.email not in (select email from user_campaign_info u where user_id in (select distinct user_id from free_trial)) group by 1 ) sub1 on sub1.user_id = ft.user_id left join ( select u.id \"user_id\", case when u.vertical_id = 1 and custom_link_1_link != '' and custom_link_2_link != '' then 'good' when u.vertical_id = 1 and custom_link_1_link = '' and custom_link_2_link = '' then 'bad' when u.vertical_id != 1 then 'good' else null end \"is_good_trec\" from free_trial ft inner join users u on u.id = ft.user_id inner join user_microsite_info umi on umi.user_id = ft.user_id ) sub2 on sub2.user_id = ft.user_id where is_active = 1 and is_internal = 0 and email_validated_on != '' and uci.full_name != '' and uci.email != '' and uci.address1 != '' and uci.city != '' and uci.state != '' and uci.zip != '' and (uci.logo_v2_image_hash != '' or uci.logo_image_hash != '') and (uci.headshot_v2_image_hash != '' or uci.headshot_image_hash != '') and sub1.contacts > 9 and sub2.is_good_trec = 'good' and u.is_onhold = 1 ) and u.id not in ( select user_id from campaign where campaign_status_id = 5 group by user_id having count(*) > 0) and u.is_onhold = 1 and u.id in (select user_id from free_trial) and u.email not like '%outboundengine%' and u.created_on > '2019-05-19 23:59:59' ")

	cursor.execute(query)

	rows = cursor.fetchall()

	cursor.close()
	cnx.close()


with open('missing_info.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(title)
    for row in rows: 
		  wr.writerow(row)


print "missing_info done"
