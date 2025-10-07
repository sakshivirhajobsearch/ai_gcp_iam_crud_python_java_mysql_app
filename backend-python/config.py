import os

# ---------- MySQL Configuration ----------
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'admin'
MYSQL_DB = 'ai_gcp_iam'

# ---------- Google Cloud IAM Configuration ----------
# Set to False to use real GCP credentials
USE_DUMMY = True  

# Path to your service account JSON (for real GCP)
GCP_SERVICE_ACCOUNT_FILE = os.getenv(
    'GCP_SERVICE_ACCOUNT_FILE',
    'gcp_service_account.json'  # replace with actual path to your JSON
)

if not USE_DUMMY:
    from google.oauth2 import service_account
    try:
        credentials = service_account.Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_FILE)
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account file not found: {GCP_SERVICE_ACCOUNT_FILE}")
else:
    credentials = None  # Not used in dummy mode
