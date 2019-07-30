#!/usr/bin/env bash
nohup python ../manage.py runserver 0.0.0.0:8888 >> access.log 2>&1 &