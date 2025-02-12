#!/bin/bash

dpkg -i $(ls | grep "openssh-client_.")
dpkg -i $(ls | grep "openssh-sftp-server_.")
apt-get install -y $(cat requirements2.txt)
dpkg -i $(ls | grep "openssh-server_.")
