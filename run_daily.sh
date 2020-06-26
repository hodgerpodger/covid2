


cd ~/git pullgithub/covid2
source env/bin/activate

git pull

python update.py
cd web
php index.php > index.html

git add .
git commit -m "daily bot"
git push

