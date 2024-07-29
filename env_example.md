.server-main.env

```env
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=86400
DB_HOST=server_main-db-1
DB_REMOTE_IP=0.0.0.0
DB_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
ISDOCKER=0
REDIS_PASSWORD=redis_password
REDIS_HOST=server_main-redis-1
REDIS_PORT=6379
```

Note that ISDOCKER should be equal to 0 in .env file, that's needed for our `revision.py` script that we run outside of a docker. This variable will be overriden in docker-compose files
DB_REMOTE_IP used only for alembic revisions `revision.py`, if DB running on another machine you should provide the same DB_REMOTE_IP and DB_HOST.

.server-mailer.env

```env
EMAIL_SENDER_PASSWORD=email_password
EMAIL_SENDER=uremail@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RABBITMQ_URL=amqp://guest:guest@localhost:15672
RABBITMQ_QUEUE=mailer
TEMPLATES_DIR=./templates
```
