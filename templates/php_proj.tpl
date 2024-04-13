#!/bin/sh

yum install epel-release -y
yum update
yum install -y git
yum install nginx -y
systemctl enable --now nginx
yum install -y certbot-nginx
yum install -y composer
yum install -y php-fpm
systemctl enable --now php-fpm
dnf install -y mariadb105
dnf install -y mariadb105-server
sudo systemctl enable --now mariadb
yum install -y openssl php-bcmath php-curl php-json php-mbstring php-tokenizer php-xml php-zip

touch setupcert.sh
echo"
certbot --nginx -d ${application_domain} www.${application_domain} --agree-tos --quiet
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/certbot renew --quiet") | crontab -
" > setupcert.sh


cd /etc/nginx/conf.d/
touch ${git_repo_name}.conf
echo "
server {
        listen 80 ${application_domain}; #www.${application_domain};
        listen [::]:80 ${application_domain}; #www.${application_domain};

        root /var/www/vhosts/${git_repo_name};

        index index.php index.html index.htm index.nginx-debian.html;

        server_name ${application_domain};
        location /{
		    try_files \$uri \$uri/ /index.php;

            location = /index.php {
                        include /etc/nginx/fastcgi_params;
                        fastcgi_index index.php;
                        fastcgi_intercept_errors on;
                        fastcgi_split_path_info ^(.+\.php)(/.+)$;
                        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
                        fastcgi_pass 127.0.0.1:9000;
                }
	}

}
" > ${git_repo_name}.conf
systemctl restart nginx

mkdir -p /var/www/vhosts/ 
cd /var/www/vhosts/
git init
git clone ${git_repo}

cd /var/www/vhosts/${git_repo_name}
chmod 755 -R .
chown apache -R .

sed -i "s/^listen =.*/listen = 127.0.0.1:9000/" /etc/php-fpm.d/www.conf
password=$(tr -dc 'A-Za-z0-9!?%=' < /dev/urandom | head -c 10)
mysql --user=root <<_EOF_
create user '${git_repo_name}'@'localhost' identified by '${db_pass}';
create database '${git_repo_name}';
grant all privileges on ${git_repo_name}.* TO '${git_repo_name}'@'localhost';
ALTER USER 'root'@'localhost' IDENTIFIED BY '$password';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
_EOF_

touch ~/.my.cnf
echo "
[mysql]
host=localhost
user=root
password=$password
"> ~/.my.cnf

yum -y update