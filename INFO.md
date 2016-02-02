
```
Developed using Python 3.4.3, Django 1.9.1
Database is PostgreSQL 9.1
```

### Restore database and site backups

### Install requirements and setup virtualenv:

```
$ su - global_tender	# change username
$ pip install virtualenvwrapper
...
$ export WORKON_HOME=~/Envs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv --system-site-packages --python=/usr/local/bin/python3 global-rent
$ workon global-rent

# enter repository root directory and install python packages:
$ pip install -r requirements.txt
```

### Setup Production (using nginx + gunicorn)

####Running gunicorn (WSGI HTTP Server) this way (7 instances, max timeout 1000 seconds):

```
gunicorn system.wsgi -w 7 -t 1000 --log-file=/path/to/gunicorn.log -b 127.0.0.1:9292
```

####Nginx config for our virtual host (replace PATH where needed):

```
server {
        listen 80;

        server_name gl-rent.ihptru.net;

        access_log /data/global-tender/logs/gl_rent.access.log;
        error_log /data/global-tender/logs/gl_rent.error.log;

        root /data/global-tender/global-rent/www/gl_rent/;

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
                alias /data/global-tender/global-rent/www/gl_rent/static/; # STATIC_ROOT
                expires 30d;
        }

        location = /favicon.ico {
                alias /data/global-tender/global-rent/www/gl_rent/static/favicon.png;
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
