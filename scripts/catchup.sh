#!/bin/bash
# This a the script that you can run on the production server of SHEBANQ to restore the shebanq_web and shebanq_note databases

# run it as follows:
#
# ./catchup.sh

# This script is set up to work at specific servers.
# Currently it supports 
#   clarin11.dans.knaw.nl (SELINUX)
#   PPJV003 (Ubuntu) (default)

# MYSQL_PDIR: directory with config files for talking with mysql
# SH_ADIR   : directory where the web app shebanq resides (and also web2py itself)
# INCOMING  : directory where installation files arrive

INCOMING="/home/dirkr"

if [ "$HOSTNAME" == "clarin11.dans.knaw.nl" ]; then
        ON_CLARIN=1
        MYSQL_PDIR="/opt/emdros/cfg"
        SH_ADIR="/opt/web-apps"
        MQL_OPTS="-u shebanq_admin -h mysql11.dans.knaw.nl"
        UNPACK="/data/shebanq/unpack"
fi

if [ $ON_CLARIN ]; then
    sudo -n /usr/bin/systemctl stop httpd.service
fi

cd $SH_ADIR/shebanq
mkdir -p $UNPACK

echo "unzipping database dumps for shebanq_web and shebanq_note"
cp $INCOMING/shebanq_web.sql.gz $UNPACK
cp $INCOMING/shebanq_note.sql.gz $UNPACK
gunzip -f $UNPACK/shebanq_web.sql.gz
gunzip -f $UNPACK/shebanq_note.sql.gz
echo "dropping and creating databases shebanq_web and shebanq_note"
mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt -e 'drop database if exists shebanq_note;'
mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt -e 'drop database if exists shebanq_web;'
mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt -e 'create database shebanq_web;'
mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt -e 'create database shebanq_note;'
echo "loading databases shebanq_web and shebanq_note"
echo "use shebanq_web" | cat - $UNPACK/shebanq_web.sql | mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt
echo "use shebanq_note" | cat - $UNPACK/shebanq_note.sql | mysql --defaults-extra-file=$MYSQL_PDIR/mysqldumpopt
sleep 2

if [ $ON_CLARIN ]; then
    sudo -n /usr/bin/systemctl start httpd.service
fi

