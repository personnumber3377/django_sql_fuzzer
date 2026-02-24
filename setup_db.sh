#!/bin/bash

set -e

echo "Updating package lists..."
sudo apt update

echo "Installing MySQL server..."
sudo apt install -y mysql-server

echo "Starting MySQL service..."
sudo systemctl start mysql
sudo systemctl enable mysql

echo "Configuring root user password..."

sudo mysql <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
EOF

echo "Creating database fuzzdb..."

mysql -u root -ppassword <<EOF
CREATE DATABASE fuzzdb;
EOF

echo "Testing connection..."

mysql -u root -ppassword -e "SHOW DATABASES;"

echo ""
echo "✅ MySQL setup complete."
echo "Database: fuzzdb"
echo "Username: root"
echo "Password: password"
echo ""

