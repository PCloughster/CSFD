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
yum install -y openssl php-bcmath php-curl php-json php-mbstring php-tokenizer php-xml php-zip

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$([ -z "$${XDG_CONFIG_HOME-}" ] && printf %s "$${HOME}/.nvm" || printf %s "$${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 20
yum install npm -y

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
        location = /{
                try_files \$uri \$uri/ /index.php;

                # reverse proxy for next server
                proxy_pass http://localhost:3000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
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
chown nginx -R .
npm install
npm install -g pm2 
npm run build
pm2 start "npm run start" --name "csfd-test-react"

sed -i "s/^listen =.*/listen = 127.0.0.1:9000/" /etc/php-fpm.d/www.conf
systemctl restart php-fpm
yum -y update