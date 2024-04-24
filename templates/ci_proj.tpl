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
        listen 80 ${application_domain == "default_server" ? "default_server" : "www.${application_domain} ${application_domain}"};
        listen [::]:80 ${application_domain == "default_server" ? "default_server" : "www.${application_domain} ${application_domain}"};

        root /var/www/vhosts/${git_repo_name}/public/;
        index index.php index.html index.htm index.nginx-debian.html;

        location / {
                try_files \$uri \$uri/ /index.php\$is_args\$args;
        }

        location ~ \.php$ {
                include fastcgi_params;
                fastcgi_pass unix:/var/run/php-fpm/php-fpm.sock;
                fastcgi_intercept_errors on;
                fastcgi_param SCRIPT_FILENAME \$document_root/\$fastcgi_script_name;
        }
        error_page 404 /index.php;

        location ~ /\. {
                deny all;
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
cp env .env

if [ "${application_domain}" = "default_server" ]; then
    sed -i "s/^.*app.baseURL =.*/app.baseURL = http:\/\/localhost\//" .env
else
    sed -i "s/^.*app.baseURL =.*/app.baseURL = http:\/\/${application_domain}\//" .env
fi


sed -i "s/^# CI_ENVIRONMENT =.*/CI_ENVIRONMENT = production/" .env
sed -i "s/^.*database.default.hostname =.*/database.default.hostname = localhost/" .env
sed -i "s/^.*database.default.port =.*/database.default.port = 3306/" .env
sed -i "s/^.*database.default.database =.*/database.default.database = ${git_repo_name}/" .env
sed -i "s/^.*database.default.username =.*/database.default.username = ${git_repo_name}/" .env
sed -i "s/^.*database.default.password =.*/database.default.password = ${db_pass}/" .env

export COMPOSER_ALLOW_SUPERUSER=1
export COMPOSER_HOME=/var/www/vhosts/${git_repo_name}
composer update --no-interaction
composer install --no-interaction

yum install php-pdo php-mysql -y

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

sed -i "s/^listen =.*/listen = \/var\/run\/php-fpm\/php-fpm.sock/" /etc/php-fpm.d/www.conf
systemctl restart php-fpm

yum -y update