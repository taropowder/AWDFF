#!/usr/bin/env bash
cp ../config.yml.bak ../config.yml
python ../manage.py makemigrations
python ../manage.py collectstatic
python ../manage.py migrate