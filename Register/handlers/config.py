from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN= os.getenv("BOT_TOKEN")
PSQL_USER= os.getenv("PSQL_USER")
PSQL_PASSWORD= os.getenv("PSQL_PASSWORD")
PSQL_HOST= os.getenv("PSQL_HOST")
PSQLDB_NAME= os.getenv("PSQLDB_NAME")
ADMIN_ID=int(os.getenv("ADMIN_ID"))