#!/usr/bin/env bash
python ../manage.py crontab add
date '+%s' > /tmp/start_check.txt