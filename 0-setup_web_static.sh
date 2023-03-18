#!/usr/bin/env bash
# Script to prepare a web server for web static project

## Update server
apt update
apt -y upgrade

## Install NGINX
apt -y install nginx

## Creates directories
mkdir -p /data/web_static/shared /data/web_static/releases/test

## Write Hello World in index with tee command
echo "Hello World" | tee /data/web_static/releases/test/index.html

## Create Symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

## Change owner and group like ubuntu
chown -R ubuntu:ubuntu /data

## Add static location to nginx settings:

printf %s "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By $HOSTNAME;
        root /var/www/html;
        index index.html;

        location /hbnb_static {
            alias /data/web_static/current;
            index index.html index.htm;
        }
}" > /etc/nginx/sites-available/default

## Restart NGINX
service nginx restart
