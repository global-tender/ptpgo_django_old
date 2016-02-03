
```
Developed using Python 3.4.3, Django 1.9.1
Database is PostgreSQL 9.1
```

### Restore database, disk backups, ssl certificates

### Install requirements and setup virtualenv:

```
$ su - ptpgo	# change username
$ pip install virtualenvwrapper
...
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv --python=/usr/bin/python3 ptpgo
$ workon ptpgo

# enter repository root directory and install python packages:
$ pip install -r requirements.txt
```

### Setup Production (using nginx + gunicorn)

####Running gunicorn (WSGI HTTP Server) this way (7 instances, max timeout 1000 seconds):

```
gunicorn system.wsgi -w 7 -t 1000 --log-file=/path/to/logs/ptpgo-backend.gunicorn.log -b 127.0.0.1:9292
```

####Nginx config for our virtual host (replace PATH where needed):

```
server {
		listen         80;
		server_name    ptpgo.ihptru.net;
		return         301 https://$server_name$request_uri;
}

server {
		listen 443 ssl;

		ssl_certificate /etc/letsencrypt/live/ptpgo.ihptru.net/fullchain.pem;
		ssl_certificate_key /etc/letsencrypt/live/ptpgo.ihptru.net/privkey.pem;

		server_name ptpgo.ihptru.net;

		access_log /path/to/logs/ptpgo-backend.access.log;
		error_log /path/to/logs/ptpgo-backend.error.log;

		root /path/to/ptpgo/app/name/;

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
			application/xml
			application/xml+rss;


		location /static/ { # STATIC_URL
				alias /path/to/ptpgo/app/name/static/; # STATIC_ROOT
				expires 30d;
		}

		location = /favicon.ico {
				alias /path/to/ptpgo/app/name/static/favicon.png;
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
