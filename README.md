Деплой на сервер (Yandex Cloud)

1. Установить зависимости:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx git


Клонировать репозиторий:

git clone git@github.com:AlexeyYanchenkov/Django_RDF.git


Создать и активировать виртуальное окружение:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Настроить .env и переменные:

DEBUG=1
SECRET_KEY=...
DJANGO_ALLOWED_HOSTS=89.169.xxx.xxx 127.0.0.1 localhost


Настроить gunicorn:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn


Настроить nginx:

sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
Готово! Приложение доступно по IP-адресу.
