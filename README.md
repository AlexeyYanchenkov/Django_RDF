Деплой на сервер (Yandex Cloud)

Установить зависимости:

sudo apt update
sudo apt install python3-pip python3-venv nginx git


Клонировать репозиторий:

git clone git@github.com:AlexeyYanchenkov/Django_RDF.git


Создать и активировать виртуальное окружение:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Настроить .env и переменные(все указано в .env.sample):

DEBUG=1
SECRET_KEY=...
DJANGO_ALLOWED_HOSTS=89.169.xxx.xxx 127.0.0.1 localhost


Применить миграции и собрать статику:

python manage.py migrate
python manage.py collectstatic --noinput


Создайте файл сервиса Gunicorn: /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=alexey-1408
Group=www-data
WorkingDirectory=/home/alexey-1408/Django_RDF
ExecStart=/home/alexey-1408/Django_RDF/venv/bin/gunicorn drf_lms.wsgi:application \
    --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target


Затем запустите и включите службу:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn


Настройка Nginx
Создайте конфигурацию /etc/nginx/sites-available/django_rdf:

server {
    listen 80;
    server_name 89.169.xxx.xxx;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/alexey-1408/Django_RDF/static/;
    }

    location /media/ {
        alias /home/alexey-1408/Django_RDF/media/;
    }
}


Активируйте сайт и перезапустите Nginx:

sudo ln -s /etc/nginx/sites-available/django_rdf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx


Проверка статуса сервисов

sudo systemctl status gunicorn
sudo systemctl status nginx


Приложение будет доступно по IP-адресу:

http://89.169.xxx.xxx/
