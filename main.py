import os
from dotenv import load_dotenv

load_dotenv()
usr=os.getenv("USR")
pwd=os.getenv("PWD")
idb=os.getenv("IDB")
ddb=os.getenv("DDB")
endpoint=os.getenv("ENDPOINT")
print(usr,pwd,idb,ddb,endpoint)
