import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_USERNAME = os.getenv('DB_USERNAME', 'jjumaev')
DB_PASSWORD = os.getenv('DB_PASSWORD', '34fgres3456@2001')
DB_HOST = os.getenv('DB_HOST', 'csdb.fu.campus')
DB_PORT = os.getenv('DB_PORT', '1521')
DB_SERVICE_NAME = os.getenv('DB_SERVICE_NAME', 'CS40') 