1. Клонирование и подготовка
   
git clone https://github.com/AlexeyYanchenkov/Django_RDF.git
cd Django_RDF

2. Создание .env файла

Создать файл .env на основе .env.sample и добавить в него реальные значения:
cp .env.sample .env
Заполнить EMAIL_HOST_USER, EMAIL_HOST_PASSWORD и другие переменные.

3. Сборка и запуск через Docker

docker compose build --no-cache
docker compose up
