
#!/bin/bash

# Setup python virtual env with project dependencies
# Setup postgres db 
# Seed db with ingest user, metabase user, and ingest data
# Setup metabase app


set -e

echo "➡️ Begin development environment setup ..."

echo "🐍 Setup Python virtual env and install deps ..."
if [ ! -d venv ]; then
    virtualenv venv
    source venv/bin/activate
    pip install -e .
else
    source venv/bin/activate
fi


echo "🗂 Create sample ingest data ..."
kidsfirst test d3b_ingest_packages/packages/SD_ME0WME0W

echo "🐳 Start postgres db ..."
source .env && source .env.fly
docker-compose down
docker-compose up -d postgres-db 

sleep 3

echo "🗃 Bootstrap postgres dbs ..."
./scripts/init_metabase.py metabase_db -u $POSTGRES_ADMIN -w $POSTGRES_ADMIN_PASSWORD -p 5432
./scripts/init_db.py ingest_db -u $POSTGRES_ADMIN -w $POSTGRES_ADMIN_PASSWORD -p 5432
./scripts/load_db.py SD_ME0WME0W ingest_db -p 5432

echo "🐳 Start metabase app ..."
docker-compose up -d metabase 

sleep 45

echo "🛠 Setup metabase app ..."
./scripts/setup_metabase.py ingest_db SD_ME0EWME0W

echo "✅ --- Development environment setup complete! ---"

