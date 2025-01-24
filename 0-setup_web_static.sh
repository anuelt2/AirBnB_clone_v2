#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

if ! command -v nginx > /dev/null 2>&1
then
	sudo apt-get update -y
	sudo apt-get install -y nginx
	sudo ufw allow OpenSSH
	sudo ufw enable
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

sudo echo "<!DOCTYPE html>
<html>
<head>
</head>
<body>
	Welcome to Nginx Server - ALX
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

NGINX_CONFIG_FILE="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/ {" "$NGINX_CONFIG_FILE"
then
	sudo cp --backup=numbered "$NGINX_CONFIG_FILE" "$NGINX_CONFIG_FILE".bak
	sudo sed -i "/server_name/ a\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" "$NGINX_CONFIG_FILE"
fi

sudo nginx -t
exit_code=$?

if (( exit_code == 0 ))
then
	sudo service nginx restart
fi
