#!/bin/bash

service ssh start
service rsyslog start

python3 exporter.py
