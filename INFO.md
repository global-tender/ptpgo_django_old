
```
Разработано с использованием Python 3.4.3, Django 1.9.4
База данных: PostgreSQL 9.1
```

### Развернуть проект:

 * Склонировать репозиторий в директорию на диске
 * Создать пользователя и БД в PostgreSQL:
```
CREATE USER ptpgo WITH PASSWORD 'ptpgo_password';

CREATE DATABASE "ptpgo"
  WITH OWNER "ptpgo"
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';

GRANT ALL PRIVILEGES ON DATABASE "ptpgo" to ptpgo;
```
 * Отредактировать параметры подключения к БД в файле `ptpgo/settings.py` (файл в .gitignore, создать с копии `ptpgo/settings_example.py`)
 * Установить `python3`
 * Установить `virtualenvwrapper` (виртуальная python среда):
```
sudo pip install virtualenvwrapper
mkdir ~/Envs

export WORKON_HOME=~/Envs  # Добавить в .bashrc
source /usr/local/bin/virtualenvwrapper.sh  # Путь может отличаться, добавить в .bashrc

mkvirtualenv --python=/usr/bin/python3 ptpgo  # Создает виртуальную среду с именем ptpgo, путь к python3 может отличаться

workon ptpgo  # Вход в созданную виртуальную среду; выполнять команду всегда когда запускаем встроенный веб сервер для тестирования; команда не выполнится в следующий раз, если в .bashrc не добавлены команды из этой инструкции, где была указана необходимость их добавления туда


pip install -r requirements.txt  # Установка в виртуальную среду всех пакетов указанных в файле requirements.txt; выполняется один раз, либо если количество зависимостей было расширено
```
 * Находясь в директории проекта и подключившись к виртуальной среде, запустить первоначальные миграции, чтобы создать структуру БД:
```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

# Все миграции коммитятся в git, поэтому все изменения модели можно накатывать на тестовом или продакшен сервере с использованием команды: python manage.py migrate
```
 * Запустить встроенный веб сервер:
```
python manage.py runserver 127.0.0.1:8090
```


### Setup Production (using nginx + gunicorn)

####Restore database, disk backups, ssl certificates

####Running gunicorn (WSGI HTTP Server) this way (7 instances, max timeout 1000 seconds):

```
gunicorn ptpgo.wsgi -w 7 -t 1000 --log-file=/path/to/logs/ptpgo.gunicorn.log -b 127.0.0.1:9292
```

####Nginx config for our virtual host (replace PATH where needed):

```
server {
	listen		80;
	server_name	ptpgo.com www.ptpgo.com;
	return		301 https://$server_name$request_uri;
}

server {
	listen		80;
	server_name	ptpgo.ru www.ptpgo.ru;
	return		301 https://$server_name$request_uri;
}

server {
	listen 443 ssl;

	ssl_certificate /etc/letsencrypt/live/ptpgo.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/ptpgo.com/privkey.pem;

	server_name ptpgo.com www.ptpgo.com;

	access_log /data/global-tender/ptpgo/ptpgo.access.log;
	error_log /data/global-tender/ptpgo/ptpgo.error.log;

	root /data/global-tender/ptpgo/www/ptpgo/;

	location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
		expires 10d;
		add_header Pragma public;
		add_header Cache-Control "public";
	}

	gzip on;
	gzip_disable "msie6";

	gzip_comp_level 6;
	gzip_min_length 1100;
	gzip_buffers 16 8k;
	gzip_proxied any;
	gzip_types
		text/plain
		text/css
		text/js
		text/xml
		text/javascript
		application/javascript
		application/x-javascript
		application/json
		application/vnd.api+json
		application/xml
		application/xml+rss;


	location /static/ { # STATIC_URL
		alias /data/global-tender/ptpgo/www/ptpgo/static/; # STATIC_ROOT
		expires 30d;
	}

	location = /favicon.ico {
		alias /data/global-tender/ptpgo/www/ptpgo/static/favicon.png;
	}

	location / {
		proxy_pass_header Server;
		proxy_set_header Host $http_host;
		proxy_redirect off;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Scheme $scheme;
		proxy_connect_timeout 120;
		proxy_read_timeout 1000;
		proxy_pass http://127.0.0.1:9292/;
	}
}


server {
	listen 443 ssl;

	ssl_certificate /etc/letsencrypt/live/ptpgo.ru/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/ptpgo.ru/privkey.pem;

	server_name ptpgo.ru www.ptpgo.ru;

	access_log /data/global-tender/ptpgo/ptpgo.access.log;
	error_log /data/global-tender/ptpgo/ptpgo.error.log;

	root /data/global-tender/ptpgo/www/ptpgo/;

	location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
		expires 10d;
		add_header Pragma public;
		add_header Cache-Control "public";
	}

	gzip on;
	gzip_disable "msie6";

	gzip_comp_level 6;
	gzip_min_length 1100;
	gzip_buffers 16 8k;
	gzip_proxied any;
	gzip_types
		text/plain
		text/css
		text/js
		text/xml
		text/javascript
		application/javascript
		application/x-javascript
		application/json
		application/vnd.api+json
		application/xml
		application/xml+rss;


	location /static/ { # STATIC_URL
		alias /data/global-tender/ptpgo/www/ptpgo/static/; # STATIC_ROOT
		expires 30d;
	}

	location = /favicon.ico {
		alias /data/global-tender/ptpgo/www/ptpgo/static/favicon.png;
	}

	location / {
		proxy_pass_header Server;
		proxy_set_header Host $http_host;
		proxy_redirect off;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Scheme $scheme;
		proxy_connect_timeout 120;
		proxy_read_timeout 1000;
		proxy_pass http://127.0.0.1:9292/;
	}
}
```
