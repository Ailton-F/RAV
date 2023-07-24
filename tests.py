from dotenv import load_dotenv
import os
load_dotenv()

print('URI: ',os.getenv('MYSQL_URI'))