Supabase setup and local configuration
===================================

1) Store secrets locally

- Copy `.env.sample` to `.env` and fill in real secrets. **Do not commit `.env`.**

2) Install dependencies

- Create virtualenv and install packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt  # or pip install django-environ psycopg[binary] dj-database-url
```

3) Run migrations and start dev server

```bash
python manage.py migrate
python manage.py runserver
```

4) Notes

- `DATABASE_URL` in your `.env` should point to the Supabase Postgres connection string.
- `SUPABASE_ANON_KEY` is safe for client-side usage; never commit `SUPABASE_SERVICE_ROLE_KEY`.
