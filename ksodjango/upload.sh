#!/usr/bin/expect
set pass [lindex $argv 0]
set userandserver "davidmus@web236.webfaction.com"
set webroot "/webapps"
set timeout -1
spawn rsync -rtv --exclude media --exclude .idea --exclude upload.sh --exclude todo.txt --exclude settings.webfactional --exclude ksodjango.* --exclude out . $userandserver:~$webroot/kso/ksodjango/
expect {
    password: {send "$pass\r"; exp_continue}
}
spawn scp ./settings.webfactional $userandserver:~$webroot/kso/ksodjango/settings.py
expect {
    password: {send "$pass\r"; exp_continue}
}
spawn scp ./static/submenu.html $userandserver:~$webroot/media/
expect {
    password: {send "$pass\r"; exp_continue}
}
spawn scp ./static/submenumember.html $userandserver:~$webroot/media/
expect {
    password: {send "$pass\r"; exp_continue}
}
cd static
spawn rsync -rtv . $userandserver:~$webroot/media/
expect {
    password: {send "$pass\r"; exp_continue}
}
spawn ssh $userandserver .$webroot/kso/apache2/bin/restart
expect {
    password: {send "$pass\r"; exp_continue}
}
#rsync -rtv --exclude media --exclude .idea --exclude upload.sh --exclude todo.txt --exclude settings.webfactional --exclude ksodjango.* --exclude out . davidmus@web236.webfaction.com:~/webapps/kso/ksodjango/
#scp ./settings.webfactional davidmus@web236.webfaction.com:~/webapps/kso/ksodjango/settings.py
#rsync -rtv . davidmus@web236.webfaction.com:~/webapps/media/
#ssh davidmus@web236.webfaction.com ./webapps/kso/apache2/bin/restart