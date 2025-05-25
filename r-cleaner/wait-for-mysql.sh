#!/bin/bash

host="db"
port="3306"
user="projeto"
password="projeto"
database="app_db"

echo "⏳ Waiting for MySQL on $host:$port..."

# Wait for MySQL port
until nc -z "$host" "$port"; do
  echo "❌ MySQL not available yet..."
  sleep 2
done

echo "✅ Port open - now checking DB connection..."

# Wait for successful login
until mysql -h "$host" -u"$user" -p"$password" -e "SELECT 1;" "$database" > /dev/null 2>&1; do
  echo "❌ MySQL login still failing"
  sleep 2
done

echo "✅ Connected to MySQL - checking if table 'rios' has data..."

# Check if the 'rios' table has any rows
row_count=$(mysql -h "$host" -u"$user" -p"$password" -D "$database" -se "SELECT COUNT(*) FROM dados_alagamento;" 2>/dev/null)

if [ "$row_count" -eq 0 ]; then
  echo "⚠️ A tabela 'rios' está vazia. Encerrando sem rodar o script R."
  exit 0
fi

echo "✅ Tabela 'rios' possui $row_count registros - executando script R"

# Run the R script or other command passed to this script
exec "$@"
