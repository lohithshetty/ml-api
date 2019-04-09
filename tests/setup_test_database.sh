sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
export DATABASE_URL='postgres://postgres:postgres@127.0.0.1/postgres'
python3 $PWD/tests/setup_db.py
