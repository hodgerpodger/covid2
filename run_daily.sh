#!/usr/bin/env bash

# Wrapper script to excecute run.py from a cronjob
set -euo pipefail

cd ~/github/covid2
source env/bin/activate
git pull

python update.py >> /tmp/covid2.stdout.log 2>> /tmp/covid2.stderr.log

cd docs
php index.php > index.html

cd ../
git add .
git commit -m "daily bot"
git push

