#!/bin/sh

#yum -y install httpd php mysql php-mysql

# Install Packages
# Will need if statement adding to only install required packages once a different script determines what's required

yum install epel-release -y
yum update
yum install -y git
yum install nginx -y
systemctl enable --now nginx
#systemctl enable --now php-fpm
yum install -y certbot-nginx

touch setupcert.sh
echo"
certbot --nginx -d ${application_domain} www.${application_domain} --agree-tos --quiet
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/certbot renew --quiet") | crontab -
" > setupcert.sh


# Configure NGINX
cd /etc/nginx/conf.d/
touch ${git_repo_name}.conf
echo "
server {
        listen 80 ${application_domain} #www.${application_domain};
        listen [::]:80 ${application_domain} #www.${application_domain};

        root /var/www/vhosts/${git_repo_name};

        index index.html index.htm index.nginx-debian.html;

        server_name ${application_domain};

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
}
" > ${git_repo_name}.conf
systemctl reload nginx

# setup git repository in /var/www/vhosts
mkdir -p /var/www/vhosts/ 
cd /var/www/vhosts/
git init
git clone ${git_repo}

yum -y update









## write a bash script that installs mysql/nginx and php-fpm
## then it needs to configure nginx configs
## then it needs to setup and configure openSSL