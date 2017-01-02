#!/usr/bin/expect
set pass [lindex $argv 0]
set dateString [lindex $argv 1]
set userandserver "davidmus@web236.webfaction.com"
set webroot "/webapps"
set timeout -1
spawn scp "/Users/david/Documents/KSO/KSO programme $dateString.pdf" $userandserver:~$webroot/media/programmes/
expect {
    password: {send "$pass\r"; exp_continue}
}
spawn scp "/Users/david/Documents/KSO/KSO programme cover $dateString.jpg" $userandserver:~$webroot/media/programmes/
expect {
    password: {send "$pass\r"; exp_continue}
}
