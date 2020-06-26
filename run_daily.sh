


cd /home/rhong/github/covid2
source env/bin/activate

git pull

python update.py
cd web
php index.php > index.html

git add .
git commit
git push

