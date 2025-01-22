#!/bin/bash
# 获取当前登录用户
CurrentUser=$(ls -l /dev/console | awk '{ print $3 }')
# 获取当前用户的UID
CurrentUserUID=$(id -u "$CurrentUser")
# 以当前用户身份发送通知
launchctl asuser $CurrentUserUID sudo -iu "$CurrentUser" terminal-notifier -title "通知标题" -subtitle "通知副标题" -message "通知内容" -sound default