#!/usr/bin/env bash
# install nginx and configure with landing page
# redirect_me to my github account
# render an error 404 page
# add response header
# create static page (hbnb_static) and render it

sudo apt-get update
sudo apt-get install -y nginx
echo "Hello World!" > /var/www/html/index.nginx-debian.html
touch /var/www/html/404.html
echo "Ceci n'est pas une page" > /var/www/html/404.html

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
printf %s "<!DOCTYPE html>
<html>
  <head>
    <title>MrBridge</title>
  </head>
  <body>Welcome to MrBridge</body>
</html>
" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen      80 default_server;
    listen      [::]:80 default_server;
    add_header  X-Served-By $HOSTNAME;
    root        /var/www/html;
    index       index index.html index.htm index.nginx-debian.html;

    location /redirect_me {
                return 301 https://github.com/mrbridge-mrbridge/;
    }
    error_page 404 /404.html;
    location = /404.html {
                root /var/www/html;
                internal;
    }

    location /hbnb_static {
                alias /data/web_static/current;
                index index.html index.htm;
    }
}
" > /etc/nginx/sites-available/default
sudo service nginx restart
