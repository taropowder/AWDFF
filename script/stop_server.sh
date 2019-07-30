#!/usr/bin/env bash
kill -9 $(ps aux | grep "python ../manage.py runserver" | awk '{print $2}')