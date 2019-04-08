#!/bin/bash
##############################################################################
# Make a new file:
# vi install.sh
# Place this content in it and then make the file executable:
#  chmod +x install.sh
# Execute the script to install Odoo:
# ./install.sh
##############################################################################

########################## [Directory tree] ##################################
#/home/pllab
#|--------pllab-production
#|---------------------|----pllab (soure code)
#|---------------------|----data (filestore, sesssion, ...)
#|---------------------|----pllab.log (log file)

##############################################################################


##fixed parameters
#odoo
ODOO_USER="pllab"
PROJECT_NAME="pllab"
ODOO_HOME="opt/${ODOO_USER}-server"
LOG_FILE=$ODOO_HOME/${PROJECT_NAME}.log
#The default port where this Odoo instance will run under (provided you use the command -c in the terminal)
#Set to true if you want to install it, false if you don't need it or have it already installed.
INSTALL_WKHTMLTOPDF="True"
#Set the default Odoo port (you still have to use -c /etc/odoo-server.conf for example to use this.)
ODOO_PORT="8069"
#Choose the Odoo version which you want to install. For example: 10.0, 9.0, 8.0, 7.0 or saas-6. When using 'trunk' the master version will be installed.
#IMPORTANT! This script contains extra libraries that are specifically needed for Odoo 10.0
ODOO_VERSION="10.0"

# ~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~

# 0. Fix locale issues
locale-gen "en_US.UTF-8"
dpkg-reconfigure locales
export LC_ALL="en_US.UTF-8"

cat <<EOF > /etc/environment
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8

EOF

# 1. Update & upgrade server
echo -e "\n---- Update Server ----"
apt-get update
echo -e "\n---- Install dialog ----"
apt-get install dialog -y

# 2. Add user & change password
useradd -m -g sudo -s /bin/bash pllab
passwd pllab

# 3. Install libs
apt-get install -y git python3.5 nano virtualenv  xz-utils wget fontconfig libfreetype6 libx11-6 libxext6 libxrender1  node-less node-clean-css xfonts-75dpi python-pip gcc python3.5-dev libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libssl-dev libldap2-dev  libpq-dev libpng12-dev libjpeg-dev python-setuptools

# . Set git alias
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status


# 4. Install WKHTMLTOPDF
_url=https://nightly.odoo.com/extra/wkhtmltox-0.12.1.2_linux-jessie-amd64.deb
wget --quiet $_url
gdebi --n `basename $_url`
rm `basename $_url`

# 5. Install postgresql
cat <<EOF > /etc/apt/sources.list.d/pgdg.list
deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main

EOF

echo -e "\n---- Install PostgreSQL Repo Key ----"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


echo -e "\n---- Install PostgreSQL Server 10 ----"
apt-get update
apt-get install postgresql-10 postgresql-server-dev-10 -y

echo -e "\n---- Creating the ODOO PostgreSQL User  ----"
su - postgres -c "createuser -s pllab" 2> /dev/null || true

# 5. Create instance's folder
mkdir /home/pllab/pllab-production
mkdir /home/pllab/pllab-production/data
touch /home/pllab/pllab-production/pllab.log

# 6. Clone source code
echo -e "\n==== Clone source code ===="
git clone https://nguyenductamlhp@github.com/nguyenductamlhp/pllab.git /home/pllab/pllab-production/pllab

# . set owner
chown -R pllab /home/pllab/pllab-production/

# 7. Install requirements.txt
sudo -H pip install -r /home/pllab/pllab-production/pllab/odoo/requirements.txt

# 8. Setup as service
echo -e "* Create service file"
cat <<EOF > /etc/systemd/system/pllab.service
[Unit]
Description=pllab server
After=postgresql.service

[Service]
Type=simple
User=pllab
ExecStart=/home/pllab/pllab-production/pllab/odoo/odoo-bin --config=/home/pllab/pllab-production/pllab/config/server.conf

[Install]
WantedBy=multi-user.target

EOF

echo -e "* Reload daemon"
systemctl daemon-reload

echo -e "* Start ODOO on Startup"
systemctl enable pllab.service

echo -e "* Starting Odoo Service"
# systemctl start pllab
