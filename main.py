import os
from dotenv import load_dotenv
import requests
import logging
import mysql.connector
import json

load_dotenv()

#used for logging messages 'included in log.log file'
logging.basicConfig(level=logging.INFO, filename="log.log",filemode="w",
format="%(asctime)s - %(levelname)s - %(message)s")

# Assign Env to variables to make them easy to call
usr=os.getenv("USR")
pwd=os.getenv("PWD")
idb=os.getenv("IDB")
ddb=os.getenv("DDB")
srv=os.getenv("SERVER")
endpoint=os.getenv("ENDPOINT")

#test API connection
try:
    request = requests.get(endpoint)
    logging.info("sql connection success")

except:
    logging.error("sql connection failed")

finally:
    logging.info("sql connection closed")

mydb = mysql.connector.connect(
  host=srv,
  user=usr,
  password=pwd,
  database=idb
)

mycursor = mydb.cursor()
try:
    mycursor.execute("""select c.country_name,c.adm0_code,c.iso3_code,l.cfii_calcualtion from countries_iso3 as c
join cfii_list as l
on c.adm0_code = l.adm0_code
where l.cfii_calcualtion = '1' """)
    myresult= mycursor.fetchall()
    logging.info("sql query excecuted")
except:
    logging.error("sql query failed")
finally:
    logging.info("sql connection closed")


#get countries list to be calculated
countries_list = []

for result in myresult:
    countries_list.append({"adm0":result[1],"iso3" : result[2]})
print(countries_list[0]['iso3'])


# print(request.text)