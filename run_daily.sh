#!/usr/bin/env bash

# Wrapper script to excecute run.py from a cronjob

cd ~/github/covid2
source env/bin/activate
git pull

python update.py

cd docs
php index.php > index.html

git add .
git commit -m "daily bot"
git push

