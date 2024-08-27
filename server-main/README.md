FastAPI application that use Alembic, SQLAlchemy (PostgreSQL), Redis and Docker + Docker-compose

Alembic Revision (run from project folder):
```bash
cp ../.server-main.env .env
python revision.py
```

Migrate (run from root folder):
```bash
sudo ./migrate_main.sh
```

Notice that you should run docker-compose with --build option after revision, if you want to run migration
