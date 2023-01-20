
#!/bin/bash

# Setup python virtual env with project dependencies
# Setup postgres db 
# Seed db with ingest user, metabase user, and ingest data
# Setup metabase app


set -e

echo "➡️ Begin development environment setup ..."

echo "\n🐍 Setup Python virtual env and install deps ..."
if [ ! -d venv ]; then
    virtualenv venv
    source venv/bin/activate
    pip install -e .
else
    source venv/bin/activate
fi


echo "\n🗂 Create sample ingest data ..."
kidsfirst test d3b_ingest_packages/packages/SD_ME0WME0W

echo "\n🐳 Start postgres db ..."
source .env.local
docker-compose down
docker-compose up -d postgres-db 

sleep 3

echo "\n🗃 Bootstrap postgres dbs ..."
./scripts/init_metabase_db.py $MB_DB_DBNAME -u $MB_DB_USER -w $MB_DB_PASS -p 5432
./scripts/init_db.py $INGEST_DB_DBNAME -u $POSTGRES_ADMIN -w $POSTGRES_ADMIN_PASSWORD -p 5432
./scripts/load_db.py SD_ME0WME0W $INGEST_DB_DBNAME -p 5432

echo "\n🐳 Start metabase app ..."
docker-compose up -d metabase 

echo "\nWaiting for metabase to deploy (may take a minute) ..."
docker-compose logs -f metabase | grep -cm1 "Metabase Initialization COMPLETE"

echo "\n🛠 Setup metabase app ..."
./scripts/setup_metabase.py ingest_db SD_ME0EWME0W

echo "✅ --- Development environment setup complete! ---"

