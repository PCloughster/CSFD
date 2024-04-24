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
        listen 80 ${var.application_domain == "default_server" ? "default_server" : "www.${var.application_domain} ${var.application_domain}"};
        listen [::]:80 ${var.application_domain == "default_server" ? "default_server" : "www.${var.application_domain} ${var.application_domain}"};

        root /var/www/vhosts/${git_repo_name}/public/;

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

cp .env.example .env
sed -i "s/^APP_URL=.*/APP_URL=${application_domain}/" .env
sed -i "s/^APP_DEBUG=.*/APP_DEBUG=false/" .env
sed -i "s/^DB_HOST=.*/DB_HOST=localhost/" .env
sed -i "s/^DB_PORT=.*/DB_PORT=3306/" .env
sed -i "s/^DB_DATABASE=.*/DB_DATABASE=${git_repo_name}/" .env
sed -i "s/^DB_USERNAME=.*/DB_USERNAME=${git_repo_name}/" .env
sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=${db_pass}/" .env

export COMPOSER_ALLOW_SUPERUSER=1
export COMPOSER_HOME=/var/www/vhosts/${git_repo_name}
composer update --no-interaction
composer install --no-interaction

yum install php-pdo -y
yum install php-mysql -y

php artisan key:generate

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

sed -i "s/^listen =.*/listen = 127.0.0.1:9000/" /etc/php-fpm.d/www.conf
systemctl restart php-fpm

php artisan migrate

yum -y update