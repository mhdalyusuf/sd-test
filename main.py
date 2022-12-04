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
informaitondb=os.getenv("INFODB")
dedicateddb=os.getenv("DEDICATEDDB")
srv=os.getenv("SERVER")

country = "AFG"
startdate= "2022-12-01"
enddate= "2022-12-01"

endpoint=f"https://api.hungermapdata.org/v1/foodsecurity/country/{country}/region?date_start={startdate}&date_end={enddate}"

#test API connection
try:
    request = requests.get(endpoint)
    logging.info("sql connection success")

except:
    logging.error("sql connection failed")

finally:
    logging.info("sql connection closed")

infodb = mysql.connector.connect(
  host=srv,
  user=usr,
  password=pwd,
  database=informaitondb
)

resultdb = mysql.connector.connect(
  host=srv,
  user=usr,
  password=pwd,
  database=dedicateddb
)

mycursor = infodb.cursor()
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

fulldata = ""
#get countries list to be calculated
countries_list = []

for result in myresult:
    country=result[2]
    endpoint=f"https://api.hungermapdata.org/v1/foodsecurity/country/{country}/region?date_start={startdate}&date_end={enddate}"
    # countries_list.append(result[1],"iso3" : result[2]})
    x = requests.get(endpoint)
    print(endpoint)
    formatted=x.json()
    for region in formatted:
        region_name= region['region']['name']
        rcsi=region['metrics']['rcsi']['prevalence']
        fcs=region['metrics']['fcs']['prevalence']
        cfii=0
        if fcs>0.5:
            cfii = (fcs+rcsi) / 2
        elif fcs<=0.5:
            cfii=((0.5*fcs) + (1.5 * rcsi))/2
        else:
            fcs=0
        

        # print (country,region_name,rcsi,fcs,cfii)
        try:
            resultdb.connect()
            mycursor = resultdb.cursor()
            val = (country,region_name,rcsi,fcs,cfii)
            sql = f"INSERT INTO cfii_calculation (country, region,rcsi,fcs,cfii) VALUES ('{country}','{region_name}',{rcsi},{fcs},{cfii})"
            print (sql)
            mycursor.execute(sql)
            resultdb.commit()
        except:
            logging.error("sql query failed")
        finally:
            mycursor.close()
            resultdb.close()
            logging.info("sql connection closed")    