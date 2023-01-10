import os

ROOT_DIR = os.path.dirname(os.path.dirname((__file__)))
PACKAGES_DIR = "d3b_ingest_packages/packages"

INGEST_DB_HOST = os.getenv("POSTGRES_HOST") or "localhost"
INGEST_DB_PORT = os.getenv("POSTGRES_PORT") or 5432
INGEST_PROCESS_USER = os.getenv("INGEST_PROCESS_USER")
INGEST_PROCESS_PASSWORD = os.getenv("INGEST_PROCESS_PASSWORD")
INGEST_VIEWER_USER = os.getenv("INGEST_VIEWER_USER")
INGEST_VIEWER_PASSWORD = os.getenv("INGEST_VIEWER_PASSWORD")

METABASE_DB_USER = os.getenv("MB_DB_USER")
METABASE_DB_PASSWORD = os.getenv("MB_DB_PASS")
METABASE_APP_ADMIN = os.getenv("MB_APP_ADMIN")
METABASE_APP_ADMIN_EMAIL = os.getenv("MB_APP_ADMIN_EMAIL")
METABASE_APP_ADMIN_PASSWORD = os.getenv("MB_APP_ADMIN_PASS")
METABASE_APP_URL = os.getenv("MB_APP_URL")

METABASE_SETUP_TEMPLATE = os.path.join(
    ROOT_DIR, "config", "metabase_setup_template.json"
)
