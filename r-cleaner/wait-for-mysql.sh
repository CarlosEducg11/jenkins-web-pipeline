#!/bin/bash

host="db"
port="3306"

echo "⏳ Waiting for MySQL on $host:$port..."

until nc -z "$host" "$port"; do
  echo "❌ MySQL not available yet..."
  sleep 2
done

echo "✅ Port open - now checking DB connection..."

# Now test MySQL with real credentials
mysql -h db -u projeto -pprojeto -e "SELECT 1;" app_db || {
  echo "❌ MySQL login still failing"
  exit 1
}

echo "✅ MySQL is ready - running command"
exec "$@"