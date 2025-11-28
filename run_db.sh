docker run -d \
  --name mysql-fuzz \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=fuzzdb \
  -p 3306:3306 \
  mysql:8

