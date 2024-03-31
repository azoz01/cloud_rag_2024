export HOST_ADDRESS=$1
export USER=$2
export PGPASSWORD=$3

psql -h $HOST_ADDRESS -p 5432 -U $USER -d postgres -f scripts/db_setup/create_database.sql
psql -h $HOST_ADDRESS -p 5432 -U $USER -d user_history -f scripts/db_setup/setup_db.sql
