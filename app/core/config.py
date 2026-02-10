from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")