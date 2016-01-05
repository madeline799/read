#!/bin/bash

ROOT=$(pwd)

SITE=bankofbook

EXCLUDEMODE="flase"

proxy="false"
prerequisite="false"
apache="false"
buildenv="false"
inflate="false"

read -s -p "enter sudo password:" sudopasswd
echo ''

for para in $@
do
    if [ "test-$para" = "test-exclude" ]
    then
        EXCLUDEMODE="true"
    elif [ "test-$para" = "test-proxy" ]
    then
        proxy="true"
    elif [ "test-$para" = "test-prerequisite" ]
    then
        prerequisite="true"
    elif [ "test-$para" = "test-apache" ]
    then
        apache="true"
    elif [ "test-$para" = "test-buildenv" ]
    then
        buildenv="true"
    elif [ "test-$para" = "test-inflate" ]
    then
        inflate="true"
    fi
done

####################################################################
####################################################################
####################################################################

#proxy
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${proxy} = "false" ]
    then
        export http_proxy=http://proxy-prc.intel.com:911
        export https_proxy=http://proxy-prc.intel.com:911
    fi
else
    if [ ${proxy} = "true" ]
    then
        export http_proxy=http://proxy-prc.intel.com:911
        export https_proxy=http://proxy-prc.intel.com:911
    fi
fi





#prerequisite
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${prerequisite} = "false" ]
    then
        echo ${sudopasswd} |sudo -S apt-get update
        echo ${sudopasswd} |sudo -S apt-get -y install python-dev
        echo ${sudopasswd} |sudo -S apt-get -y install python-virtualenv
        echo ${sudopasswd} |sudo -S apt-get -y install libmysqlclient-dev
        echo ${sudopasswd} |sudo -S apt-get -y install openjdk-7-jre
    fi
else
    if [ ${prerequisite} = "true" ]
    then
        echo ${sudopasswd} |sudo -S apt-get update
        echo ${sudopasswd} |sudo -S apt-get -y install python-dev
        echo ${sudopasswd} |sudo -S apt-get -y install python-virtualenv
        echo ${sudopasswd} |sudo -S apt-get -y install libmysqlclient-dev
        echo ${sudopasswd} |sudo -S apt-get -y install openjdk-7-jre
    fi
fi


#apache2 
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${apache} = "false" ]
    then
        echo ${sudopasswd} |sudo -S apt-get -y install apache2 libapache2-mod-wsgi
        echo ${sudopasswd} |sudo -S bash -c  "cat apache.cfg > /etc/apache2/sites-available/${SITE}"
        echo ${sudopasswd} |sudo -S a2dissite default
        echo ${sudopasswd} |sudo -S a2ensite ${SITE}
        echo ${sudopasswd} |sudo -S service apache2 restart
    fi
else
    if [ ${apache} = "true" ]
    then
        echo ${sudopasswd} |sudo -S apt-get -y install apache2 libapache2-mod-wsgi
        echo ${sudopasswd} |sudo -S bash -c  "cat apache.cfg > /etc/apache2/sites-available/${SITE}"
        echo ${sudopasswd} |sudo -S a2dissite default
        echo ${sudopasswd} |sudo -S a2ensite ${SITE}
        echo ${sudopasswd} |sudo -S service apache2 restart
    fi
fi


#python virtualenv
if [ ${EXCLUDEMODE} = "true" ]
then
    if [ ${buildenv} = "false" ]
    then
        echo ${sudopasswd} |sudo -S rm -rf ${ROOT}/venv
        virtualenv venv
        ${ROOT}/venv/bin/pip install -r ${ROOT}/requirements.txt 
    fi
else
    if [ ${buildenv} = "true" ]
    then
        echo ${sudopasswd} |sudo -S rm -rf ${ROOT}/venv
        virtualenv venv
        ${ROOT}/venv/bin/pip install -r ${ROOT}/requirements.txt 
    fi
fi

#collect static file
${ROOT}/venv/bin/python ${ROOT}/bankofbook/manage.py collectstatic --noinput --ignore "bookstore"

#minimize js/css file collected in static folder
mini="java -jar ${ROOT}/tools/yuicompressor-2.4.7.jar"
minimized="bootstrap jquery"
function substr()
{
    if [[ ${1/${2}//} = $1 ]]
    then
        ## $2 is NOT substring of $1.
        echo N
        return 0
    else
        ## $2 is substring of $1.
        echo Y
        return 1
    fi
}

for file in $(find ${ROOT}/${SITE}/media/static -name "*.js")
do
    skip="N"
    for sub in ${minimized}
    do
        if [ "$(substr ${file} ${sub})" = "Y" ]
        then
            skip="Y"
        fi
    done

    if [ "${skip}" == "N" ]
    then
        echo ${file}
        ${mini} ${file} >./tmp && mv ./tmp ${file}
    fi
done

for file in $(find ${ROOT}/${SITE}/media/static -name "*.css")
do
    skip="N"
    for sub in ${minimized}
    do
        if [ "$(substr ${file} ${sub})" = "Y" ]
        then
            skip="Y"
        fi
    done

    if [ "${skip}" == "N" ]
    then
        echo ${file}
        ${mini} ${file} >./tmp && mv ./tmp ${file}
    fi
done

cat ${ROOT}/bankofbook/media/bookstore/readme
